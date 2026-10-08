---
description: >-
  ID document recognition SDK for Windows. On-premise passport, ID card, and driver license OCR, MRZ, and barcode extraction. Document liveness routes run when licensed.
icon: desktop
---

# ID Document SDK — Windows (recognition + liveness)


## Overview

ID document recognition SDK for Windows. On-premise passport, ID card, and driver license OCR, MRZ, and barcode extraction. Document liveness routes run when licensed.

Processing runs **on your server (or in your container)**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) |
| **Platform** | Windows |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows" %}

[`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) · [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Visual-zone fields (name, document number, dates, and related data) |
| MRZ | Machine-readable zone parse and checksum checks |
| Barcode / QR | Extracted when present on the document |
| Front and back | Capture both sides when your workflow requires it |
| Document authenticity | Anti-spoof checks when the license includes `authenticity` |
| Structured JSON | Same result model on mobile and server — see Result JSON |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| OS | Windows 10/11 x64 |
| Runtime | Product `lib/` (CPU) next to the server |
| Python | As required by the sample server (see repo README) |
| Port | Full face **14103** · recognition-only **14104** · face liveness **14105** · document **14102** · document liveness **14107** |
| License | `.env` `LICENSE=` or `POST /api/activate` |

## Download and place the runtime

Native engines and model databases are **not** stored in git. Every product ships `scripts/get_runtime.py`, which downloads the correct GitHub Release assets and places them where the sample expects.

### Download (recommended)

```bash
python scripts/get_runtime.py
```

To pin a specific Release tag:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

| | |
| --- | --- |
| **Release asset** | GitHub Release `*-windows.zip` / `*-linux.zip` |
| **Local path after download** | `lib/cpu/` (`DocumentFullSDK.dll` on Windows, or the `.so` files on Linux, **and** every required `*.xdb` at the top level) |
| **Databases** | Face recognition needs the full `recognition*.xdb` set; face liveness needs `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb`; document products need `document.xdb`. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows/releases/latest/download/<asset>
```

Unzip so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

Default API port for this product family: **`14102`**. Gradio demo (when shipped) uses **`14202`**.

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows.git
cd ID-Document-Recognition-Liveness-Detection-Windows
```

### 2. Download and place the runtime

Native libraries and `*.xdb` databases are not in git. From the repository root:

```bash
python scripts/get_runtime.py
```

Files must land under `lib/cpu/` (DLLs or `.so` files **and** every required database pack). See [Download and place the runtime](#download-and-place-the-runtime).

### 3. Configure and start the server

```bash
cp -n .env.example .env   # Windows: copy .env.example .env
pip install -r requirements.txt
python run_server.py
```

Configuration lives in **`.env`**: `PORT`, `LICENSE`, `API_BASE`, `DEMO_PORT`. Shell / Compose environment variables still win over `.env`.

### 4. Machine code → license → activate

```bash
curl -s http://127.0.0.1:14102/api/machinecode
```

Send `data.machinecode` to Identixia and receive a license. Then either set `LICENSE=` in `.env` and restart, or:

```bash
curl -s -X POST http://127.0.0.1:14102/api/activate \
  -H "Content-Type: application/json" \
  -d '{\"license\":\"YOUR_KEY\"}'
curl -s http://127.0.0.1:14102/api/licenseStatus
curl -s http://127.0.0.1:14102/api/health
```

Prefer `.env` (`LICENSE=`) for the key — do not use a separate `license.txt`.

### Try document process

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/process \
  -H "Content-Type: application/json" \
  -d "{\"images\":[{\"image\":\"BASE64_JPEG\"}]}"
```


## License and activation (server)

1. Start the API (it stays up even without a key so you can read the machine code).
2. `GET /api/machinecode` → copy `data.machinecode`.
3. Contact Identixia with that code (Docker and bare metal codes differ).
4. `POST /api/activate` with the key **or** set `LICENSE=` in `.env` and restart.
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
| `POST` | `/api/document/process` | `{ "images":[…], "rfid"?, "response"? }` | Full process (OCR + optional authenticity) |
| `POST` | `/api/document/recognition` | `{ "images":[…] }` | Recognition only |
| `POST` | `/api/document/liveness` | `{ "images":[…] }` | Authenticity / liveness only |
| `POST` | `/api/document/general` | `{ "image", "options"? }` | General process helper |

`images` entries are objects with base64 `image` (and optional metadata) or raw base64 strings depending on binding — see the sample Postman collection in the repo `postman/` folder.

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/process \
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

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png" alt="Status" width="420"><figcaption>Status</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-fields-visual.png" alt="Visual fields" width="420"><figcaption>Visual fields</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-validity.png" alt="Validity checks" width="420"><figcaption>Validity checks</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png" alt="Liveness checks" width="420"><figcaption>Liveness checks</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-images.png" alt="Images" width="420"><figcaption>Images</figcaption></figure>

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows/releases/latest) |
| **Runtime helper** | `python scripts/get_runtime.py` in the product clone |
| **Documentation site** | [docs.identixia.com](https://docs.identixia.com) |
| **SDK Server (HTTP)** | [SDK Server](https://docs.identixia.com/sdk-server) |
| **Website** | [identixia.com](https://identixia.com) |
| **Hugging Face** | [huggingface.co/Identixia](https://huggingface.co/Identixia) |
| **Docker Hub** | [hub.docker.com/u/identixia](https://hub.docker.com/u/identixia) |
| **Playground** | [playground.identixia.com](https://playground.identixia.com/) |
| **License & support** | [Request a license](https://docs.identixia.com/guides/request-a-license-and-support) · [Contact](https://docs.identixia.com/guides/contact-us) |

Postman collections live under each product repository’s `postman/` folder (and the monorepo `postman/Identixia-API.postman_collection.json` for all HTTP routes).

## Next steps

1. Complete **Integration guide — start the project** until the sample shows **Ready**.
2. Confirm runtime files and databases are in place (`python scripts/get_runtime.py`).
3. Activate with a license issued for **your** application id or machine code.
4. Call only the APIs your license allows; treat missing flags as “not evaluated”, not as pass.
5. Return to the [ID Document SDK](https://docs.identixia.com/id-document-sdk) hub for Result JSON and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use images from the identixia-assets repository.

## Identixia ID Document Recognition and Liveness Detection — Windows

**On-premise ID document recognition** for Windows: passport MRZ OCR, ID card barcode, document process API, and optional document liveness / authenticity. Identity data stays on your host — ideal for KYC / eKYC backends in a VPC. CPU-only.

HTTP API on port **14102**; Gradio demo on **14202**.

> For setup, integration, and API guides, see the [Identixia documentation](https://docs.identixia.com/developers/id-document-sdk/windows). This page covers the sample repository.

## Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then set `LICENSE=` in `.env` and activate (or POST `/api/activate`).

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **ID document recognition SDK** for Windows (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · MRZ · barcode · optional authenticity |
| **What you run** | HTTP API on port **14102** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Set `LICENSE=` in `.env`, or `POST /api/activate` with the key (saved into `.env`). |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | `lib\\cpu\\` via `python scripts/get_runtime.py` (GitHub Release) |
| **Tools** | Windows 10/11 x64 · Python 3.10+ · CPU only |
| **Privacy** | Documents stay on your host — no Identixia cloud |
| **Primary API** | `POST /api/document/process` (+ recognition / liveness routes when licensed) |

---

## Install

> **GitHub Release:** `python scripts/get_runtime.py` (or `--tag 1.0.0`)

Unzip **directly** into `lib\cpu\` so DLLs and models sit at the top level (not nested):

```text
lib\cpu\DocumentFullSDK.dll
lib\cpu\document.xdb
… (other runtime files from the zip)
```

---

## Initial commands

```bat
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows.git
cd ID-Document-Recognition-Liveness-Detection-Windows
python scripts/get_runtime.py
pip install -r requirements.txt
python run_server.py
```
Configuration lives in **`.env`** (see `.env.example`): `PORT`, `LICENSE`, `API_BASE`, `DEMO_PORT`. Copy `.env.example` → `.env` and edit. Shell variables already set still win over `.env`.

```bash
curl -s http://127.0.0.1:14102/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

Set `LICENSE=` in `.env` to the key we send you (or POST it below — activate writes `.env`). From the repository folder:

```bash
curl -s -X POST http://127.0.0.1:14102/api/activate -H "Content-Type: application/json" -d "{\"license\":\"YOUR_KEY\"}"
```

```bash
curl -s http://127.0.0.1:14102/api/health
```

Replace `BASE64_JPEG` with a base64-encoded JPEG of the document.

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/process -H "Content-Type: application/json" -d "{\"images\":[{\"image\":\"BASE64_JPEG\"}]}"
```

Keep the API running, then open a second terminal in the repository folder.

```bat
pip install -r requirements-demo.txt
python run_demo.py
```

Open http://127.0.0.1:14202

---

## What you get

| Capability | What it does |
| --- | --- |

| Endpoint focus | Notes |
| --- | --- |
| Health / license | `/api/health`, `/api/activate`, `/api/licenseStatus` |
| Process | `/api/document/process` (and related recognition / liveness routes) |

---

## Requirements

| | |
| --- | --- |
| OS | Windows 10/11 x64 |
| Runtime | Python 3.10+ recommended |
| Hardware | CPU only (no GPU required) |
| Ports | API **14102**, Gradio **14202** |

---

## Gradio demo

Keep the API running, then open a second terminal in the repository folder.

```bat
pip install -r requirements-demo.txt
python run_demo.py
```

Open http://127.0.0.1:14202

## API

HTTP API on port **14102**. Send a JPEG as base64 JSON.

| Call | Route |
| --- | --- |
| Health | `GET /api/health` |
| Machine code | `GET /api/machinecode` |
| Activate | `POST /api/activate` with your `license.txt` |
| Process | `POST /api/document/process` |

Returns identity, fields, checks, and images. Document liveness runs only when the license includes it.

```bash
curl -s http://127.0.0.1:14102/api/health
```

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

---

{% include "../.gitbook/includes/footer.md" %}
