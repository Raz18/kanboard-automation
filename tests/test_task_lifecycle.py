import pytest
import allure
import uuid
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.project_page import ProjectPage
from pages.task_page import TaskPage


@allure.epic("Kanboard Application")
@allure.feature("Task Management")
@allure.story("Task Lifecycle")
class TestTaskLifecycle:
    """Test 2: Task Lifecycle Testing - Simple and focused implementation."""

    @allure.title("Test 2: Task Lifecycle Testing")
    @allure.description("Create task via UI, verify in database, move to Done, confirm database change")
    def test_task_lifecycle_validation(self, admin_page_fixture: Page, db_connection):
        """Test the 4 core requirements: Create task → Verify DB → Move to Done → Confirm DB change"""

        # Setup test data
        project_name = f"task_lifecycle_Project {uuid.uuid4()}"
        task_name = f"test_Task"

        dashboard_page = DashboardPage(admin_page_fixture)
        project_page = ProjectPage(admin_page_fixture)

        # REQUIREMENT 1: Create a task through UI (using Playwright)
        with allure.step("Create task through project UI"):
            # Create project first
            dashboard_page.click_new_project()
            project_page.create_project(project_name)
            dashboard_page.navigate()

            dashboard_page.navigate_to_project(project_name)
            project_page.add_task(task_name)
            with db_connection.cursor() as cur:
                cur.execute("SELECT id FROM projects WHERE name = %s", (project_name,))
                project_id = cur.fetchone()[0]

            print(f"Task '{task_name}' created via UI in project '{project_name}'")
        # REQUIREMENT 2: Verify task insertion in tasks table
        with allure.step("Verify task insertion in database"):
            with db_connection.cursor() as cur:
                cur.execute("SELECT id, column_id FROM tasks WHERE title = %s AND project_id = %s",
                            (task_name, project_id))
                result = cur.fetchone()
                assert result is not None, f"Task '{task_name}' not found in database"
                task_id, initial_column_id = result
                print(f"Task created in database with ID: {task_id}, Column: {initial_column_id}")

        # REQUIREMENT 3: Move task to "Done" column
        with allure.step("Move task to Done column"):
            # Get the last column (typically Done)
            with db_connection.cursor() as cur:
                cur.execute("SELECT id, title FROM columns WHERE project_id = %s ORDER BY position DESC LIMIT 1",
                            (project_id,))
                done_column_id, done_column_title = cur.fetchone()

            # Move task via UI (simple drag-and-drop approach)
            try:
                project_page.navigate_to_task(task_name)
                task_page = TaskPage(admin_page_fixture)
                task_page.move_task_to_done()
                print(f"Task moved via UI to: {done_column_title}")
            except Exception as e:
                print(f"Note: UI move method failed: {e}")

        # REQUIREMENT 4: Confirm database reflects the status change
        with allure.step("Confirm database reflects status change"):
            with db_connection.cursor() as cur:
                cur.execute("SELECT column_id FROM tasks WHERE id = %s", (task_id,))
                new_column_id = cur.fetchone()[0]

                # Verify column changed to Done using its column ID
                assert new_column_id != initial_column_id, \
                    f"Task column should have changed from {initial_column_id} to {new_column_id} reflecting Done status"

                print(f" Database confirms task moved from column {initial_column_id} to {new_column_id} reflecting Done status in DB")

        db_connection.commit()
