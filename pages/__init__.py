"""Pages package initialization - Page Object Model for Kanboard UI automation."""

from .base_page import BasePage
from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .project_page import ProjectPage
from .task_page import TaskPage
from .settings_page import SettingsPage
from .locators import KanboardSelectors
from .page_factory import PageFactory

__all__ = [
    'BasePage',
    'LoginPage',
    'DashboardPage', 
    'ProjectPage',
    'TaskPage',
    'SettingsPage',
    'KanboardSelectors',
    'PageFactory'
]
