import pytest
import allure
import uuid
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.project_page import ProjectPage


@allure.epic("Kanboard Application")
@allure.feature("Project Management")
@allure.story("Project Creation")
class TestProjectCreation:
    """
    Test suite for the project creation workflow using a fully synchronous stack.
    """

    @allure.title("Test 1: Project Creation and Database Validation (Sync)")
    @allure.description(
        "Creates a project using the UI and validates the data in the database, "
        "all using synchronous operations."
    )
    # The test now correctly depends on the 'page' fixture from pytest-playwright.
    def test_project_creation_and_db_validation(self, admin_page_fixture: Page, db_connection):
        """
        This test uses the standard synchronous 'page' fixture and performs
        login steps at the beginning of the test.
        """
        # --- 1. Setup & Login ---
        project_name = f"Test Project {uuid.uuid4()}"

        # The login steps are now part of the test itself.
        # Instantiate the other page objects after login
        dashboard_page = DashboardPage(admin_page_fixture)
        project_page = ProjectPage(admin_page_fixture)

        # --- 2. UI Actions (Synchronous) ---
        with allure.step("Step 1: Create a new project via UI"):
            dashboard_page.click_new_project()
            project_page.create_project(project_name)
            dashboard_page.navigate()
            assert dashboard_page.is_project_listed(project_name)

        # --- 3. Database Validation (Synchronous) ---
        with allure.step("Step 2: Verify project data in the 'projects' table"):
            with db_connection.cursor() as cur:
                cur.execute("SELECT name, is_active, owner_id FROM projects WHERE name = %s", (project_name,))
                result = cur.fetchone()

        # --- 4. Commit transaction to avoid open transactions
        db_connection.commit()

        # --- 5. Assertions ---
        with allure.step("Step 3: Assert database records are correct and properly stored"):
            assert result is not None, f"Project '{project_name}' was not found in the database."
            print(f"Database record for project '{project_name}': {result}")
            db_project_name, is_active, owner_id = result
            assert db_project_name == project_name
            print(f"Project Name: {db_project_name}, Is Active: {is_active}, Owner ID: {owner_id}")
            assert is_active == 1
            assert owner_id == 1
