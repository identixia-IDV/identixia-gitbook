---
description: >-
  On-premise face recognition SDK for Linux and Docker. Detection, landmarks, attributes, ICAO-style quality, templates, and 1:1 match through a local API.
---

# Face Recognition Linux / Docker SDK


## Overview

On-premise face recognition SDK for Linux and Docker. Detection, landmarks, attributes, ICAO-style quality, templates, and 1:1 match through a local API.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `FaceRecognition-Docker` |
| **Platform** | Linux |
| **Docs site** | [doc.identixia.com](https://doc.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-Docker" %}

Source: [`identixia-IDV/FaceRecognition-Docker`](https://github.com/identixia-IDV/FaceRecognition-Docker)

## What you can do

| Capability | Description |
| --- | --- |
| Detect faces | Bounding box, landmarks, pose |
| Attributes | Age / gender / expression-style traits when enabled |
| Image / face quality | ICAO-style quality scores |
| Templates | Compact face feature vectors you store yourself |
| 1:1 match | Compare two images or two templates |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Host | Linux x86_64 or any Docker host |
| Docker | Optional — same repository builds the image |
| Port | Face **14103** · Document **14102** · Document liveness **14106** (product-specific) |
| Machine code | Different for bare metal vs container — license the environment you ship |

## Quick start (server)

Default API port for this product family: **`14103`**.

### 1. Clone and start

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-Docker.git
cd FaceRecognition-Docker
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

### Docker (when the repo ships an image)

```bash
# See the repository README for the exact image name and tags (CPU/GPU).
docker compose up -d   # or the documented docker run line
curl -s http://127.0.0.1:PORT/api/health
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

## Identixia Face Recognition — Linux / Docker

On-premise **face recognition** for Linux / Docker: detect, attributes, quality, landmarks, 1:1 match, and 1:N search. This image ships recognition model packs only. Liveness is `FaceLivenessDetection-Docker`.

| Topic | Detail |
| --- | --- |
| API | `http://127.0.0.1:14104` |
| Demo | `http://127.0.0.1:14204` |
| Image | `identixia/face-recognition` |
| Models | `recognition-common.xdb`, `recognition.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb` |
| Left out | `recognition-liveness.xdb`, `recognition-deepfake.xdb` |

```bash
# place Linux runtime into lib/cpu (see lib/README.md)
./docker/build_docker.sh
docker compose -f docker/docker-compose.yml up
```

```bash
curl -s http://127.0.0.1:14104/api/machinecode
curl -s -X POST http://127.0.0.1:14104/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
curl -s http://127.0.0.1:14104/api/health
```

Recognition calls: `POST /api/face/analyze`, `/boxes`, `/traits`, `/image-quality`, `/landmarks`, `/quality`, `/compare`, `/template`, `/score`, `/enroll`, `/search`.
