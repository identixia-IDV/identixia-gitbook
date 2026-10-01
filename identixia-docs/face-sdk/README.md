---
description: >-
  On-premise Face SDK: recognition and passive liveness for mobile and server platforms.
---

# Face SDK

<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>

## What this SDK is

The **Face SDK** runs on the phone or on your server. It covers two licensed functions:

| Function | What it does | License flag |
| --- | --- | --- |
| **Recognition** | Detect faces, attributes, quality, templates, 1:1 match, 1:N identify | `recognition` |
| **Liveness** | Passive presentation-attack score (real person vs photo/screen) | `liveness` |

Pick a **repository that matches your license**. A recognition-only build will not invent liveness scores.

## Choose a product line

| You need | Use |
| --- | --- |
| Recognition **and** liveness in one app / API | Full platforms below (Android → Docker) |
| Recognition only | [Windows](recognition-windows.md) · [Linux / Docker](recognition-linux-docker.md) |
| Liveness only | [Android](liveness-android.md) · [iOS](liveness-ios.md) · [Windows](liveness-windows.md) · [Linux / Docker](liveness-linux-docker.md) |

Read the function guides first if you are new:

* [Face recognition](recognition.md) — APIs, gallery, match
* [Face liveness](liveness.md) — when scores appear, how to gate UX

## Full product (recognition + liveness)

| Platform | Repository | Docs |
| --- | --- | --- |
| Android | [`FaceRecognition-LivenessDetection-Android`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) | [Android](android.md) |
| iOS | [`FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) | [iOS](ios.md) |
| Flutter | [`FaceRecognition-LivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) | [Flutter](flutter.md) |
| React Native | [`FaceRecognition-LivenessDetection-React-Native`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) | [React Native](react-native.md) |
| Ionic Capacitor | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) | [Ionic Capacitor](ionic-capacitor.md) |
| Ionic Cordova | [`FaceRecognition-LivenessDetection-Ionic-Cordova`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) | [Ionic Cordova](ionic-cordova.md) |
| Windows | [`FaceRecognition-LivenessDetection-Windows`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) | [Windows](windows.md) |
| Linux / Docker | [`FaceRecognition-LivenessDetection-Docker`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) | [Linux / Docker](linux-docker.md) |

<figure><img src="../.gitbook/assets/face-android-home.png" alt="Face SDK Android home" width="160"><figcaption>Android demo home</figcaption></figure>

## How to integrate

1. Open the platform page for your stack.
2. Clone the sample → place engine binaries from GitHub Releases → run until **Ready**.
3. Activate with **your** application id / machine code (demo keys only work for demo ids).
4. Call recognition and liveness APIs on a **background** thread (mobile) or via HTTP (server).

{% hint style="info" %}
Biometric images and templates stay on **your** device or server. Identixia does not host them.
{% endhint %}
