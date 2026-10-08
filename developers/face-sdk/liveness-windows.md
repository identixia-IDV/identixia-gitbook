---
description: >-
  Integrate Identixia face liveness detection on Windows. Follow setup and license activation steps for passive anti-spoofing and deepfake checks.
icon: shield-halved
---

# Face Liveness Detection SDK for Windows


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
| Passive face liveness + deepfake | Check a color face image for presentation attacks and deepfakes; report REAL only when both checks pass |
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
| **Local path after download** | `lib/cpu/` (`FaceLivenessSDK.dll` on Windows, or the `.so` files on Linux, **and** every required `*.xdb` at the top level) |
| **Databases** | Face recognition needs the full `recognition*.xdb` set; face liveness needs `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb`; document products need `document.xdb`. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceLivenessDetection-Windows/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

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

![Mobile liveness result](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/mobile/liveness.png)

![Desktop liveness demo](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/desktop/demo-ui.png)

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

## Face Liveness Detection SDK for Windows — HTTP API Demo | Identixia

Integrate **face liveness detection and anti-spoofing** with the **Identixia Windows SDK**. This repository provides a self-hosted Windows HTTP API for passive face liveness detection and deepfake detection. Use presentation attack detection (PAD) to check for face spoofing and deepfake detection to check for manipulated face images. The combined authenticity result is REAL only when both checks pass. Face recognition and matching are not included.

Use the sample to add selfie liveness checks to remote onboarding and biometric identity verification alongside a separate face matching service. Processing runs on your own server; images are not sent to the Identixia cloud.

> For setup, integration, and API guides, see the [Face Liveness Detection SDK documentation for Windows](https://docs.identixia.com/developers/face-sdk/liveness-windows). This page covers the sample repository.

## SDK overview

Start the server and request its machine code using `GET /api/machinecode`. Send that code to [contact@identixia.com](mailto:contact@identixia.com) to request a license for this machine. Apply the returned key using the activation instructions below.

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

## SDK installation

Run the following script to download the native SDK libraries and model files from this repository’s GitHub Releases. The script places each file in the folder used by the sample.

```bash
python scripts/get_runtime.py
```

To select a release explicitly, pass its tag with `--tag`. For example:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

Unzip **directly** into `lib\cpu\` so DLLs and `*.xdb` packs sit at the top level (not nested).

---

## Quick start

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Windows.git
cd FaceLivenessDetection-Windows
python scripts/get_runtime.py
pip install -r requirements.txt
python run_server.py
```

Copy `.env.example` to `.env` and edit the settings for your installation: `PORT`, `LICENSE`, `API_BASE`, and `DEMO_PORT`. Environment variables already set in the shell take precedence over values in `.env`.

```bash
curl -s http://127.0.0.1:14105/api/machinecode
```

The JSON response contains your machine code in `data.machinecode`. This value identifies the machine for licensing.

Email the machine code and the product you want to use to [contact@identixia.com](mailto:contact@identixia.com) to request a license key.

Replace `YOUR_KEY` in the request below with the license key issued for this machine. The activation endpoint saves the key to the server’s `.env` file and attempts to initialize the SDK. For a local installation, you can also set `LICENSE=YOUR_KEY` in the repository’s `.env` file and restart the server.

```bash
curl -s -X POST http://127.0.0.1:14105/api/activate -H "Content-Type: application/json" -d "{\"license\":\"YOUR_KEY\"}"
```

```bash
curl -s http://127.0.0.1:14105/api/health
```

Liveness calls:

- `POST /api/face/liveness` — Combined authenticity result from presentation attack detection and deepfake checks
- `POST /api/face/deepfake` — deepfake-only check

`recognition-common.xdb` stays because the detector is shared. The matcher pack is not included.

---

## Features

| Capability | What it does |
| --- | --- |
| **Passive liveness** | Run presentation attack detection when licensed |
| **Deepfake** | Check for manipulated face images; report REAL only when both liveness and deepfake checks pass |
| **HTTP API** | Local on-premise service on port 14105 |

---

## System requirements

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

HTTP API on port **14105**. For image-processing requests, encode the JPEG image as base64 and include it in the JSON request body. Control routes return `{success, code, message, request_id, data}`.

| Call | Route |
| --- | --- |
| Health | `GET /api/health` |
| Machine code | `GET /api/machinecode` |
| Activate | `POST /api/activate` with a JSON body containing your license key: `{"license":"YOUR_KEY"}` |
| License status | `GET /api/licenseStatus` |
| Liveness | `POST /api/face/liveness` — REAL only if PAD and deepfake both pass |
| Recognition / 1:N | Not in this build. Use a Face Recognition repository. |

```bash
curl -s http://127.0.0.1:14105/api/health
```

---

## SDKs for other platforms

| | Platform | Repo |
| --- | --- | --- |

---

{% include "../.gitbook/includes/footer.md" %}
