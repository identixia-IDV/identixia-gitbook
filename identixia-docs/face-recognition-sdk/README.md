---
description: >-
  Face recognition SDK for Android, iOS, Windows, and Docker. Mobile apps enroll and run 1:N identification. Server APIs detect, score quality, and match 1:1. Passive liveness requires the matching license.
---

# Face Recognition SDK


## Overview

Face recognition SDK for Android, iOS, Windows, and Docker. Mobile apps enroll and run 1:N identification. Server APIs detect, score quality, and match 1:1. Passive liveness requires the matching license.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `Face-Recognition-SDK` |
| **Platform** | Hub |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/Face-Recognition-SDK" %}

Source: [`identixia-IDV/Face-Recognition-SDK`](https://github.com/identixia-IDV/Face-Recognition-SDK)

## What you can do

See the platform pages linked below for capabilities.

## Prerequisites

See the product README for toolchain details.

## Start here

Open the platform page that matches your license and stack. Each page includes quick start, activation, full API reference, and troubleshooting.

## Related platforms

| Platform | Docs |
| --- | --- |
| Android | [Face Recognition Android SDK](face-recognition-android-sdk.md) |
| iOS | [Face Recognition iOS SDK](face-recognition-ios-sdk.md) |
| Flutter | [Face Recognition Flutter SDK](face-recognition-android-sdk-2.md) |
| React Native | [Face Recognition React Native SDK](face-recognition-android-sdk-1.md) |
| Ionic Capacitor | [Face Recognition Ionic Capacitor SDK](face-recognition-ionic-capacitor-sdk.md) |
| Ionic Cordova | [Face Recognition Ionic Cordova SDK](face-recognition-android-sdk-3.md) |
| Windows (+ liveness) | [Face Recognition + Liveness Windows](face-recognition-sdk-windows.md) |
| Linux / Docker (+ liveness) | [Face Recognition + Liveness Linux](face-recognition-sdk-linux.md) |
| Windows (recognition only) | [Face Recognition Windows](face-recognition-windows-sdk.md) |
| Linux (recognition only) | [Face Recognition Linux](face-recognition-linux-sdk.md) |

## Screenshots

<figure><img src="../.gitbook/assets/face-android-home.png" alt="Android home" width="160"><figcaption>Android home</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-identify.png" alt="Identify" width="160"><figcaption>Identify</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-match.png" alt="1:1 match" width="160"><figcaption>1:1 match</figcaption></figure>

<figure><img src="../.gitbook/assets/face-desktop-detect.png" alt="Desktop detect" width="280"><figcaption>Desktop detect</figcaption></figure>


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

Adapted from the shipping repository README for exact commands and platform-specific notes. Screenshots above use the current Identixia asset pack.

## Identixia Face Recognition SDK — Fully On-Premise

> On-premise face recognition for phones and servers. Detection, landmarks, quality, templates, and 1:1 match stay on your device. Passive liveness is available when the license includes it.

---

## Overview

Identixia **Face Recognition SDK** is an on-premise face recognition SDK for KYC, access control, and identity verification. A separate liveness SDK is available when you need a passive liveness check.

You get **face detection** (box, landmarks, pose, attributes), **ICAO-style face quality**, **template extraction**, **1:1 match**, and **1:N identify** — on the phone or on your server.

All processing stays on the device. **NO** biometric data is sent to Identixia cloud.

Docs: [https://docs.identixia.com](https://docs.identixia.com)

Dedicated PAD-only product: **[Face Liveness Detection SDK](https://github.com/identixia-IDV/Face-Liveness-Detection-SDK)**.

---

## Try it

### Mobile SDK on Google Play

<a href="https://play.google.com/store/apps/details?id=ai.identixia.recognition" target="_blank">
  <img alt="Get Identixia Face Recognition on Google Play" src="https://user-images.githubusercontent.com/125717930/230804673-17c99e7d-6a21-4a64-8b9e-a465142da148.png" height="80"/>
</a>

### Server SDK on Playground & Hugging Face

- [Identixia Playground](https://playground.identixia.com/)
- [Hugging Face Space](https://huggingface.co/spaces/Identixia/FaceRecognition-LivenessDetection-SDK)

### Linux / Docker (no Drive)

```bash
docker pull identixia/face-recognition:latest
docker run -d --name identixia-face-recognition \
  --shm-size=2gb --privileged \
  -p 14103:14103 \
  -v /etc/machine-id:/etc/machine-id:ro \
  identixia/face-recognition:latest
curl -s http://127.0.0.1:14103/api/health
```

Then `POST /api/detect`, `/api/quality`, `/api/match`. Guide: [FaceRecognition-Docker](https://github.com/identixia-IDV/FaceRecognition-Docker).

---

## On YouTube

<a href="https://www.youtube.com/watch?v=qVtdkwtGtqs" target="_blank">
 <img src="https://img.youtube.com/vi/qVtdkwtGtqs/maxresdefault.jpg" alt="Watch Identixia Face Recognition SDK on YouTube" width="720"/>
</a>

---

## Choose your platform

This GitHub repo is the **product hub**. Clone the platform SDK you need. Engine binaries are on Google Drive (too large for GitHub); Docker Hub already includes the runtime.

| Platform | Repository | Fastest path |
| -------- | ---------- | ------------ |
| **Android (Java, Kotlin)** | [FaceRecognition-LivenessDetection-Android](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) | Drop `facerecognitionsdk.aar` → Enroll / Identify |
| **iOS (Objective-C, Swift)** | [FaceRecognition-LivenessDetection-iOS](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) | Add frameworks → run the sample |
| **Windows** | [FaceRecognition-Windows](https://github.com/identixia-IDV/FaceRecognition-Windows) | Native Windows SDK + demo |
| **Linux / Docker** | [FaceRecognition-Docker](https://github.com/identixia-IDV/FaceRecognition-Docker) | `docker pull identixia/face-recognition` |
| **React Native** | [FaceRecognition-LivenessDetection-React-Native](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) | Android + iOS sample |
| **Flutter** | [FaceRecognition-LivenessDetection-Flutter](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) | Android + iOS plugin + example |
| **Ionic Capacitor** | [FaceRecognition-LivenessDetection-Ionic-Capacitor](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) | Capacitor Android / iOS |
| **Ionic Cordova** | [FaceRecognition-LivenessDetection-Ionic-Cordova](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) | Cordova Android / iOS |
| **.NET MAUI** | [FaceRecognition-.Net](https://github.com/identixia-IDV/FaceRecognition-.Net) | .NET sample |
| **.NET WPF** | [FaceRecognition-WPF-.Net](https://github.com/identixia-IDV/FaceRecognition-WPF-.Net) | WPF desktop |
| **JavaScript** | [FaceRecognition-LivenessDetection-Javascript](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Javascript) | Web SDK |
| **React** | [FaceRecognition-LivenessDetection-React](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React) | React web |
| **Vue** | [FaceRecognition-LivenessDetection-Vue](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Vue) | Vue web |

---

### Platforms in this section

* [Face Recognition Android SDK](face-recognition-android-sdk.md)
* [Face Recognition iOS SDK](face-recognition-ios-sdk.md)
* [Face Recognition Flutter SDK](face-recognition-android-sdk-2.md)
* [Face Recognition React Native SDK](face-recognition-android-sdk-1.md)
* [Face Recognition Ionic Capacitor SDK](face-recognition-ionic-capacitor-sdk.md)
* [Face Recognition Ionic Cordova SDK](face-recognition-android-sdk-3.md)
* [Face Recognition + Liveness Windows SDK](face-recognition-sdk-windows.md)
* [Face Recognition + Liveness Linux / Docker SDK](face-recognition-sdk-linux.md)
* [Face Recognition Windows SDK](face-recognition-windows-sdk.md)
* [Face Recognition Linux / Docker SDK](face-recognition-linux-sdk.md)
