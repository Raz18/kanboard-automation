from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from config.app_settings import AppSettings
from utils.logger import setup_logger

class LoginPage(BasePage):
    """
    Represents the Login Page of the Kanboard application.
    This class contains all the locators and methods required to interact with the login page,
    such as entering credentials and verifying successful login.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = setup_logger(self.__class__.__name__)
        # --- Locators ---
        self.username_input = self.locate("#form-username")
        self.password_input = self.locate("#form-password")
        self.login_button = self.locate("button[type='submit']")
        self.dashboard_header = self.locate("h1:has-text('Dashboard')")

    def navigate(self):
        """Navigates to the application's login page."""
        self.logger.info(f"Navigating to the login page at {AppSettings.get_base_url()}")
        self.navigate_to(AppSettings.get_base_url())

    def login(self, username, password):
        """Fills the login form and submits it."""
        self.logger.info(f"Attempting to log in with username: {username}")
        try:
            self.write_on_element(self.username_input, username)
            self.write_on_element(self.password_input, password)
            self.click_element(self.login_button)
            self.logger.info("Login form submitted successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred during the login process: {e}")
            self.take_screenshot("login_error.png")
            raise

    def verify_login_successful(self):
        """Verifies that the login was successful by checking for a key element on the dashboard."""
        self.logger.info("Verifying that login was successful by checking for the Dashboard header.")
        try:
            expect(self.dashboard_header).to_be_visible(timeout=10000)
            self.logger.info("Login verification successful: Dashboard header is visible.")
        except Exception as e:
            self.logger.error(f"Login verification failed. Dashboard header was not found: {e}")
            self.take_screenshot("login_verification_failed.png")
            raise