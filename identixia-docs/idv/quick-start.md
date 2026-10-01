---
description: >-
  Run IDV server, Identity Console, company backend/admin, and licence admin locally.
---

# Quick start

## Order that works locally

1. Document engine `:14102` + Face engine `:14103` (see [Engines](engines.md))
2. [IDV server](platform-server.md) `:14187`
3. [Identity Console](platform-console.md) `:14188` (optional in prod — built into `/admin`)
4. [Company backend](company-backend.md) `:14195` + [Company Admin](company-admin.md) `:14189`
5. [License Admin](license-admin.md) `:14190` when testing Hybrid issue
6. An [applicant demo](components-clients.md)

## Storage defaults

| Project | Default SQLite |
| --- | --- |
| `idv-server` | `idv-server/database/idv.sqlite` (or `IDV_SQLITE_PATH`) |
| `company-backend` | `company-backend/database/company.sqlite` |
| `license-admin` | `license-admin/database/` |

PostgreSQL / media / Valkey / RabbitMQ: `python setup_database.py` from `IDV/`. See [Environment & storage](environment.md).

## Minimal commands

```bash
# Platform
cd IDV/idv-server && python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
# → http://127.0.0.1:14187/v1  and  /admin/

# Identity Console (develop)
cd IDV/idv-server-ui && npm install && npm run dev
# → http://127.0.0.1:14188/

# Company server + admin UI
cd IDV/company-backend && pip install -r requirements.txt
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
# → http://127.0.0.1:14195/  (built admin at /admin/)

cd IDV/company-admin && npm install && npm run dev
# → http://127.0.0.1:14189/

# Licence issuer (localhost only)
cd IDV/license-admin && pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
# → http://127.0.0.1:14190/
```
