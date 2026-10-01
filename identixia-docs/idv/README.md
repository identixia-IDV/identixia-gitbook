---
description: >-
  Identixia IDV: platform server, company integration, licensing, engines, and applicant clients.
---

# IDV platform

<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>
<p align="center"><img src="../.gitbook/assets/favicon.png" alt="Identixia mark" width="48"></p>

## What IDV is

**IDV** is the Identixia identity-verification **platform** (`IDV/` in the monorepo). It does **not** replace the Face or Document SDKs — it **orchestrates** them and sits between your company systems and capture apps.

## Who runs what

| Role | Folders | Typical ports |
| --- | --- | --- |
| **Platform** (tenant API, workers, reviews) | `idv-server/`, `idv-server-ui/` | 14187 · 14188 |
| **Company / merchant sample** | `company-backend/`, `company-admin/` | 14195 · 14189 |
| **Identixia licence issuer** | `license-admin/` (+ brand) | 14190 |
| **Applicant capture** | `client/` | e.g. web 5175 |
| **Shared libraries** | `packages/`, `license_v2/` | — |
| **Biometric engines** | Face SDK + Document SDK (HTTP) | 14103 · 14102 |

```text
Applicant app ──► Company backend :14195 ──► IDV server :14187 ──► Face/Document engines
                      │                         │
               Company Admin :14189      Identity Console :14188 /admin
                                                    │
                                           License Admin :14190 (issuer)
```

## Read next

1. [Architecture](architecture.md)
2. [Getting started](getting-started.md) → [Quick start](quick-start.md)
3. [Platform](platform.md) · [Company integration](company.md) · [Licensing](licensing.md)
4. [Engines](engines.md) · [Applicant clients](components-clients.md)

Deep handbook / Postman: `IDV/docs/` and `IDV/idv-server/postman/` in source — not copied here.

{% hint style="info" %}
The **service bearer token stays on the company backend**. Capture apps use a short-lived **capture token**, not the company service secret.
{% endhint %}
