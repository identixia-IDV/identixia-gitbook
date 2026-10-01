---
description: >-
  Identixia IDV: customer-run verification server, consoles, licensing, and applicant clients.
---

# IDV platform

<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>
<p align="center"><img src="../.gitbook/assets/favicon.png" alt="Identixia mark" width="48"></p>

## What IDV is

**IDV** is the Identixia identity-verification **platform** (folder `IDV/` in the monorepo). It is not a replacement for the Face or Document SDKs — it **orchestrates** them.

| Piece | Role |
| --- | --- |
| `idv-server` | Platform API + workers (`:14187`) |
| `idv-server-ui` | Identity Console (dev `:14188`, production `/admin`) |
| `company-backend` + `company-admin` | Sample merchant backend + UI |
| `license-admin` | Hybrid licence issuer (`:14190`) |
| `client/` | Applicant SDKs and demo apps |
| `license_v2` / `packages/` | Shared protocol and libraries |

Brand logo and favicons for the consoles live in `IDV/license-admin/brand/` and are served at `/brand/*`.

## Read next

1. [Architecture](architecture.md) — who owns what
2. [Quick start](quick-start.md) — run locally
3. [Document & Face engines](engines.md) — HTTP wiring to the SDKs
4. [Components & clients](components.md) — packages and demos

Deep offline handbook (chapters, Postman, schema): see `IDV/docs/` in the source tree — not duplicated here.

{% hint style="info" %}
With `IDV_ENGINES=http`, IDV calls your local Document and Face HTTP APIs. Start those SDK servers first (or point env URLs at your deployment).
{% endhint %}
