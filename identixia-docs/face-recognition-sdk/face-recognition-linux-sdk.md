---
description: >-
  On-premise face recognition SDK for Linux and Docker. Detection, landmarks, attributes, ICAO-style quality, templates, and 1:1 match through a local API.
---

# Face Recognition Linux SDK

On-premise face recognition SDK for Linux and Docker. Detection, landmarks, attributes, ICAO-style quality, templates, and 1:1 match through a local API.

### Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-Docker" %}

[`identixia-IDV/FaceRecognition-Docker`](https://github.com/identixia-IDV/FaceRecognition-Docker)

### From the product README

## Identixia Face Recognition — Linux / Docker

On-premise **face recognition** for Linux / Docker: detect, attributes, quality, landmarks, 1:1 match, and 1:N search. This image ships recognition model packs only. Liveness is `FaceLivenessDetection-Docker`.

| Topic | Detail |
| --- | --- |
| API | `http://127.0.0.1:14104` |
| Demo | `http://127.0.0.1:14204` |
| Image | `identixia/face-recognition` |
| Models | `recognition-common.xdb`, `recognition.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb` |
| Left out | `recognition-liveness.xdb`, `recognition-deepfake.xdb` |

```bash
# place Linux runtime into lib/cpu (see lib/README.md)
./docker/build_docker.sh
docker compose -f docker/docker-compose.yml up
```

```bash
curl -s http://127.0.0.1:14104/api/machinecode
curl -s -X POST http://127.0.0.1:14104/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
curl -s http://127.0.0.1:14104/api/health
```

Recognition calls: `POST /api/face/analyze`, `/boxes`, `/traits`, `/image-quality`, `/landmarks`, `/quality`, `/compare`, `/template`, `/score`, `/enroll`, `/search`.


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}
