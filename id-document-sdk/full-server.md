---
description: >-
  Deploy Identixia ID document recognition and OCR with licensed liveness checks using self-hosted HTTP APIs on Windows or Linux and Docker.
---

# ID Document Recognition and OCR APIs for Windows and Docker

## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](windows.md) | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) | 14102 |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) | 14102 |

## Routes

| Route | Role |
| --- | --- |
| `POST /api/document/process` | Full process (recognition + authenticity when licensed) |
| `POST /api/document/recognition` | OCR / MRZ / barcode only |
| `POST /api/document/liveness` | Authenticity only |

Control routes use `{success, code, message, request_id, data}`. Response shape: [Result JSON](result-json.md).

Parent: [Full product](full-product.md).
