---
description: >-
  Full Document SDK HTTP APIs for Windows and Linux/Docker.
icon: server
---

# Server (Windows & Docker)

## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](https://docs.identixia.com/developers/id-document-sdk/windows) | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) | 14102 |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/linux-docker) | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) | 14102 |

## Routes

| Route | Role |
| --- | --- |
| `POST /api/document/process` | Full process (recognition + authenticity when licensed) |
| `POST /api/document/recognition` | OCR / MRZ / barcode only |
| `POST /api/document/liveness` | Authenticity only |

Control routes use `{success, code, message, request_id, data}`. Response shape: [Result JSON](result-json.md).

Parent: [Full product](full-product.md).

{% include "../.gitbook/includes/footer.md" %}
