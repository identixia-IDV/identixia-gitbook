---
description: >-
  IDV client SDKs and demo apps under IDV/app/.
---

# Applicant clients

Capture SDKs and demos. The **service token stays on the company backend**; apps use capture tokens.

## Packages (`IDV/app/packages/`)

| Package | Role |
| --- | --- |
| `idv-web` | Embeddable web capture UI |
| `idv-react` | React wrapper |
| `idv-android` | Android SDK (CameraX) |
| `idv-ios` | Swift package `IdvSdk` |

## Demo hosts

| App | Docs |
| --- | --- |
| Web | [Web demo](client-web.md) |
| Android | [Android demo](client-android.md) |
| iOS | [iOS demo](client-ios.md) |
| Flutter / React Native | [Other demos](client-other.md) |

```bash
python IDV/app/tools/refresh_client.py
```
