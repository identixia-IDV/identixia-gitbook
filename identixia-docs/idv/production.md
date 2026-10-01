---
description: >-
  Hardening checklist: auth, TLS, databases, engines, and what not to expose.
---

# Production

## Checklist

| Area | Guidance |
| --- | --- |
| Demo auth | Set `IDV_OPEN_API=0` (or unset). Issue real service tokens per tenant. |
| Capture secrets | Keep `IDV_SERVICE_TOKEN` on the **company backend** only. Apps use capture tokens. |
| TLS | Terminate HTTPS on a reverse proxy in front of `:14187` (and company `:14195` if public). |
| License Admin | Keep `:14190` on **localhost** / private network. Do not publish the issuer UI. |
| Engines | Point IDV at internal Document `:14102` and Face `:14103` URLs; activate each host/container with its own machine code. |
| Database | Prefer PostgreSQL via `python IDV/setup_database.py` (or `--yes` for a guided default). SQLite is fine for local demos only. |
| Memory store | `IDV_FORCE_MEMORY` / `COMPANY_FORCE_MEMORY` are for tests — not production. |
| Webhooks | Require `whsec_…` HMAC verification; idempotent handlers; poll session API if a delivery is missed. |
| Brand | Serve `/brand/*` from `license/admin/brand/` (or the configured `IDV_BRAND_DIR`). |

## Reverse proxy (sketch)

```text
Internet clients
      │
      ▼
 HTTPS terminator  ──►  platform/server :14187  (/v1, /admin)
      │
      └──►  company/backend :14195  (merchant APIs + /admin)
                 │
                 ├──► platform/server (service bearer)
                 └──► (optional) capture CDN / static hosting

Internal only:
  document-engine :14102
  face-engine     :14103
  license/admin   :14190   ← Identixia / ops, not public
```

## Database

```bash
cd IDV
python setup_database.py --check   # inspect current config
python setup_database.py --yes     # non-interactive recommended local/prod bootstrap
```

Writes `IDV/.env` and creates schema. Production authority is **PostgreSQL**; media / Valkey / RabbitMQ options appear in the same wizard when you need them.

## Engine URLs

Configure IDV to reach engines on your private network (not `127.0.0.1` from another host). Confirm:

```bash
curl -s https://doc-engine.internal/api/health
curl -s https://face-engine.internal/api/health
```

Machine codes differ for bare metal vs Docker — license the environment you ship.

## Go-live smoke test

1. Health on IDV, company backend, both engines
2. Start verification → capture document + face → `session.completed` webhook
3. Inspect identity `trust_state` in Identity Console
4. Confirm License Admin and issuer ports are not internet-facing

Related: [Project setup](environment.md) · [Walkthrough](walkthrough.md) · [Creating a session (API)](api.md).
