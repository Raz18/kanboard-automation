from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProjectPage(BasePage):
    """
    Represents project-related pages (creation, board, settings) with synchronous methods.
    """

    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        super().__init__(page)
        self.base_url = base_url

        # --- Locators ---
        self.project_name_input = self.locate('#form-name')
        self.submit_button = self.locate('button[type="submit"]')
        self.project_header_title = self.locate("span.title")

        # Task related locators
        self.add_task_link_to_ready = self.locate('th.board-column-header:has-text("Ready")')
        self.task_title_input = self.locate('input#form-title')
        self.description_input_placeholder = 'Write your text in Markdown'

        # Board related locators
        self.done_column = self.locate('td.board-column-done')

        # Project deletion locators
        self.settings_link = self.locate('a.action-menu.dropdown-menu')
        # UPDATED: More specific locator for the "Configure this project" link inside the dropdown.
        self.configure_project_link = self.locate('#dropdown a:has-text("Configure this project")')
        self.remove_link = self.get_by_role("link", name="Remove")
        self.confirm_yes_button = self.get_by_role("button", name="Yes")


    def create_project(self, name: str):
        """Fills out and submits the new project form."""
        self.write_on_element(self.project_name_input, name)
        self.click_element(self.submit_button)
        # Verify that the page has navigated to the new project board
        expect(self.project_header_title).to_contain_text(name)

    def add_task(self, title: str):
        """Navigates to the new task form and creates a task."""
        add_task_button = self.add_task_link_to_ready.locator('.board-add-icon a')
        # Use the click method from BasePage
        self.click_element(add_task_button)
        # Verify navigation to the new task page
        expect(self.locate('h2')).to_contain_text("New task")
        self.write_on_element(self.task_title_input, title)
        # Fill in the description if needed
        self.write_on_element(self.locate('textarea[placeholder="' + self.description_input_placeholder + '"]'), "This is a test task.")

        self.click_element(self.submit_button)
        # Verify the task appears on the board
        new_task_locator = self.locate(f'.task-board-title:has-text("{title}")')
        expect(new_task_locator).to_be_visible()

    def navigate_to_task(self, task_name: str):
        """
        Navigates to the task detail page by finding and clicking the task on the board.

        Args:
            task_name: The exact title of the task to click on.
        """
        # This locator specifically targets the link within an element that has the task title.
        # This is more robust than a generic text selector.
        task_link_locator = self.locate(f'.task-board-title:has-text("{task_name}") a')
        self.click_element(task_link_locator)
        # Verify that we've landed on the correct task detail page.

    def delete_project(self):
        """
        Deletes the current project by navigating through the UI menus and confirming.
        This implementation follows the user's specified click sequence.
        """
        # First, click on settings to open the dropdown.
        self.click_element(self.settings_link)

        # On the project board, find and click "Configure this project" in the now-visible dropdown.
        self.click_element(self.configure_project_link)

        # On the project settings page, find and click the "Remove" link.
        self.click_element(self.remove_link)

        # In the confirmation modal, click the "Yes" button.
        self.click_element(self.confirm_yes_button)

        # Verify that we are redirected back to the main project list.
        self.page.wait_for_url("**/projects")
        self.logger.info("Successfully deleted project and confirmed redirect to the dashboard.")
