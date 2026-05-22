# Car Store Management System

A web-based car dealership platform built as two REST-communicating microservices.
**Sprint 1 — Foundation** delivers the foundational layer: user authentication,
admin vehicle inventory management, and a customer-facing browsing experience.

> **Course context:** Software Engineering Lab (LA10), Gdańsk University of Technology
> **Sprint duration:** 15 May – 29 May 2026 (2 weeks)
> **Team:** 4 members

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                          │
└────────────────┬──────────────────────────────┬─────────────────┘
                 │                              │
       login / register                browse / add vehicles
                 │                              │
                 ▼                              ▼
┌────────────────────────────┐   ┌────────────────────────────┐
│    AUTH SERVICE            │   │   CATALOG SERVICE          │
│    Port: 8001              │   │   Port: 8002               │
│                            │   │                            │
│  POST /register            │   │  GET  /vehicles  (HTML)    │
│  POST /login    → JWT      │   │  GET  /vehicles/{id} (HTML)│
│  GET  /verify              │ ◄─┤  POST /api/vehicles        │
│  GET  /me                  │   │       (calls /verify)      │
│                            │   │                            │
│  SQLite: users             │   │  SQLite: vehicles          │
└────────────────────────────┘   └────────────────────────────┘
            │                              │
            └─── Docker network: ──────────┘
                  carstore_net
                         │
                         ▼
                 docker-compose.yml
```

**Communication pattern:** When the Catalog Service receives a request to a
protected endpoint (e.g. `POST /api/vehicles`), it extracts the `Authorization: Bearer <token>`
header and performs an HTTP GET to the Auth Service's `/verify` endpoint.
Auth Service decodes the JWT, looks up the user, and returns `{valid, user_id, email, role}`.
Catalog then proceeds with the operation, or rejects with 401.

This direct, explicit inter-service REST call is the LA10 requirement.

---

## 🚀 Quick Start

### Prerequisites
- Docker 24+
- Docker Compose v2+

### Run everything

```bash
git clone <repo-url>
cd car-store-management-system
docker compose up --build
```

Both services boot together. Wait ~10 seconds for healthchecks, then:

- **Auth Service:**     <http://localhost:8001/docs>
- **Catalog Service:**  <http://localhost:8002/docs>
- **Browse inventory:** <http://localhost:8002/vehicles>

### Demo flow

```bash
# 1. Register a customer
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"securepass123"}'

# 2. Log in to get a token
curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"securepass123"}'
# → copy the access_token from the response

# 3. Add a vehicle (Catalog calls Auth /verify under the hood)
curl -X POST http://localhost:8002/api/vehicles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <PASTE_TOKEN_HERE>" \
  -d '{"brand":"Tesla","model":"Model 3","year":2023,"mileage":15000,"price":"42500.00","fuel_type":"electric"}'

# 4. Browse the listing in your browser
open http://localhost:8002/vehicles
```

Or, use the helper pages: visit <http://localhost:8002/login> and follow the UI.

---

## 📁 Repository Structure

```
car-store-management-system/
├── auth_service/                  # Auth Service (port 8001)
│   ├── app/
│   │   ├── main.py                # FastAPI app entry
│   │   ├── core/
│   │   │   ├── config.py          # Env-based config
│   │   │   ├── database.py        # SQLAlchemy setup
│   │   │   ├── security.py        # bcrypt password hashing (SCRUM-88)
│   │   │   └── jwt_handler.py     # JWT create/decode (SCRUM-88)
│   │   ├── models/
│   │   │   └── user.py            # User SQLAlchemy model (SCRUM-89)
│   │   ├── schemas/
│   │   │   └── auth.py            # Pydantic request/response schemas
│   │   └── routers/
│   │       ├── auth.py            # /register, /login, /verify, /me
│   │       └── health.py          # /health
│   ├── tests/
│   │   └── test_auth.py           # Unit tests (SCRUM-92, 105)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
│
├── catalog_service/               # Catalog Service (port 8002)
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── auth_client.py     # ⭐ REST call to Auth /verify
│   │   ├── models/
│   │   │   └── vehicle.py         # Vehicle model (SCRUM-109)
│   │   ├── schemas/
│   │   │   └── vehicle.py
│   │   ├── routers/
│   │   │   ├── vehicles.py        # JSON API (SCRUM-101)
│   │   │   ├── pages.py           # HTML pages (SCRUM-106, 107)
│   │   │   └── health.py
│   │   ├── templates/             # Jinja2 templates
│   │   │   ├── base.html
│   │   │   ├── listing.html       # SCRUM-106 ⭐
│   │   │   ├── detail.html        # SCRUM-107
│   │   │   ├── add_vehicle.html
│   │   │   ├── login.html
│   │   │   └── not_found.html
│   │   └── static/css/style.css
│   ├── tests/
│   │   └── test_catalog.py        # Unit tests with mocked Auth
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
│
├── docker-compose.yml             # SCRUM-161 ⭐ Two services + network
├── .github/workflows/ci.yml       # GitHub Actions CI (SCRUM-162)
├── .gitlab-ci.yml                 # GitLab CI (SCRUM-162)
├── .env.example
├── .gitignore
└── README.md                      # This file (SCRUM-164)
```

---

## 🧪 Running Tests

Each service has its own pytest suite. Run them independently:

```bash
# Auth Service tests
cd auth_service
pip install -r requirements.txt
pytest

# Catalog Service tests
cd catalog_service
pip install -r requirements.txt
pytest
```

Or run via Docker:

```bash
docker compose run --rm auth_service pytest
docker compose run --rm catalog_service pytest
```

---

## 🌿 Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready. Only merged via PR with green CI. |
| `feature/sprint-1-*` | Sprint 1 work, one branch per ticket or domain. |

**Definition of Done:**
1. Code written and follows project conventions
2. Pytest tests written and passing locally
3. Code merged to `main` via Pull Request
4. CI pipeline green
5. Feature demonstrable via `docker compose up`
6. Jira ticket moved to "Done" with assignee filled

**Code on a feature branch only is NOT Done** (per LA10).

---

## 🔄 GitLab Repository Synchronization

To comply with the software engineering course requirements, this repository is fully tracked and submitted through the Gdańsk University of Technology GitLab server.

### Remote Configuration

Ensure your local repository has the university GitLab set as the primary remote (`origin`):

*   **GitLab (`origin`):** `https://git.pg.edu.pl/GuneyYilmaz/lab3fastapi.git`

#### Verify and Setup Remotes:
```bash
# Check current configured remotes
git remote -v

# If origin points elsewhere, set it to the official GitLab repository:
git remote set-url origin https://git.pg.edu.pl/GuneyYilmaz/lab3fastapi.git
```

#### Synchronization Workflow:
When working on sprint branches (e.g. `feature/sprint-1`), always push your latest commits to the official GitLab repository to keep the team and instructors updated:

```bash
# Push the current sprint branch to GitLab
git push origin feature/sprint-1
```

Once pushed, the branch and all its commits will be fully visible in the GitLab Repository Graph.

---

## 📚 API Reference

### Auth Service (port 8001)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/register` | — | Create a new user account |
| POST | `/login` | — | Authenticate, receive JWT |
| GET | `/verify` | Bearer | Validate token; called by other services |
| GET | `/me` | Bearer | Get current user's profile |
| GET | `/health` | — | Health check |
| GET | `/docs` | — | Interactive Swagger UI |

### Catalog Service (port 8002)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vehicles` | — | HTML listing page (browser) |
| GET | `/vehicles/{id}` | — | HTML detail page |
| GET | `/admin/add-vehicle` | — | HTML admin form (token in form) |
| GET | `/login` | — | HTML login helper page |
| GET | `/api/vehicles` | — | JSON list of vehicles (paginated) |
| GET | `/api/vehicles/{id}` | — | JSON vehicle by id |
| POST | `/api/vehicles` | Bearer | Create vehicle (calls Auth `/verify`) |
| GET | `/health` | — | Health check |
| GET | `/docs` | — | Interactive Swagger UI |

---

## 🎯 Sprint 1 Scope (delivered)

| Ticket | Type | What |
|--------|------|------|
| SCRUM-160 | Task | GitHub repo + FastAPI structure |
| SCRUM-161 | Task | Docker + docker-compose with two services |
| SCRUM-88 | Task | Password hashing (bcrypt) + JWT session |
| SCRUM-86 | Story | Customer register & login |
| SCRUM-109 | Task | Vehicle database model |
| SCRUM-101 | Story | Admin adds vehicles to inventory |
| SCRUM-106 ⭐ | Story | Customer browses inventory listing page |
| SCRUM-107 | Story | Customer views vehicle detail page |
| SCRUM-163 | Task | Pytest test suites for both services |
| SCRUM-162 | Task | CI/CD pipelines (GitHub + GitLab) |
| SCRUM-164 | Task | README + architecture documentation |
| SCRUM-165 | Task | GitHub/GitLab repository synchronization |

**Total:** 12 work items, 32 story points.

## 🔮 What's next (Sprint 2)

- SCRUM-111/112/113: Search, filter, sort vehicles
- SCRUM-114: Backend query logic
- SCRUM-154/158: Purchase request flow
- SCRUM-85: Admin role enforcement on protected endpoints
- SCRUM-108: Edit/delete vehicles

---

## 🛠️ Tech Stack

- **Backend:** Python 3.11, FastAPI 0.110, SQLAlchemy 2.0, Pydantic 2.6
- **Auth:** bcrypt (passlib), python-jose (JWT)
- **Templates:** Jinja2
- **Database:** SQLite (one file per service, isolated)
- **HTTP client (Catalog → Auth):** httpx
- **Containerization:** Docker, Docker Compose
- **Testing:** pytest, FastAPI TestClient, unittest.mock
- **CI/CD:** GitHub Actions, GitLab CI

---

## 📄 License

This project is part of a university course assignment.
