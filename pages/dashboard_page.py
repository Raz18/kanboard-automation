"""Dashboard page object model for Kanboard application."""

from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List


class DashboardPage(BasePage):
    """Dashboard/Projects listing page object for Kanboard."""
    
    # Main navigation and dashboard elements
    MAIN_MENU = '#main-menu'
    USER_DROPDOWN = '.dropdown-menu'
    USER_AVATAR = '.avatar'
    LOGOUT_LINK = 'a[href*="logout"]'
    
    # Projects section
    PROJECTS_LINK = 'a[href*="/projects"], a[href*="project"]'
    NEW_PROJECT_BUTTON = 'a[href*="project/create"], .btn-blue[href*="create"]'
    PROJECT_TABLE = '.table-list, .project-table'
    PROJECT_ROWS = '.table-list tr, .project-table tr'
    PROJECT_LINKS = 'a[href*="project/show"]'
    PROJECT_TITLES = '.table-list td:first-child a, .project-table td:first-child a'
    
    # Quick actions
    ADD_PROJECT_LINK = 'a[href*="project/create"]'
    SEARCH_BOX = 'input[name="search"]'
    
    # Page indicators
    PAGE_TITLE = 'h1, .page-header h1'
    BREADCRUMB = '.breadcrumb'
    
    # Sidebar navigation
    SIDEBAR = '#sidebar'
    SIDEBAR_PROJECTS = '#sidebar a[href*="projects"]'
    SIDEBAR_DASHBOARD = '#sidebar a[href*="dashboard"]'
    
    def __init__(self, page: Page, base_url: str = "http://localhost:8080/"):
        super().__init__(page)
        self.base_url = base_url
        self.dashboard_url = f"{base_url}/dashboard"
    
    def navigate(self):
        """Navigate to the main dashboard."""
        self.navigate_to(self.dashboard_url)
    
    def go_to_projects(self):
        """Navigate to the projects listing page."""
        # Try multiple ways to access projects
        if self.is_element_visible(self.SIDEBAR_PROJECTS):
            self.click_element(self.SIDEBAR_PROJECTS)
        elif self.is_element_visible(self.PROJECTS_LINK):
            self.click_element(self.PROJECTS_LINK)
        else:
            # Direct navigation as fallback
            self.navigate_to(f"{self.base_url}/projects")
        
        self.wait_for_page_load()
    
    def click_new_project(self):
        """Click the new/create project button."""
        # First ensure we're on projects page
        self.go_to_projects()
        
        # Look for various forms of "new project" button
        selectors_to_try = [
            'a[href*="project/create"]',
            '.btn-blue[href*="create"]',
            'a:has-text("New project")',
            'a:has-text("Create")',
            'a[title*="project"]',
            '.btn[href*="create"]'
        ]
        
        for selector in selectors_to_try:
            if self.is_element_visible(selector):
                self.click_element(selector)
                self.wait_for_page_load()
                return
        
        raise Exception("Could not find 'New Project' button")
    
    def get_project_names(self) -> List[str]:
        """Get list of all project names displayed on the page."""
        if not self.is_element_visible(self.PROJECT_TABLE):
            return []
        
        # Get all project title elements
        project_elements = self.page.query_selector_all(self.PROJECT_TITLES)
        return [element.text_content().strip() for element in project_elements if element.text_content()]
    
    def is_project_listed(self, project_name: str) -> bool:
        """Check if a specific project is listed on the dashboard."""
        project_names = self.get_project_names()
        return project_name in project_names
    
    def click_project(self, project_name: str):
        """Click on a specific project by name to open it."""
        # Find the project link by text content
        project_links = self.page.query_selector_all(self.PROJECT_LINKS)
        
        for link in project_links:
            if link.text_content() and project_name in link.text_content():
                link.click()
                self.wait_for_page_load()
                return
        
        raise Exception(f"Project '{project_name}' not found in project list")
    
    def search_project(self, project_name: str):
        """Search for a project using the search box if available."""
        if self.is_element_visible(self.SEARCH_BOX):
            self.fill_element(self.SEARCH_BOX, project_name)
            # Press Enter to search
            self.page.keyboard.press('Enter')
            self.wait_for_page_load()
    
    def get_page_title(self) -> str:
        """Get the current page title."""
        if self.is_element_visible(self.PAGE_TITLE):
            return self.get_element_text(self.PAGE_TITLE)
        return ""
    
    def logout(self):
        """Logout from the application."""
        # Click user avatar/dropdown to open menu
        if self.is_element_visible(self.USER_AVATAR):
            self.click_element(self.USER_AVATAR)
        
        # Click logout link
        if self.is_element_visible(self.LOGOUT_LINK):
            self.click_element(self.LOGOUT_LINK)
            self.wait_for_page_load()
    
    def get_project_count(self) -> int:
        """Get the total number of projects displayed."""
        return len(self.get_project_names())
    
    def is_on_projects_page(self) -> bool:
        """Check if currently on the projects listing page."""
        current_url = self.get_current_url()
        page_title = self.get_page_title().lower()
        
        return ('project' in current_url.lower() or 
                'project' in page_title or 
                self.is_element_visible(self.PROJECT_TABLE))
    
    def navigate_to_dashboard(self):
        """Navigate back to main dashboard."""
        if self.is_element_visible(self.SIDEBAR_DASHBOARD):
            self.click_element(self.SIDEBAR_DASHBOARD)
        else:
            self.navigate_to(self.dashboard_url)
        
        self.wait_for_page_load()
