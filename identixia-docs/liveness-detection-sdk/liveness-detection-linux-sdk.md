---
description: >-
  On-premise passive face liveness SDK for Linux and Docker. Scores one RGB face image through the local liveness API when the license allows it.
---

# Liveness Detection Linux SDK

On-premise passive face liveness SDK for Linux and Docker. Scores one RGB face image through the local liveness API when the license allows it.

### Repository

{% embed url="https://github.com/identixia-IDV/FaceLivenessDetection-Docker" %}

[`identixia-IDV/FaceLivenessDetection-Docker`](https://github.com/identixia-IDV/FaceLivenessDetection-Docker)

### From the product README

## Identixia Face Liveness — Linux / Docker

On-premise **passive face liveness** for Linux / Docker, including deepfake when licensed. This image ships liveness model packs only. Matching is `FaceRecognition-Docker`.

| Topic | Detail |
| --- | --- |
| API | `http://127.0.0.1:14105` |
| Demo | `http://127.0.0.1:14205` |
| Image | `identixia/face-liveness` |
| Models | `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb` |
| Left out | `recognition.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb` |

```bash
./docker/build_docker.sh
docker compose -f docker/docker-compose.yml up
```

```bash
curl -s http://127.0.0.1:14105/api/machinecode
curl -s -X POST http://127.0.0.1:14105/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
curl -s http://127.0.0.1:14105/api/health
```

Liveness calls: `POST /api/face/liveness` and `POST /api/face/deepfake`.


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}
