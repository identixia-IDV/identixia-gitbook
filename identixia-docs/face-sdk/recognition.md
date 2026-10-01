---
description: >-
  What Identixia face recognition does, which APIs to call, and which repositories ship it.
---

# Face recognition

## Overview

Face **recognition** turns a camera image into data you can store and compare:

1. **Detect** the face (box, landmarks, pose).
2. **Describe** it (optional attributes and quality).
3. **Encode** it as a compact **template** (feature vector).
4. **Compare** templates (1:1) or search a gallery (1:N).

You own the gallery database. The SDK does not upload faces to Identixia.

## Typical mobile flow

```text
activate(license) → initSDK()
        │
        ├─ detect / attributes / quality / landmarks
        ├─ template (enroll) → save in YOUR database
        ├─ match (1:1) two images or two templates
        └─ identify (1:N) probe against enrolled people
```

## Typical server flow (HTTP)

Control routes use `{success, code, message, request_id, data}`. Process routes return engine JSON.

| Step | Route (examples) |
| --- | --- |
| Health | `GET /api/health` |
| Machine code | `GET /api/machinecode` |
| Activate | `POST /api/activate` |
| Detect / analyze | `POST /api/face/analyze` or `/api/face/boxes` |
| Template | `POST /api/face/template` |
| 1:1 | `POST /api/face/compare` |
| 1:N | `POST /api/face/enroll` · `/api/face/search` · `/api/face/gallery` |

### Example — 1:1 compare (Linux / Windows)

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/compare \
  -H "Content-Type: application/json" \
  -d '{"image1":"BASE64_A","image2":"BASE64_B"}'
```

Parse the process JSON for score / match decision. Do not scrape the demo UI.

## Repositories that include recognition

| Variant | Platforms |
| --- | --- |
| Full (recognition + liveness) | [Android](android.md) · [iOS](ios.md) · [Flutter](flutter.md) · [React Native](react-native.md) · [Ionic](ionic-capacitor.md) · [Windows](windows.md) · [Docker](linux-docker.md) |
| Recognition only | [Windows](recognition-windows.md) · [Docker](recognition-linux-docker.md) |

Hub pack: [`Face-Recognition-SDK`](https://github.com/identixia-IDV/Face-Recognition-SDK)

## License

Without `recognition` entitlement, detect/template/match calls fail or return empty results. Check `GET /api/licenseStatus` (server) or the kit license status (mobile).
