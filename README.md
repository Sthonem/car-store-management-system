# Car Store Management System

GitHub-ready FastAPI starter project for a university Scrum Sprint 1 laboratory. The implementation keeps the original lab style: one simple FastAPI entry point in `src/main.py`, pytest tests in `src/test_main.py`, Docker support, docker-compose, SQLite, SQLAlchemy, Jinja2 templates, and CI configuration.

## Tech Stack

- Python FastAPI
- SQLite
- SQLAlchemy
- Jinja2 templates
- Basic HTML/CSS
- pytest
- Docker
- docker-compose
- GitHub Actions CI
- Existing GitLab CI file retained from the lab project

## Sprint 1 Features

- User registration
- User login
- Password hashing
- Basic session management
- Vehicle inventory model
- Add vehicle endpoint and HTML form
- Vehicle listing page
- Vehicle detail page and JSON detail endpoint
- Empty inventory message
- Simple pytest coverage

## Project Structure

```text
.
├── .github/workflows/ci.yml
├── src/
│   ├── static/css/styles.css
│   ├── templates/
│   │   ├── add_vehicle.html
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── vehicle_detail.html
│   │   └── vehicles.html
│   ├── main.py
│   └── test_main.py
├── .gitignore
├── .gitlab-ci.yml
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## Initial Git Branches

Recommended branch structure for the Scrum/Jira lab:

- `main`: stable branch for reviewed work
- `develop`: integration branch for Sprint work
- `feature/erdem-car-store-sprint1`: personal Sprint 1 implementation branch
- `feature/authentication`: optional branch for registration, login, hashing, and sessions
- `feature/vehicle-inventory`: optional branch for vehicle model and add form
- `feature/vehicle-listing`: optional branch for listing and detail pages

Current Sprint 1 work should stay on:

```bash
feature/erdem-car-store-sprint1
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

Run from the repository root:

```bash
PYTHONPATH=src uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

The SQLite database file `car_store.db` is created automatically.

## Run With Docker

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000
```

Stop the app:

```bash
docker compose down
```

## Run Tests

```bash
pytest
```

## Example Pages and API Endpoints

HTML pages:

- `GET /` - home page
- `GET /register` - registration form
- `POST /register` - create user account
- `GET /login` - login form
- `POST /login` - start user session
- `GET /logout` - clear user session
- `GET /vehicles` - vehicle listing page
- `GET /vehicles/add` - add vehicle form
- `POST /vehicles/add` - create vehicle
- `GET /vehicles/{vehicle_id}` - vehicle detail page

JSON endpoints:

- `GET /health` - health check
- `GET /api/vehicles` - list vehicles as JSON
- `GET /api/vehicles/{vehicle_id}` - vehicle details as JSON

## Sprint 1 Backlog Mapping

| Backlog Item | File |
| --- | --- |
| User registration and login | `src/main.py`, `src/templates/register.html`, `src/templates/login.html` |
| Password hashing | `src/main.py` |
| Basic session management | `src/main.py` |
| Vehicle inventory model | `src/main.py` |
| Add vehicle endpoint/form | `src/main.py`, `src/templates/add_vehicle.html` |
| Vehicle listing page | `src/templates/vehicles.html` |
| Vehicle detail endpoint/page | `src/main.py`, `src/templates/vehicle_detail.html` |
| Tests | `src/test_main.py` |
| Docker support | `Dockerfile`, `docker-compose.yml` |
| CI | `.github/workflows/ci.yml`, `.gitlab-ci.yml` |

## Notes

This project is intentionally simple and suitable for a university laboratory. It is not a production authentication system, but it is functional enough for Sprint 1 demonstrations, Jira backlog tracking, and basic Git branch workflow practice.
