# Impacto Digifin Python Automation Project

This project contains API automation tests for the jsonplaceholder.typicode.com API, built as part of a take-home assignment for Impacto Digifin Technologies.

## Overview

This automation framework tests user-related API endpoints including:
- GET all users
- GET single user by ID
- POST create user
- Negative test cases (404 errors)
- Data-driven tests (users loaded from `data/users_to_create.json`)

## Project Structure

```
Impacto Digifin Python Automation Project/
├── src/
│   ├── config.py       # Configuration (base URL, timeout, logging, test data path)
│   ├── api_client.py   # Reusable API client and custom APIError
│   └── utils.py        # Logger setup and get_test_data_path helper
├── tests/
│   ├── test_api_users.py      # API user tests (GET, POST, negative)
│   └── test_data_driven.py    # Data-driven create-user tests
├── data/
│   └── users_to_create.json   # Test data for data-driven tests
├── logs/                      # Log output (e.g. automation.log)
├── .github/workflows/
│   └── ci.yml          # GitHub Actions CI workflow
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/agnihombali301-maker/impacto-digifin-python-automation.git
   cd "Impacto Digifin Python Automation Project"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file in the project root to customize settings:
   ```
   API_BASE_URL=https://jsonplaceholder.typicode.com
   REQUEST_TIMEOUT=10
   LOG_LEVEL=INFO
   LOG_FILE_PATH=logs/automation.log
   TEST_DATA_DIR=data
   ```

## How to Run Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_api_users.py -v
pytest tests/test_data_driven.py -v
```

### Run with Output (see print statements and logs)
```bash
pytest tests/ -v -s
```

### Run a Specific Test
```bash
pytest tests/test_api_users.py::TestAPIUsers::test_get_all_users -v
```

## Design Decisions

- **API choice:** Tests use jsonplaceholder.typicode.com. The assignment initially referenced reqres.in; I switched because reqres.in was returning 403 (Cloudflare blocking automated requests). jsonplaceholder is a public test API that accepts the same style of requests and returns predictable responses.

- **Separation of concerns:** Test logic lives in `tests/`; automation logic (API client, config, utils) lives in `src/`. Tests depend on `APIClient`, `Config`, and helpers from `src`, not on implementation details.

- **Reusable API client:** `APIClient` in `src/api_client.py` uses a `requests.Session`, supports GET/POST, raises a custom `APIError` for status codes >= 400, and reads base URL and timeout from `Config`. All tests use this single client.

- **Configuration:** `Config` in `src/config.py` reads from environment variables (with defaults). Optional `.env` support via python-dotenv allows local overrides without changing code.

- **Logging:** `setup_logger` in `src/utils.py` configures a logger with console and file handlers, level and path from `Config`, and avoids duplicate handlers when called multiple times.

- **Data-driven tests:** User creation is driven by `data/users_to_create.json`. The same test logic runs for each user in the file, satisfying the requirement for at least one data-driven test.

- **CI/CD:** GitHub Actions (`.github/workflows/ci.yml`) runs on push and pull_request to `main`/`master`: checkout, set up Python 3.11, install from `requirements.txt`, and run `pytest tests/ -v`.

- **Custom exception:** `APIError` carries message, status_code, and response so tests can assert on error details (e.g. 404 for non-existent user).
