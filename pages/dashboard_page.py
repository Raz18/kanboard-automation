from typing import List
from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Represents the main Dashboard page with synchronous interactions.
    """

    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        super().__init__(page)
        self.base_url = base_url
        self.new_project_button = self.locate('.page-header a[href="/project/create"]')
        self.project_list_section = self.locate('div.table-list')
        self.project_links = self.project_list_section.locator('.table-list-title a')
        self.next_page_link = self.locate('span.pagination-next a')

    def navigate(self):
        """Navigate to the main dashboard."""
        self.navigate_to(f"{self.base_url}/dashboard")

    def navigate_to_project(self, project_name: str):
        """
        Navigates to a specific project, handling pagination.
        It searches through pages until it finds the project link and clicks it.
        """
        self.navigate()
        while True:
            project_link = self.project_list_section.locator(f'a:has-text("{project_name}")')
            # Use a short timeout to quickly check for visibility on the current page.
            if project_link.is_visible():
                self.logger.info(f"Found project '{project_name}', clicking it.")
                self.click_element(project_link)
                # Verify navigation was successful
                expect(self.locate('span.title')).to_contain_text(project_name)
                return

            # Use a short timeout to prevent long waits on the last page.
            if self.next_page_link.is_visible():
                self.logger.info(f"Project '{project_name}' not on this page, clicking 'Next'.")
                self.click_element(self.next_page_link)
                self.project_list_section.wait_for(state="visible")
            else:
                self.logger.error(f"Project '{project_name}' not found after checking all pages.")
                raise ValueError(f"Project '{project_name}' not found after checking all pages.")


    def click_new_project(self):
        """Clicks the 'New project' button."""
        self.click_element(self.new_project_button)
        expect(self.locate('h2')).to_contain_text("New project")

    def get_project_names(self) -> List[str]:
        """Gets a list of all project names on the page."""
        if not self.project_list_section.is_visible():
            return []
        return self.project_links.all_text_contents()

    def is_project_listed(self, project_name: str) -> bool:
        """
        Checks if a project is listed on the dashboard, handling pagination.
        It iterates through all pages of the project list until the project is found
        or there are no more pages.
        """
        self.navigate()
        while True:
            current_projects = self.get_project_names()
            if project_name in current_projects:
                self.logger.info(f"Found project '{project_name}' on the current page.")
                return True

            # Use a short timeout to prevent long waits on the last page.
            if self.next_page_link.is_visible():
                self.logger.info("Project not found on this page, clicking 'Next' to check the next page.")
                self.click_element(self.next_page_link)
                self.project_list_section.wait_for(state="visible")
            else:
                self.logger.info(f"Project '{project_name}' not found after checking all pages.")
                return False
