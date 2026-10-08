---
description: >-
  ID document liveness API for Linux and Docker. On-premise presentation-attack checks for passports and ID cards, separate from OCR. Runs when the license includes it.
icon: shield-halved
---

# Document liveness — Linux / Docker


## Overview

ID document liveness API for Linux and Docker. On-premise presentation-attack checks for passports and ID cards, separate from OCR. Runs when the license includes it.

Processing runs **on your server (or in your container)**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) |
| **Platform** | Linux |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker" %}

[`identixia-IDV/ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) · [Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Document authenticity API | Checks against screen replay, printout, and substitution |
| Separate from OCR | Complements ID Document Recognition; does not replace it |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Host | Linux x86_64 or any Docker host |
| Docker | Optional — same repository builds the image |
| Port | Full face **14103** · recognition-only **14104** · face liveness **14105** · document **14102** · document liveness **14107** |
| Machine code | Different for bare metal vs container — license the environment you ship |

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
| **Local path after download** | `lib/cpu/` (`DocumentLivenessSDK.dll` on Windows, or the `.so` files on Linux, **and** every required `*.xdb` at the top level) |
| **Databases** | Face recognition needs the full `recognition*.xdb` set; face liveness needs `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb`; document products need `document.xdb`. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker/releases/latest/download/<asset>
```

Unzip so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

Default API port for this product family: **`14107`**. Gradio demo (when shipped) uses **`14207`**.

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker.git
cd ID-Document-Liveness-Detection-Docker
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
curl -s http://127.0.0.1:14107/api/machinecode
```

Send `data.machinecode` to Identixia and receive a license. Then either set `LICENSE=` in `.env` and restart, or:

```bash
curl -s -X POST http://127.0.0.1:14107/api/activate \
  -H "Content-Type: application/json" \
  -d '{\"license\":\"YOUR_KEY\"}'
curl -s http://127.0.0.1:14107/api/licenseStatus
curl -s http://127.0.0.1:14107/api/health
```

Prefer `.env` (`LICENSE=`) for the key — do not use a separate `license.txt`.

### Try document liveness

```bash
curl -s -X POST http://127.0.0.1:14107/api/document/liveness \
  -H "Content-Type: application/json" \
  -d "{\"images\":[\"BASE64_JPEG\"]}"
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

## API reference — document liveness HTTP

Base URL: `http://{host}:14107` (dedicated product; Document Recognition on **14102** also exposes `/api/document/liveness` when licensed).

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | Entitlement |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/document/liveness` | `{ "images": ["<b64>", ...] }` |

This product is **PAD / authenticity**, not OCR. Pair with ID Document Recognition when you need fields.

**Postman:** import `postman/DocumentLiveness-API.postman_collection.json` from the product repo.

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

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png" alt="Liveness checks" width="420"><figcaption>Liveness checks</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png" alt="Status card" width="420"><figcaption>Status card</figcaption></figure>

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker/releases/latest) |
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

## Identixia ID Document Liveness — Linux / Docker

**On-premise document liveness / authenticity** API for KYC and eKYC: detect screen replay, print attacks, and photo-swap style presentation attacks on ID documents. Complements full OCR recognition — this image focuses on **document PAD** so you can reject spoofed IDs before (or after) MRZ / barcode extraction.

Image: [`identixia/document-liveness`](https://hub.docker.com/r/identixia/document-liveness).

> For setup, integration, and API guides, see the [Identixia documentation](https://docs.identixia.com/developers/id-document-sdk/liveness-linux-docker). This page covers the sample repository.

## Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then set `LICENSE=` in `.env` and activate (or POST `/api/activate`).

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **document liveness / authenticity** API (KYC / eKYC) |
| **Documents** | ID document presentation-attack detection (screen / print / photo-swap) |
| **What you run** | HTTP API on port **14107** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Set `LICENSE=` in `.env`, or `POST /api/activate` with the key (saved into `.env`). |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | Included in the Docker image |
| **Tools** | Linux x64 with Docker |
| **Privacy** | Authenticity checks stay in your VPC — no Identixia cloud |

---

## Install

Download the native engine files from this repository’s GitHub Release. The helper script places libraries and database packs in the correct folders.

```bash
python scripts/get_runtime.py
```

To download a specific Release tag instead of the latest build:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

---

## Initial commands

```bash
docker pull identixia/document-liveness:latest
docker run -d --name identixia-document-liveness \
  --shm-size=2gb --privileged \
  -p 14107:14107 \
  -v /etc/machine-id:/etc/machine-id:ro \
  identixia/document-liveness:latest
```
Configuration lives in **`.env`** (see `.env.example`): `PORT`, `LICENSE`, `API_BASE`, `DEMO_PORT`. Copy `.env.example` → `.env` and edit. Shell / Compose `environment:` values still win over `.env`.

```bash
curl -s http://127.0.0.1:14107/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

Set `LICENSE=` in `.env` to the key we send you (or POST it below — activate writes `.env`). From the repository folder:

```bash
curl -s -X POST http://127.0.0.1:14107/api/activate -H "Content-Type: application/json" -d "{\"license\":\"YOUR_KEY\"}"
```

```bash
curl -s http://127.0.0.1:14107/api/health
```

Replace `BASE64_JPEG` with a base64-encoded JPEG of the document.

```bash
curl -s -X POST http://127.0.0.1:14107/api/document/liveness -H "Content-Type: application/json" -d "{\"images\":[{\"image\":\"BASE64_FRONT\",\"page_idx\":0},{\"image\":\"BASE64_BACK\",\"page_idx\":1}]}"
```

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
python3 run_demo.py
```

Open http://127.0.0.1:14207

---

## What you get

| Capability | Notes |
| --- | --- |
| Document liveness / authenticity | Presentation-attack signals for ID images |
| KYC / eKYC gate | Reject spoofed documents before trusting OCR fields |
| HTTP API | Default port **14107** |
| Gradio demo | Port **14207** |
| Postman | `postman/DocumentLiveness-API.postman_collection.json` |

---

## Requirements

| | |
| --- | --- |
| Host | Linux x64 with Docker |
| Ports | API **14107**, Gradio **14207** |
| Licensing | Bind-mount `/etc/machine-id` for stable machine codes |

---

## Gradio demo

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
python3 run_demo.py
```

Open http://127.0.0.1:14207

## Related

Full OCR product: [ID-Document-Recognition-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) · Hub: [ID-Document-Recognition-Liveness-Detection-SDK](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK)

## API

HTTP API on port **14107**. Send a JPEG as base64 JSON.

| Call | Route |
| --- | --- |
| Health | `GET /api/health` |
| Machine code | `GET /api/machinecode` |
| Activate | `POST /api/activate` with your `license.txt` |
| Process | `POST /api/document/liveness` |

Send the document image. This build does not extract MRZ or barcodes.

```bash
curl -s http://127.0.0.1:14107/api/health
```

---

{% include "../.gitbook/includes/footer.md" %}
