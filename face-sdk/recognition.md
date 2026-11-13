---
description: >-
  Learn how Identixia face recognition works, which APIs to use, and which sample repositories match your platform.
---

# Face Recognition SDK Features and Integration

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

Recognition and liveness together. Server port **14103**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`FaceRecognition-LivenessDetection-Android`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| iOS | [iOS](ios.md) | [`FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| Flutter | [Flutter](flutter.md) | [`FaceRecognition-LivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| React Native | [React Native](react-native.md) | [`FaceRecognition-LivenessDetection-React-Native`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`FaceRecognition-LivenessDetection-Ionic-Cordova`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`FaceRecognition-LivenessDetection-Windows`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`FaceRecognition-LivenessDetection-Docker`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) |

Recognition without a liveness score. Server port **14104**. Do not call `/api/face/liveness` on this build.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](recognition-android.md) | [`FaceRecognition-Android`](https://github.com/identixia-IDV/FaceRecognition-Android) |
| iOS | [iOS](recognition-ios.md) | [`FaceRecognition-iOS`](https://github.com/identixia-IDV/FaceRecognition-iOS) |
| Flutter | [Flutter](recognition-flutter.md) | [`FaceRecognition-Flutter`](https://github.com/identixia-IDV/FaceRecognition-Flutter) |
| React Native | [React Native](recognition-react-native.md) | [`FaceRecognition-React-Native`](https://github.com/identixia-IDV/FaceRecognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](recognition-ionic-capacitor.md) | [`FaceRecognition-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceRecognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](recognition-ionic-cordova.md) | [`FaceRecognition-Ionic-Cordova`](https://github.com/identixia-IDV/FaceRecognition-Ionic-Cordova) |
| Windows | [Windows](recognition-windows.md) | [`FaceRecognition-Windows`](https://github.com/identixia-IDV/FaceRecognition-Windows) |
| Linux / Docker | [Linux / Docker](recognition-linux-docker.md) | [`FaceRecognition-Docker`](https://github.com/identixia-IDV/FaceRecognition-Docker) |

Hub pack: [`Face-Recognition-SDK`](https://github.com/identixia-IDV/Face-Recognition-SDK)

## License

Without `recognition` entitlement, detect/template/match calls fail or return empty results. Check `GET /api/licenseStatus` (server) or the kit license status (mobile).
