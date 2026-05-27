# Görev Paylaşımı — Sprint 1

Bu dokümanda her takım üyesinin hangi Jira ticket'ı sahiplendiği ve hangi dosyaları kendi GitLab hesabından commit/push edeceği listelenmiştir.

> **Strateji:** Erdem kodun tamamını yazıyor. Her kişi kendi atandığı ticket'ın dosyalarını **kendi GitLab hesabından** commit/push yapacak. Bu, commit history'sinde her ihtimalin katılımını gösterir.

---

## 🟣 Erdem (Tech Lead)

**Sahiplendiği Jira ticket'lar:**
- SCRUM-160 GitHub repo + structure (2 SP)
- SCRUM-86 Register/Login user story (5 SP)
- SCRUM-164 README documentation (2 SP)
- SCRUM-165 GitHub/GitLab synchronization (1 SP)

**Toplam: 10 SP**

**Commit/push yapacağı dosyalar:**

```
Initial commit (SCRUM-160):
├── .gitignore
├── .env.example
├── auth_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── app/__init__.py
│   ├── app/main.py
│   ├── app/core/__init__.py
│   ├── app/core/config.py
│   ├── app/core/database.py
│   ├── app/models/__init__.py
│   ├── app/routers/__init__.py
│   ├── app/routers/health.py
│   ├── app/schemas/__init__.py
│   └── tests/__init__.py
└── catalog_service/
    ├── Dockerfile
    ├── requirements.txt
    ├── pytest.ini
    ├── app/__init__.py
    ├── app/main.py
    ├── app/core/__init__.py
    ├── app/core/config.py
    ├── app/core/database.py
    ├── app/models/__init__.py
    ├── app/routers/__init__.py
    ├── app/routers/health.py
    ├── app/schemas/__init__.py
    └── tests/__init__.py

SCRUM-86 commit (register/login user story coordination):
├── auth_service/app/models/user.py
├── auth_service/app/schemas/auth.py
└── auth_service/app/routers/auth.py
   (Bu bölümü Erdem yazar, çünkü cross-service coordination gerekir)

SCRUM-164 commit (README):
└── README.md

SCRUM-165 commit (sync):
└── (sadece git push komutları, kod yok)
```

**GitLab komutları (Erdem):**
```bash
# Initial commit
git add .gitignore .env.example auth_service/Dockerfile auth_service/requirements.txt \
        auth_service/pytest.ini auth_service/app/__init__.py auth_service/app/main.py \
        auth_service/app/core/__init__.py auth_service/app/core/config.py \
        auth_service/app/core/database.py auth_service/app/models/__init__.py \
        auth_service/app/routers/__init__.py auth_service/app/routers/health.py \
        auth_service/app/schemas/__init__.py auth_service/tests/__init__.py \
        catalog_service/Dockerfile catalog_service/requirements.txt \
        catalog_service/pytest.ini catalog_service/app/__init__.py \
        catalog_service/app/main.py catalog_service/app/core/__init__.py \
        catalog_service/app/core/config.py catalog_service/app/core/database.py \
        catalog_service/app/models/__init__.py catalog_service/app/routers/__init__.py \
        catalog_service/app/routers/health.py catalog_service/app/schemas/__init__.py \
        catalog_service/tests/__init__.py
git commit -m "SCRUM-160: Initial repo structure with two-service skeleton"
git push

# Register/Login commit
git add auth_service/app/models/user.py auth_service/app/schemas/auth.py \
        auth_service/app/routers/auth.py
git commit -m "SCRUM-86: Implement user registration and login endpoints"
git push

# README
git add README.md
git commit -m "SCRUM-164: Add README with architecture diagram and API reference"
git push
```

---

## 🔵 Güney (Lacivert avatar — DevOps + Auth Backend)

**Sahiplendiği Jira ticket'lar:**
- SCRUM-161 Docker + docker-compose (3 SP)
- SCRUM-88 Password hashing + session (3 SP)
- SCRUM-162 CI/CD pipeline (2 SP)

**Toplam: 8 SP**

**Commit/push yapacağı dosyalar:**

```
SCRUM-88 commit (password + JWT):
├── auth_service/app/core/security.py        (bcrypt password hashing)
└── auth_service/app/core/jwt_handler.py     (JWT create/decode)

SCRUM-161 commit (Docker):
└── docker-compose.yml

SCRUM-162 commit (CI/CD):
├── .github/workflows/ci.yml
└── .gitlab-ci.yml
```

**GitLab komutları (Güney):**
```bash
# SCRUM-88
git add auth_service/app/core/security.py auth_service/app/core/jwt_handler.py
git commit -m "SCRUM-88: Implement bcrypt password hashing and JWT session tokens"
git push

# SCRUM-161
git add docker-compose.yml
git commit -m "SCRUM-161: Add docker-compose for two-service setup with REST communication"
git push

# SCRUM-162
git add .github/workflows/ci.yml .gitlab-ci.yml
git commit -m "SCRUM-162: Configure GitHub Actions and GitLab CI pipelines"
git push
```

---

## 🟠 Piotr veya Mikołaj — Turuncu avatar (Catalog Backend)

**Sahiplendiği Jira ticket'lar:**
- SCRUM-109 Vehicle DB model (2 SP)
- SCRUM-101 Add vehicles (3 SP)
- SCRUM-163 Pytest tests (3 SP)

**Toplam: 8 SP**

**Commit/push yapacağı dosyalar:**

```
SCRUM-109 commit (Vehicle model):
└── catalog_service/app/models/vehicle.py

SCRUM-101 commit (Add vehicles + auth_client):
├── catalog_service/app/schemas/vehicle.py
├── catalog_service/app/core/auth_client.py  ⭐ (REST call to Auth)
└── catalog_service/app/routers/vehicles.py

SCRUM-163 commit (Tests):
├── auth_service/tests/test_auth.py
└── catalog_service/tests/test_catalog.py
```

**GitLab komutları:**
```bash
# SCRUM-109
git add catalog_service/app/models/vehicle.py
git commit -m "SCRUM-109: Create Vehicle SQLAlchemy model with type constraints"
git push

# SCRUM-101
git add catalog_service/app/schemas/vehicle.py catalog_service/app/core/auth_client.py \
        catalog_service/app/routers/vehicles.py
git commit -m "SCRUM-101: Add vehicle creation endpoint with Auth Service REST verification"
git push

# SCRUM-163
git add auth_service/tests/test_auth.py catalog_service/tests/test_catalog.py
git commit -m "SCRUM-163: Add pytest test suites for both services (25 tests)"
git push
```

---

## 🔷 Piotr veya Mikołaj — Açık mavi avatar (Catalog Frontend)

**Sahiplendiği Jira ticket'lar:**
- SCRUM-106 ⭐ Listing/Browse page (3 SP)
- SCRUM-107 Detail page (3 SP)

**Toplam: 6 SP**

**Commit/push yapacağı dosyalar:**

```
SCRUM-106 + SCRUM-107 commit (HTML pages + templates + CSS):
├── catalog_service/app/routers/pages.py
├── catalog_service/app/templates/base.html
├── catalog_service/app/templates/listing.html       ⭐ SCRUM-106
├── catalog_service/app/templates/detail.html       SCRUM-107
├── catalog_service/app/templates/add_vehicle.html   (SCRUM-101 destek)
├── catalog_service/app/templates/login.html         (login helper)
├── catalog_service/app/templates/not_found.html
└── catalog_service/app/static/css/style.css
```

**GitLab komutları:**
```bash
# SCRUM-106 ve SCRUM-107 birlikte (template sharing var)
git add catalog_service/app/routers/pages.py \
        catalog_service/app/templates/base.html \
        catalog_service/app/templates/listing.html \
        catalog_service/app/templates/detail.html \
        catalog_service/app/templates/add_vehicle.html \
        catalog_service/app/templates/login.html \
        catalog_service/app/templates/not_found.html \
        catalog_service/app/static/css/style.css
git commit -m "SCRUM-106 + SCRUM-107: Add listing and detail pages with Jinja2 templates"
git push
```

> Daha temiz commit history için isteğe bağlı **iki ayrı commit**:
> 1. `git commit -m "SCRUM-106: Add vehicle listing page with Jinja2 templates and CSS"` (listing, base, not_found, login, add_vehicle, style.css)
> 2. `git commit -m "SCRUM-107: Add vehicle detail page"` (detail.html)

---

## 📋 Commit Sırası — Önerilen Akış

Tüm takım aynı feature branch'te çalışıyor (örn. `feature/sprint-1`). Sırayla commit/push:

| # | Kim | Ticket | Açıklama |
|---|-----|--------|----------|
| 1 | Erdem | SCRUM-160 | Initial repo structure |
| 2 | Güney | SCRUM-88 | Password hash + JWT (Auth core) |
| 3 | Erdem | SCRUM-86 | Register/Login endpoints |
| 4 | Piotr/Mikołaj 🟠 | SCRUM-109 | Vehicle model |
| 5 | Piotr/Mikołaj 🟠 | SCRUM-101 | Add vehicles + auth_client |
| 6 | Piotr/Mikołaj 🔷 | SCRUM-106 | Listing page ⭐ |
| 7 | Piotr/Mikołaj 🔷 | SCRUM-107 | Detail page |
| 8 | Piotr/Mikołaj 🟠 | SCRUM-163 | Tests for both services |
| 9 | Güney | SCRUM-161 | docker-compose.yml |
| 10 | Güney | SCRUM-162 | CI/CD pipelines |
| 11 | Erdem | SCRUM-164 | README |
| 12 | Erdem | SCRUM-165 | GitHub-GitLab sync (sadece push'lar) |

**Bu sıra kritik çünkü:**
- Önce iskelet (SCRUM-160) → diğer dosyalar var olan klasörlere konur
- Auth core (SCRUM-88) → register/login bunu kullanır
- Vehicle model → add-vehicle endpoint bunu kullanır
- Routes → templates bunlardan gelir
- Tests sonda → tüm kod yazıldıktan sonra

---

## 🔄 Jira'da Status Güncellemeleri

Her commit/push'tan sonra Jira'da ilgili ticket'ı güncelle:

1. **Coding başlarken:** `To Do` → `In Progress`
2. **Code push'ladığında:** `In Progress` kalır
3. **Tüm subtask'lar bittiğinde:** `In Progress` → `Done` (master'a merge sonrası)

LA10 grading: *"Keep the task status up to date, so it reflects the actual implementation status"* — 2 puan değerinde.

---

## ⚠️ Önemli Notlar

1. **Bütün takım aynı feature branch'te:** `feature/sprint-1` (LA10 talimatı)
2. **Done = master'da:** Sprint sonunda PR aç, master'a merge et. Feature branch'te kalan kod Done sayılmaz (LA10 talimatı).
3. **CI passing must:** Her push CI'da yeşil olmalı.
4. **Her kişi kendi GitLab hesabıyla push yapar** — commit author'ı doğru olsun ki burndown ve activity raporu adil görünsün.

---

## 🎯 Sprint Sonu (29 May)

Sprint kapandığında:
1. Tüm 12 ticket Done
2. Feature branch master'a merge edildi
3. CI yeşil
4. `docker compose up` ile demo edilebilir
5. README güncel
6. 25 test geçiyor

**LA11 Sprint Review'da bu liste hocaya gösterilir.**
