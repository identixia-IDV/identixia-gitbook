---
description: >-
  Integrate the self-hosted Identixia face recognition HTTP API on Windows or Docker. Follow setup, activation, and request examples.
icon: magnifying-glass
---

# Face Recognition HTTP API

Start Face Recognition (+ Liveness) Windows/Docker on port **14103** (recognition-only uses **14104**).

## Start the project

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows.git
cd FaceRecognition-LivenessDetection-Windows
python scripts/get_runtime.py
cp -n .env.example .env
pip install -r requirements.txt
python run_server.py
```

Linux / Docker: see [Linux / Docker](../face-sdk/linux-docker.md). Place files under `lib/cpu/` including every `recognition*.xdb` pack.

## Activate

```bash
curl -s http://127.0.0.1:14103/api/machinecode
curl -s -X POST http://127.0.0.1:14103/api/activate \
  -H "Content-Type: application/json" \
  -d '{"license":"YOUR_KEY"}'
curl -s http://127.0.0.1:14103/api/licenseStatus
```

## All endpoints

### Control

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Process up |
| `GET` | `/api/backend` | Backend / SDK info |
| `GET` | `/api/machinecode` | Machine fingerprint |
| `GET` | `/api/licenseStatus` | `recognition`, `liveness` flags |
| `POST` | `/api/activate` | Activate license |

### Face process

| Method | Path | Body (summary) | Description |
| --- | --- | --- | --- |
| `POST` | `/api/face/analyze` | `image`, optional `cropImage` | Full analyze |
| `POST` | `/api/face/boxes` | `image` | Face boxes |
| `POST` | `/api/face/traits` | `image` | Attributes |
| `POST` | `/api/face/image-quality` | `image` | Image quality |
| `POST` | `/api/face/landmarks` | `image`, `mode` `14` or `68` | Landmarks |
| `POST` | `/api/face/quality` | `image` | Face quality |
| `POST` | `/api/face/template` | `image` | Template / feature |
| `POST` | `/api/face/compare` | `image1`, `image2` | 1:1 image match |
| `POST` | `/api/face/score` | `feature1`, `feature2` | Template similarity |
| `POST` | `/api/face/liveness` | `image` | PAD + deepfake (when licensed) |
| `POST` | `/api/face/deepfake` | `image` | Deepfake-only |
| `POST` | `/api/face/enroll` | `image`, `name` | Gallery enroll |
| `POST` | `/api/face/search` | `image`, `threshold` | 1:N search |
| `GET` | `/api/face/gallery` | — | List gallery |
| `DELETE` | `/api/face/gallery/{id}` | — | Remove entry |
| `POST` | `/api/face/track/start` | config | Start track session |
| `POST` | `/api/face/track/frame` | `image` | Push frame |
| `GET` | `/api/face/track/events` | — | Poll events |
| `POST` | `/api/face/track/stop` | — | Stop session |

## cURL — analyze

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/analyze \
  -H "Content-Type: application/json" \
  -d '{"image":"BASE64_JPEG","cropImage":false}'
```

## cURL — compare (1:1)

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/compare \
  -H "Content-Type: application/json" \
  -d '{"image1":"BASE64_A","image2":"BASE64_B"}'
```

## cURL — liveness (when licensed)

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/liveness \
  -H "Content-Type: application/json" \
  -d '{"image":"BASE64_JPEG"}'
```

Authenticity is **REAL** only when PAD and deepfake both pass.

## Python

```python
import base64, json, urllib.request
from pathlib import Path

image = base64.b64encode(Path("photo.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:14103/api/face/analyze",
    data=json.dumps({"image": image, "cropImage": False}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

## JavaScript

```javascript
const image = /* base64 string */;
const res = await fetch("http://127.0.0.1:14103/api/face/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image, cropImage: false }),
});
console.log(await res.json());
```

## Resources

* [Windows product guide](../face-sdk/windows.md)
* [Linux / Docker product guide](../face-sdk/linux-docker.md)
* [Postman](https://docs.identixia.com/sdk-server#postman)
* [Request a license](https://docs.identixia.com/guides/request-a-license-and-support)

{% include "../.gitbook/includes/footer.md" %}
