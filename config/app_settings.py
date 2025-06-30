import os
from dotenv import load_dotenv


class AppSettings:
    """
    Centralized application settings for the Kanboard test automation framework.
    Loads configuration from a .env file and provides access via static methods.
    """
    load_dotenv()  # Load variables from .env file at the project root

    # --- Load settings as class attributes ---
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    number_of_tasks = os.getenv("NUMBER_OF_TASKS", "50")  # Default to 50 tasks if not set
    try:
        SLOW_MO = int(os.getenv("SLOW_MO", "0"))
    except (ValueError, TypeError):
        SLOW_MO = 0

    @staticmethod
    def get_base_url():
        """Returns the base URL for the application."""
        return AppSettings.BASE_URL

    @staticmethod
    def get_admin_password():
        """Returns the admin password."""
        return AppSettings.ADMIN_PASSWORD

    @staticmethod
    def is_headless():
        """Returns whether the browser should run in headless mode."""
        return AppSettings.HEADLESS

    @staticmethod
    def get_slow_mo():
        """Returns the delay in milliseconds between Playwright actions."""
        return AppSettings.SLOW_MO

    @staticmethod
    def get_number_of_tasks():
        """Returns the number of tasks to create."""
        try:
            return int(AppSettings.number_of_tasks)
        except ValueError:
            return 50  # Default to 50 if conversion fails
