---
description: >-
  On-premise face recognition SDK for Windows with passive liveness. Detection, quality, templates, and 1:1 match. Liveness routes require the matching license.
---

# Face Recognition + Liveness Windows SDK


## Overview

On-premise face recognition SDK for Windows with passive liveness. Detection, quality, templates, and 1:1 match. Liveness routes require the matching license.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `FaceRecognition-LivenessDetection-Windows` |
| **Platform** | Windows |
| **Docs site** | [doc.identixia.com](https://doc.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows" %}

Source: [`identixia-IDV/FaceRecognition-LivenessDetection-Windows`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows)

## What you can do

| Capability | Description |
| --- | --- |
| Detect faces | Bounding box, landmarks, pose |
| Attributes | Age / gender / expression-style traits when enabled |
| Image / face quality | ICAO-style quality scores |
| Templates | Compact face feature vectors you store yourself |
| 1:1 match | Compare two images or two templates |
| 1:N identify | Enroll gallery + live search (mobile VideoWorker / server gallery) |
| Passive liveness | Presentation-attack score when the license includes it |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| OS | Windows 10/11 x64 |
| Runtime | Product `lib/` (CPU) next to the server |
| Python | As required by the sample server (see repo README) |
| Port | Face **14103** · Document **14102** (default) |
| License | `license.txt` or `POST /api/activate` |

## Quick start (server)

Default API port for this product family: **`14103`**.

### 1. Clone and start

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows.git
cd FaceRecognition-LivenessDetection-Windows
# Follow README: place lib/ runtime, then start the HTTP server / demo UI
```

### 2. Machine code → license → activate

```bash
curl -s http://127.0.0.1:14103/api/machinecode
# Send data.machinecode to Identixia → receive license
curl -s -X POST http://127.0.0.1:14103/api/activate \
  -H "Content-Type: text/plain" \
  --data-binary @license.txt
curl -s http://127.0.0.1:14103/api/licenseStatus
curl -s http://127.0.0.1:14103/api/health
```

You can also drop `license.txt` next to the server and restart.

### Try a process call

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/analyze \
  -H "Content-Type: application/json" \
  -d "{\"image\":\"BASE64_JPEG\"}"
```


## License and activation (server)

1. Start the API (it stays up even without a key so you can read the machine code).
2. `GET /api/machinecode` → copy `data.machinecode`.
3. Contact Identixia with that code (Docker and bare metal codes differ).
4. `POST /api/activate` with the license file/bytes **or** place `license.txt` and restart.
5. `GET /api/licenseStatus` → check capability flags (`recognition`, `liveness` / `authenticity`).

Control routes return the envelope `{success, code, message, request_id, data}`. Process routes return **engine / process JSON** (not the control envelope).

## API reference — HTTP (Windows / Linux / Docker)

Base URL: `http://{host}:14103`

### Control routes (envelope)

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Process up (no license required) |
| `GET` | `/api/backend` | Backend / SDK info |
| `GET` | `/api/machinecode` | Machine fingerprint for licensing |
| `GET` | `/api/licenseStatus` | Flags: `recognition`, `liveness` |
| `POST` | `/api/activate` | License text, JSON `{"license":"…"}`, or multipart |

### Process routes (engine / process JSON)

Same path accepts JSON (base64 fields) or `multipart/form-data` (`image`, `image1`, `image2`, …).

| Method | Path | Body (summary) | Description |
| --- | --- | --- | --- |
| `POST` | `/api/face/analyze` | `image`, optional `cropImage` | Full analyze |
| `POST` | `/api/face/boxes` | `image` | Face boxes |
| `POST` | `/api/face/traits` | `image` | Attributes |
| `POST` | `/api/face/image-quality` | `image` | Image quality |
| `POST` | `/api/face/landmarks` | `image`, `mode` `14` or `68` | Landmarks |
| `POST` | `/api/face/quality` | `image` | Face quality |
| `POST` | `/api/face/template` | `image` | Template / feature |
| `POST` | `/api/face/compare` | `image1`, `image2` | 1:1 image match |
| `POST` | `/api/face/score` | `feature1`, `feature2` | Template similarity |

| `POST` | `/api/face/liveness` | `{ "image": "<b64>" }` | Passive liveness (license-gated) |
| `POST` | `/api/face/deepfake` | `{ "image": "<b64>" }` | Deepfake score when enabled |
| `POST` | `/api/face/enroll` | `{ "image", "name" }` | Server gallery enroll |
| `POST` | `/api/face/search` | `{ "image", "threshold" }` | 1:N search |
| `DELETE` | `/api/face/gallery/{id}` | — | Remove gallery entry |

### Example — compare two images

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/compare \
  -H "Content-Type: application/json" \
  -d '{"image1":"BASE64_JPEG","image2":"BASE64_JPEG"}'
```

### Example — template similarity

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/score \
  -H "Content-Type: application/json" \
  -d '{"feature1":"<b64>","feature2":"<b64>"}'
```

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Invalid license | Application / bundle id must match the key; server needs the correct machine code |
| Init failed | Runtime AAR/framework/`lib` missing or wrong ABI |
| No face / no document | Lighting, crop, distance; try still gallery image first |
| Liveness / authenticity empty | License flag off — request the matching entitlement |
| Camera black / crash | Use a **physical** device; grant camera permission |
| Docker license fails after bare-metal license | Machine codes differ — re-license the container |

| Port in use | Change host port or stop the other Identixia server |
| Multipart vs JSON | Field names must match (`image`, `image1`, `images`) |
| Envelope vs process JSON | Only control routes use `{success,code,…}`; process routes return engine JSON |

## Related platforms

| Platform | Docs |
| --- | --- |
| Android | [Face Recognition Android SDK](face-recognition-android-sdk.md) |
| iOS | [Face Recognition iOS SDK](face-recognition-ios-sdk.md) |
| Flutter | [Face Recognition Flutter SDK](face-recognition-android-sdk-2.md) |
| React Native | [Face Recognition React Native SDK](face-recognition-android-sdk-1.md) |
| Ionic Capacitor | [Face Recognition Ionic Capacitor SDK](face-recognition-ionic-capacitor-sdk.md) |
| Ionic Cordova | [Face Recognition Ionic Cordova SDK](face-recognition-android-sdk-3.md) |
| Windows (+ liveness) | [Face Recognition + Liveness Windows](face-recognition-sdk-windows.md) |
| Linux / Docker (+ liveness) | [Face Recognition + Liveness Linux](face-recognition-sdk-linux.md) |
| Windows (recognition only) | [Face Recognition Windows](face-recognition-windows-sdk.md) |
| Linux (recognition only) | [Face Recognition Linux](face-recognition-linux-sdk.md) |


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

The following is adapted from the shipping repository README for screenshots, exact commands, and platform-specific notes.

## <img src="https://cdn.simpleicons.org/windows/0078D4" width="32" height="32" alt="" /> Identixia Face Recognition SDK — Windows

**On-premise face recognition SDK** for Windows with **passive face liveness**: detect, quality, face template matching, 1:1 compare, and PAD (+ deepfake when licensed). Biometrics stay on your host — built for private KYC / access-control backends. CPU-only. Standalone App repo.

<p><img src="https://img.shields.io/badge/On-premise-0F766E?style=flat-square" alt="On-premise" /> <img src="https://img.shields.io/badge/1%3AN%20%2F%201%3A1-0F766E?style=flat-square" alt="1%3AN%20%2F%201%3A1" /> <img src="https://img.shields.io/badge/Passive%20liveness-0F766E?style=flat-square" alt="Passive%20liveness" /> <img src="https://img.shields.io/badge/API%208083-0F766E?style=flat-square" alt="API%208083" /> <img src="https://img.shields.io/badge/Postman-FF6C37?style=flat-square" alt="Postman" /></p>

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then replace the key in `license.txt` and activate.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **face recognition SDK** for Windows (+ passive liveness) |
| **Modes** | Detect · quality · templates · 1:1 match · PAD (+ deepfake when licensed) |
| **What you run** | HTTP API on port **14103** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Replace the key in the included `license.txt`, then send that file with `POST /api/activate`. |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | `lib\\cpu\\` from Google Drive zip `PENDING` |
| **Tools** | Windows 10/11 x64 · Python 3.10+ · CPU only |
| **Privacy** | Biometrics stay on your host — no Identixia cloud |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Run the server

```bat
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows.git
cd FaceRecognition-LivenessDetection-Windows
:: place lib\\cpu from the runtime zip (PENDING)
pip install -r requirements.txt
run.bat
```

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Get a license

```bash
curl -s http://127.0.0.1:14103/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> Activate

This repository includes `license.txt`. Replace the key in that file with the license we send you, then run this command from the repository folder:

```bash
curl -s -X POST http://127.0.0.1:14103/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
```

### <img src="https://img.shields.io/badge/-4-0F766E?style=for-the-badge" alt="" /> Check that it is running

```bash
curl -s http://127.0.0.1:14103/api/health
```

### <img src="https://img.shields.io/badge/-5-0F766E?style=for-the-badge" alt="" /> Detect / match / liveness

Replace `BASE64_JPEG` with a base64-encoded JPEG.

Detect a face:

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/analyze -H "Content-Type: application/json" -d "{\"image\":\"BASE64_JPEG\"}"
```

Compare two faces:

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/compare -H "Content-Type: application/json" -d "{\"image1\":\"BASE64_JPEG\",\"image2\":\"BASE64_JPEG\"}"
```

Check liveness:

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/liveness -H "Content-Type: application/json" -d "{\"image\":\"BASE64_JPEG\"}"
```

### <img src="https://img.shields.io/badge/-6-0F766E?style=for-the-badge" alt="" /> Open the Gradio demo

Keep the API running, then open a second terminal in the repository folder.

```bat
pip install -r requirements-demo.txt
run_demo.bat
```

Open http://127.0.0.1:14203

---

## <img src="https://api.iconify.design/lucide/list-checks.svg?color=%230F766E" width="24" height="24" alt="" /> What you get

| Capability | What it does |
| --- | --- |
| <img src="https://api.iconify.design/lucide/user-plus.svg?color=%230F766E" width="16" height="16" alt="" /> Enroll | Capture face templates into an on-device gallery |
| <img src="https://api.iconify.design/lucide/users.svg?color=%230F766E" width="16" height="16" alt="" /> Identify (1:N) | Match a live or still face against enrolled templates |
| <img src="https://api.iconify.design/lucide/aperture.svg?color=%230F766E" width="16" height="16" alt="" /> Capture | Guided still capture with quality feedback |
| <img src="https://api.iconify.design/lucide/sliders.svg?color=%230F766E" width="16" height="16" alt="" /> Attribute | Age / gender / expression-style attributes when enabled |
| <img src="https://api.iconify.design/lucide/shield.svg?color=%230F766E" width="16" height="16" alt="" /> Passive liveness | Optional face PAD (and deepfake checks when licensed on server) |
| <img src="https://api.iconify.design/lucide/fingerprint.svg?color=%230F766E" width="16" height="16" alt="" /> Templates | Compact face template extraction + similarity / matching |

| Surface | Port |
| --- | --- |
| HTTP API | **14103** |
| Gradio demo | **14203** |

---

## <img src="https://api.iconify.design/lucide/pc-case.svg?color=%230F766E" width="24" height="24" alt="" /> Requirements

| | |
| --- | --- |
| OS | Windows 10/11 x64 |
| Runtime | Python 3.10+ recommended |
| Hardware | CPU only |
| Ports | **14103** / **14203** |

---

## <img src="https://api.iconify.design/lucide/package.svg?color=%230F766E" width="24" height="24" alt="" /> Runtime zip

> **Google Drive (single zip):** `PENDING`

Unzip **directly** into `lib\cpu\`:

```text
lib\cpu\FaceRecognitionSDK.dll
lib\cpu\recognition*.xdb
… (other runtime files)
```

---

## <img src="https://api.iconify.design/lucide/app-window.svg?color=%230F766E" width="24" height="24" alt="" /> Gradio demo

Keep the API running, then open a second terminal in the repository folder.

```bat
pip install -r requirements-demo.txt
run_demo.bat
```

Open http://127.0.0.1:14203

---

## <img src="https://api.iconify.design/lucide/puzzle.svg?color=%230F766E" width="24" height="24" alt="" /> Use in your app

Call the HTTP API for detect, match, and liveness. See [docs](https://doc.identixia.com).

---

## <img src="https://api.iconify.design/lucide/images.svg?color=%230F766E" width="24" height="24" alt="" /> Screenshots

<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-detect.png" width="420" alt="Face detection Gradio demo" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-attribute.png" width="420" alt="Face attribute Gradio demo" />
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-quality.png" width="420" alt="Face image quality Gradio demo" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-landmarks.png" width="420" alt="Face landmarks Gradio demo" />
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-match.png" width="420" alt="Face template matching 1:1 demo" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-liveness.png" width="420" alt="Face liveness and deepfake Gradio demo" />
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-identify.png" width="420" alt="1:N identity Gradio demo" />
</p>

---

## <img src="https://api.iconify.design/lucide/layers.svg?color=%230F766E" width="24" height="24" alt="" /> Platforms

| | Platform | Repo |
| --- | --- | --- |
| <img src="https://cdn.simpleicons.org/android/3DDC84" width="18" height="18" alt="" /> | Android | [FaceRecognition-LivenessDetection-Android](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| <img src="https://cdn.simpleicons.org/apple/000000" width="18" height="18" alt="" /> | iOS | [FaceRecognition-LivenessDetection-iOS](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| <img src="https://cdn.simpleicons.org/flutter/02569B" width="18" height="18" alt="" /> | Flutter | [FaceRecognition-LivenessDetection-Flutter](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| <img src="https://cdn.simpleicons.org/react/61DAFB" width="18" height="18" alt="" /> | React Native | [FaceRecognition-LivenessDetection-React-Native](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) |
| <img src="https://cdn.simpleicons.org/ionic/3880FF" width="18" height="18" alt="" /> | Ionic Capacitor | [FaceRecognition-LivenessDetection-Ionic-Capacitor](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| <img src="https://cdn.simpleicons.org/apachecordova/E8E8E8" width="18" height="18" alt="" /> | Ionic Cordova | [FaceRecognition-LivenessDetection-Ionic-Cordova](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| <img src="https://cdn.simpleicons.org/windows/0078D4" width="18" height="18" alt="" /> | Windows | [FaceRecognition-LivenessDetection-Windows](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) |
| <img src="https://cdn.simpleicons.org/docker/2496ED" width="18" height="18" alt="" /> | Linux / Docker | [FaceRecognition-LivenessDetection-Docker](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) |

---
