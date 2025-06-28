"""
Centralized locators for Kanboard UI elements.
This file contains all CSS selectors and XPath expressions organized by page/functionality.
"""

class LoginPageLocators:
    """Locators for Kanboard login page."""
    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    LOGIN_BUTTON = 'button[type="submit"], input[type="submit"]'
    LOGIN_FORM = 'form[method="post"]'
    ERROR_MESSAGE = '.alert-error, .alert.alert-error'
    REMEMBER_ME_CHECKBOX = 'input[name="remember_me"]'
    PAGE_HEADER = 'h1'


class DashboardLocators:
    """Locators for Kanboard dashboard and navigation."""
    # Main navigation
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
    
    # Sidebar navigation
    SIDEBAR = '#sidebar'
    SIDEBAR_PROJECTS = '#sidebar a[href*="projects"]'
    SIDEBAR_DASHBOARD = '#sidebar a[href*="dashboard"]'
    
    # Search and filters
    SEARCH_BOX = 'input[name="search"]'
    FILTER_DROPDOWN = '.filter-dropdown'


class ProjectPageLocators:
    """Locators for project creation and management."""
    # Project creation form
    PROJECT_NAME_INPUT = 'input[name="name"]'
    PROJECT_DESCRIPTION_INPUT = 'textarea[name="description"]'
    PROJECT_IDENTIFIER_INPUT = 'input[name="identifier"]'
    CREATE_PROJECT_BUTTON = 'input[type="submit"], button[type="submit"]'
    SAVE_BUTTON = 'button:has-text("Save"), input[value="Save"]'
    
    # Project board view
    BOARD_VIEW = '.board'
    BOARD_COLUMNS = '.board-column'
    COLUMN_HEADER = '.board-column-header'
    COLUMN_TITLE = '.board-column-title'
    
    # Default Kanboard columns
    BACKLOG_COLUMN = '.board-column:has-text("Backlog")'
    TODO_COLUMN = '.board-column:has-text("To Do"), .board-column:has-text("Ready")'
    DOING_COLUMN = '.board-column:has-text("Work in progress"), .board-column:has-text("Doing")'
    DONE_COLUMN = '.board-column:has-text("Done")'
    
    # Task elements on board
    TASK_ITEMS = '.task-board, .board-task'
    TASK_TITLE = '.task-board-title, .task-title'
    ADD_TASK_BUTTON = 'a[href*="task/create"], .btn[href*="task/create"]'
    
    # Project actions
    PROJECT_SETTINGS = 'a[href*="project/edit"], a:has-text("Settings")'
    PROJECT_DELETE = 'a[href*="project/remove"]'


class TaskPageLocators:
    """Locators for task creation and management."""
    # Task form elements
    TASK_TITLE_INPUT = 'input[name="title"]'
    TASK_DESCRIPTION_INPUT = 'textarea[name="description"]'
    TASK_COLOR_SELECT = 'select[name="color_id"]'
    TASK_PRIORITY_SELECT = 'select[name="priority"]'
    TASK_CATEGORY_SELECT = 'select[name="category_id"]'
    TASK_ASSIGNEE_SELECT = 'select[name="owner_id"]'
    TASK_DUE_DATE_INPUT = 'input[name="date_due"]'
    TASK_START_DATE_INPUT = 'input[name="date_started"]'
    TASK_TIME_ESTIMATED_INPUT = 'input[name="time_estimated"]'
    TASK_TIME_SPENT_INPUT = 'input[name="time_spent"]'
    
    # Task actions
    SAVE_TASK_BUTTON = 'input[type="submit"], button[type="submit"]'
    CANCEL_BUTTON = 'a:has-text("Cancel")'
    DELETE_TASK_BUTTON = 'a[href*="task/remove"]'
    DUPLICATE_TASK_BUTTON = 'a[href*="task/duplicate"]'
    MOVE_TASK_BUTTON = 'a[href*="task/move"]'
    
    # Task display
    TASK_DETAILS = '.task-details'
    TASK_HEADER = '.task-header'
    TASK_TITLE_DISPLAY = '.task-title, h1'
    TASK_DESCRIPTION_DISPLAY = '.task-description'
    
    # Comments
    COMMENTS_SECTION = '.comments'
    COMMENT_TEXTAREA = 'textarea[name="comment"]'
    ADD_COMMENT_BUTTON = 'input[value="Add comment"], button:has-text("Add comment")'
    COMMENT_ITEMS = '.comment'
    
    # Subtasks
    SUBTASKS_SECTION = '.subtasks'
    ADD_SUBTASK_BUTTON = 'a[href*="subtask/create"]'
    SUBTASK_ITEMS = '.subtask'
    
    # Attachments
    ATTACHMENTS_SECTION = '.attachments'
    ADD_ATTACHMENT_BUTTON = 'input[type="file"]'
    ATTACHMENT_ITEMS = '.attachment'


class SettingsPageLocators:
    """Locators for project settings and administration."""
    # Settings navigation
    SETTINGS_MENU = '.sidebar-menu'
    PROJECT_SETTINGS_TAB = 'a[href*="project/edit"]'
    USERS_TAB = 'a[href*="project/users"]'
    PERMISSIONS_TAB = 'a[href*="project/permissions"]'
    CATEGORIES_TAB = 'a[href*="category"]'
    COLUMNS_TAB = 'a[href*="column"]'
    
    # Project settings form
    PROJECT_NAME_INPUT = 'input[name="name"]'
    PROJECT_IDENTIFIER_INPUT = 'input[name="identifier"]'
    PROJECT_DESCRIPTION_INPUT = 'textarea[name="description"]'
    PROJECT_OWNER_SELECT = 'select[name="owner_id"]'
    PROJECT_PRIVATE_CHECKBOX = 'input[name="is_private"]'
    
    # Column management
    COLUMNS_TABLE = '.columns-table'
    ADD_COLUMN_BUTTON = 'a[href*="column/create"]'
    COLUMN_NAME_INPUT = 'input[name="title"]'
    COLUMN_LIMIT_INPUT = 'input[name="task_limit"]'
    
    # User management
    USERS_TABLE = '.users-table'
    ADD_USER_BUTTON = 'a[href*="project/users/add"]'
    USER_SELECT = 'select[name="user_id"]'
    ROLE_SELECT = 'select[name="role"]'
    
    # Categories
    CATEGORIES_TABLE = '.categories-table'
    ADD_CATEGORY_BUTTON = 'a[href*="category/create"]'
    CATEGORY_NAME_INPUT = 'input[name="name"]'
    CATEGORY_COLOR_SELECT = 'select[name="color_id"]'
    
    # Danger zone
    DELETE_PROJECT_BUTTON = 'a[href*="project/remove"]'
    CONFIRM_DELETE_INPUT = 'input[name="confirmation"]'
    CONFIRM_DELETE_BUTTON = 'input[type="submit"][value*="Remove"]'


class CommonLocators:
    """Common locators used across multiple pages."""
    # Form elements
    SAVE_BUTTON = 'input[type="submit"], button[type="submit"]'
    CANCEL_BUTTON = 'a:has-text("Cancel")'
    DELETE_BUTTON = 'a[href*="remove"], button:has-text("Delete")'
    EDIT_BUTTON = 'a[href*="edit"], button:has-text("Edit")'
    
    # Confirmation dialogs
    CONFIRM_YES_BUTTON = 'button:has-text("Yes"), input[value*="Yes"]'
    CONFIRM_NO_BUTTON = 'button:has-text("No"), input[value*="No"]'
    CONFIRM_CANCEL_BUTTON = 'button:has-text("Cancel")'
    
    # Alerts and messages
    SUCCESS_MESSAGE = '.alert-success, .success-message'
    ERROR_MESSAGE = '.alert-error, .error-message'
    WARNING_MESSAGE = '.alert-warning, .warning-message'
    INFO_MESSAGE = '.alert-info, .info-message'
    
    # Navigation
    BREADCRUMB = '.breadcrumb'
    PAGE_TITLE = 'h1, .page-header h1'
    BACK_BUTTON = 'a:has-text("Back")'
    
    # Loading states
    LOADING_SPINNER = '.loading, .spinner'
    LOADING_OVERLAY = '.loading-overlay'
    
    # Tables
    TABLE_HEADER = 'th'
    TABLE_ROW = 'tr'
    TABLE_CELL = 'td'
    
    # Dropdowns and selects
    DROPDOWN_TOGGLE = '.dropdown-toggle'
    DROPDOWN_MENU = '.dropdown-menu'
    SELECT_OPTION = 'option'


class KanboardSelectors:
    """Main class containing all locator groups."""
    Login = LoginPageLocators
    Dashboard = DashboardLocators
    Project = ProjectPageLocators
    Task = TaskPageLocators
    Settings = SettingsPageLocators
    Common = CommonLocators
