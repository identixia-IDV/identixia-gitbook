---
description: >-
  On-premise ID document liveness API for Linux and Docker. Separate from OCR. Document liveness runs when the license includes it.
---

# ID Document Liveness SDK


## Overview

On-premise ID document liveness API for Linux and Docker. Separate from OCR. Document liveness runs when the license includes it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `ID-Document-Liveness-Detection-Docker` |
| **Platform** | Linux |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker" %}

Source: [`identixia-IDV/ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

## What you can do

| Capability | Description |
| --- | --- |
| Document liveness API | Anti-spoofing against screen replay, printout, substitution |
| Separate from OCR | Does not replace ID Document Recognition |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Host | Linux x86_64 or any Docker host |
| Docker | Optional — same repository builds the image |
| Port | Face **14103** · Document **14102** · Document liveness **14106** (product-specific) |
| Machine code | Different for bare metal vs container — license the environment you ship |

## Quick start (server)

Default API port for this product family: **`14106`**.

### 1. Clone and start

```bash
git clone https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker.git
cd ID-Document-Liveness-Detection-Docker
# Follow README: place lib/ runtime, then start the HTTP server / demo UI
```

### 2. Machine code → license → activate

```bash
curl -s http://127.0.0.1:14106/api/machinecode
# Send data.machinecode to Identixia → receive license
curl -s -X POST http://127.0.0.1:14106/api/activate \
  -H "Content-Type: text/plain" \
  --data-binary @license.txt
curl -s http://127.0.0.1:14106/api/licenseStatus
curl -s http://127.0.0.1:14106/api/health
```

You can also drop `license.txt` next to the server and restart.

### Try document liveness

```bash
curl -s -X POST http://127.0.0.1:14106/api/documentLiveness \
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
4. `POST /api/activate` with the license file/bytes **or** place `license.txt` and restart.
5. `GET /api/licenseStatus` → check capability flags (`recognition`, `liveness` / `authenticity`).

Control routes return the envelope `{success, code, message, request_id, data}`. Process routes return **engine / process JSON** (not the control envelope).

## API reference — document liveness HTTP

Base URL: `http://{host}:14106` (dedicated product; Document Recognition on **14102** also exposes `/api/documentLiveness` when licensed).

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | Entitlement |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/documentLiveness` | `{ "images": ["<b64>", ...] }` |

This product is **PAD / authenticity**, not OCR. Pair with ID Document Recognition when you need fields.

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

## Identixia ID Document Liveness — Linux / Docker

**On-premise document liveness / authenticity** API for KYC and eKYC: detect screen replay, print attacks, and photo-swap style presentation attacks on ID documents. Complements full OCR recognition — this image focuses on **document PAD** so you can reject spoofed IDs before (or after) MRZ / barcode extraction.

Image: [`identixia/document-liveness`](https://hub.docker.com/r/identixia/document-liveness).

---

## Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then replace the key in `license.txt` and activate.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **document liveness / authenticity** API (KYC / eKYC) |
| **Documents** | ID document presentation-attack detection (screen / print / photo-swap) |
| **What you run** | HTTP API on port **14107** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Replace the key in the included `license.txt`, then send that file with `POST /api/activate`. |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | Included in the Docker image |
| **Tools** | Linux x64 with Docker |
| **Privacy** | Authenticity checks stay in your VPC — no Identixia cloud |

---

## Initial commands

```bash
docker pull identixia/document-liveness:latest
docker run -d --name identixia-api -p 14107:14107 \
  -v /etc/machine-id:/etc/machine-id:ro \
  identixia/document-liveness:latest
```

```bash
curl -s http://127.0.0.1:14107/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

This repository includes `license.txt`. Replace the key in that file with the license we send you, then run this command from the repository folder:

```bash
curl -s -X POST http://127.0.0.1:14107/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
```

```bash
curl -s http://127.0.0.1:14107/api/health
```

Replace `BASE64_JPEG` with a base64-encoded JPEG of the document.

```bash
curl -s -X POST http://127.0.0.1:14107/api/documentLiveness -H "Content-Type: application/json" -d "{\"images\":[{\"image\":\"BASE64_JPEG\"}]}"
```

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
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
./run_demo.sh
```

Open http://127.0.0.1:14207

---

## Use in your app

POST document images to the liveness routes on **14107**. For full on-premise ID document recognition (passport MRZ OCR, ID card barcode, fields), use the recognition product on **14102**.

---

## Related

Full OCR product: [ID-Document-Recognition-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) · Hub: [ID-Document-Recognition-Liveness-Detection-SDK](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK)

---
