---
description: >-
  Integrate the self-hosted Identixia face liveness detection HTTP API on Windows or Docker. Follow setup, activation, and request examples.
---

# Face Liveness Detection HTTP API

Start Face Liveness Windows/Docker on port **14105** (the full Face product also exposes liveness on **14103**).

## Start the project

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Windows.git
cd FaceLivenessDetection-Windows
python scripts/get_runtime.py
cp -n .env.example .env
pip install -r requirements.txt
python run_server.py
```

Place under `lib/cpu/`: engine binaries plus `recognition-common.xdb`, `recognition-liveness.xdb`, and `recognition-deepfake.xdb`. Matcher packs (`recognition.xdb`, attr, quality) are **not** included in the liveness-only product.

## Activate

```bash
curl -s http://127.0.0.1:14105/api/machinecode
curl -s -X POST http://127.0.0.1:14105/api/activate \
  -H "Content-Type: application/json" \
  -d '{"license":"YOUR_KEY"}'
curl -s http://127.0.0.1:14105/api/licenseStatus
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | Liveness entitlement |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/face/liveness` | PAD + deepfake (combined authenticity) |
| `POST` | `/api/face/deepfake` | Deepfake-only score |

Authenticity is **REAL** only when PAD and deepfake both pass.

## cURL

```bash
curl -s -X POST http://127.0.0.1:14105/api/face/liveness \
  -H "Content-Type: application/json" \
  -d '{"image":"BASE64_JPEG"}'
```

## Python

```python
import base64, json, urllib.request
from pathlib import Path

image = base64.b64encode(Path("photo.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:14105/api/face/liveness",
    data=json.dumps({"image": image}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

## JavaScript

```javascript
const image = /* base64 string */;
const res = await fetch("http://127.0.0.1:14105/api/face/liveness", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image }),
});
console.log(await res.json());
```

## Resources

* [Face Liveness (Windows)](../face-sdk/liveness-windows.md)
* [Face Liveness (Linux / Docker)](../face-sdk/liveness-linux-docker.md)
* [Postman](README.md#postman)
