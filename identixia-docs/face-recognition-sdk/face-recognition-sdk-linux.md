---
description: >-
  On-premise face recognition SDK for Linux and Docker with passive liveness. Detection, quality, templates, and 1:1 match. Liveness routes require the matching license.
---

# Face Recognition + Liveness Linux SDK

On-premise face recognition SDK for Linux and Docker with passive liveness. Detection, quality, templates, and 1:1 match. Liveness routes require the matching license.

### Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker" %}

[`identixia-IDV/FaceRecognition-LivenessDetection-Docker`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker)

### From the product README

## <img src="https://cdn.simpleicons.org/docker/2496ED" width="32" height="32" alt="" /> Identixia Face Recognition SDK — Linux / Docker

**On-premise face recognition SDK** with **passive face liveness** as a Linux / Docker HTTP API: detect, quality, face template matching, 1:1 compare, and PAD. Biometrics stay in your cluster — ideal for KYC backends and private access control. Image: [`identixia/face-recognition-liveness-sdk`](https://hub.docker.com/r/identixia/face-recognition-liveness-sdk).

<p><img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square" alt="Docker" /> <img src="https://img.shields.io/badge/On-premise-0F766E?style=flat-square" alt="On-premise" /> <img src="https://img.shields.io/badge/Passive%20liveness-0F766E?style=flat-square" alt="Passive%20liveness" /> <img src="https://img.shields.io/badge/1%3A1%20match-0F766E?style=flat-square" alt="1%3A1%20match" /></p>

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then replace the key in `license.txt` and activate.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **face recognition SDK** Linux / Docker (+ passive liveness) |
| **Modes** | Detect · quality · templates · 1:1 match · PAD |
| **What you run** | HTTP API on port **14103** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Replace the key in the included `license.txt`, then send that file with `POST /api/activate`. |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | Included in the Docker image |
| **Tools** | Linux x64 with Docker |
| **Privacy** | Biometrics stay in your cluster — no Identixia cloud |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Run the server

```bash
docker pull identixia/face-recognition-liveness-sdk:latest
docker run -d --name identixia-api -p 14103:14103 \
  -v /etc/machine-id:/etc/machine-id:ro \
  identixia/face-recognition-liveness-sdk:latest
```

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Get a license

```bash
curl -s http://127.0.0.1:14103/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> Activate

This repository includes `license.txt`. Replace the key in that file with the license we send you, then run this command from the repository folder:

```bash
curl -s -X POST http://127.0.0.1:14103/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
```

### <img src="https://img.shields.io/badge/-4-0F766E?style=for-the-badge" alt="" /> Check that it is running

```bash
curl -s http://127.0.0.1:14103/api/health
```

### <img src="https://img.shields.io/badge/-5-0F766E?style=for-the-badge" alt="" /> Detect / match / liveness

Replace `BASE64_JPEG` with a base64-encoded JPEG.

Detect a face:

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/analyze -H "Content-Type: application/json" -d "{\"image\":\"BASE64_JPEG\"}"
```

Compare two faces:

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/compare -H "Content-Type: application/json" -d "{\"image1\":\"BASE64_JPEG\",\"image2\":\"BASE64_JPEG\"}"
```

Check liveness:

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/liveness -H "Content-Type: application/json" -d "{\"image\":\"BASE64_JPEG\"}"
```

### <img src="https://img.shields.io/badge/-6-0F766E?style=for-the-badge" alt="" /> Open the Gradio demo

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
```

Open http://127.0.0.1:14203

---

## <img src="https://api.iconify.design/lucide/list-checks.svg?color=%230F766E" width="24" height="24" alt="" /> What you get

| Capability | What it does |
| --- | --- |
| Face detection | Bounding box, landmarks, pose, and attributes |
| Quality | Face quality score |
| Templates | Template extraction and 1:1 match |
| Passive liveness | Runs when the license allows it |

---

## <img src="https://api.iconify.design/lucide/pc-case.svg?color=%230F766E" width="24" height="24" alt="" /> Requirements

| | |
| --- | --- |
| Host | Linux x64 with Docker |
| Ports | API **14103**, Gradio **14203** |
| Licensing | Bind-mount `/etc/machine-id` for stable machine codes |

---

## <img src="https://api.iconify.design/lucide/app-window.svg?color=%230F766E" width="24" height="24" alt="" /> Gradio demo

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
```

Open http://127.0.0.1:14203

---

## <img src="https://api.iconify.design/lucide/puzzle.svg?color=%230F766E" width="24" height="24" alt="" /> Use in your app

Point your backend at `http://<host>:14103` for detect, match, and liveness. See [docs](https://doc.identixia.com).

---

## <img src="https://api.iconify.design/lucide/images.svg?color=%230F766E" width="24" height="24" alt="" /> Screenshots

<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-detect.png" width="420" alt="Face detection Gradio demo" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-attribute.png" width="420" alt="Face attribute Gradio demo" />
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-quality.png" width="420" alt="Face image quality Gradio demo" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-landmarks.png" width="420" alt="Face landmarks Gradio demo" />
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-match.png" width="420" alt="Face template matching 1:1 demo" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-liveness.png" width="420" alt="Face liveness and deepfake Gradio demo" />
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/desktop/demo-ui-identify.png" width="420" alt="1:N identity Gradio demo" />
</p>

---

## <img src="https://api.iconify.design/lucide/layers.svg?color=%230F766E" width="24" height="24" alt="" /> Platforms

| | Platform | Repo |
| --- | --- | --- |
| <img src="https://cdn.simpleicons.org/android/3DDC84" width="18" height="18" alt="" /> | Android | [FaceRecognition-LivenessDetection-Android](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| <img src="https://cdn.simpleicons.org/apple/000000" width="18" height="18" alt="" /> | iOS | [FaceRecognition-LivenessDetection-iOS](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| <img src="https://cdn.simpleicons.org/flutter/02569B" width="18" height="18" alt="" /> | Flutter | [FaceRecognition-LivenessDetection-Flutter](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| <img src="https://cdn.simpleicons.org/react/61DAFB" width="18" height="18" alt="" /> | React Native | [FaceRecognition-LivenessDetection-React-Native](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) |
| <img src="https://cdn.simpleicons.org/ionic/3880FF" width="18" height="18" alt="" /> | Ionic Capacitor | [FaceRecognition-LivenessDetection-Ionic-Capacitor](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| <img src="https://cdn.simpleicons.org/apachecordova/E8E8E8" width="18" height="18" alt="" /> | Ionic Cordova | [FaceRecognition-LivenessDetection-Ionic-Cordova](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| <img src="https://cdn.simpleicons.org/windows/0078D4" width="18" height="18" alt="" /> | Windows | [FaceRecognition-LivenessDetection-Windows](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) |
| <img src="https://cdn.simpleicons.org/docker/2496ED" width="18" height="18" alt="" /> | Linux / Docker | [FaceRecognition-LivenessDetection-Docker](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) |

---

## <img src="https://api.iconify.design/lucide/mail.svg?color=%230F766E" width="24" height="24" alt="" /> Contact

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}
