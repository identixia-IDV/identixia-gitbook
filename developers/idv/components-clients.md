---
description: >-
  Choose web, Android, iOS, Flutter, or React Native applicant clients for document and selfie capture with Identixia IDV.
icon: mobile-screen
---

# Identity Verification Client SDKs and Sample Apps

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
