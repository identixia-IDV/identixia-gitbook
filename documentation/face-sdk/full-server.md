---
description: >-
  Full Face SDK HTTP APIs for Windows and Linux/Docker.
icon: server
---

# Server (Windows & Docker)

## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](https://docs.identixia.com/developers/face-sdk/windows) | [`FaceRecognition-LivenessDetection-Windows`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) | 14103 |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/linux-docker) | [`FaceRecognition-LivenessDetection-Docker`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) | 14103 |

## HTTP contract

| Route type | Shape |
| --- | --- |
| Control (`/api/health`, `/api/machinecode`, `/api/activate`, `/api/licenseStatus`) | `{success, code, message, request_id, data}` |
| Process (`/api/face/*`) | Engine JSON (scores, templates, boxes) |

Confirm the bind address and port in the product README before production.

Parent: [Full product](full-product.md).

{% include "../.gitbook/includes/footer.md" %}
