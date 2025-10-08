# Django E-Commerce Project: REST Cart API
## Project Overview
This project implements key backend components for e-commerce, based on Django and Django Rest Framework (DRF). Special attention is paid to creating a reliable, clean RESTful API for managing the shopping cart.

Key Features
- RESTful Cart Management: Full CRUD cycle (Adding, Viewing, Updating quantity, Deleting) for the cart using the session mechanism.

- Catalog API: Read-only endpoints (ReadOnlyModelViewSet) for the product catalog.

- Startup Automation: Using entrypoint.sh to automatically apply migrations and create a superuser on the container's initial run.

- Dockerized Environment: The application is deployed via Docker Compose.

- Automated Testing: Unit testing of the Cart API using Pytest.

## Setup and Launch
### Prerequisites

- Docker and Docker Compose must be installed.
- clone repository\
```bash
git clone https://github.com/karasevich/django_shopping_cart.git
cd django_shopping_cart
```
- Configuration (.env file)
To securely run the project, you need to create a file with environment variables.\
Create a file named .env in the project root directory, and fill it with your data. Docker Compose uses these values to configure PostgreSQL and create the superuser.

### Example variables that should be in your .env:
DEBUG=1\
DJANGO_SUPERUSER_USERNAME=admin\
DJANGO_SUPERUSER_PASSWORD=secure_admin_password\
DJANGO_SUPERUSER_EMAIL=admin@example.com\
POSTGRES_DB=dev_db\
POSTGRES_USER=postgres\
POSTGRES_PASSWORD=postgres\
POSTGRES_HOST=db\
POSTGRES_PORT=5432

## Build and Run
Run Docker Compose to build the images and start the services. The --build flag is critical for applying changes in Dockerfile and entrypoint.sh.

**Rebuild the image and run in the background**
```bash
docker compose up -d --build
```
## Automation Verification
The entrypoint.sh script automatically performs the following steps:

Waits for the database (db) to be ready.

Executes migrations (python manage.py migrate).

Creates a superuser, using data from .env.

Access Addresses:

Application: http://127.0.0.1:8000

Admin Panel: http://127.0.0.1:8000/admin/

## API Testing with Pytest
**Pytest Configuration**\
Test execution is simplified thanks to the pytest.ini file, which automatically instructs Pytest to use Django settings, eliminating the need for long commands.

**Running the Full Test Suite**\
Execute the command to run the entire Cart API test suite inside the container:
```bash
docker compose exec web python -m pytest store/api/tests.py
```
**Debugging Options**\
To view maximum information about test progress (including print() output and local variables on failure), use the following flags:
```bash
docker compose exec web python -m pytest -v -s --showlocals store/api/tests.py
```

## End-to-End API Verification
To fully verify the functionality of the Cart API (add, view, delete), use the built-in script test_api.sh.

**Requirements:**

*The web service must be running (docker compose up -d).*

*At least one product with id=1 must exist in the database.*

**Execution:**

*Execute the following command from the project's root directory:*

```bash
docker compose exec web ./test_api.sh
```
Expected Output: The script should output a sequence of steps, concluding with the message: **Success: Cart is empty. All tests passed.**