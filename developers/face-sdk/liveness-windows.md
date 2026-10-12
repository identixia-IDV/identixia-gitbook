---
description: >-
  Passive face liveness for Windows. Presentation-attack and deepfake checks run on your server. A face is REAL only when both pass.
icon: shield
---

# Face Liveness Detection SDK for Windows


## Overview

| | |
| --- | --- |
| **Repository** | [`FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) · [Releases](https://github.com/identixia-IDV/FaceLivenessDetection-Windows/releases/latest) |
| **Platform** | Windows |
| **Runs** | On your server or in your container. Images stay there. |

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

Native engines and model databases are **not** stored in git. Download the runtime zip from [GitHub Releases](https://github.com/identixia-IDV/FaceLivenessDetection-Windows/releases/latest) and unzip it into the path below.

| | |
| --- | --- |
| **Release asset** | GitHub Release `*-windows.zip` / `*-linux.zip` |
| **Local path** | `lib/cpu/` (`FaceLivenessSDK.dll` on Windows, or the `.so` files on Linux, **and** every required `*.xdb` at the top level) |
| **Databases** | Face recognition needs the full `recognition*.xdb` set; face liveness needs `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb`; document products need `document.xdb`. |

```text
https://github.com/identixia-IDV/FaceLivenessDetection-Windows/releases/latest
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. An unavailable check is not a pass.
{% endhint %}

## Integration guide — start the project

Default API port for this product family: **`14105`**. Gradio demo (when shipped) uses **`14205`**.

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Windows.git
cd FaceLivenessDetection-Windows
```

### 2. Download and place the runtime

Native libraries and `*.xdb` databases are not in git. Download the runtime zip from [GitHub Releases](https://github.com/identixia-IDV/FaceLivenessDetection-Windows/releases/latest) and unzip it into `lib/cpu/`. DLLs or `.so` files and every required database pack sit in that folder, not inside an extra directory. See [Download and place the runtime](#download-and-place-the-runtime).

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


## Support

{% include "../.gitbook/includes/contact.md" %}

{% include "../.gitbook/includes/footer.md" %}
