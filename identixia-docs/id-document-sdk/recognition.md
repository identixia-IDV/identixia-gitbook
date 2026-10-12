---
description: >-
  Learn how Identixia ID document recognition and OCR works, which APIs to use, and which sample repositories match your platform.
---

# ID Document Recognition and OCR SDK Features and Integration

## Overview

Document **recognition** finds the card in the frame and extracts:

* Read printed document fields such as the name, document number, and dates using optical character recognition
* **MRZ** (machine-readable zone)
* Barcode / QR when present
* Cropped images (portrait, document, signature, and related crops)

Issuing countries and document series are listed in the [supported ID documents list](supported-id-documents.pdf).

## Capture tips

* Prefer a **physical** device for camera demos.
* Align the document inside the guide; capture front (and back when required).
* On mobile, call locate → capture → `recognize` on a **background** thread.

## Server routes

The full product listens on **14102**. Recognition only listens on **14106** and does not serve `/api/document/liveness`.

| Route | Role | Which build |
| --- | --- | --- |
| `POST /api/document/process` | OCR, MRZ, barcode, and authenticity when that license flag is on | Full product and recognition only |
| `POST /api/document/recognition` | OCR / MRZ / barcode only | Full product and recognition only |
| `POST /api/document/liveness` | Authenticity only | Full product and liveness only (port **14107**) |

```bash
curl -s -X POST http://127.0.0.1:14106/api/document/recognition \
  -H "Content-Type: application/json" \
  -d '{"images":[{"image":"BASE64_FRONT","page_idx":0},{"image":"BASE64_BACK","page_idx":1}]}'
```

Response shape: [Result JSON](result-json.md).

## Repositories

Recognition and document liveness together. Server port **14102**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) |
| iOS | [iOS](ios.md) | [`ID-Document-Recognition-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS) |
| Flutter | [Flutter](flutter.md) | [`ID-Document-Recognition-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Flutter) |
| React Native | [React Native](react-native.md) | [`ID-Document-Recognition-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) |

Recognition without document liveness. Server port **14106**. This build does not serve `/api/document/liveness`.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](recognition-android.md) | [`ID-Document-Recognition-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Android) |
| iOS | [iOS](recognition-ios.md) | [`ID-Document-Recognition-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-iOS) |
| Flutter | [Flutter](recognition-flutter.md) | [`ID-Document-Recognition-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Flutter) |
| React Native | [React Native](recognition-react-native.md) | [`ID-Document-Recognition-React-Native`](https://github.com/identixia-IDV/ID-Document-Recognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](recognition-ionic-capacitor.md) | [`ID-Document-Recognition-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](recognition-ionic-cordova.md) | [`ID-Document-Recognition-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Recognition-Ionic-Cordova) |
| Windows | [Windows](recognition-windows.md) | [`ID-Document-Recognition-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Windows) |
| Linux / Docker | [Linux / Docker](recognition-linux-docker.md) | [`ID-Document-Recognition-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Docker) |

Packaging hub: [`ID-Document-Recognition-Liveness-Detection-SDK`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK)
