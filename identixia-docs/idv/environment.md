---
description: >-
  Configure IDV .env, engine URLs, tokens, and storage — keep secrets out of apps and git.
---

# Project setup

## 1. Copy environment file

```bash
cd IDV
copy .env.example .env
# or: cp .env.example .env
```

Edit `IDV/.env`. Restart servers after changes.

## 2. Required keys for a real engine demo

| Key | Local demo value | Notes |
| --- | --- | --- |
| `IDV_ENGINES` | `http` | Use `fake` only for UI smoke tests without engines |
| `DOCUMENT_API_URL` | `http://127.0.0.1:14102` | Internal Document engine |
| `FACE_API_URL` | `http://127.0.0.1:14103` | Internal Face engine |
| `IDV_PORT` / `IDV_BASE_URL` | `14187` / `http://127.0.0.1:14187` | Platform listen URL |
| `IDV_OPEN_API` | `1` locally only | Demo bearer `demo` — **off in production** |

Company backend (process env or its own config):

| Key | Local demo | Notes |
| --- | --- | --- |
| `IDV_BASE_URL` | `http://127.0.0.1:14187` | Platform URL |
| `IDV_SERVICE_TOKEN` | `demo` with open API | Real token in production — **never in client apps** |
| `IDV_TENANT_ID` | `ten_demo` | Tenant scope |

## 3. Folder overrides

| Env key | Default |
| --- | --- |
| `IDV_SERVER_DIR` | `platform/server` |
| `IDV_SERVER_UI_DIST` | `platform/console/dist` |
| `IDV_BRAND_DIR` | `license/admin/brand` |
| `COMPANY_ADMIN_DIST` | `company/admin/dist` |
| `COMPANY_ADMIN_DIR` | `company/admin` |
| `LICENSE_ADMIN_DIR` | `license/admin` |

## 4. Storage

| Project | Default |
| --- | --- |
| `platform/server` | SQLite under `database/` (tenant-separated rows) |
| `company/backend` | `company/backend/database/company.sqlite` |
| `license/admin` | `license/admin/database/` (issuer ledger) |

Production: `python IDV/setup_database.py` (or `--yes`) for PostgreSQL / media / Valkey / RabbitMQ. Memory stores are for tests only (`IDV_FORCE_MEMORY` / `COMPANY_FORCE_MEMORY`).

## 5. Security rules (non-negotiable)

| Rule | Why |
| --- | --- |
| Do not commit `.env` or licence files | Secrets and machine-bound keys |
| Service bearer stays on company backend | Capture apps use capture tokens only |
| No open “allow all” auth | Unlike public test-mode cloud rules — deny by default |
| License Admin on localhost / private net | Issuer must not be internet-facing |

Next: [Initial setup process](initial-setup.md).
