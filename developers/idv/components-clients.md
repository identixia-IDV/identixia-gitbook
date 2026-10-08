---
description: >-
  IDV client SDKs and demo apps under IDV/demo_clients/.
icon: mobile-screen
---

# Applicant clients

Capture SDKs and demos. The **service token stays on the company backend**; apps use capture tokens.

## Packages (`IDV/demo_clients/packages/`)

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
python IDV/demo_clients/tools/refresh_client.py
```

{% include "../.gitbook/includes/footer.md" %}
