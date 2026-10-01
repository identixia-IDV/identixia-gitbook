---
description: >-
  On-premise ID document recognition SDK for Windows. Passport, ID card, and driver license OCR, MRZ, and barcode extraction. Document liveness routes require the matching license.
---

# ID Document SDK — Windows (recognition + liveness)


## Overview

On-premise ID document recognition SDK for Windows. Passport, ID card, and driver license OCR, MRZ, and barcode extraction. Document liveness routes require the matching license.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `ID-Document-Recognition-Liveness-Detection-Windows` |
| **Platform** | Windows |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows" %}

Source: [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows)

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
| OS | Windows 10/11 x64 |
| Runtime | Product `lib/` (CPU) next to the server |
| Python | As required by the sample server (see repo README) |
| Port | Face **14103** · Document **14102** (default) |
| License | `license.txt` or `POST /api/activate` |

## Quick start (server)

Default API port for this product family: **`14102`**.

### 1. Clone and start

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows.git
cd ID-Document-Recognition-Liveness-Detection-Windows
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

<figure><img src="../.gitbook/assets/document-desktop-status.png" alt="Status" width="420"><figcaption>Status</figcaption></figure>

<figure><img src="../.gitbook/assets/document-desktop-fields-visual.png" alt="Visual fields" width="420"><figcaption>Visual fields</figcaption></figure>

<figure><img src="../.gitbook/assets/document-desktop-checks-validity.png" alt="Validity checks" width="420"><figcaption>Validity checks</figcaption></figure>

<figure><img src="../.gitbook/assets/document-desktop-checks-liveness.png" alt="Liveness checks" width="420"><figcaption>Liveness checks</figcaption></figure>

<figure><img src="../.gitbook/assets/document-desktop-images.png" alt="Images" width="420"><figcaption>Images</figcaption></figure>


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

Adapted from the shipping repository README for exact commands and platform-specific notes. Screenshots above use the current Identixia asset pack.

## Identixia ID Document Recognition and Liveness Detection — Windows

**On-premise ID document recognition** for Windows: passport MRZ OCR, ID card barcode, document process API, and optional document liveness / authenticity. Identity data stays on your host — ideal for KYC / eKYC backends in a VPC. CPU-only.

HTTP API on port **14102**; Gradio demo on **14202**.

---

## Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then replace the key in `license.txt` and activate.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **ID document recognition SDK** for Windows (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · MRZ · barcode · optional authenticity |
| **What you run** | HTTP API on port **14102** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Replace the key in the included `license.txt`, then send that file with `POST /api/activate`. |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | `lib\\cpu\\` from Google Drive zip `PENDING` |
| **Tools** | Windows 10/11 x64 · Python 3.10+ · CPU only |
| **Privacy** | Documents stay on your host — no Identixia cloud |
| **Primary API** | `POST /api/documentProcess` (+ recognition / liveness routes when licensed) |

---

## Initial commands

```bat
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows.git
cd ID-Document-Recognition-Liveness-Detection-Windows
:: place lib\\cpu from the runtime zip (PENDING)
pip install -r requirements.txt
run.bat
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

Keep the API running, then open a second terminal in the repository folder.

```bat
pip install -r requirements-demo.txt
run_demo.bat
```

Open http://127.0.0.1:14202

---

## What you get

| Capability | What it does |
| --- | --- |

| Endpoint focus | Notes |
| --- | --- |
| Health / license | `/api/health`, `/api/activate`, `/api/licenseStatus` |
| Process | `/api/documentProcess` (and related recognition / liveness routes) |

---

## Requirements

| | |
| --- | --- |
| OS | Windows 10/11 x64 |
| Runtime | Python 3.10+ recommended |
| Hardware | CPU only (no GPU required) |
| Ports | API **14102**, Gradio **14202** |

---

## Runtime zip

> **Google Drive (single zip):** `PENDING`

Unzip **directly** into `lib\cpu\` so DLLs and models sit at the top level (not nested):

```text
lib\cpu\DocumentReaderSDK.dll
lib\cpu\document.xdb
… (other runtime files from the zip)
```

---

## Gradio demo

Keep the API running, then open a second terminal in the repository folder.

```bat
pip install -r requirements-demo.txt
run_demo.bat
```

Open http://127.0.0.1:14202

---

## Use in your app

Call the HTTP API from your backend. See [docs](https://docs.identixia.com).

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

---
