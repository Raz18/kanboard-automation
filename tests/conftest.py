# conftest.py
# This file contains fully synchronous fixtures for the test suite.
import asyncio
import os

import asyncpg
import pytest
import psycopg2
import time

import pytest_asyncio
from playwright.sync_api import Page, Playwright, BrowserContext
from pages.login_page import LoginPage  # Ensure this path is correct
from config.app_settings import AppSettings  # Ensure this path is correct


# --- Database Fixture (Synchronous with Retry) ---
@pytest.fixture(scope="session")
def db_connection():
    """
    Creates and manages a standard synchronous connection to the PostgreSQL database.
    Includes a retry mechanism to handle race conditions during startup.
    """
    conn = None
    last_exception = None
    for _ in range(15):
        try:
            conn = psycopg2.connect(
                dsn="dbname=kanboard user=kanboard password=kanboard123 host=localhost port=5432"
            )
            print("\nSynchronous database connection successful.")
            yield conn
            conn.close()
            print("\nDatabase connection closed.")
            return
        except psycopg2.OperationalError as e:
            print(f"\nDatabase connection attempt failed: {e}. Retrying in 2 seconds...")
            last_exception = e
            time.sleep(2)
    pytest.fail(f"Database connection failed after multiple retries: {last_exception}")





# --- Playwright Fixtures (Synchronous) ---

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """
    Overrides pytest-playwright's default launch arguments.
    Allows controlling headless mode and slow_mo via environment variables.
    Example for visible browser with delay:
        HEADLESS=false SLOW_MO=500 pytest
    """
    headless = AppSettings.is_headless()
    slow_mo = AppSettings.get_slow_mo()
    options = {"headless": headless, "slow_mo": slow_mo}
    print(f"\nConfiguring main test browser with: {options}")
    return options



AUTH_FILE = "auth.json"

@pytest.fixture(scope="session")
def authenticated_state_fixture(playwright: Playwright):
    """
    A session-scoped fixture that logs in ONCE via the UI.
    It saves the authentication state (cookies, local storage) to a file
    and yields the path to that file.
    It also handles cleanup of the auth file at the end of the session.
    """
    # Check if auth file already exists to avoid re-login during a session
    if not os.path.exists(AUTH_FILE):
        print("\nPerforming one-time UI login for the session...")
        # Use a new browser for a clean login process
        browser = playwright.chromium.launch(headless=False, slow_mo=10)
        page = browser.new_page()

        # Perform the login
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(AppSettings.ADMIN_USER, AppSettings.ADMIN_PASSWORD)
        login_page.verify_login_successful()

        # Save the authentication state
        page.context.storage_state(path=AUTH_FILE)
        print(f"Authentication state saved to {AUTH_FILE}")

        # Close the browser used for login
        browser.close()

    # Yield the path to the auth file for other fixtures to use
    yield AUTH_FILE

    # --- Teardown for the entire session ---
    # Clean up the auth file after all tests are done
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)
        print(f"\nSession finished. Cleaned up and removed {AUTH_FILE}.")


@pytest.fixture(scope="function")
def admin_page_fixture(browser, authenticated_state_fixture) -> Page:
    """
    A function-scoped fixture that provides a fresh, authenticated page for each test.

    It does NOT log in via the UI. Instead, it creates a new, isolated browser context
    for each test and loads the session's saved authentication state into it.
    This is fast and ensures tests do not interfere with each other.
    """
    # Create a new, isolated context with the saved authentication state
    context: BrowserContext = browser.new_context(storage_state=authenticated_state_fixture)
    page = context.new_page()

    page.goto(AppSettings.get_base_url())

    yield page

    # Teardown for each function (test)
    context.close()
