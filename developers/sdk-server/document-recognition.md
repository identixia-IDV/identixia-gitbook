---
description: >-
  Full HTTP integration guide for ID document recognition (+ optional authenticity).
icon: id-card
---

# Document Recognition

Start Document full product on port **14102** (recognition-only uses **14106**).

## Start the project

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows.git
cd ID-Document-Recognition-Liveness-Detection-Windows
python scripts/get_runtime.py
cp -n .env.example .env
pip install -r requirements.txt
python run_server.py
```

Place under `lib/cpu/`: `DocumentReaderSDK.dll` (or Linux `.so` files) **and** `document.xdb`.

## Activate

```bash
curl -s http://127.0.0.1:14102/api/machinecode
curl -s -X POST http://127.0.0.1:14102/api/activate \
  -H "Content-Type: application/json" \
  -d '{"license":"YOUR_KEY"}'
curl -s http://127.0.0.1:14102/api/licenseStatus
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/backend` | Backend info |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | `recognition`, `authenticity` flags |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/document/process` | Full process (OCR + optional authenticity) |
| `POST` | `/api/document/recognition` | Recognition only |
| `POST` | `/api/document/liveness` | Authenticity / PAD only |
| `POST` | `/api/document/general` | General helper |

Prefer `images: [{ "image": "<b64>" }, …]` when the binding expects an array (see Postman). Some samples also accept `image` / `image2`.

## cURL — process

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/process \
  -H "Content-Type: application/json" \
  -d '{"images":[{"image":"BASE64_FRONT"},{"image":"BASE64_BACK"}]}'
```

## Python

```python
import base64, json, urllib.request
from pathlib import Path

front = base64.b64encode(Path("front.jpg").read_bytes()).decode()
back = base64.b64encode(Path("back.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:14102/api/document/process",
    data=json.dumps({"images": [{"image": front}, {"image": back}]}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

## Resources

* [Result Format](https://docs.identixia.com/id-document-sdk/result-json)
* [Security check fields](https://docs.identixia.com/id-document-sdk/security-fields)
* [Windows](../id-document-sdk/windows.md) · [Linux / Docker](../id-document-sdk/linux-docker.md)
* [Postman](https://docs.identixia.com/sdk-server#postman)

{% include "../.gitbook/includes/footer.md" %}
