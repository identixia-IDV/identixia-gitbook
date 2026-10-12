---
description: >-
  Understand Identixia face liveness detection, presentation attack checks, license requirements, and how to interpret results.
icon: shield-halved
---

# Face Liveness Detection and Anti-Spoofing

## Overview

Face **liveness** answers whether the subject is a live person or a photo, screen, or replay.

It is **passive**: the user looks at the camera. The core API does not require smile or blink challenges.

## When a score appears

| Situation | Result |
| --- | --- |
| License includes `liveness` | Engine returns a liveness score / decision |
| License is recognition-only | No liveness score — treat as “not evaluated”, not as “pass” |
| Wrong product repo | Use a **liveness** or **full** repository, not recognition-only |

## Products

| Product line | Docs |
| --- | --- |
| Face Recognition & Liveness Detection | Platform pages under [Face SDK](README.md). Server port **14103**. |
| Face Liveness Detection | [Android](https://docs.identixia.com/developers/face-sdk/liveness-android) · [iOS](https://docs.identixia.com/developers/face-sdk/liveness-ios) · [Windows](https://docs.identixia.com/developers/face-sdk/liveness-windows) · [Docker](https://docs.identixia.com/developers/face-sdk/liveness-linux-docker). Flutter, React Native, and Ionic samples are in the repository list on [Choose a product](https://docs.identixia.com/guides/choose-a-product). Server port **14105**. |

Hub pack: [`Face-Liveness-Detection-SDK`](https://github.com/identixia-IDV/Face-Liveness-Detection-SDK)

## Server example

Default Face API port is **14103** (confirm in the product README).

```bash
# Full / recognition+liveness Docker stack
curl -s -X POST http://127.0.0.1:14103/api/face/liveness \
  -H "Content-Type: application/json" \
  -d '{"image":"BASE64_JPEG"}'
```

Liveness-only Docker uses the same `/api/face/liveness` path on port **14105** — see [Linux / Docker (liveness only)](https://docs.identixia.com/developers/face-sdk/liveness-linux-docker).

## Mobile tip

Run activate → init → liveness on a **background** thread. Keep the camera preview on the UI thread. If VideoWorker / tracking is used, start it when the camera screen appears and stop it when the screen closes.

![Mobile liveness](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/mobile/liveness.png)

{% include "../.gitbook/includes/footer.md" %}
