---
description: >-
  Choose a standalone Identixia ID document liveness detection SDK for anti-spoofing checks, separate from recognition.
---

# Standalone ID Document Liveness Detection SDKs

## When to use

Use this line when the license is document authenticity only. The sample checks presentation attacks. It does not read MRZ, barcodes, or visual fields. Pair it with [Document recognition](recognition.md) when you also need the printed data.

| Platform | Port | Where to start | Repository |
| --- | ---: | --- | --- |
| Android | — | Repository README | [`ID-Document-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android) |
| iOS | — | Repository README | [`ID-Document-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-iOS) |
| Flutter | — | Repository README | [`ID-Document-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Flutter) |
| React Native | — | Repository README | [`ID-Document-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-React-Native) |
| Ionic Capacitor | — | Repository README | [`ID-Document-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | — | Repository README | [`ID-Document-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Cordova) |
| Windows | 14107 | Repository README | [`ID-Document-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows) |
| Linux / Docker | 14107 | [Docker guide](liveness-linux-docker.md) | [`ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) |

The HTTP call is `POST /api/document/liveness` with `images` entries `{image, page_idx}`. A liveness-only server does not expose `/api/document/process`.

Concept guide: [Document liveness](liveness.md). For OCR and authenticity in one build, use the [full product](full-product.md).
