from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Represents the Login page with synchronous user interactions.
    """

    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        super().__init__(page)
        self.base_url = base_url
        self.username_input = self.locate('#form-username')
        self.password_input = self.locate('#form-password')
        self.login_button = self.locate('button[type="submit"]')
        self.dashboard_title = self.locate("div.title-container")

    def navigate(self):
        """Navigates to the login page."""
        self.navigate_to(f"{self.base_url}/")

    def login(self, username, password):
        """Executes the synchronous login flow."""
        self.write_on_element(self.username_input, username)
        self.write_on_element(self.password_input, password)
        self.click_element(self.login_button)

    def verify_login_successful(self):
        """Verifies that the login was successful by checking the dashboard title."""

        self.wait_for(self.dashboard_title)
        self.logger.info("login successful.")
