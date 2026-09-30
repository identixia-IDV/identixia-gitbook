---
description: >-
  On-premise passive face liveness SDK for Windows. Scores one RGB face image through the local liveness API when the license allows it.
---

# Liveness Detection Windows SDK

On-premise passive face liveness SDK for Windows. Scores one RGB face image through the local liveness API when the license allows it.

### Repository

{% embed url="https://github.com/identixia-IDV/FaceLivenessDetection-Windows" %}

[`identixia-IDV/FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows)

### From the product README

## Identixia Face Liveness — Windows

On-premise **passive face liveness** for Windows, including deepfake when the license allows it. This app ships the liveness model packs only. Matching and 1:N search are a separate app, `FaceRecognition-Windows`.

| Topic | Detail |
| --- | --- |
| API | `http://127.0.0.1:14105` |
| Demo | `http://127.0.0.1:14205` |
| Runtime | `lib\cpu\` — about **316 MB** |
| Models | `recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb` |
| Left out | `recognition.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb` |

`recognition-common.xdb` stays because the detector is shared. The matcher pack is not included.

```bat
pip install -r requirements.txt
run.bat
```

```bash
curl -s http://127.0.0.1:14105/api/machinecode
curl -s -X POST http://127.0.0.1:14105/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
curl -s http://127.0.0.1:14105/api/health
```

Replace the key in `license.txt` with the liveness license for this machine. Then, in a second terminal:

```bat
pip install -r requirements-demo.txt
run_demo.bat
```

Liveness calls: `POST /api/face/liveness` and `POST /api/face/deepfake`.

---

## Contact

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}
