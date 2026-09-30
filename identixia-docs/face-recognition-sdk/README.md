---
description: >-
  Face recognition SDK for Android, iOS, Windows, and Docker. Mobile apps enroll and run 1:N identification. Server APIs detect, score quality, and match 1:1. Passive liveness requires the matching license.
---

# Face Recognition SDK

Face recognition SDK for Android, iOS, Windows, and Docker. Mobile apps enroll and run 1:N identification. Server APIs detect, score quality, and match 1:1. Passive liveness requires the matching license.

### Repository

{% embed url="https://github.com/identixia-IDV/Face-Recognition-SDK" %}

[`identixia-IDV/Face-Recognition-SDK`](https://github.com/identixia-IDV/Face-Recognition-SDK)

### From the product README

## Identixia Face Recognition SDK — Fully On-Premise

> On-premise face recognition for phones and servers. Detection, landmarks, quality, templates, and 1:1 match stay on your device. Passive liveness is available when the license includes it.

---

## Overview

Identixia **Face Recognition SDK** is an on-premise face recognition SDK for KYC, access control, and identity verification. A separate liveness SDK is available when you need a passive liveness check.

You get **face detection** (box, landmarks, pose, attributes), **ICAO-style face quality**, **template extraction**, **1:1 match**, and **1:N identify** — on the phone or on your server.

All processing stays on the device. **NO** biometric data is sent to Identixia cloud.

Docs: [https://doc.identixia.com](https://doc.identixia.com)

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

## Screenshots

| Home | Identity | Enroll | Identify |
| ---- | -------- | ------ | -------- |
| <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/home.png" alt="Face recognition home" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/capture.png" alt="Identity camera" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/enroll.png" alt="Enroll result" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/identify.png" alt="Identify result" width="180"/></p> |

| Detect | Attribute | Quality | Landmarks |
| ------ | --------- | ------- | --------- |
| <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/detect.png" alt="Face detect result" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/attribute.png" alt="Face attribute result" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/attribute-quality.png" alt="Image quality result" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/landmarks.png" alt="68-point landmarks" width="180"/></p> |

| Match | Liveness | Settings | About |
| ----- | -------- | -------- | ----- |
| <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/match.png" alt="1:1 match result" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/attribute-liveness.png" alt="Liveness result" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/settings.png" alt="Settings" width="180"/></p> | <p align="center"><img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-recognition/android/about.png" alt="About" width="180"/></p> |

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

## Contact

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}

### Platforms

* [Face Recognition Android SDK](face-recognition-android-sdk.md)
* [Face Recognition iOS SDK](face-recognition-ios-sdk.md)
* [Face Recognition Flutter SDK](face-recognition-android-sdk-2.md)
* [Face Recognition React Native SDK](face-recognition-android-sdk-1.md)
* [Face Recognition Ionic Capacitor SDK](face-recognition-ionic-capacitor-sdk.md)
* [Face Recognition Ionic Cordova SDK](face-recognition-android-sdk-3.md)
* [Face Recognition + Liveness Windows SDK](face-recognition-sdk-windows.md)
* [Face Recognition + Liveness Linux SDK](face-recognition-sdk-linux.md)
* [Face Recognition Windows SDK](face-recognition-windows-sdk.md)
* [Face Recognition Linux SDK](face-recognition-linux-sdk.md)
