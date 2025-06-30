from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class TaskPage(BasePage):
    """
    Represents the task detail view and its associated actions with synchronous methods.
    """

    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        super().__init__(page)
        self.base_url = base_url

        # --- Locators based on the provided HTML ---

        # Main task view elements
        self.task_summary_title = self.locate('#task-summary h2')
        self.task_description = self.locate('details.accordion-section:has-text("Description") .markdown')

        # Sidebar action links
        self.close_task_link = self.locate('.sidebar a[href*="/close"]')
        self.remove_task_link = self.locate('.sidebar a[href*="/remove"]')

        # Comment form elements
        self.comment_textarea = self.locate('textarea[name="comment"]')
        self.save_comment_button = self.locate('#comments .form-actions button[type="submit"]')

        # Confirmation modal button (for closing or deleting)
        self.confirm_button = self.locate('button#modal-confirm-button')

    def get_task_title(self) -> str:
        """Gets the task title from the task summary view."""
        return self.get_text(self.task_summary_title)

    def get_task_description(self) -> str:
        """Gets the task description from the accordion section."""
        if self.task_description.is_visible():
            return self.get_text(self.task_description)
        return ""

    def move_task_to_done(self):
        """
        Moves the task to the 'Done' state by closing it from the task view.
        This is the functional equivalent of moving to the 'Done' column.
        """

        #click the move task status link in the sidebar
        move_task_status = self.page.get_by_role("link", name="Move position")
        self.click_element(move_task_status)
        #from dropdown menu, select "Done"
        dropdown_menu = self.locate('select#form-columns')
        dropdown_menu.select_option(value="Done")
        #click the save button
        save_button = self.locate('button[type="submit"]').nth(1)
        self.click_element(save_button)
        # Verify that the task is now in the Done column
        expect(self.locate('div.task-summary-column')).to_contain_text("Done")

    def delete_task(self):
        """
        Deletes the current task from the sidebar actions.
        """
        delete_task = self.page.get_by_role("link", name="Remove")

        # Click the "Remove" link in the sidebar
        self.click_element(delete_task)

        # Click the final confirmation button in the modal
        self.click_element(self.confirm_button)

        # After deleting, the user is returned to the board view.
        expect(self.locate('#board')).to_be_visible()
