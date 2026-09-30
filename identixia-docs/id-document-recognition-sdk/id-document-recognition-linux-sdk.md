---
description: >-
  On-premise ID document recognition SDK for Linux and Docker. Passport, ID card, and driver license OCR, MRZ, and barcode extraction. Document liveness routes require the matching license.
---

# ID Document Recognition Linux / Docker SDK


## Overview

On-premise ID document recognition SDK for Linux and Docker. Passport, ID card, and driver license OCR, MRZ, and barcode extraction. Document liveness routes require the matching license.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `ID-Document-Recognition-Liveness-Detection-Docker` |
| **Platform** | Linux |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker" %}

Source: [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker)

## What you can do

| Capability | Description |
| --- | --- |
| Locate & crop | Find the ID document in a camera frame or still |
| OCR | Visual-zone fields (name, document number, dates, …) |
| MRZ | Machine-readable zone parse + checks |
| Barcode / QR | When present on the document |
| Front + back | Capture both sides when required |
| Document liveness | Authenticity / PAD checks when the license includes it |
| Structured JSON | Same result idea on mobile and server |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Host | Linux x86_64 or any Docker host |
| Docker | Optional — same repository builds the image |
| Port | Face **14103** · Document **14102** · Document liveness **14106** (product-specific) |
| Machine code | Different for bare metal vs container — license the environment you ship |

## Quick start (server)

Default API port for this product family: **`14102`**.

### 1. Clone and start

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker.git
cd ID-Document-Recognition-Liveness-Detection-Docker
# Follow README: place lib/ runtime, then start the HTTP server / demo UI
```

### 2. Machine code → license → activate

```bash
curl -s http://127.0.0.1:14102/api/machinecode
# Send data.machinecode to Identixia → receive license
curl -s -X POST http://127.0.0.1:14102/api/activate \
  -H "Content-Type: text/plain" \
  --data-binary @license.txt
curl -s http://127.0.0.1:14102/api/licenseStatus
curl -s http://127.0.0.1:14102/api/health
```

You can also drop `license.txt` next to the server and restart.

### Try document process

```bash
curl -s -X POST http://127.0.0.1:14102/api/documentProcess \
  -H "Content-Type: application/json" \
  -d "{\"images\":[{\"image\":\"BASE64_JPEG\"}]}"
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

## API reference — document HTTP (Windows / Linux / Docker)

Base URL: `http://{host}:14102`

### Control routes

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/backend` | Backend info |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | `recognition`, `authenticity` flags |
| `POST` | `/api/activate` | Activate license |

### Process routes

| Method | Path | Body | Description |
| --- | --- | --- | --- |
| `POST` | `/api/documentProcess` | `{ "images":[…], "rfid"?, "response"? }` | Full process (OCR + optional authenticity) |
| `POST` | `/api/documentRecognition` | `{ "images":[…] }` | Recognition only |
| `POST` | `/api/documentLiveness` | `{ "images":[…] }` | Authenticity / liveness only |
| `POST` | `/api/generalProcess` | `{ "image", "options"? }` | General process helper |

`images` entries are objects with base64 `image` (and optional metadata) or raw base64 strings depending on binding — see the sample Postman collection in the repo `postman/` folder.

```bash
curl -s -X POST http://127.0.0.1:14102/api/documentProcess \
  -H "Content-Type: application/json" \
  -d '{"images":[{"image":"BASE64_JPEG"}]}'
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

## Screenshots

<figure><img src="../.gitbook/assets/document-desktop-result.png" alt="Document recognition result UI" width="520"><figcaption>Document recognition result UI</figcaption></figure>

<figure><img src="../.gitbook/assets/document-docker-result.png" alt="Docker document result" width="520"><figcaption>Docker document result</figcaption></figure>


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

Adapted from the shipping repository README for exact commands and platform-specific notes. Screenshots above use the current Identixia asset pack.

## Identixia ID Document Recognition and Liveness Detection — Linux / Docker

**On-premise ID document recognition** as a Linux / Docker HTTP API: passport MRZ OCR, ID card barcode, document process, and optional document liveness / authenticity for KYC / eKYC. Identity data stays in your cluster — **no** Identixia cloud upload.

Image: [`identixia/document-reader`](https://hub.docker.com/r/identixia/document-reader).

---

## Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then replace the key in `license.txt` and activate.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **ID document recognition** Linux / Docker API (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · MRZ · barcode · optional authenticity |
| **What you run** | HTTP API on port **14102** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Replace the key in the included `license.txt`, then send that file with `POST /api/activate`. |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | Included in the Docker image |
| **Tools** | Linux x64 · Docker (or host Python + zip) |
| **Privacy** | Identity data stays in your VPC — no Identixia cloud |
| **Primary API** | `POST /api/documentProcess` (+ recognition / liveness routes when licensed) |

---

## Initial commands

```bash
docker pull identixia/document-reader:latest
docker run -d --name identixia-api -p 14102:14102 \
  -v /etc/machine-id:/etc/machine-id:ro \
  --shm-size=2gb --privileged identixia/document-reader:latest
```

```bash
curl -s http://127.0.0.1:14102/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

This repository includes `license.txt`. Replace the key in that file with the license we send you, then run this command from the repository folder:

```bash
curl -s -X POST http://127.0.0.1:14102/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
```

```bash
curl -s http://127.0.0.1:14102/api/health
```

Replace `BASE64_JPEG` with a base64-encoded JPEG of the document.

```bash
curl -s -X POST http://127.0.0.1:14102/api/documentProcess -H "Content-Type: application/json" -d "{\"images\":[{\"image\":\"BASE64_JPEG\"}]}"
```

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
```

Open http://127.0.0.1:14202

---

## What you get

| Capability | What it does |
| --- | --- |

---

## Requirements

| | |
| --- | --- |
| Host | Linux x64 with Docker (or bare-metal Python + runtime zip) |
| Ports | API **14102**, Gradio **14202** |
| Privileges | `--shm-size=2gb --privileged` recommended for the published image |

---

## Gradio demo

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
```

Open http://127.0.0.1:14202

---

## Use in your app

Point your backend at `http://<host>:14102`. See [docs](https://docs.identixia.com).

Common KYC wiring: health → activate → `documentProcess` (OCR / MRZ / barcode) → optional authenticity when licensed → map fields into your case system.

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

Document liveness only (API **14107**): [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

---
