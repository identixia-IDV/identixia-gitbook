---
description: >-
  IDV .env keys, ports, and database defaults.
---

# Environment & storage

## Folder overrides (`.env`)

Copy `IDV/.env.example` → `IDV/.env`.

| Env key | Default |
| --- | --- |
| `IDV_SERVER_DIR` | `idv-server` |
| `IDV_SERVER_UI_DIST` | `idv-server-ui/dist` |
| `IDV_PORTAL_DIR` | `idv-server-ui/portal` |
| `IDV_BRAND_DIR` | `license-admin/brand` |
| `COMPANY_ADMIN_DIST` | `company-admin/dist` |
| `COMPANY_ADMIN_DIR` | `company-admin` |
| `LICENSE_ADMIN_DIR` | `license-admin` |
| `IDV_PORT` / `IDV_BASE_URL` | `14187` / `http://127.0.0.1:14187` |

## Durable storage

| Project | Default |
| --- | --- |
| `idv-server` | SQLite under `database/` (tenant-separated rows) |
| `company-backend` | `company-backend/database/company.sqlite` |
| `license-admin` | `license-admin/database/` (issuer ledger) |

Production: `python IDV/setup_database.py` for PostgreSQL / media / Valkey / RabbitMQ. Memory stores are for tests only (`IDV_FORCE_MEMORY` / `COMPANY_FORCE_MEMORY`).
