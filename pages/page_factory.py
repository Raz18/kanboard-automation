"""Page Factory for creating and managing page objects."""

from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.project_page import ProjectPage
from pages.task_page import TaskPage
from pages.settings_page import SettingsPage
from typing import Union


class PageFactory:
    """Factory class for creating page objects with consistent configuration."""
    
    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        """
        Initialize the page factory.
        
        Args:
            page: Playwright page instance
            base_url: Base URL of the Kanboard application
        """
        self.page = page
        self.base_url = base_url
    
    def get_login_page(self) -> LoginPage:
        """Get an instance of the login page."""
        return LoginPage(self.page, self.base_url)
    
    def get_dashboard_page(self) -> DashboardPage:
        """Get an instance of the dashboard page."""
        return DashboardPage(self.page, self.base_url)
    
    def get_project_page(self) -> ProjectPage:
        """Get an instance of the project page."""
        return ProjectPage(self.page, self.base_url)
    
    def get_task_page(self) -> TaskPage:
        """Get an instance of the task page."""
        return TaskPage(self.page, self.base_url)
    
    def get_settings_page(self) -> SettingsPage:
        """Get an instance of the settings page."""
        return SettingsPage(self.page, self.base_url)
    
    def navigate_and_login(self, username: str = "admin", password: str = "admin") -> DashboardPage:
        """
        Navigate to login page, perform login, and return dashboard page.
        
        Args:
            username: Login username (default: admin)
            password: Login password (default: admin)
            
        Returns:
            DashboardPage instance after successful login
        """
        login_page = self.get_login_page()
        login_page.navigate()
        login_page.login(username, password)
        
        if not login_page.is_logged_in():
            raise Exception("Login failed")
        
        return self.get_dashboard_page()
    
    def create_authenticated_session(self, username: str = "admin", password: str = "admin"):
        """
        Create an authenticated session and return page factory.
        
        Args:
            username: Login username
            password: Login password
            
        Returns:
            Self for method chaining
        """
        self.navigate_and_login(username, password)
        return self
    
    def get_current_page_type(self) -> str:
        """
        Detect the current page type based on URL and page content.
        
        Returns:
            String indicating the page type
        """
        current_url = self.page.url.lower()
        
        if 'login' in current_url or self.page.query_selector('form[method="post"]'):
            return "login"
        elif 'project/edit' in current_url or 'settings' in current_url:
            return "settings"
        elif 'project/show' in current_url or 'board' in current_url:
            return "project"
        elif 'task' in current_url:
            return "task"
        elif 'projects' in current_url or self.page.query_selector('.project-table'):
            return "dashboard"
        else:
            return "unknown"
    
    def get_appropriate_page_object(self) -> Union[LoginPage, DashboardPage, ProjectPage, TaskPage, SettingsPage]:
        """
        Get the appropriate page object based on current page.
        
        Returns:
            The appropriate page object for the current page
        """
        page_type = self.get_current_page_type()
        
        if page_type == "login":
            return self.get_login_page()
        elif page_type == "dashboard":
            return self.get_dashboard_page()
        elif page_type == "project":
            return self.get_project_page()
        elif page_type == "task":
            return self.get_task_page()
        elif page_type == "settings":
            return self.get_settings_page()
        else:
            # Default to dashboard page
            return self.get_dashboard_page()
    
    def ensure_logged_in(self, username: str = "admin", password: str = "admin"):
        """
        Ensure user is logged in, login if necessary.
        
        Args:
            username: Login username
            password: Login password
        """
        # Check if already logged in by looking for login form
        if self.page.query_selector('form[method="post"]') and 'login' in self.page.url.lower():
            self.navigate_and_login(username, password)
    
    def logout(self):
        """Logout from the application."""
        dashboard = self.get_dashboard_page()
        dashboard.logout()
    
    def take_screenshot(self, name: str):
        """Take a screenshot with the given name."""
        import os
        os.makedirs("screenshots", exist_ok=True)
        self.page.screenshot(path=f"screenshots/{name}.png", full_page=True)
