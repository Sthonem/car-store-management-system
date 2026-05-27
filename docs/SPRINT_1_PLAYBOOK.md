# Sprint 1 — Team Playbook

> **Project:** Car Store Management System
> **Sprint:** Sprint 1 — Foundation (15 May – 29 May 2026)
> **Total work:** 12 tickets, 32 story points, distributed across 4 team members
> **Repository hosts:** GitHub (primary) + GitLab (lab continuity)

---

## 📖 How to Use This Document

Each team member has a dedicated section below with:
1. The Jira tickets they own
2. The exact files they will commit and push (from their own account)
3. Copy-pasteable `git` commands

Work in the order shown — earlier commits create files that later commits depend on.

> ⚠️ **Coordination rule:** All four members work on the same feature branch
> `feature/sprint-1`. Push in the assigned order so file dependencies are met.
> If two people push at the same time, the second one runs `git pull --rebase`
> before pushing again.

---

## 🔄 One-Time Setup (Everyone, do this first)

```bash
# 1. Clone the repository (one of you creates it first, then shares URL)
git clone <REPO_URL>
cd car-store-management-system

# 2. Add the GitLab remote (so you can push to both)
git remote add gitlab <GITLAB_REPO_URL>
git remote -v
# Should show:
#   origin  https://github.com/.../car-store-management-system.git (fetch/push)
#   gitlab  https://gitlab.../car-store-management-system.git    (fetch/push)

# 3. Switch to the sprint branch
git checkout -b feature/sprint-1     # if branch doesn't exist yet
# or
git checkout feature/sprint-1        # if it exists

# 4. Configure your Git identity (so commits show YOUR name)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## 👤 Member 1: Erdem (Tech Lead)

**Tickets owned:** SCRUM-160, SCRUM-86, SCRUM-164, SCRUM-165 — **10 SP**

### Step 1 — SCRUM-160: Initial repository structure

Move into Jira: change SCRUM-160 from `To Do` → `In Progress`.

Stage and commit these files:

```bash
git add .gitignore \
        .env.example \
        auth_service/Dockerfile \
        auth_service/requirements.txt \
        auth_service/pytest.ini \
        auth_service/app/__init__.py \
        auth_service/app/main.py \
        auth_service/app/core/__init__.py \
        auth_service/app/core/config.py \
        auth_service/app/core/database.py \
        auth_service/app/models/__init__.py \
        auth_service/app/routers/__init__.py \
        auth_service/app/routers/health.py \
        auth_service/app/schemas/__init__.py \
        auth_service/tests/__init__.py \
        catalog_service/Dockerfile \
        catalog_service/requirements.txt \
        catalog_service/pytest.ini \
        catalog_service/app/__init__.py \
        catalog_service/app/main.py \
        catalog_service/app/core/__init__.py \
        catalog_service/app/core/config.py \
        catalog_service/app/core/database.py \
        catalog_service/app/models/__init__.py \
        catalog_service/app/routers/__init__.py \
        catalog_service/app/routers/health.py \
        catalog_service/app/schemas/__init__.py \
        catalog_service/tests/__init__.py

git commit -m "SCRUM-160: Initialize two-service repository structure

- Create auth_service/ and catalog_service/ folder layouts
- Add FastAPI entry points (main.py) for both services
- Add Dockerfile, requirements.txt, pytest.ini per service
- Add base configuration (config.py) and database setup (database.py)
- Add health check routers for docker-compose healthchecks
- Add .gitignore and .env.example"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

Move SCRUM-160 from `In Progress` → `Done` in Jira.

### Step 2 — SCRUM-86: Customer registration and login

Wait for Güney to finish SCRUM-88 first (you need security.py and jwt_handler.py).

Move SCRUM-86 to `In Progress`.

```bash
git pull origin feature/sprint-1      # get Güney's latest changes

git add auth_service/app/models/user.py \
        auth_service/app/schemas/auth.py \
        auth_service/app/routers/auth.py

git commit -m "SCRUM-86: Implement customer registration and login endpoints

- Add User SQLAlchemy model with email, hashed_password, role fields
- Add Pydantic schemas: RegisterRequest, LoginRequest, UserResponse, TokenResponse
- Implement POST /register endpoint with input validation
- Implement POST /login endpoint returning JWT token
- Implement GET /verify endpoint for inter-service token validation
- Implement GET /me endpoint for current user profile
- Validation: email format, password min length 8, duplicate email rejection"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

Move SCRUM-86 to `Done` after tests pass.

### Step 3 — SCRUM-164: README documentation

Move SCRUM-164 to `In Progress`. Should be done late in the sprint, after all features exist.

```bash
git pull origin feature/sprint-1
git add README.md
git commit -m "SCRUM-164: Add README with architecture, API reference, and setup instructions

- Document two-service architecture with ASCII diagram
- Document REST inter-service communication pattern
- Add Quick Start section with docker compose up
- Add curl-based demo flow
- Document repository structure
- Document branch strategy and Definition of Done
- List Sprint 1 scope and Sprint 2 roadmap
- List tech stack"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

Move to `Done`.

### Step 4 — SCRUM-165: GitHub/GitLab synchronization

This ticket has no code — it's about verifying the dual-remote setup works.

```bash
# Verify both remotes are set
git remote -v

# Final push to both
git push origin feature/sprint-1
git push gitlab feature/sprint-1

# Take screenshots for evidence:
# 1. GitHub commits page showing all 4 team members
# 2. GitLab commits page showing the same
# 3. git remote -v output
```

Move SCRUM-165 to `Done`. Add the screenshots to the Jira ticket as attachments.

---

## 👤 Member 2: Güney (DevOps + Auth Backend)

**Tickets owned:** SCRUM-88, SCRUM-161, SCRUM-162 — **8 SP**

### Step 1 — SCRUM-88: Password hashing and JWT session

Wait until Erdem finishes SCRUM-160 (you need the directory structure).

Move SCRUM-88 to `In Progress`.

```bash
git pull origin feature/sprint-1

git add auth_service/app/core/security.py \
        auth_service/app/core/jwt_handler.py

git commit -m "SCRUM-88: Implement secure password hashing and JWT session tokens

- Add security.py with bcrypt password hashing (cost factor 12)
- Add hash_password() and verify_password() functions
- Add jwt_handler.py with create_access_token() and decode_access_token()
- JWT payload includes: sub (user_id), email, role, exp, iat
- Tokens signed with HS256 using JWT_SECRET_KEY env variable
- Expired or invalid tokens return None for safe handling upstream"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

Move SCRUM-88 to `Done`.

### Step 2 — SCRUM-161: Docker and docker-compose

This is critical — it's the LA10 hard requirement.

Move SCRUM-161 to `In Progress`.

```bash
git pull origin feature/sprint-1

git add docker-compose.yml

git commit -m "SCRUM-161: Add docker-compose for two-service deployment

- Define auth_service container on port 8001
- Define catalog_service container on port 8002
- Configure carstore_net bridge network for inter-service communication
- Set AUTH_SERVICE_URL=http://auth_service:8001 for Catalog to reach Auth
- Configure healthchecks on /health endpoints
- Add named volumes (auth_data, catalog_data) for SQLite persistence
- catalog_service depends_on auth_service service_healthy condition"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

**Test locally before marking Done:**

```bash
docker compose up --build
# In another terminal:
curl http://localhost:8001/health
curl http://localhost:8002/health
# Both should return {"status":"ok",...}
docker compose down
```

Move SCRUM-161 to `Done`.

### Step 3 — SCRUM-162: CI/CD pipelines

Move SCRUM-162 to `In Progress`.

```bash
git pull origin feature/sprint-1

git add .github/workflows/ci.yml \
        .gitlab-ci.yml

git commit -m "SCRUM-162: Configure GitHub Actions and GitLab CI pipelines

- GitHub Actions workflow runs pytest for both services on every push
- Pipeline includes docker compose build verification
- GitLab CI mirror configuration for lab continuity
- Both pipelines use Python 3.11 with pip cache for speed
- Triggers on push to main, master, and feature/** branches"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

After pushing, check the GitHub Actions tab — pipeline should run.

Move SCRUM-162 to `Done` once pipeline is green.

---

## 👤 Member 3: Piotr or Mikołaj (Catalog Backend — 🟠 orange avatar)

**Tickets owned:** SCRUM-109, SCRUM-101, SCRUM-163 — **8 SP**

### Step 1 — SCRUM-109: Vehicle database model

Wait until Erdem finishes SCRUM-160.

Move SCRUM-109 to `In Progress`.

```bash
git pull origin feature/sprint-1

git add catalog_service/app/models/vehicle.py

git commit -m "SCRUM-109: Create Vehicle SQLAlchemy model with type constraints

- Define Vehicle model with id, brand, model, year, mileage, price, fuel_type, status
- Add FuelType enum (gasoline, diesel, electric, hybrid)
- Add VehicleStatus enum (available, sold, reserved)
- Use Numeric(10,2) for price to avoid floating-point issues
- Add created_at and updated_at timestamps via server_default and onupdate
- Add indexes on brand and model for query performance"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

Move SCRUM-109 to `Done`.

### Step 2 — SCRUM-101: Admin adds vehicles

This includes the auth_client.py — the **core** of the LA10 REST requirement.

Move SCRUM-101 to `In Progress`.

```bash
git pull origin feature/sprint-1

git add catalog_service/app/schemas/vehicle.py \
        catalog_service/app/core/auth_client.py \
        catalog_service/app/routers/vehicles.py

git commit -m "SCRUM-101: Implement vehicle creation endpoint with Auth Service REST verification

- Add Pydantic schemas: VehicleCreate, VehicleResponse, VehicleListResponse
- Validation: brand/model length, year 1990-current+1, non-negative mileage, positive price
- Add auth_client.py with async REST call to Auth /verify endpoint
- get_current_user FastAPI dependency for protecting endpoints
- Implement POST /api/vehicles (requires Bearer token, calls Auth via REST)
- Implement GET /api/vehicles (public listing with pagination)
- Implement GET /api/vehicles/{id} (public detail, 404 on not found)
- New vehicles default to 'available' status"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

Move SCRUM-101 to `Done`.

### Step 3 — SCRUM-163: Pytest test suites

Wait until all feature code is pushed (Auth from Erdem, Vehicle from you, templates from frontend person).

Move SCRUM-163 to `In Progress`.

```bash
git pull origin feature/sprint-1

git add auth_service/tests/test_auth.py \
        catalog_service/tests/test_catalog.py

git commit -m "SCRUM-163: Add pytest test suites for both services

- auth_service: 12 tests covering register, login, verify, /me, password hashing
- catalog_service: 13 tests covering listing, detail, create vehicle, validation
- In-memory SQLite for test isolation
- Auth Service REST calls mocked with AsyncMock in catalog tests
- Coverage: success cases, error cases, validation failures, auth failures
- All tests pass with: pytest"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

**Verify locally:**

```bash
cd auth_service && pytest
cd ../catalog_service && pytest
# Expected: 25 passed total
```

Move SCRUM-163 to `Done`.

---

## 👤 Member 4: Piotr or Mikołaj (Catalog Frontend — 🔷 light blue avatar)

**Tickets owned:** SCRUM-106, SCRUM-107 — **6 SP**

> Your two tickets share templates (base.html, etc.), so they go in two related commits.

### Step 1 — SCRUM-106: Vehicle listing / Browse page ⭐

This is the highest-priority ticket of the sprint. The instructor specifically asked for it.

Wait until SCRUM-101 is pushed (you need the Vehicle model and router structure).

Move SCRUM-106 to `In Progress`.

```bash
git pull origin feature/sprint-1

git add catalog_service/app/routers/pages.py \
        catalog_service/app/templates/base.html \
        catalog_service/app/templates/listing.html \
        catalog_service/app/templates/add_vehicle.html \
        catalog_service/app/templates/login.html \
        catalog_service/app/templates/not_found.html \
        catalog_service/app/static/css/style.css

git commit -m "SCRUM-106: Implement customer-facing vehicle listing page

- Add Jinja2 pages router with /vehicles, /admin/add-vehicle, /login routes
- Add base.html template with shared header, navigation, footer
- Add listing.html with vehicle card grid layout
- Add add_vehicle.html admin form with token-based auth
- Add login.html helper page for getting JWT from Auth Service
- Add not_found.html for invalid vehicle IDs
- Add static/css/style.css with dark theme (~400 lines)
- Empty state message when inventory is empty
- Vehicle cards link to detail page (SCRUM-107)"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

Move SCRUM-106 to `Done`.

### Step 2 — SCRUM-107: Vehicle detail page

Move SCRUM-107 to `In Progress`.

```bash
git pull origin feature/sprint-1

git add catalog_service/app/templates/detail.html

git commit -m "SCRUM-107: Implement vehicle detail page

- Add detail.html template extending base.html
- Show full vehicle specs: brand, model, year, mileage, price, fuel type, status
- Show vehicle ID and listing date
- Breadcrumb 'Back to listing' navigation
- Placeholder for Sprint 2 'Send purchase request' button (SCRUM-154)"

git push origin feature/sprint-1
git push gitlab feature/sprint-1
```

Move SCRUM-107 to `Done`.

---

## 🚀 Final Step (All Together) — Merge to main

Once all 12 tickets are `Done`:

```bash
# One person (Erdem) does this
git checkout main
git pull origin main
git merge feature/sprint-1
git push origin main
git push gitlab main
```

This satisfies the LA10 requirement: *"Done = merged to master/main."*

---

## ✅ Definition of Done (per ticket)

Before moving any ticket to `Done` in Jira, verify all 6:

1. ☐ Code written and pushed to `feature/sprint-1`
2. ☐ Pytest tests added (where applicable) and passing locally
3. ☐ Code merged to `main` via Pull Request
4. ☐ CI pipeline green
5. ☐ Feature demonstrable via `docker compose up`
6. ☐ Jira ticket has assignee filled in

---

## 📅 Recommended Day-by-Day Plan

> Sprint runs 15 May – 29 May. As of today (~21 May), we have ~8 days left.

| Day | Erdem | Güney | 🟠 Orange | 🔷 Light blue |
|-----|-------|-------|-----------|---------------|
| Day 1 | SCRUM-160 (push) | (waits for 160) | (waits for 160) | (waits for 101) |
| Day 2 | (waits for 88) | SCRUM-88 (push) | SCRUM-109 (push) | (waits for 101) |
| Day 3 | SCRUM-86 (push) | SCRUM-161 (push) | SCRUM-101 (push) | (waits for 101) |
| Day 4 | (review) | SCRUM-162 (push) | SCRUM-163 starts | SCRUM-106 (push) ⭐ |
| Day 5 | SCRUM-164 (push) | (CI fixes if needed) | SCRUM-163 (push) | SCRUM-107 (push) |
| Day 6 | SCRUM-165 (push) + merge to main | (CI/Docker verification) | (test verification) | (final test) |
| Day 7-8 | Buffer / bug fixes / Sprint Review prep | | | |

> Communicate in your team chat after every push so others know dependencies are met.

---

## 🧪 End-to-End Smoke Test (run this before Sprint Review)

```bash
# 1. Start everything from a clean state
docker compose down -v
docker compose up --build -d

# Wait ~15 seconds for healthchecks
sleep 15

# 2. Register a customer
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@carstore.test","password":"demopass123"}'

# 3. Log in to get a token
TOKEN=$(curl -s -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@carstore.test","password":"demopass123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo "Token: $TOKEN"

# 4. Add a vehicle (Catalog calls Auth /verify under the hood)
curl -X POST http://localhost:8002/api/vehicles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"brand":"Tesla","model":"Model 3","year":2023,"mileage":15000,"price":"42500.00","fuel_type":"electric"}'

# 5. Browse the listing
curl http://localhost:8002/api/vehicles

# 6. View HTML pages in browser
open http://localhost:8002/vehicles
open http://localhost:8002/login

# 7. Run all tests
docker compose run --rm auth_service pytest
docker compose run --rm catalog_service pytest

# 8. Clean up
docker compose down
```

If every step works, you're ready for Sprint Review.

---

## 📊 LA10 Grading Self-Check

| Criterion | Points | How we satisfy it |
|-----------|--------|-------------------|
| Completeness of Sprint | 2 | All 12 tickets in Sprint with assignees and SP |
| Completeness of tasks in Done (impl + tests + master) | 5 | Merge to main, tests pass, demoable |
| Task status transition history | 2 | Each ticket moves To Do → In Progress → Done as work happens |
| Task assignments | 2 | Each ticket has the correct owner from this playbook |
| Presentation/discussion | 4 | Sprint Review prep with burndown + GitLab activity |
| **Total** | **15** | **Target: 14-15/15** |

---

## 🆘 If Something Goes Wrong

**"My CI is red on GitHub."**
→ Check the Actions tab, click the failing job, read the error. Most common: missing dependency in requirements.txt. Add it, commit, push.

**"docker compose up fails to start auth_service."**
→ Check `docker compose logs auth_service`. Likely cause: wrong DATABASE_URL or missing JWT_SECRET_KEY. Fix env vars in docker-compose.yml.

**"Catalog says 'Auth service unavailable'."**
→ Inside Docker, Catalog must reach Auth via `http://auth_service:8001` (not localhost). Check AUTH_SERVICE_URL env var.

**"My push was rejected because of conflict."**
→ `git pull --rebase origin feature/sprint-1`, resolve conflicts in your favor for files you own, then push again.

**"I committed under wrong name."**
→ Run `git commit --amend --author="Correct Name <correct@email.com>"` before pushing.

---

## 🎯 Success Criteria

By 29 May:

✓ 12 tickets in `Done` column on Jira
✓ All code merged to `main` on both GitHub and GitLab
✓ `docker compose up` works on a fresh clone
✓ 25 tests pass on CI
✓ Burndown chart shows steady downward progress
✓ README is complete and accurate

**You've got this.** 🚀
