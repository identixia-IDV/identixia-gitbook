---
description: >-
  On-premise face recognition SDK for Windows. Detection, landmarks, attributes, ICAO-style quality, templates, and 1:1 match through a local API.
---

# Face Recognition Windows SDK

On-premise face recognition SDK for Windows. Detection, landmarks, attributes, ICAO-style quality, templates, and 1:1 match through a local API.

### Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-Windows" %}

[`identixia-IDV/FaceRecognition-Windows`](https://github.com/identixia-IDV/FaceRecognition-Windows)

### From the product README

## Identixia Face Recognition — Windows

On-premise **face recognition** for Windows: detect, attributes, quality, landmarks, 1:1 match, and 1:N search. This app ships the recognition model packs only. Passive liveness and deepfake are a separate app, `FaceLivenessDetection-Windows`.

| Topic | Detail |
| --- | --- |
| API | `http://127.0.0.1:14104` |
| Demo | `http://127.0.0.1:14204` |
| Runtime | `lib\cpu\` — about **295 MB** |
| Models | `recognition-common.xdb`, `recognition.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb` |
| Left out | `recognition-liveness.xdb`, `recognition-deepfake.xdb` |

The same `FaceRecognitionSDK.dll` is used. It skips a model pack that is not in `lib\cpu\`.

```bat
pip install -r requirements.txt
run.bat
```

```bash
curl -s http://127.0.0.1:14104/api/machinecode
curl -s -X POST http://127.0.0.1:14104/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
curl -s http://127.0.0.1:14104/api/health
```

Replace the key in `license.txt` with the recognition license for this machine. Then, in a second terminal:

```bat
pip install -r requirements-demo.txt
run_demo.bat
```

Recognition calls: `POST /api/face/analyze`, `/boxes`, `/traits`, `/image-quality`, `/landmarks`, `/quality`, `/compare`, `/template`, `/score`, `/enroll`, `/search`.

---

## Contact

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}
