# Kanboard QA Automation Framework

This repository contains a professional-grade, end-to-end automation testing framework for the Kanboard application. It is engineered for robustness, scalability, and maintainability, providing comprehensive test coverage from the UI layer down to the database.

## 1. Architecture and Design

The framework is built upon a clean, layered architecture that separates concerns, enhances code reusability, and simplifies test maintenance.

### 1.1. Architecture Diagram
The project follows a standardized and intuitive directory structure.
```
kanboard-automation/
├── .env                  # Local environment variables (credentials, URLs). Not committed to Git.
├── .gitignore            # Specifies files and directories to be ignored by Git.
├── config/               
│   └── app_settings.py   # Application configuration settings.
├── docker-compose.yml    # Defines and configures the multi-container Docker environment.
├── pages/                # The Page Object Model layer. Each file represents a page in the UI.
│   ├── base_page.py      # Base class for all page objects with common methods (click, navigate).
│   ├── dashboard_page.py
│   ├── login_page.py
│   ├── project_page.py
│   └── task_page.py
├── pytest.ini            # Configuration file for pytest (e.g., markers, default options).
├── README.md             # This documentation file.
├── requirements.txt      # List of Python dependencies for the project.
├── screenshots/          # Directory where screenshots are saved on test failure.
├── tests/                # Contains all the automated test cases.
│   ├── conftest.py       # Pytest fixtures for setup and teardown (e.g., browser, DB connection).
│   ├── test_*.py         # Test files, each focused on a specific feature.
└── utils/                # Reusable helper modules and utilities.
    ├── logger.py         # Centralized logging configuration.

```

### 1.2. Architectural Layers

**Test Cases** (`/tests`): This is the highest level of abstraction. Each test file corresponds to a specific feature or user flow (e.g., `test_project_creation.py`). Tests are written to be descriptive and readable, focusing on the *what* (the business logic being tested) rather than the *how* (the implementation details).

**Page Object Model** (`/pages`): This layer abstracts the UI components. Each page in the Kanboard application (e.g., LoginPage, DashboardPage) is represented by a class. These classes encapsulate the locators and the methods to interact with the elements on that page. This design makes tests resilient to UI changes; if a locator changes, the update is only required in one place.

**Utilities** (`/utils`): This layer contains reusable helper modules that are not specific to any single page, such as:
- `logger.py`: Provides a centralized logging setup.

**Configuration** (`/config` & `.env`): Manages all external configuration parameters, such as URLs, credentials, and test execution settings (e.g., headless mode). This separation allows for easy modification of settings without changing the test code.

## 2. Technological Stack & Key Features

This framework leverages a modern stack to deliver a robust and efficient testing solution.

| Component | Technology | Purpose & Key Features |
|-----------|------------|------------------------|
| Test Runner | pytest | A powerful testing framework for Python. Used for its simple syntax, powerful fixture model (`conftest.py`), and extensive plugin ecosystem. |
| UI Automation | Playwright | A modern browser automation library. Chosen for its speed, reliability, and auto-waiting capabilities, which eliminate most flaky tests caused by timing issues. It also provides rich features like network interception and device emulation. |
| Database Validation | psycopg2 | The most popular PostgreSQL adapter for Python. It allows for direct database queries to validate that UI actions result in the correct data state, providing a deeper level of verification than UI checks alone. |
| Environment Mgmt | Docker / python-dotenv | Docker and docker-compose create a consistent, isolated environment for the Kanboard app and its database. python-dotenv loads sensitive data (like credentials) and configurations from an `.env` file, keeping them out of the code. |
| Reporting | Allure | A flexible, lightweight multi-language test report tool. It creates rich, interactive HTML reports with test steps, screenshots on failure, and clear categorizations, making it easy to analyze test results. |

### 2.1. Advanced Technical Implementations

#### Robust UI Interactions
The framework is engineered to handle the complexities of modern web applications:

- **Explicit and Implicit Waits**: While Playwright's auto-waiting handles most synchronization, the BasePage includes a `wait_for()` method for scenarios requiring explicit waits for elements or states.

- **Retry Mechanisms**: The custom `click_element` method includes a built-in retry loop, making it resilient to occasional UI lag where an element might not be immediately clickable.

- **Complex Gestures**: The framework demonstrates advanced interactions like `find project` that go over all project pages to find the desired project page name.

- **Smart Locators**: Locators are defined at the top of each page object for easy maintenance. Dynamic locators (e.g., `task_selector_by_title`) are implemented as functions to find elements based on runtime data.

#### Efficient Test Execution: Session-Based Authentication
To significantly speed up the test suite, the `authenticated_state_fixture` in `conftest.py` implements a highly efficient authentication strategy:

1. **One-Time Login**: At the beginning of the entire test session, it performs a single UI login.
2. **State Caching**: It saves the browser's authentication state (cookies, local storage) to a file (`playwright/.auth/auth.json`).
3. **Context Injection**: For every subsequent test, it creates a new, pristine browser context and injects the saved authentication state.

This approach bypasses the slow and repetitive UI login for each test, shaving significant time off the total execution run while maintaining perfect test isolation.

#### Comprehensive Logging
Traceability is key for debugging. The `utils/logger.py` module provides a centralized `setup_logger` function that is used in every class.

- **Class-Specific Loggers**: Each class (LoginPage, DBValidator, etc.) gets its own named logger instance.
- **Clear & Formatted Output**: Logs are formatted with a timestamp, logger name, level, and message, making it easy to trace the execution flow and pinpoint exactly where an error occurred.

**Example Log Output:**
```
2025-06-30 15:55:10 - LoginPage - INFO - Attempting to log in with username: admin
2025-06-30 15:55:11 - ProjectPage - INFO - Creating a new project with name: Project-a1b2c3d4
2025-06-30 15:55:12 - DBValidator - INFO - Executing query: SELECT id FROM projects WHERE name = %s;
```

## 3. Test Plan

The following test plan outlines the critical user flows covered by this automation suite.

| Test ID | Test Case | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| TC-01 | Test Project Creation & DB Validation | Creates a new project via the UI and validates that the project record is correctly created in the projects table in the database. | The project appears in the UI, and a corresponding record with the correct name exists in the database. |
| TC-02 | Test Full Task Lifecycle | Creates a task, drags it from the "Backlog" to the "Done" column, and verifies that its column_id is updated in the tasks table. | The task visually moves on the board, and its column_id in the database is updated to reflect the "Done" state. |
| TC-03 | Test Data Integrity on Deletion | Creates a project with multiple tasks, deletes the project, and then verifies that the project and all its child tasks are removed. | The project and all associated tasks are no longer present in the database, ensuring no orphaned data. |
| TC-04 | Test Database Retrieval Performance | Creates a project with 50 tasks and measures the time taken to retrieve all tasks for that project with a single database query. | The query response time is within an acceptable performance threshold (e.g., < 1.0 second). |

## 4. Getting Started

Follow these steps to set up the project and run the tests.

### 4.1. Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Git

### 4.2. Setup and Installation

```bash
# 1. Clone the repository from GitHub
git clone <your-repo-link>
cd kanboard-automation

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install the necessary Playwright browsers
playwright install

# 4. Create your local environment configuration file
# (You can copy the provided .env.example)
cp .env.example .env

# 5. Start the Dockerized application environment
# This will pull and run the Kanboard and PostgreSQL containers
docker-compose up -d
```

### 4.3. Running the Tests

Execute the tests using the pytest command.

```bash
# Run all tests in the 'tests' directory
pytest

# Run only the tests marked as 'sanity'
pytest -m sanity

# Run tests in a specific file
pytest tests/test_task_lifecycle.py

# Run tests in headless mode (default) or headful mode for debugging
# To run with a visible browser, set HEADLESS=false in your .env file
```

### 4.4. Viewing Test Reports

The framework is integrated with Allure for detailed reporting.

```bash
# 1. Run the tests and generate Allure results
pytest --alluredir=allure-results

# 2. Serve the interactive HTML report
allure serve allure-results
```

This will open a web server with a dashboard where you can explore the test results.
