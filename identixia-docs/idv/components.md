---
description: >-
  IDV folders, applicant SDKs, and demo apps — without duplicating the handbook.
---

# Components & clients

## Top-level layout (`IDV/`)

| Path | Role | Port (dev) |
| --- | --- | --- |
| `idv-server/` | Platform API + workers | 14187 |
| `idv-server-ui/` | Identity Console | 14188 |
| `company-backend/` | Sample company API | 14195 |
| `company-admin/` | Company operator UI | 14189 |
| `license-admin/` | Identixia Hybrid issuer + **brand** | 14190 |
| `client/` | Applicant SDKs and demos | (per app) |
| `packages/` | Shared server/console libraries | — |
| `license_v2/` | Shared licence protocol | — |
| `docs/` | Offline handbook + API reference | — |

## Applicant clients (`IDV/client/`)

| Path | Role |
| --- | --- |
| `packages/idv-web` | Embeddable web verification UI |
| `packages/idv-react` | React wrapper |
| `packages/idv-android` | Android SDK (CameraX capture) |
| `packages/idv-ios` | Swift package `IdvSdk` |
| `app/web` · `app/android` · `app/ios` · `app/flutter` · `app/react_native` | Demo hosts |

Web demo:

```bash
cd IDV/client/app/web
npm install && npm run dev
# http://127.0.0.1:5175/
```

Refresh engines/catalog into demos (from monorepo root):

```bash
python IDV/client/tools/refresh_client.py
```

## Brand assets

Use **one** brand pack — do not copy logos into every app:

* Source: `IDV/license-admin/brand/` (`logo.png`, `favicon.ico`, `favicon.png`, `apple-touch-icon.png`)
* Runtime: served as `/brand/*` from licence admin / configured brand dir
* Docs site: same files under `.gitbook/assets/` (`brand-logo.png`, `favicon.png`, …)

GitHub: monorepo [`identixia-IDV`](https://github.com/identixia-IDV) — IDV sources ship with your distribution; Face/Document demos are separate public product repos under the same org.
