---
description: >-
  IDV folders mapped to Admin, Company, Applicant, and Engines roles.
---

# Project structure

## Components

IDV is a self-host KYC platform that uses Identixia **SDK-integrated HTTP engines** as the biometric backend.

| Role | What it is | Folder | Typical port |
| --- | --- | --- | ---: |
| **Admin (platform)** | Tenant API, workers, Identity Console | `idv-server/`, `idv-server-ui/` | 14187 · 14188 |
| **Company (merchant)** | Your backend sample + operator UI | `company-backend/`, `company-admin/` | 14195 · 14189 |
| **Applicant (user)** | Capture SDKs and demo apps | `client/` | e.g. 5175 |
| **Engines** | Document + Face recognition / liveness | Face / Document SDK repos | 14102 · 14103 |

## Supporting folders

| Path | Role |
| --- | --- |
| `license-admin/` | Hybrid licence **issuer** (Identixia ops) — `:14190`, private only |
| `license_v2/` | Shared Hybrid protocol sources |
| `packages/` | Shared admin UI / decision / licence helpers |
| `docs/` | Offline handbook + API notes |

## Data flow

```text
Applicant (client) → Company backend (:14195) → IDV server (:14187) → Engines (:14102 / :14103)
                         ↑                              ↓
                  Company Admin                  Identity Console
```

Next: [Prerequisites: engines](engines.md).
