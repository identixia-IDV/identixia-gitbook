---
description: >-
  ID document recognition and liveness for Linux and Docker. Passport, national ID, and driver license OCR, MRZ, and barcode reading run on your server. Document liveness runs when the license includes it.
---

# ID Document OCR and Liveness Detection SDK for Linux and Docker


## Overview

ID document recognition SDK for Linux and Docker. On-premise passport, ID card, and driver license OCR, MRZ, and barcode extraction. Document liveness runs when licensed.

Processing runs **on your server (or in your container)**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) |
| **Platform** | Linux |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker" %}

[`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) · [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Read printed document fields such as the name, document number, and dates using optical character recognition |
| MRZ | Read the machine-readable zone (MRZ) and validate its check digits |
| Barcode / QR | Extracted when present on the document |
| Front and back | Capture both sides when your workflow requires it |
| Document authenticity | Anti-spoof checks when the license includes `authenticity` |
| Structured JSON | Same result model on mobile and server — see Result JSON |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Host | Linux x86_64 or any Docker host |
| Docker | Optional — same repository builds the image |
| Port | Full face **14103** · recognition-only **14104** · face liveness **14105** · document **14102** · document liveness **14107** |
| Machine code | Different for bare metal vs container — license the environment you ship |

## Download and place the runtime

Download the native SDK libraries and model files before running the sample. Use `scripts/get_runtime.py` to retrieve the required GitHub Release assets and place them in the sample's expected folders.

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
https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

Default API port for this product family: **`14102`**. Gradio demo (when shipped) uses **`14202`**.

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker.git
cd ID-Document-Recognition-Liveness-Detection-Docker
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
python3 run_server.py
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

![Status](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png)

![Visual fields](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-fields-visual.png)

![Validity checks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-validity.png)

![Liveness checks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png)

![Images](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-images.png)

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker/releases/latest) |
| **Runtime helper** | `python scripts/get_runtime.py` in the product clone |
| **Documentation site** | [docs.identixia.com](https://docs.identixia.com) |
| **SDK Server (HTTP)** | [SDK Server](../sdk-server/README.md) |
| **Website** | [identixia.com](https://identixia.com) |
| **Hugging Face** | [huggingface.co/Identixia](https://huggingface.co/Identixia) |
| **Docker Hub** | [hub.docker.com/u/identixia](https://hub.docker.com/u/identixia) |
| **Playground** | [playground.identixia.com](https://playground.identixia.com/) |
| **License & support** | [Request a license](../request-a-license-and-support.md) · [Contact](../contact-us.md) |

Postman collections live under each product repository’s `postman/` folder (and the monorepo `postman/Identixia-API.postman_collection.json` for all HTTP routes).

## Next steps

1. Complete **Integration guide — start the project** until the sample shows **Ready**.
2. Confirm runtime files and databases are in place (`python scripts/get_runtime.py`).
3. Activate with a license issued for **your** application id or machine code.
4. Call only the APIs your license allows; treat missing flags as “not evaluated”, not as pass.
5. Return to the [ID Document SDK](README.md) hub for Result JSON and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use images from the identixia-assets repository.

## ID Document Recognition and Liveness Detection SDK for Linux / Docker — HTTP API Demo | Identixia

Integrate **ID document OCR and liveness detection** with the **Identixia Linux / Docker SDK**. This repository provides a self-hosted Linux / Docker HTTP API for reading passports, national ID cards, and driver licenses. Extract identity fields using optical character recognition (OCR), read the machine-readable zone (MRZ), and decode supported document barcodes. Add document liveness checks for screen replays, printed copies, and replaced photos when enabled by your license.

Use the sample to build document capture and data extraction into customer onboarding, Know Your Customer (KYC), and electronic KYC (eKYC) workflows. Processing runs on your own server; images are not sent to the Identixia cloud.

Image: [`identixia/document-reader`](https://hub.docker.com/r/identixia/document-reader).

> For setup, integration, and API guides, see the [ID Document Recognition and Liveness Detection SDK documentation for Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/linux-docker). This page covers the sample repository.

## SDK overview

Start the server and request its machine code using `GET /api/machinecode`. Send that code to [contact@identixia.com](mailto:contact@identixia.com) to request a license for this machine. Apply the returned key using the activation instructions below.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **ID document recognition** Linux / Docker API (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · MRZ · barcode · optional authenticity |
| **What you run** | HTTP API on port **14102** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Set `LICENSE=` in `.env`, or `POST /api/activate` with the key (saved into `.env`). |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | Included in the Docker image |
| **Tools** | Linux x64 · Docker (or host Python + zip) |
| **Privacy** | Identity data stays in your VPC — no Identixia cloud |
| **Primary API** | `POST /api/document/process` (+ recognition / liveness routes when licensed) |

---

## SDK installation

Run the following script to download the native SDK libraries and model files from this repository’s GitHub Releases. The script places each file in the folder used by the sample.

```bash
python scripts/get_runtime.py
```

To select a release explicitly, pass its tag with `--tag`. For example:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

---

## Quick start

```bash
docker pull identixia/document-reader:latest
docker run -d --name identixia-document-reader \
  --shm-size=2gb --privileged \
  -p 14102:14102 \
  -v /etc/machine-id:/etc/machine-id:ro \
  identixia/document-reader:latest
```
Copy `.env.example` to `.env` and edit the settings for your installation: `PORT`, `LICENSE`, `API_BASE`, and `DEMO_PORT`. Values set in the shell or in Compose’s `environment:` section take precedence over values in `.env`.

```bash
curl -s http://127.0.0.1:14102/api/machinecode
```

The JSON response contains your machine code in `data.machinecode`. This value identifies the machine for licensing.

Email the machine code and the product you want to use to [contact@identixia.com](mailto:contact@identixia.com) to request a license key.

Replace `YOUR_KEY` in the request below with the license key issued for this machine. The activation endpoint saves the key to the server’s `.env` file and attempts to initialize the SDK. For a local installation, you can also set `LICENSE=YOUR_KEY` in the repository’s `.env` file and restart the server.

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

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
python3 run_demo.py
```

Open http://127.0.0.1:14202

---

## Features

| Capability | What it does |
| --- | --- |

---

## System requirements

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
python3 run_demo.py
```

Open http://127.0.0.1:14202

## API

HTTP API on port **14102**. For image-processing requests, encode the JPEG image as base64 and include it in the JSON request body.

| Call | Route |
| --- | --- |
| Health | `GET /api/health` |
| Machine code | `GET /api/machinecode` |
| Activate | `POST /api/activate` with a JSON body containing your license key: `{"license":"YOUR_KEY"}` |
| Process | `POST /api/document/process` |

Returns identity, fields, checks, and images. Document liveness runs only when the license includes it.

```bash
curl -s http://127.0.0.1:14102/api/health
```

---

## SDKs for other platforms

| | Platform | Repo |
| --- | --- | --- |

Document liveness only (API **14107**): [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

---
