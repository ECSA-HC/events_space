# ECSA Events System — Session Handoff

Paste this into a new Claude Code session to restore full context.

---

## Who I Am

**Davis Kondo** — sole developer and sysadmin for all COSECSA/ECSAHC servers, with full root SSH access to all production hosts.

---

## What This Project Is

The ECSA events management system for `events.ecsahc.org`. It handles event registration, attendance, abstracts, and email notifications for ECSAHC conferences and activities.

---

## Architecture

Two separate parts in this repo:

| Part | Local path | Purpose |
|------|-----------|---------|
| API | `events_space/api/` | FastAPI (Python) REST backend |
| Web | `events_space/web/` | Vue 3 / Vite / Pinia / Tailwind SPA |

### API Stack
- **FastAPI 0.115** — Python 3.9
- **SQLAlchemy 2.0** — ORM for MySQL
- **mysql-connector-python** — DB driver
- **python-jose** — JWT auth (RS256 keypair)
- **SMTP** — email notifications
- **qrcode** — QR code generation for attendance
- **reportlab** — PDF generation

### Frontend Stack
- **Vue 3** + Vite + Pinia (state) + Tailwind CSS
- Source in `web/src/`: App.vue, pages/, components/, stores/, services/, router/, composables/, layouts/, plugins/, utils/

### Database
- MySQL database: `events_db` (separate from `cosecsa` / `cosecsamis.org`)
- Connection via env vars: `MYSQL_HOSTNAME`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `DATABASE_PORT`

---

## Production Setup

| Item | Value |
|------|-------|
| URL | `https://events.ecsahc.org` |
| Server path | `/var/www/events/` |
| FastAPI port | `8001` (runs as systemd service or gunicorn) |
| Apache config | Proxies `/api/` → `http://127.0.0.1:8001/` |
| SSL | Let's Encrypt via certbot |
| Uploads | Served at `/uploads/` from local filesystem |

Apache virtualhost pattern:
```apache
ProxyPass /api/ http://127.0.0.1:8001/
ProxyPassReverse /api/ http://127.0.0.1:8001/
```

---

## API Routers

`api/main.py` includes routers for:
- `auth` — login, token refresh, JWT
- `events` — create/list/manage events
- `registrations` — event registrations
- `organisations` — organizations
- `org_units` — organization units
- `countries` — country reference data
- `roles` / `permissions` — RBAC
- `users` — user management
- `dashboard` — stats/summary
- `email_logs` — sent email history
- `event_attendance` — QR-code attendance
- `activities` — event sub-activities
- `abstracts` — abstract submissions

---

## Environment Variables (`.env` in `api/`)

```
DATABASE_PORT=3306
MYSQL_HOSTNAME=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DB=events_db

JWT_ALGORITHM=RS256
JWT_PUBLIC_KEY=
JWT_PRIVATE_KEY=
ACCESS_TOKEN_EXPIRES_IN=
REFRESH_TOKEN_EXPIRES_IN=

SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=

CLIENT_ORIGIN=https://events.ecsahc.org
BASE_URL=https://events.ecsahc.org
```

---

## Deploy Flow

### API (Python backend)
```bash
rsync -avz --delete \
  --exclude='.env' --exclude='__pycache__/' --exclude='*.pyc' --exclude='.git/' \
  --exclude='venv/' --exclude='uploads/' \
  /Applications/XAMPP/xamppfiles/htdocs/events_space/api/ \
  root@events.ecsahc.org:/var/www/events/api/

# Restart FastAPI service on server
ssh root@events.ecsahc.org "systemctl restart events-api"
# or if using gunicorn:
# ssh root@events.ecsahc.org "cd /var/www/events/api && pkill gunicorn; gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8001 --daemon"
```

### Frontend (Vue build → deploy dist)
```bash
# Build locally first
cd /Applications/XAMPP/xamppfiles/htdocs/events_space/web && npm run build

# Rsync dist to server
rsync -avz --delete \
  /Applications/XAMPP/xamppfiles/htdocs/events_space/web/dist/ \
  root@events.ecsahc.org:/var/www/events/web/dist/
```

---

## Key Files

| File | Purpose |
|------|---------|
| `api/main.py` | FastAPI app entry point, router registration, CORS config |
| `api/scheduler.py` | Background task scheduler (email jobs etc.) |
| `api/seed_permissions.py` | Seed script for permission records |
| `api/seed_roles.py` | Seed script for role records |
| `web/src/App.vue` | Root Vue component |
| `web/src/router/` | Vue Router config |
| `web/src/stores/` | Pinia stores |
| `web/src/services/` | API call helpers |
| `web/src/pages/` | Page-level views |

---

## Auth Pattern

- JWT with RS256 keypair (not HS256 symmetric)
- `JWT_PRIVATE_KEY` signs tokens; `JWT_PUBLIC_KEY` verifies
- Two token types: access (short-lived) + refresh (long-lived)
- Auth header: `Authorization: Bearer <token>`

---

## Notes

- This project is **independent** from `cosecsamis.org` — different database, different server, different auth system
- The main `cosecsa` database is on `cosecsamis.org`; this one uses `events_db` on `events.ecsahc.org`
- Uploads directory must exist and be writable on the server
- Python version on server is 3.9 — do not use 3.10+ syntax locally without verifying
