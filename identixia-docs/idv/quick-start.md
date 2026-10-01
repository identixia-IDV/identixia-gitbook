---
description: >-
  Run IDV server, Identity Console, company backend/admin, and licence admin locally.
---

# Quick start

## Order that works locally

1. Complete [Project setup](environment.md) (`.env`)
2. Document engine `:14102` + Face engine `:14103` — [Prerequisites: engines](engines.md)
3. Run `python IDV/scripts/start_local.py` **or** start services manually below
4. [Initial setup process](initial-setup.md) — console, company settings, webhook
5. [End-to-end walkthrough](walkthrough.md)

## Helper (recommended)

```bash
# Engines must already be healthy on :14102 and :14103
python IDV/scripts/start_local.py
```

Preflight checks engine health, starts IDV server + company backend, and prints URLs. It does **not** start License Admin and does **not** mean the stack is production-ready when `IDV_OPEN_API=1`.

## Storage defaults

| Project | Default SQLite |
| --- | --- |
| `platform/server` | `platform/server/database/idv.sqlite` (or `IDV_SQLITE_PATH`) |
| `company/backend` | `company/backend/database/company.sqlite` |
| `license/admin` | `license/admin/database/` |

PostgreSQL / media / Valkey / RabbitMQ: `python setup_database.py` from `IDV/`. See [Project setup](environment.md).

## Manual commands

```bash
# Platform (localhost demo auth only)
cd IDV/platform/server && python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
# → http://127.0.0.1:14187/v1  and  /admin/

# Identity Console (develop)
cd IDV/platform/console && npm install && npm run dev
# → http://127.0.0.1:14188/

# Company server + admin UI
cd IDV/company/backend && pip install -r requirements.txt
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
# → http://127.0.0.1:14195/  (built admin at /admin/)

cd IDV/company/admin && npm install && npm run dev
# → http://127.0.0.1:14189/

# Licence issuer (localhost / private network only — never public)
cd IDV/license/admin && pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
# → http://127.0.0.1:14190/
```
