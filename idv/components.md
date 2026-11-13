---
description: >-
  Find the IDV server, company backend, applicant clients, admin consoles, and biometric engines in the project structure.
---

# Identity Verification Platform Components

## Top-level layout (`IDV/`)

| Path | Role | Docs |
| --- | --- | --- |
| `IDV_server/` | Platform API + workers (`:14187`) | [Platform server](platform-server.md) |
| `IDV_console/` | Identity Console (`:14188` / `/admin`) | [Identity Console](platform-console.md) |
| `company/backend/` | Sample **company server** (`:14195`) | [Company backend](company-backend.md) |
| `company/admin/` | Company operator UI (`:14189`) | [Company Admin](company-admin.md) |
| `license/` | Hybrid issuer + brand (`:14190`) | [License Admin](license-admin.md) |
| `app/` | Applicant SDKs + demos | [Applicant clients](components-clients.md) |
| `packages/` | Shared UI / decision / licence libs | [Shared packages](shared-packages.md) |
| `license/license_v2/` | Shared Hybrid protocol | [Hybrid protocol](license-protocol.md) |
| `docs/` | Offline handbook + API notes | [Reference](reference.md) |

## Brand

Brand files live in [`identixia-assets`](https://github.com/identixia-IDV/identixia-assets) under `brand/`.

Org: [`identixia-IDV`](https://github.com/identixia-IDV).
