---
description: >-
  Full Document SDK HTTP APIs for Windows and Linux/Docker.
---

# Server (Windows & Docker)

## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](windows.md) | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) | 14102 |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) | 14102 |

## Routes

| Route | Role |
| --- | --- |
| `POST /api/documentProcess` | Full process (recognition + authenticity when licensed) |
| `POST /api/documentRecognition` | OCR / MRZ / barcode only |
| `POST /api/documentLiveness` | Authenticity only |

Control routes use `{success, code, message, request_id, data}`. Response shape: [Result JSON](result-json.md).

Parent: [Full product](full-product.md).
