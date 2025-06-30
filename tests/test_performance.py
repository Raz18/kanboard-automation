import asyncio
import time
import uuid

import allure
import pytest
from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage
from pages.project_page import ProjectPage
from config.app_settings import AppSettings

NUMBER_OF_TASKS = AppSettings.get_number_of_tasks()  # Number of tasks to create in the project for performance testing
MEASUREMENT_RUNS = 5  # Number of times to run the query for averaging
MAX_AVG_RESPONSE_TIME = 1.0  # Performance threshold in seconds


@pytest.fixture(scope="function")
def performance_test_project(admin_page_fixture: Page, db_connection):
    """
    A pytest fixture to set up the necessary data for the performance test.
    It creates a new project and populates it with a specified number of tasks.
    """
    project_name = f"Performance Test Project {uuid.uuid4()}"
    dashboard_page = DashboardPage(admin_page_fixture)
    project_page = ProjectPage(admin_page_fixture)

    with allure.step(f"SETUP: Create a project and {NUMBER_OF_TASKS} tasks"):
        # Create the project
        dashboard_page.click_new_project()
        project_page.create_project(project_name)
        dashboard_page.navigate()
        dashboard_page.navigate_to_project(project_name)

        # Add the specified number of tasks
        for i in range(NUMBER_OF_TASKS):
            task_title = f"Perf Task {i + 1}"
            project_page.add_task(task_title)
        print(f"SETUP complete: Created {NUMBER_OF_TASKS} tasks in project '{project_name}'.")

    # Retrieve the created project's ID to pass to the test
    with db_connection.cursor() as cur:
        cur.execute("SELECT id FROM projects WHERE name = %s", (project_name,))
        project_id_result = cur.fetchone()
        assert project_id_result is not None, "SETUP FAILED: Could not find created project in DB."
        project_id = project_id_result[0]

    # The fixture yields the project_id for the test to use
    yield project_id


@allure.epic("Kanboard Application")
@allure.feature("Performance")
@allure.story("Task Retrieval Performance")
class TestSYNCPerformance:
    """
    Test 4: Basic Performance Test
    Focuses on measuring the database performance for task retrieval using synchronous operations.
    """

    @allure.title("Measure DB Time to Retrieve All Tasks from a Project")
    @allure.description(
        "Measures the database query time to fetch all tasks from a project containing 50 tasks. "
        "The test uses a warm-up run and averages multiple measurements for reliability."
    )
    def test_database_retrieval_performance(self, performance_test_project, db_connection):
        """
        This test's sole responsibility is to measure the database query performance.
        Data creation is handled by the 'performance_test_project' fixture.
        """
        project_id = performance_test_project

        with allure.step(f"Measure DB query performance across {MEASUREMENT_RUNS} runs"):
            with db_connection.cursor() as cur:
                # --- Warm-up Run ---
                with allure.step("Sub-step: Perform a warm-up query"):
                    cur.execute("SELECT id, title FROM tasks WHERE project_id = %s", (project_id,))
                    _ = cur.fetchall()  # Fetch to complete the operation and ensure caching
                    print("Completed warm-up query.")

                # --- Measurement Runs ---
                response_times = []
                retrieved_tasks = []
                with allure.step(f"Sub-step: Execute and time {MEASUREMENT_RUNS} measurement queries"):
                    for i in range(MEASUREMENT_RUNS):
                        start_time = time.time()
                        cur.execute("SELECT id, title FROM tasks WHERE project_id = %s", (project_id,))
                        retrieved_tasks = cur.fetchall()
                        end_time = time.time()
                        run_time = end_time - start_time
                        response_times.append(run_time)
                        print(f"Measurement run {i + 1}/{MEASUREMENT_RUNS} took: {run_time:.4f}s")

                # --- Calculate and Report Average ---
                average_response_time = sum(response_times) / len(response_times)
                allure.attach(
                    f"Individual runs (s): {response_times}\n"
                    f"Average response time: {average_response_time:.4f}s",
                    name="DB Query Performance Summary",
                    attachment_type=allure.attachment_type.TEXT
                )

            db_connection.commit()

        with allure.step("Verify task count and average response time"):
            # Verify that the correct number of tasks were retrieved
            assert len(retrieved_tasks) == NUMBER_OF_TASKS, \
                f"Expected to retrieve {NUMBER_OF_TASKS} tasks, but got {len(retrieved_tasks)}."
            print(f"Successfully retrieved {len(retrieved_tasks)} tasks from the database.")

            # Verify that the average response time is within the acceptable threshold
            assert average_response_time < MAX_AVG_RESPONSE_TIME, \
                f"Average DB query time ({average_response_time:.4f}s) exceeds the threshold of {MAX_AVG_RESPONSE_TIME}s."
            print(f"Average database query was performant, taking {average_response_time:.4f}s.")
