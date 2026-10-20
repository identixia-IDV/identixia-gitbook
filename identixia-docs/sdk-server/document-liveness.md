---
description: >-
  Integrate the self-hosted Identixia ID document liveness detection HTTP API on Windows or Docker. Follow setup, activation, and request examples.
---

# ID Document Liveness Detection HTTP API

Start Document Liveness Windows/Docker on port **14107** (the full Document product also exposes authenticity on **14102**).

## Start the project

Download the `runtime` GitHub Release and extract it into `lib/cpu/` before you start the server.

```bash
git clone https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows.git
cd ID-Document-Liveness-Detection-Windows
cp -n .env.example .env
pip install -r requirements.txt
python run_server.py
```

Place under `lib/cpu/`: engine binaries and liveness-only `document.xdb` (packed from `db_liveness.dat`). OCR recognition databases are **not** included.

## Activate

```bash
curl -s http://127.0.0.1:14107/api/machinecode
curl -s -X POST http://127.0.0.1:14107/api/activate \
  -H "Content-Type: application/json" \
  -d '{"license":"YOUR_KEY"}'
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | Entitlement |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/document/liveness` | Authenticity / PAD for front (+ back) images |

This product is **PAD / authenticity**, not OCR. Pair with Document Recognition when you need fields.

## cURL

```bash
curl -s -X POST http://127.0.0.1:14107/api/document/liveness \
  -H "Content-Type: application/json" \
  -d '{"images":["BASE64_FRONT","BASE64_BACK"]}'
```

## Python

```python
import base64, json, urllib.request
from pathlib import Path

front = base64.b64encode(Path("front.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:14107/api/document/liveness",
    data=json.dumps({"images": [front]}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

## JavaScript

```javascript
const image = /* front base64 */;
const res = await fetch("http://127.0.0.1:14107/api/document/liveness", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image }),
});
console.log(await res.json());
```

See [Security check fields](../id-document-sdk/security-fields.md).
