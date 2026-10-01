---
description: >-
  Windows and Linux/Docker standalone face liveness APIs.
---

# Liveness-only — server

## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](liveness-windows.md) | [`FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) | 14103 |
| Linux / Docker | [Linux / Docker](liveness-linux-docker.md) | [`FaceLivenessDetection-Docker`](https://github.com/identixia-IDV/FaceLivenessDetection-Docker) | 14103 |

Process path is typically `POST /api/liveness` (confirm in the product README). Control routes use the standard `{success, code, message, request_id, data}` envelope.

Parent: [Liveness-only products](liveness-only.md).
