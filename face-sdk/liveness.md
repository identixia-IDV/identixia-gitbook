---
description: >-
  Understand Identixia face liveness detection, presentation attack checks, license requirements, and how to interpret results.
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

Presentation-attack and deepfake checks. Report REAL only when both pass. These builds do not enroll a gallery and do not run 1:N search. Server port **14105**. The routes are `POST /api/face/liveness` and `POST /api/face/deepfake`.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](liveness-android.md) | [`FaceLivenessDetection-Android`](https://github.com/identixia-IDV/FaceLivenessDetection-Android) |
| iOS | [iOS](liveness-ios.md) | [`FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) |
| Flutter | [Flutter](liveness-flutter.md) | [`FaceLivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceLivenessDetection-Flutter) |
| React Native | [React Native](liveness-react-native.md) | [`FaceLivenessDetection-React-Native`](https://github.com/identixia-IDV/FaceLivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](liveness-ionic-capacitor.md) | [`FaceLivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](liveness-ionic-cordova.md) | [`FaceLivenessDetection-Ionic-Cordova`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Cordova) |
| Windows | [Windows](liveness-windows.md) | [`FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](liveness-linux-docker.md) | [`FaceLivenessDetection-Docker`](https://github.com/identixia-IDV/FaceLivenessDetection-Docker) |

Recognition and liveness in one sample use the repositories on [Face SDK](README.md). That server listens on port **14103** and uses the same `/api/face/liveness` path.

Hub pack: [`Face-Liveness-Detection-SDK`](https://github.com/identixia-IDV/Face-Liveness-Detection-SDK)

## Server example

Default Face API port is **14103** (confirm in the product README).

```bash
# Full / recognition+liveness Docker stack
curl -s -X POST http://127.0.0.1:14103/api/face/liveness \
  -H "Content-Type: application/json" \
  -d '{"image":"BASE64_JPEG"}'
```

Liveness-only Docker uses the same `/api/face/liveness` path on port **14105** — see [Linux / Docker (liveness only)](liveness-linux-docker.md).

## Mobile tip

Run activate → init → liveness on a **background** thread. Keep the camera preview on the UI thread. If VideoWorker / tracking is used, start it when the camera screen appears and stop it when the screen closes.

![Mobile liveness](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/mobile/liveness.png)
