import pytest
import allure
import uuid
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.project_page import ProjectPage


@allure.epic("Kanboard Application")
@allure.feature("Project Management")
@allure.story("Data Integrity")
class TestDataIntegrity:
    """
    Test 3: Data Integrity Check
    """

    @allure.title("Test Data Integrity on Project Deletion")
    @allure.description(
        "Creates a project with tasks, deletes the project via the UI, "
        "and verifies the project and its related tasks are removed from the database."
    )
    def test_project_and_task_deletion(self, admin_page_fixture: Page, db_connection):
        """
        Tests that deleting a project also removes its associated tasks from the database.
        """
        # --- 1. Setup Test Data ---
        project_name = f"Integrity Test Project {uuid.uuid4()}"
        task_1_title = "Task One for Deletion"
        task_2_title = "Task Two for Deletion"

        # --- 2. Instantiate Page Objects ---
        dashboard_page = DashboardPage(admin_page_fixture)
        project_page = ProjectPage(admin_page_fixture)

        # --- 3. UI Action: Create Project and Tasks ---
        with allure.step("Step 1: Create a project and two tasks"):
            dashboard_page.click_new_project()
            project_page.create_project(project_name)
            dashboard_page.navigate()
            dashboard_page.navigate_to_project(project_name)
            project_page.add_task(task_1_title)
            project_page.add_task(task_2_title)

        # --- 4. DB Verification (Before Deletion) ---
        with allure.step("Step 2: Verify project and tasks exist in DB before deletion"):
            with db_connection.cursor() as cur:
                cur.execute("SELECT id FROM projects WHERE name = %s", (project_name,))
                project_id_result = cur.fetchone()
                assert project_id_result is not None, "Project was not created successfully in the database."
                project_id = project_id_result[0]

                cur.execute("SELECT COUNT(*) FROM tasks WHERE project_id = %s", (project_id,))
                task_count = cur.fetchone()[0]
                assert task_count == 2, f"Expected 2 tasks in the DB, but found {task_count}."
            db_connection.commit()

        # --- 5. UI Action: Delete the Project ---
        with allure.step("Step 3: Delete the project via UI"):
            # This method now waits for the redirect to complete, so no extra wait is needed here.
            project_page.delete_project()

            # Verify the project is no longer listed on the dashboard
            assert not dashboard_page.is_project_listed(
                project_name), "Project was still listed on the dashboard after deletion."

        # --- 6. DB Verification (After Deletion) ---
        with allure.step("Step 4: Verify project and tasks are deleted from DB"):
            with db_connection.cursor() as cur:
                cur.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
                project_result = cur.fetchone()
                assert project_result is None, "Project record was not deleted from the database."

                cur.execute("SELECT COUNT(*) FROM tasks WHERE project_id = %s", (project_id,))
                remaining_task_count = cur.fetchone()[0]
                assert remaining_task_count == 0, "Tasks associated with the project were not deleted."
            db_connection.commit()
