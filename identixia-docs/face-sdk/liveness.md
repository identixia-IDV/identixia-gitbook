---
description: >-
  Passive face liveness: when it runs, which products include it, and how to read the score.
---

# Face liveness

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
| Full Face SDK (recognition + liveness) | Platform pages under [Face SDK](README.md) |
| Liveness-only | [Android](liveness-android.md) · [iOS](liveness-ios.md) · [Windows](liveness-windows.md) · [Docker](liveness-linux-docker.md) |

Hub pack: [`Face-Liveness-Detection-SDK`](https://github.com/identixia-IDV/Face-Liveness-Detection-SDK)

## Server example

Default Face API port is **14103** (confirm in the product README).

```bash
# Full / recognition+liveness Docker stack
curl -s -X POST http://127.0.0.1:14103/api/face/liveness \
  -H "Content-Type: application/json" \
  -d '{"image":"BASE64_JPEG"}'
```

Liveness-only Docker uses the path documented on [Linux / Docker (liveness only)](liveness-linux-docker.md) (often `/api/liveness`).

## Mobile tip

Run activate → init → liveness on a **background** thread. Keep the camera preview on the UI thread. If VideoWorker / tracking is used, start it when the camera screen appears and stop it when the screen closes.

<figure><img src="../.gitbook/assets/liveness-mobile.png" alt="Mobile liveness" width="200"><figcaption>Mobile liveness result</figcaption></figure>
