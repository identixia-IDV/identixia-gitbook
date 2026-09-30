---
description: >-
  Passive face liveness SDK for Android, iOS, Windows, and Docker. Presentation-attack detection runs on device or on your server when the license allows it.
---

# Liveness Detection SDK


## Overview

Passive face liveness SDK for Android, iOS, Windows, and Docker. Presentation-attack detection runs on device or on your server when the license allows it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `Face-Liveness-Detection-SDK` |
| **Platform** | Hub |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/Face-Liveness-Detection-SDK" %}

Source: [`identixia-IDV/Face-Liveness-Detection-SDK`](https://github.com/identixia-IDV/Face-Liveness-Detection-SDK)

## What you can do

See the platform pages linked below for capabilities.

## Prerequisites

See the product README for toolchain details.

## Start here

Open the platform page that matches your license and stack. Each page includes quick start, activation, full API reference, and troubleshooting.

## Screenshots

<figure><img src="../.gitbook/assets/liveness-mobile.png" alt="Mobile liveness result" width="220"><figcaption>Mobile liveness result</figcaption></figure>

<figure><img src="../.gitbook/assets/liveness-desktop.png" alt="Desktop liveness demo" width="480"><figcaption>Desktop liveness demo</figcaption></figure>


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

Adapted from the shipping repository README for exact commands and platform-specific notes. Screenshots above use the current Identixia asset pack.

## Identixia Face Liveness Detection SDK — Fully On-Premise

> On-device passive face liveness for KYC. The check runs on the phone or on your server. No challenge gesture, and no data is sent to Identixia.

---

## Overview

Identixia **Face Liveness Detection SDK** is a fully **on-premise liveness detection SDK** (presentation-attack detection) for KYC, eKYC, and remote identity verification.

It is passive liveness: no smile or turn-head challenge, no extra hardware, and no Identixia cloud. A live camera frame or a still face image is scored on your device. The result is available only after the license is activated.

All processing stays on the phone or in your VPC. **NO** biometric data leaves the device.

Docs: [https://docs.identixia.com](https://docs.identixia.com)

| You need | This SDK returns |
| -------- | ---------------- |
| Passive PAD | Score + `Real` / `Spoof` + pass / fail |
| Mobile KYC | Live camera HUD (track / liveness / luminance) |
| Server KYC | `POST /api/liveness` on Linux / Docker |
| Privacy | 100% on-device / on-premise |

Need **1:1 / 1:N face match** as well? Use **[Face Recognition SDK](https://github.com/identixia-IDV/Face-Recognition-SDK)**.

---

## Try it

### Mobile SDK on Google Play

<a href="https://play.google.com/store/apps/details?id=ai.identixia.liveness" target="_blank">
  <img alt="Get Identixia Face Liveness on Google Play" src="https://user-images.githubusercontent.com/125717930/230804673-17c99e7d-6a21-4a64-8b9e-a465142da148.png" height="80"/>
</a>

### Server SDK on Playground & Hugging Face

- [Identixia Playground](https://playground.identixia.com/) — try the **server liveness detection SDK** in the browser
- [Hugging Face Space](https://huggingface.co/spaces/Identixia/FaceRecognition-LivenessDetection-SDK) — face recognition + liveness demo

### Linux / Docker (no Drive)

```bash
docker pull identixia/face-liveness:latest
docker run -d --name identixia-face-liveness \
  --shm-size=2gb --privileged \
  -p 14104:14104 \
  -v /etc/machine-id:/etc/machine-id:ro \
  identixia/face-liveness:latest
curl -s http://127.0.0.1:14104/api/health
```

```bash
curl -s -X POST http://127.0.0.1:14104/api/liveness \
  -H 'Content-Type: application/json' \
  -d '{"image":"<base64-jpeg>"}'
```

Score **≥ 0.5** → `Real` / `pass: true`. Full guide: [FaceLivenessDetection-Docker](https://github.com/identixia-IDV/FaceLivenessDetection-Docker).

---

## On YouTube

<a href="https://www.youtube.com/watch?v=cjvEBzFpHGk" target="_blank">
 <img src="https://img.youtube.com/vi/cjvEBzFpHGk/maxresdefault.jpg" alt="Watch Identixia Face Liveness Detection SDK on YouTube" width="720"/>
</a>

---

## Choose your platform

This GitHub repo is the **product hub**. Clone the platform SDK you need — each one is standalone. Engine binaries are on Google Drive (too large for GitHub); Docker Hub already includes the runtime.

| Platform | Repository | Fastest path |
| -------- | ---------- | ------------ |
| **Android (Java, Kotlin)** | [FaceLivenessDetection-Android](https://github.com/identixia-IDV/FaceLivenessDetection-Android) | Drop `facelivenessdk.aar` → Liveness tile |
| **iOS (Objective-C, Swift)** | [FaceLivenessDetection-iOS](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) | Add frameworks → run the sample |
| **Windows** | [FaceLivenessDetection-Windows](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) | Native Windows liveness demo |
| **Linux / Docker** | [FaceLivenessDetection-Docker](https://github.com/identixia-IDV/FaceLivenessDetection-Docker) | `docker pull identixia/face-liveness` |

Building **enroll + identify + liveness** together? Start from Face Recognition (liveness is on the identify / capture path):

| Combined KYC | Repository |
| ------------ | ---------- |
| Android | [FaceRecognition-LivenessDetection-Android](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| iOS | [FaceRecognition-LivenessDetection-iOS](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| React Native | [FaceRecognition-LivenessDetection-React-Native](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) |
| Flutter | [FaceRecognition-LivenessDetection-Flutter](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| Ionic Capacitor | [FaceRecognition-LivenessDetection-Ionic-Capacitor](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [FaceRecognition-LivenessDetection-Ionic-Cordova](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| Windows | [FaceRecognition-LivenessDetection-Windows](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) |
| Linux / Docker | [FaceRecognition-LivenessDetection-Docker](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) |

---

### Platforms in this section

* [Liveness Detection Android SDK](liveness-detection-android-sdk.md)
* [Liveness Detection iOS SDK](liveness-detection-ios-sdk.md)
* [Liveness Detection Windows SDK](liveness-detection-windows-sdk.md)
* [Liveness Detection Linux / Docker SDK](liveness-detection-linux-sdk.md)
