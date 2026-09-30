---
description: >-
  On-premise ID document liveness API for Linux and Docker. Separate from OCR. Document liveness runs when the license includes it.
---

# ID Document Liveness SDK

On-premise ID document liveness API for Linux and Docker. Separate from OCR. Document liveness runs when the license includes it.

### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker" %}

[`identixia-IDV/ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

### From the product README

## <img src="https://cdn.simpleicons.org/docker/2496ED" width="32" height="32" alt="" /> Identixia ID Document Liveness — Linux / Docker

**On-premise document liveness / authenticity** API for KYC and eKYC: detect screen replay, print attacks, and photo-swap style presentation attacks on ID documents. Complements full OCR recognition — this image focuses on **document PAD** so you can reject spoofed IDs before (or after) MRZ / barcode extraction.

Image: [`identixia/document-liveness`](https://hub.docker.com/r/identixia/document-liveness).

<p><img src="https://img.shields.io/badge/Document%20PAD-0F766E?style=flat-square" alt="Document%20PAD" /> <img src="https://img.shields.io/badge/Authenticity-0F766E?style=flat-square" alt="Authenticity" /> <img src="https://img.shields.io/badge/API%208086-0F766E?style=flat-square" alt="API%208086" /> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square" alt="Docker" /> <img src="https://img.shields.io/badge/KYC%20%2F%20eKYC-5A6573?style=flat-square" alt="KYC%20%2F%20eKYC" /></p>

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Start the server, copy the machine code, and contact us with that code to get a license. Then replace the key in `license.txt` and activate.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **document liveness / authenticity** API (KYC / eKYC) |
| **Documents** | ID document presentation-attack detection (screen / print / photo-swap) |
| **What you run** | HTTP API on port **14107** |
| **Machine code** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate** | Replace the key in the included `license.txt`, then send that file with `POST /api/activate`. |
| **Check status** | `GET /api/health` and `GET /api/licenseStatus` after activate |
| **Runtime** | Included in the Docker image |
| **Tools** | Linux x64 with Docker |
| **Privacy** | Authenticity checks stay in your VPC — no Identixia cloud |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Run the server

```bash
docker pull identixia/document-liveness:latest
docker run -d --name identixia-api -p 14107:14107 \
  -v /etc/machine-id:/etc/machine-id:ro \
  identixia/document-liveness:latest
```

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Get a license

```bash
curl -s http://127.0.0.1:14107/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> Activate

This repository includes `license.txt`. Replace the key in that file with the license we send you, then run this command from the repository folder:

```bash
curl -s -X POST http://127.0.0.1:14107/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
```

### <img src="https://img.shields.io/badge/-4-0F766E?style=for-the-badge" alt="" /> Check that it is running

```bash
curl -s http://127.0.0.1:14107/api/health
```

### <img src="https://img.shields.io/badge/-5-0F766E?style=for-the-badge" alt="" /> Run document liveness

Replace `BASE64_JPEG` with a base64-encoded JPEG of the document.

```bash
curl -s -X POST http://127.0.0.1:14107/api/documentLiveness -H "Content-Type: application/json" -d "{\"images\":[{\"image\":\"BASE64_JPEG\"}]}"
```

### <img src="https://img.shields.io/badge/-6-0F766E?style=for-the-badge" alt="" /> Open the Gradio demo

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
```

Open http://127.0.0.1:14207

---

## <img src="https://api.iconify.design/lucide/list-checks.svg?color=%230F766E" width="24" height="24" alt="" /> What you get

| Capability | Notes |
| --- | --- |
| Document liveness / authenticity | Presentation-attack signals for ID images |
| KYC / eKYC gate | Reject spoofed documents before trusting OCR fields |
| HTTP API | Default port **14107** |
| Gradio demo | Port **14207** |
| Postman | `postman/DocumentLiveness-API.postman_collection.json` |

---

## <img src="https://api.iconify.design/lucide/pc-case.svg?color=%230F766E" width="24" height="24" alt="" /> Requirements

| | |
| --- | --- |
| Host | Linux x64 with Docker |
| Ports | API **14107**, Gradio **14207** |
| Licensing | Bind-mount `/etc/machine-id` for stable machine codes |

---

## <img src="https://api.iconify.design/lucide/app-window.svg?color=%230F766E" width="24" height="24" alt="" /> Gradio demo

Gradio runs on your computer, not inside the container. Clone this repository, keep the API running, then open a second terminal in the repository folder.

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
```

Open http://127.0.0.1:14207

---

## <img src="https://api.iconify.design/lucide/puzzle.svg?color=%230F766E" width="24" height="24" alt="" /> Use in your app

POST document images to the liveness routes on **14107**. For full on-premise ID document recognition (passport MRZ OCR, ID card barcode, fields), use the recognition product on **14102**.

---

## <img src="https://api.iconify.design/lucide/boxes.svg?color=%230F766E" width="24" height="24" alt="" /> Related

Full OCR product: [ID-Document-Recognition-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) · Hub: [ID-Document-Recognition-Liveness-Detection-SDK](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK)

---

## <img src="https://api.iconify.design/lucide/mail.svg?color=%230F766E" width="24" height="24" alt="" /> Contact

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}
