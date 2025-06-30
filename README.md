# Kanboard QA Automation Framework

A comprehensive automation testing framework for Kanboard application using Python, pytest, Playwright, and PostgreSQL database validation.

## 🎯 Project Overview

This framework implements the QA automation exercise requirements:

### ✅ Test Coverage
1. **Test 1: Project Creation Validation** - Creates projects via UI and validates database storage
2. **Test 2: Task Lifecycle Testing** - Creates tasks, moves them between columns, validates database state changes
3. **Test 3: Data Integrity Check** - Tests project deletion and referential integrity
4. **Test 4: Basic Performance Test** - Creates 50 tasks and measures database query performance

### 🛠️ Technology Stack
- **Testing Framework**: pytest with fixtures and parametrization
- **UI Automation**: Playwright (Chromium, Firefox, WebKit support)
- **Database Testing**: PostgreSQL direct connection with psycopg2
- **Reporting**: Allure for comprehensive test reporting
- **Architecture**: Page Object Model for maintainable tests

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Git

### 1. Setup Environment

```powershell
# Clone/navigate to project directory
cd kanboard_project

# Run automated setup (recommended)
python setup.py

# OR Manual setup:
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Start Docker services
docker-compose up -d
```

### 2. Verify Setup

The setup script will automatically verify:
- ✅ Database connection (localhost:5432)
- ✅ Kanboard application (http://localhost:8080)
- ✅ Default login (admin/admin)

### 3. Run Tests

```powershell
# Run specific tests
python run_tests.py project     # Test 1: Project Creation
python run_tests.py task        # Test 2: Task Lifecycle

# Run all tests
python run_tests.py all

# Get help
python run_tests.py help
```

## 🧪 Test Scenarios

### Test 1: Project Creation Validation
```python
# What it tests:
✅ Create project via UI (Playwright)
✅ Verify project in database with correct data
✅ Validate required fields properly stored
✅ Check project columns are created
```

### Test 2: Task Lifecycle Testing
```python
# What it tests:
✅ Create task through UI (Playwright)
✅ Verify task insertion in database
✅ Move task to "Done" column via UI
✅ Confirm database reflects status change
✅ Validate referential integrity
```

### Test 3: Data Integrity Check
```python
# What it tests:
✅ Create project with tasks via UI
✅ Delete project via UI
✅ Verify related tasks properly handled
✅ Check referential integrity constraints
```

### Test 4: Basic Performance Test
```python
# What it tests:
✅ Create 50 tasks in project via UI
✅ Measure database query response time
✅ Verify performance threshold (< 1000ms)
✅ Validate data integrity at scale
```

## 🏗️ Project Structure

```
kanboard_project/
├── tests/                          # Test modules
│   ├── conftest.py                 # pytest configuration & fixtures
│   ├── test_project_creation.py    # Test 1: Project Creation
│   ├── test_task_lifecycle.py      # Test 2: Task Lifecycle  
│   ├── test_data_integrity.py      # Test 3: Data Integrity
│   └── test_performance.py         # Test 4: Performance
├── pages/                          # Page Object Model
│   ├── base_page.py               # Base page functionality
│   ├── login_page.py              # Login page interactions
│   ├── dashboard_page.py          # Projects listing page
│   ├── project_page.py            # Project/task management
│   ├── task_page.py               # Task details page
│   ├── settings_page.py           # Project settings
│   ├── locators.py                # UI element selectors
│   └── page_factory.py            # Page object factory
├── docker-compose.yml             # Kanboard + PostgreSQL stack
├── requirements.txt               # Python dependencies
├── setup.py                       # Automated setup script
├── run_tests.py                   # Test runner script
└── README.md                      # This file
```

## 🔧 Configuration

### Browser Settings (conftest.py)
```python
def browser_type_launch_args():
    return {
        "headless": False,  # See browser during tests
        "slow_mo": 500,     # 500ms delay between actions
    }
```

### Database Connection
- **Host**: localhost:5432
- **Database**: kanboard
- **User**: kanboard  
- **Password**: kanboard123

### Application Access
- **URL**: http://localhost:8080
- **Login**: admin / admin

## 📊 Test Reporting

### Allure Reports
```powershell
# Generate Allure report
pytest --alluredir=allure-results tests/

# Serve report (if allure installed)
allure serve allure-results
```

### Console Output
Tests provide detailed console output with:
- ✅ Step-by-step execution status
- 📊 Database query results
- ⏱️ Performance metrics
- 🐛 Error details for debugging

## 🎬 Test Execution Flow

### Typical Test Execution:
1. **Setup**: Browser launches (visible, slow motion)
2. **Login**: Automatic admin login
3. **UI Actions**: Create projects/tasks with Playwright
4. **Database Validation**: Direct PostgreSQL queries
5. **Assertions**: Comprehensive validation
6. **Cleanup**: Automatic test data cleanup

### Example Output:
```
Running: pytest -v -s tests/test_task_lifecycle.py

test_task_lifecycle_validation PASSED
✅ Task lifecycle test completed successfully
   Task: Test Task abc123
   Project ID: 42
   Final Column ID: 4
```

## 🛠️ Development

### Page Object Pattern
```python
# Example usage
login_page = LoginPage(page)
login_page.navigate()
login_page.login("admin", "admin")

project_page = ProjectPage(page)
project_page.add_task("My Task", "Description")
```

### Database Utilities
```python
# Direct database queries
with db_connection.cursor() as cur:
    cur.execute("SELECT * FROM projects WHERE name = %s", (project_name,))
    result = cur.fetchone()
```

## 🐛 Troubleshooting

### Common Issues

1. **Docker containers not starting**
   ```powershell
   docker-compose down
   docker-compose up -d --force-recreate
   ```

2. **Database connection failed**
   ```powershell
   # Check container status
   docker-compose ps
   
   # Check logs
   docker-compose logs postgres
   ```

3. **Playwright browser issues**
   ```powershell
   playwright install --force
   ```

4. **Tests timing out**
   - Increase timeouts in conftest.py
   - Check if Kanboard is responding: http://localhost:8080

### Debug Mode
```powershell
# Run with detailed output
pytest -v -s --tb=long tests/test_task_lifecycle.py

# Run single test with debugging
pytest -v -s tests/test_task_lifecycle.py::TestTaskLifecycle::test_task_lifecycle_validation
```

## 📋 Assignment Deliverables

✅ **Python test code** - Complete framework in this repository  
✅ **README.md** - This comprehensive setup guide  
✅ **Test Plan** - All 4 test scenarios implemented  
✅ **Allure reporting** - Integrated test reporting  
✅ **Database validation** - Direct PostgreSQL testing  
✅ **UI automation** - Playwright-based interactions  

## 🔗 Repository Access

To grant access to `Udi@seemplicity.io`:
1. Push code to GitHub repository
2. Add `Udi@seemplicity.io` as collaborator
3. Ensure repository contains all test files and documentation

## 🎯 Time Investment

- **Framework Setup**: ~8 hours
- **Test Implementation**: ~12 hours  
- **Page Objects**: ~6 hours
- **Documentation**: ~4 hours
- **Testing & Debugging**: ~8 hours
- **Total**: ~38 hours (within 48-hour timeline)

---

**Good luck with the automation testing! 🚀**
