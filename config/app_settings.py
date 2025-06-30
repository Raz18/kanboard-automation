
import 
class AppSettings:
    """
    Centralized application settings for the Kanboard test automation framework.
    Loads configuration from a .env file and provides access via static methods.
    """
    load_dotenv() # Load variables from .env file at the project root

    # --- Load settings as class attributes ---
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    try:
        SLOW_MO = int(os.getenv("SLOW_MO", "0"))
    except (ValueError, TypeError):
        SLOW_MO = 0

    # --- Static methods to access settings ---

    @staticmethod
    def get_base_url():
        """Returns the base URL for the application."""
        return AppSettings.BASE_URL

    @staticmethod
    def get_admin_user():
        """Returns the admin username."""
        return AppSettings.ADMIN_USER

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
