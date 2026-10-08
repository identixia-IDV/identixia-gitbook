---
description: >-
  Run the IDV server, Identity Console, company backend, and license administration service in a local development environment.
icon: rocket
---

# IDV Platform Quick Start

## Order that works locally

1. Complete [Project setup](environment.md) (`.env`)
2. Document engine `:14102` + Face engine `:14103` — [Prerequisites: engines](https://docs.identixia.com/developers/idv/engines)
3. Run `python IDV/IDV_server (then company)` **or** start services manually below
4. [Initial setup process](initial-setup.md) — console, company settings, webhook
5. [End-to-end walkthrough](walkthrough.md)

## Helper (recommended)

```bash
# Engines must already be healthy on :14102 and :14103
python IDV/IDV_server (then company)
```

Preflight checks engine health, starts IDV server + company backend, and prints URLs. It does **not** start License Admin and does **not** mean the stack is production-ready when `IDV_OPEN_API=1`.

## Storage defaults

| Project | Default SQLite |
| --- | --- |
| `IDV_server` | `IDV_server/database/idv.sqlite` (or `IDV_SQLITE_PATH`) |
| `company/backend` | `company/backend/database/company.sqlite` |
| `license` | `license/database/` |

PostgreSQL / media / Valkey / RabbitMQ: `python IDV/Install_db/setup_database.py` from `IDV/Install_db/`. See [Project setup](environment.md).

## Manual commands

```bash
# Platform (localhost demo auth only)
cd IDV/IDV_server && python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
# → http://127.0.0.1:14187/v1  and  /admin/

# Identity Console (develop)
cd IDV/IDV_console && npm install && npm run dev
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
cd IDV/license && pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
# → http://127.0.0.1:14190/
```

{% include "../.gitbook/includes/footer.md" %}
