---
description: >-
  Windows and Linux/Docker standalone face liveness APIs.
icon: server
---

# Liveness-only — server

## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](https://docs.identixia.com/developers/face-sdk/liveness-windows) | [`FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) | 14105 |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/liveness-linux-docker) | [`FaceLivenessDetection-Docker`](https://github.com/identixia-IDV/FaceLivenessDetection-Docker) | 14105 |

Process paths: `POST /api/face/liveness` and `POST /api/face/deepfake`. Control routes use the standard `{success, code, message, request_id, data}` envelope.

Parent: [Liveness-only products](liveness-only.md).

{% include "../.gitbook/includes/footer.md" %}
