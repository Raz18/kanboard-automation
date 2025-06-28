"""Project page object model for Kanboard application."""

from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List, Dict, Optional


class ProjectPage(BasePage):
    """Project details and board management page object for Kanboard."""
    
    # Project creation form elements
    PROJECT_NAME_INPUT = 'input[name="name"]'
    PROJECT_DESCRIPTION_INPUT = 'textarea[name="description"]'
    PROJECT_IDENTIFIER_INPUT = 'input[name="identifier"]'
    CREATE_PROJECT_BUTTON = 'input[type="submit"], button[type="submit"]'
    SAVE_BUTTON = 'button:has-text("Save"), input[value="Save"]'
    
    # Project board view elements
    BOARD_VIEW = '.board'
    BOARD_COLUMNS = '.board-column'
    COLUMN_HEADER = '.board-column-header'
    COLUMN_TITLE = '.board-column-title'
    
    # Task elements
    TASK_ITEMS = '.task-board, .board-task'
    TASK_TITLE = '.task-board-title, .task-title'
    ADD_TASK_BUTTON = 'a[href*="task/create"], .btn[href*="task/create"]'
    TASK_FORM = '.task-form'
    TASK_TITLE_INPUT = 'input[name="title"]'
    TASK_DESCRIPTION_INPUT = 'textarea[name="description"]'
    TASK_COLOR_SELECT = 'select[name="color_id"]'
    TASK_PRIORITY_SELECT = 'select[name="priority"]'
    
    # Common Kanboard columns (may vary by installation)
    BACKLOG_COLUMN = '.board-column:has-text("Backlog")'
    TODO_COLUMN = '.board-column:has-text("To Do"), .board-column:has-text("Ready")'
    DOING_COLUMN = '.board-column:has-text("Work in progress"), .board-column:has-text("Doing")'
    DONE_COLUMN = '.board-column:has-text("Done")'
    
    # Task actions
    TASK_DROPDOWN = '.task-board .dropdown, .task-menu'
    TASK_EDIT_LINK = 'a[href*="task/edit"]'
    TASK_MOVE_LINK = 'a[href*="task/move"]'
    TASK_DELETE_LINK = 'a[href*="task/remove"]'
    
    # Project settings and actions
    PROJECT_SETTINGS = 'a[href*="project/edit"], a:has-text("Settings")'
    PROJECT_DELETE = 'a[href*="project/remove"]'
    PROJECT_MENU = '.dropdown-menu'
    
    # Navigation
    BREADCRUMB = '.breadcrumb'
    BACK_TO_PROJECTS = 'a[href*="/projects"]'
    
    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        super().__init__(page)
        self.base_url = base_url
    
    def create_project(self, name: str, description: str = "", identifier: str = ""):
        """Create a new project with the given details."""
        # Fill project name (required)
        self.fill_element(self.PROJECT_NAME_INPUT, name)
        
        # Fill description if provided
        if description and self.is_element_visible(self.PROJECT_DESCRIPTION_INPUT):
            self.fill_element(self.PROJECT_DESCRIPTION_INPUT, description)
        
        # Fill identifier if provided and field exists
        if identifier and self.is_element_visible(self.PROJECT_IDENTIFIER_INPUT):
            self.fill_element(self.PROJECT_IDENTIFIER_INPUT, identifier)
        
        # Submit the form
        submit_selectors = [
            self.CREATE_PROJECT_BUTTON,
            self.SAVE_BUTTON,
            'input[type="submit"]',
            'button[type="submit"]'
        ]
        
        for selector in submit_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                break
        
        self.wait_for_page_load()
    
    def add_task(self, title: str, description: str = "", column: str = ""):
        """Add a new task to the project."""
        # Click add task button
        add_task_selectors = [
            self.ADD_TASK_BUTTON,
            'a[href*="task/create"]',
            'a:has-text("Add a task")',
            '.add-task-button'
        ]
        
        for selector in add_task_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                break
        else:
            raise Exception("Could not find 'Add Task' button")
        
        self.wait_for_page_load()
        
        # Fill task form
        self.fill_element(self.TASK_TITLE_INPUT, title)
        
        if description and self.is_element_visible(self.TASK_DESCRIPTION_INPUT):
            self.fill_element(self.TASK_DESCRIPTION_INPUT, description)
        
        # Save the task
        save_selectors = [
            'input[type="submit"]',
            'button[type="submit"]',
            'button:has-text("Save")',
            '.btn-blue'
        ]
        
        for selector in save_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                break
        
        self.wait_for_page_load()
    
    def move_task_to_column(self, task_title: str, target_column: str):
        """Move a task to a specific column."""
        # Find the task element
        task_element = self.find_task_by_title(task_title)
        if not task_element:
            raise Exception(f"Task '{task_title}' not found on board")
        
        # Find target column
        target_column_element = self.find_column_by_title(target_column)
        if not target_column_element:
            raise Exception(f"Column '{target_column}' not found")
        
        # Try drag and drop first
        try:
            task_element.drag_to(target_column_element)
            self.wait_for_page_load()
            return
        except Exception:
            pass
        
        # Fallback: use task menu if drag-drop fails
        self.move_task_via_menu(task_title, target_column)
    
    def move_task_to_done(self, task_title: str):
        """Move a task to the Done column specifically."""
        self.move_task_to_column(task_title, "Done")
    
    def move_task_via_menu(self, task_title: str, target_column: str):
        """Move task using the task menu/dropdown."""
        task_element = self.find_task_by_title(task_title)
        if not task_element:
            raise Exception(f"Task '{task_title}' not found")
        
        # Click on task to access menu
        task_element.click()
        
        # Look for move option
        move_selectors = [
            'a[href*="task/move"]',
            'a:has-text("Move")',
            '.task-menu a[href*="move"]'
        ]
        
        for selector in move_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                
                # Select target column
                column_select = 'select[name="column_id"]'
                if self.is_element_visible(column_select):
                    self.page.select_option(column_select, label=target_column)
                    
                    # Save the move
                    self.click_element('input[type="submit"]')
                    self.wait_for_page_load()
                    return
        
        raise Exception(f"Could not move task '{task_title}' to '{target_column}'")
    
    def find_task_by_title(self, task_title: str):
        """Find a task element by its title."""
        task_elements = self.page.query_selector_all(self.TASK_ITEMS)
        
        for task in task_elements:
            task_text = task.text_content() or ""
            if task_title in task_text:
                return task
        
        return None
    
    def find_column_by_title(self, column_title: str):
        """Find a column element by its title."""
        column_elements = self.page.query_selector_all(self.BOARD_COLUMNS)
        
        for column in column_elements:
            column_text = column.text_content() or ""
            if column_title.lower() in column_text.lower():
                return column
        
        return None
    
    def get_tasks_in_column(self, column_name: str) -> List[str]:
        """Get all task titles in a specific column."""
        column_element = self.find_column_by_title(column_name)
        if not column_element:
            return []
        
        # Get tasks within this column
        tasks_in_column = column_element.query_selector_all(self.TASK_ITEMS)
        return [task.text_content().strip() for task in tasks_in_column if task.text_content()]
    
    def is_task_in_column(self, task_title: str, column_name: str) -> bool:
        """Check if a task is in a specific column."""
        tasks_in_column = self.get_tasks_in_column(column_name)
        return any(task_title in task for task in tasks_in_column)
    
    def is_task_in_done_column(self, task_title: str) -> bool:
        """Check if a task is in the Done column."""
        return self.is_task_in_column(task_title, "Done")
    
    def get_all_column_names(self) -> List[str]:
        """Get names of all columns in the project."""
        column_elements = self.page.query_selector_all(self.COLUMN_TITLE)
        return [col.text_content().strip() for col in column_elements if col.text_content()]
    
    def count_tasks_on_board(self) -> int:
        """Count total number of tasks visible on the board."""
        task_elements = self.page.query_selector_all(self.TASK_ITEMS)
        return len(task_elements)
    
    def count_tasks_in_column(self, column_name: str) -> int:
        """Count tasks in a specific column."""
        return len(self.get_tasks_in_column(column_name))
    
    def add_multiple_tasks(self, tasks_data: List[Dict[str, str]]):
        """Add multiple tasks efficiently."""
        for task_data in tasks_data:
            title = task_data.get('title', '')
            description = task_data.get('description', '')
            if title:
                self.add_task(title, description)
    
    def get_project_title(self) -> str:
        """Get the current project title from the page."""
        title_selectors = [
            'h1',
            '.page-header h1',
            '.project-header h1',
            '.breadcrumb li:last-child'
        ]
        
        for selector in title_selectors:
            if self.is_element_visible(selector):
                return self.get_element_text(selector)
        
        return ""
    
    def is_on_board_view(self) -> bool:
        """Check if currently viewing the project board."""
        return self.is_element_visible(self.BOARD_VIEW)
    
    def switch_to_board_view(self):
        """Switch to board view if not already there."""
        if not self.is_on_board_view():
            board_link_selectors = [
                'a[href*="board"]',
                'a:has-text("Board")',
                '.view-board'
            ]
            
            for selector in board_link_selectors:
                if self.is_element_visible(selector):
                    self.click_element(selector)
                    self.wait_for_page_load()
                    break
    
    def delete_project(self):
        """Delete the current project."""
        # Look for project settings/menu
        if self.is_element_visible(self.PROJECT_SETTINGS):
            self.click_element(self.PROJECT_SETTINGS)
        
        # Look for delete option
        if self.is_element_visible(self.PROJECT_DELETE):
            self.click_element(self.PROJECT_DELETE)
            
            # Confirm deletion if confirmation dialog appears
            confirm_selectors = [
                'button:has-text("Yes")',
                'button:has-text("Confirm")',
                'input[type="submit"][value*="Yes"]',
                'input[type="submit"][value*="Remove"]'
            ]
            
            for selector in confirm_selectors:
                if self.is_element_visible(selector):
                    self.click_element(selector)
                    self.wait_for_page_load()
                    return
    
    def go_back_to_projects(self):
        """Navigate back to projects listing."""
        if self.is_element_visible(self.BACK_TO_PROJECTS):
            self.click_element(self.BACK_TO_PROJECTS)
        else:
            self.navigate_to(f"{self.base_url}/projects")
        
        self.wait_for_page_load()
