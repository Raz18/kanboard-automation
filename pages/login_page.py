"""Login page object model for Kanboard application."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object for Kanboard application."""
    
    # Kanboard-specific login page locators
    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    LOGIN_BUTTON = 'button[type="submit"], input[type="submit"]'
    LOGIN_FORM = 'form[method="post"]'
    ERROR_MESSAGE = '.alert-error, .alert.alert-error'
    PAGE_HEADER = 'h1'
    REMEMBER_ME_CHECKBOX = 'input[name="remember_me"]'
    
    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        super().__init__(page)
        self.base_url = base_url
        self.login_url = base_url
    
    def navigate(self):
        """Navigate to the login page."""
        self.navigate_to(self.login_url)
    
    def login(self, username: str = "admin", password: str = "admin"):
        """
        Perform login with given credentials.
        Default credentials are admin/admin for fresh Kanboard installation.
        """
        # Wait for login form to be visible
        self.wait_for_element(self.LOGIN_FORM)
        
        # Fill username
        self.fill_element(self.USERNAME_INPUT, username)
        
        # Fill password
        self.fill_element(self.PASSWORD_INPUT, password)
        
        # Click login button
        self.click_element(self.LOGIN_BUTTON)
        
        # Wait for navigation after successful login
        self.wait_for_page_load()
    
    def is_login_form_visible(self) -> bool:
        """Check if login form is visible on the page."""
        return self.is_element_visible(self.LOGIN_FORM)
    
    def get_error_message(self) -> str:
        """Get error message if login fails."""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""
    
    def is_logged_in(self) -> bool:
        """
        Check if user is successfully logged in.
        After successful login, Kanboard redirects to dashboard and login form disappears.
        """
        # Wait a moment for potential redirect
        self.page.wait_for_timeout(2000)
        
        # Check if we're no longer on login page (login form not visible)
        return not self.is_login_form_visible()
    
    def set_remember_me(self, remember: bool = True):
        """Set the remember me checkbox if available."""
        if self.is_element_visible(self.REMEMBER_ME_CHECKBOX):
            if remember:
                self.page.check(self.REMEMBER_ME_CHECKBOX)
            else:
                self.page.uncheck(self.REMEMBER_ME_CHECKBOX)
    
    def get_page_header(self) -> str:
        """Get the page header text."""
        if self.is_element_visible(self.PAGE_HEADER):
            return self.get_element_text(self.PAGE_HEADER)
        return ""
    
    def login_with_invalid_credentials(self, username: str, password: str):
        """Attempt login with invalid credentials for testing purposes."""
        self.fill_element(self.USERNAME_INPUT, username)
        self.fill_element(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        
        # Wait for error message to appear
        self.page.wait_for_timeout(2000)
