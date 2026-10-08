---
description: >-
  Passive face liveness SDK for Windows. On-premise REST API runs presentation-attack and deepfake checks together for KYC. A face is REAL only when both pass.
icon: shield-halved
---

# Face liveness — Windows


## Overview

Passive face liveness SDK for Windows. On-premise REST API runs presentation-attack and deepfake checks together for KYC. A face is REAL only when both pass.

Processing runs **on your server (or in your container)**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) |
| **Platform** | Windows |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/FaceLivenessDetection-Windows" %}

[`identixia-IDV/FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) · [Releases](https://github.com/identixia-IDV/FaceLivenessDetection-Windows/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Passive face liveness + deepfake | Score one RGB face for PAD and deepfake; REAL only when both engines say real |
| License gating | Liveness / deepfake run only when the license includes `liveness` |

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
| **Local path after download** | `lib/cpu/` (`FaceLivenessSDK.dll` on Windows, or the `.so` files on Linux, **and** every required `*.xdb` at the top level) |
| **Databases** | Face recognition needs the full `recognition*.xdb` set; face liveness needs `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb`; document products need `document.xdb`. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceLivenessDetection-Windows/releases/latest/download/<asset>
```

Unzip so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

Default API port for this product family: **`14105`**. Gradio demo (when shipped) uses **`14205`**.

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Windows.git
cd FaceLivenessDetection-Windows
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
curl -s http://127.0.0.1:14105/api/machinecode
```

Send `data.machinecode` to Identixia and receive a license. Then either set `LICENSE=` in `.env` and restart, or:

```bash
curl -s -X POST http://127.0.0.1:14105/api/activate \
  -H "Content-Type: application/json" \
  -d '{\"license\":\"YOUR_KEY\"}'
curl -s http://127.0.0.1:14105/api/licenseStatus
curl -s http://127.0.0.1:14105/api/health
```

Prefer `.env` (`LICENSE=`) for the key — do not use a separate `license.txt`.

### Try liveness

```bash
curl -s -X POST http://127.0.0.1:14105/api/face/liveness \
  -H "Content-Type: application/json" \
  -d "{\"image\":\"BASE64_JPEG\"}"
```


## License and activation (server)

1. Start the API (it stays up even without a key so you can read the machine code).
2. `GET /api/machinecode` → copy `data.machinecode`.
3. Contact Identixia with that code (Docker and bare metal codes differ).
4. `POST /api/activate` with the key **or** set `LICENSE=` in `.env` and restart.
5. `GET /api/licenseStatus` → check capability flags (`recognition`, `liveness` / `authenticity`).

Control routes return the envelope `{success, code, message, request_id, data}`. Process routes return **engine / process JSON** (not the control envelope).

## API reference — face liveness HTTP

Base URL: `http://{host}:14105`

Liveness-only products expose `/api/face/liveness` and `/api/face/deepfake` (same paths as the full Face stack). There is **no** `/api/liveness` / `/api/check_liveness` alias on this release.

`POST /api/face/liveness` runs **PAD + deepfake** (`FaceSDK_liveness_all`). Demo UIs treat authenticity as **REAL** only when both traits say real. Use `/api/face/deepfake` for a deepfake-only score.

| Method | Path | Body | Description |
| --- | --- | --- | --- |
| `GET` | `/api/health` | — | Health |
| `GET` | `/api/machinecode` | — | License machine code |
| `GET` | `/api/licenseStatus` | — | Liveness entitlement |
| `POST` | `/api/activate` | license bytes / JSON | Activate |
| `POST` | `/api/face/liveness` | `{ "image": "<b64>" }` | PAD + deepfake (combined authenticity) |
| `POST` | `/api/face/deepfake` | `{ "image": "<b64>" }` | Deepfake-only score when enabled |

```bash
curl -s -X POST http://127.0.0.1:14105/api/face/liveness \
  -H "Content-Type: application/json" \
  -d '{"image":"BASE64_JPEG"}'
```

**Postman:** import `postman/FaceLiveness-API.postman_collection.json` from the product repo.

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

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/mobile/liveness.png" alt="Mobile liveness result" width="220"><figcaption>Mobile liveness result</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/desktop/demo-ui.png" alt="Desktop liveness demo" width="480"><figcaption>Desktop liveness demo</figcaption></figure>

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/FaceLivenessDetection-Windows/releases/latest) |
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
5. Return to the [Face SDK](https://docs.identixia.com/face-sdk) hub for recognition, liveness, and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use images from the identixia-assets repository.

## Identixia Face Liveness — Windows

On-premise **passive face liveness** for Windows. `POST /api/face/liveness` runs **PAD + deepfake** when licensed; authenticity is **REAL** only if both say real. This app ships the liveness model packs only. Matching and 1:N search are a separate app, `FaceRecognition-Windows`.

> For setup, integration, and API guides, see the [Identixia documentation](https://docs.identixia.com/developers/face-sdk/liveness-windows). This page covers the sample repository.

## Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then set `LICENSE=` in `.env` and activate (or POST `/api/activate`).

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **face liveness** for Windows |
| **What you run** | HTTP API on port **14105** |
| **Gradio demo** | Port **14205** |
| **Runtime** | `lib\cpu\` — about **316 MB** via `python scripts/get_runtime.py` |
| **Models included** | `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb` |
| **Models left out** | `recognition.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb` (matcher packs stay in the recognition app) |
| **Privacy** | Biometrics stay on your host — no Identixia cloud |

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

Unzip **directly** into `lib\cpu\` so DLLs and `*.xdb` packs sit at the top level (not nested).

---

## Initial commands

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Windows.git
cd FaceLivenessDetection-Windows
python scripts/get_runtime.py
pip install -r requirements.txt
python run_server.py
```

Configuration lives in **`.env`** (see `.env.example`): `PORT`, `LICENSE`, `API_BASE`, `DEMO_PORT`. Copy `.env.example` → `.env` and edit. Shell variables already set still win over `.env`.

```bash
curl -s http://127.0.0.1:14105/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

Set `LICENSE=` in `.env` to the key we send you (or POST it below — activate writes `.env`):

```bash
curl -s -X POST http://127.0.0.1:14105/api/activate -H "Content-Type: application/json" -d "{\"license\":\"YOUR_KEY\"}"
```

```bash
curl -s http://127.0.0.1:14105/api/health
```

Liveness calls:

- `POST /api/face/liveness` — PAD + deepfake combined authenticity
- `POST /api/face/deepfake` — deepfake-only check

`recognition-common.xdb` stays because the detector is shared. The matcher pack is not included.

---

## What you get

| Capability | What it does |
| --- | --- |
| **Passive liveness** | PAD check when licensed |
| **Deepfake** | Deepfake check; authenticity REAL only if PAD + deepfake both pass |
| **HTTP API** | Local on-premise service on port 14105 |

---

## Requirements

| | |
| --- | --- |
| API port | **14105** |
| Gradio demo port | **14205** |
| Runtime download | `python scripts/get_runtime.py` |

---

## Gradio demo

Keep the API running, then open a second terminal in the repository folder.

```bash
pip install -r requirements-demo.txt
python run_demo.py
```

Open http://127.0.0.1:14205

## API

HTTP API on port **14105**. Send a JPEG as base64 JSON. Control routes return `{success, code, message, request_id, data}`.

| Call | Route |
| --- | --- |
| Health | `GET /api/health` |
| Machine code | `GET /api/machinecode` |
| Activate | `POST /api/activate` with your `license.txt` |
| License status | `GET /api/licenseStatus` |
| Liveness | `POST /api/face/liveness` — REAL only if PAD and deepfake both pass |
| Recognition / 1:N | Not in this build. Use a Face Recognition repository. |

```bash
curl -s http://127.0.0.1:14105/api/health
```

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

---

{% include "../.gitbook/includes/footer.md" %}
