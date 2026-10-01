---
description: >-
  Run IDV server, console, company sample, and licence admin locally.
---

# Quick start

## Storage defaults

Local durable storage defaults to **SQLite** under each project’s `database/` folder.

| Project | Default |
| --- | --- |
| `idv-server` | `idv-server/database/idv.sqlite` (or `IDV_SQLITE_PATH`) |
| `company-backend` | `company-backend/database/company.sqlite` |
| `license-admin` | `license-admin/database/` |

For PostgreSQL / media / Valkey / RabbitMQ: `python setup_database.py` from `IDV/`.

## 1. IDV server

```bash
cd IDV/idv-server
python -m venv .venv && .venv/Scripts/activate   # or source .venv/bin/activate
pip install -r requirements.txt
set IDV_OPEN_API=1                               # Windows; export on Unix
python app.py
```

* API: `http://127.0.0.1:14187/v1`
* Admin: `http://127.0.0.1:14187/admin/`

## 2. Identity Console (develop)

```bash
cd IDV/idv-server-ui
npm install && npm run dev
```

Open `http://127.0.0.1:14188/` (proxies API to `:14187`). Production build is served from the server at `/admin/`.

## 3. Company sample

```bash
cd IDV/company-backend && pip install -r requirements.txt && python app.py
# UI: cd IDV/company-admin && npm install && npm run dev  → :14189
```

## 4. Licence admin

```bash
cd IDV/license-admin
pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
```

Open `http://127.0.0.1:14190` (localhost only). Favicon and logo: `license-admin/brand/`.

## 5. Applicant demos

See [Components & clients](components.md) and `IDV/client/README.md`.
