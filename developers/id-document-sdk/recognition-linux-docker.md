---
description: >-
  ID document recognition for Linux and Docker. Passport, national ID, and driver license OCR, MRZ, and barcode reading run on your server. This build does not include document liveness.
icon: cube
---

# ID Document Recognition and OCR SDK for Linux and Docker


## Overview

| | |
| --- | --- |
| **Repository** | [`ID-Document-Recognition-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Docker) · [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Docker/releases/latest) |
| **Platform** | Linux |
| **Runs** | On your server or in your container. Images stay there. |

## Capabilities

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Read printed document fields such as the name, document number, and dates using optical character recognition |
| MRZ | Read the machine-readable zone (MRZ) and validate its check digits |
| Barcode / QR | Extracted when present on the document |
| Front and back | Capture both sides when your workflow requires it |
| Structured JSON | Same result model on mobile and server — see Result JSON |

This sample does not include document liveness. It does not serve `/api/document/liveness` and it does not call `documentLiveness`.

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Host | Linux x86_64 or any Docker host |
| Docker | Optional — same repository builds the image |
| Port | Full face **14103** · recognition-only **14104** · face liveness **14105** · document **14102** · document liveness **14107** |
| Machine code | Different for bare metal vs container — license the environment you ship |

## Download and place the runtime

Native engines and model databases are **not** stored in git. Download the runtime zip from [GitHub Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Docker/releases/latest) and unzip it into the path below.

| | |
| --- | --- |
| **Release asset** | GitHub Release `*-windows.zip` / `*-linux.zip` |
| **Local path** | `lib/cpu/` (`DocumentRecognitionSDK.dll` on Windows, or the `.so` files on Linux, **and** every required `*.xdb` at the top level) |
| **Databases** | Face recognition needs the full `recognition*.xdb` set; face liveness needs `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb`; document products need `document.xdb`. |

```text
https://github.com/identixia-IDV/ID-Document-Recognition-Docker/releases/latest
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. An unavailable check is not a pass.
{% endhint %}

## Integration guide — start the project

Default API port for this product family: **`14106`**. Gradio demo (when shipped) uses **`14206`**.

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Docker.git
cd ID-Document-Recognition-Docker
```

### 2. Download and place the runtime

Native libraries and `*.xdb` databases are not in git. Download the runtime zip from [GitHub Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Docker/releases/latest) and unzip it into `lib/cpu/`. DLLs or `.so` files and every required database pack sit in that folder, not inside an extra directory. See [Download and place the runtime](#download-and-place-the-runtime).

### 3. Configure and start the server

```bash
cp -n .env.example .env   # Windows: copy .env.example .env
pip install -r requirements.txt
python3 run_server.py
```

Configuration lives in **`.env`**: `PORT`, `LICENSE`, `API_BASE`, `DEMO_PORT`. Shell / Compose environment variables still win over `.env`.

### 4. Machine code → license → activate

```bash
curl -s http://127.0.0.1:14106/api/machinecode
```

Send `data.machinecode` to Identixia and receive a license. Then either set `LICENSE=` in `.env` and restart, or:

```bash
curl -s -X POST http://127.0.0.1:14106/api/activate \
  -H "Content-Type: application/json" \
  -d '{\"license\":\"YOUR_KEY\"}'
curl -s http://127.0.0.1:14106/api/licenseStatus
curl -s http://127.0.0.1:14106/api/health
```

Prefer `.env` (`LICENSE=`) for the key — do not use a separate `license.txt`.

### Try document process

```bash
curl -s -X POST http://127.0.0.1:14106/api/document/recognition \
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

## API reference — document recognition HTTP

Base URL: `http://{host}:14106`

This build does not serve `/api/document/liveness`.

### Control routes

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/backend` | Backend info |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | `recognition` flag |
| `POST` | `/api/activate` | Activate license |

### Process routes

| Method | Path | Body | Description |
| --- | --- | --- | --- |
| `POST` | `/api/document/process` | `{ "images":[…] }` | OCR, MRZ, and barcode |
| `POST` | `/api/document/recognition` | `{ "images":[…] }` | OCR / MRZ / barcode |

```bash
curl -s -X POST http://127.0.0.1:14106/api/document/recognition \
  -H "Content-Type: application/json" \
  -d "{\"images\":[{\"image\":\"BASE64_FRONT\",\"page_idx\":0}]}"
```

Response shape: [Result JSON](https://docs.identixia.com/id-document-sdk/result-json).

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


## Support

{% include "../.gitbook/includes/contact.md" %}

{% include "../.gitbook/includes/footer.md" %}
