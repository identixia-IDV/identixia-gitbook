---
description: >-
  ID document liveness for Windows. Presentation-attack checks for passports and ID cards run on your server, separate from OCR.
---

# ID Document Liveness Detection SDK for Windows

## Overview

| | |
| --- | --- |
| **Repository** | [`ID-Document-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows) · [Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows/releases/latest) |
| **Platform** | Windows |
| **Runs** | On your server or in your container. Images stay there. |

## Capabilities

| Capability | Description |
| --- | --- |
| Document authenticity API | Checks against screen replay, printout, and substitution |
| Separate from OCR | Complements ID Document Recognition; does not replace it |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| OS | Windows 10/11 x64 |
| Runtime | Product `lib/` (CPU) next to the server |
| Python | As required by the sample server (see repo README) |
| Port | Full face **14103** · recognition-only **14104** · face liveness **14105** · document **14102** · document liveness **14107** |
| License | `.env` `LICENSE=` or `POST /api/activate` |

## Download and place the runtime

Download the runtime zip from GitHub Releases and unzip it into the folder listed for that platform.

| | |
| --- | --- |
| **Release asset** | GitHub Release `*-windows.zip` / `*-linux.zip` |
| **Local path after download** | `lib/cpu/` (`DocumentLivenessSDK.dll` on Windows, or the `.so` files on Linux, **and** every required `*.xdb` at the top level) |
| **Databases** | Face recognition needs the full `recognition*.xdb` set; face liveness needs `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb`; document products need `document.xdb`. |

### Download

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

## Integration guide — start the project

Default API port for this product family: **`14107`**. Gradio demo (when shipped) uses **`14207`**.

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows.git
cd ID-Document-Liveness-Detection-Windows
```

### 2. Download and place the runtime

Native libraries and `*.xdb` databases are not in git. From the repository root:

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

![Liveness checks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png)

![Status card](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png)

## Support

{% include "../.gitbook/includes/contact.md" %}
