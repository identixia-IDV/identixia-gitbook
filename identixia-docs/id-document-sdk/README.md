---
description: >-
  On-premise ID Document SDK: recognition (OCR/MRZ) and document liveness for mobile and server.
---

# ID Document SDK

<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>

## Overview

The **ID Document SDK** reads passports, national IDs, and driver licenses **on-premise**. Two independently licensed functions:

| Function | Capabilities | License flag |
| --- | --- | --- |
| **Recognition** | Locate, OCR, MRZ, barcode, cropped images | `recognition` |
| **Liveness / authenticity** | Anti-spoof checks (screen, printout, substitution) | `authenticity` |

Full product repositories run **both** when the license allows. A **liveness-only** Linux / Docker API is available when you need authenticity without the full OCR surface.

## Start here

1. [Document recognition](recognition.md) — fields, MRZ, images
2. [Document liveness](liveness.md) — authenticity checks versus OCR
3. [Result JSON](result-json.md) — shared shape for mobile and server
4. [Security check fields](security-fields.md) — how to read authenticity results

## Full product (recognition + liveness)

| Platform | Repository | Docs |
| --- | --- | --- |
| Android | [`ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) | [Android](android.md) |
| iOS | [`ID-Document-Recognition-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS) | [iOS](ios.md) |
| Flutter | [`ID-Document-Recognition-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Flutter) | [Flutter](flutter.md) |
| React Native | [`ID-Document-Recognition-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-React-Native) | [React Native](react-native.md) |
| Ionic Capacitor | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) | [Ionic Capacitor](ionic-capacitor.md) |
| Ionic Cordova | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) | [Ionic Cordova](ionic-cordova.md) |
| Windows | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) | [Windows](windows.md) |
| Linux / Docker | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) | [Linux / Docker](linux-docker.md) |

## Liveness-only API

| Platform | Repository | Docs |
| --- | --- | --- |
| Linux / Docker | [`ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) | [Document liveness Docker](liveness-linux-docker.md) |

<figure><img src="../.gitbook/assets/document-desktop-status.png" alt="Document demo status" width="480"><figcaption>Desktop demo — status</figcaption></figure>

{% hint style="info" %}
Document images and OCR fields stay on **your** device or server. Parse [Result JSON](result-json.md) — do not scrape the Result UI.
{% endhint %}
