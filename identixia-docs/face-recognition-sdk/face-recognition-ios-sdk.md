---
description: >-
  On-device face recognition SDK for iOS: enrollment, 1:N identification, and face attributes. Passive liveness is available when the license allows it.
---

# Face Recognition iOS SDK


## Overview

On-device face recognition SDK for iOS: enrollment, 1:N identification, and face attributes. Passive liveness is available when the license allows it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `FaceRecognition-LivenessDetection-iOS` |
| **Platform** | iOS |
| **Docs site** | [doc.identixia.com](https://doc.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS" %}

Source: [`identixia-IDV/FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS)

## What you can do

| Capability | Description |
| --- | --- |
| Detect faces | Bounding box, landmarks, pose |
| Attributes | Age / gender / expression-style traits when enabled |
| Image / face quality | ICAO-style quality scores |
| Templates | Compact face feature vectors you store yourself |
| 1:1 match | Compare two images or two templates |
| 1:N identify | Enroll gallery + live search (mobile VideoWorker / server gallery) |
| Passive liveness | Presentation-attack score when the license includes it |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| IDE | Xcode (recent stable) |
| Device | Physical iPhone for camera demos |
| Deployment | iOS 13+ (see sample project) |
| Frameworks | Vendored `.framework` / `.xcframework` from Release or Drive pack |

## Quick start

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS.git
cd FaceRecognition-LivenessDetection-iOS
```

### 2. Place the runtime

Engine zip/AAR/framework from GitHub Releases (`/releases/latest/download/…`) or the files already under `libfacesdk` / Frameworks when present.

Clients should download versioned assets via:

```text
https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/latest/download/<asset>
```

### 3. Run the demo

Follow the repository **Run** section (Android Studio / Xcode / `flutter run` / `yarn android` / Ionic). Wait until status shows **Ready** before opening camera modes.

### 4. Try every demo mode

Use each tile / screen once (enroll, identify, capture, document front/back, result, about). Confirm license state on the About / Result screen.


## License and activation (mobile)

| | |
| --- | --- |
| **Demo id** | `com.identixia.facerecognitionsdk` (Android) / matching iOS bundle id in the sample |
| **Demo key** | Bundled for the sample id only |
| **Your app** | New applicationId / bundle id → request a new license |

### Activate → init (concept)

1. Call activate with your license string (background thread).
2. On success, call init (unpacks on-device models; may take a few seconds the first time).
3. Gate UI on Ready / license status before camera modes.
4. Never paste the demo key into a production app id.


### Status codes

| Code | Meaning |
| ---: | ------- |
| `0` | Success |
| `1` / `-1` | Invalid license |
| `2` / `-2` | Wrong application / bundle id |
| `3` / `-3` | License expired |
| `4` / `-4` | Not activated |
| `-5` | Init / model load failed |
| `-10` | Invalid argument |
| `-11` | Invalid image |
| `-12` | No face |
| `-13` | No document |
| `-16` | Liveness failed (when gated) |

Serialize native SDK calls on **one background thread**. The engine is not concurrent.


## API reference — mobile face SDK

Prefer **`FaceRecognitionClient`** (Android kit) / the matching iOS kit wrappers. Serialize all engine calls on one queue.

### Lifecycle

| API | Purpose |
| --- | --- |
| `activate(license)` | Activate + init on a worker thread; completion returns status code |
| `deactivate()` / `release()` | Tear down engine |
| `getLicenseStatus()` | Current license flags |
| `allowsRecognition()` / `allowsLiveness()` | Capability checks |

### Still-image recognition

| API | Purpose |
| --- | --- |
| `detect(bitmap, crop?, flags?)` | Detect faces; JSON string with regions / landmarks / traits |
| `faceDetection(bitmap, param?)` | Typed `FaceBox` list |
| `templateExtraction(bitmap, face)` | Template bytes for one face box |
| `extractFeature(bitmap)` | Feature bytes (largest / primary face helpers) |
| `similarity(feature1, feature2)` | 1:1 score between templates |
| `quality(bitmap, crop?)` | Quality attributes JSON |
| `setLandmarkMode(14\|68)` | Landmark density |

### Gallery (on-device 1:N)

| API | Purpose |
| --- | --- |
| `enroll(name, feature, thumbnail?)` | Store person locally |
| `bestMatch(feature, threshold)` | 1:N search |
| `enrolledPeople()` / `removeEnrolled` / `clearEnrolled` | Gallery management |
| `syncDatabase(matchThreshold)` | Push templates into VideoWorker DB |

### Live camera (VideoWorker)

| API | Purpose |
| --- | --- |
| `startVideoWorker(config)` | Start tracking / identify session |
| `addFrame(bitmap)` | Push camera frames |
| `setVideoWorkerEventHandler` | Receive track / match / liveness events (JSON) |
| `stopVideoWorker()` | Stop session |
| `makeTrackingConfig` / `makeIdentityConfig` | Build configs (passive / active liveness options when licensed) |

### Passive liveness

When the license includes liveness, still-image detect/quality paths and VideoWorker configs can return passive 2D scores. Use `passive2DVerdict` helpers in the kit. Without the entitlement, treat missing scores as **not run**, not as pass.

### Integration checklist

1. Apply `install.gradle` (Android) or vendor iOS frameworks from Release.
2. `FaceRecognitionClient.get(context).activate(license) { code -> … }`.
3. On `0`, enable camera modes.
4. Enroll → Identify, or Capture / Attribute for still flows.
5. Persist templates in **your** database if you leave the demo gallery.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Invalid license | Application / bundle id must match the key; server needs the correct machine code |
| Init failed | Runtime AAR/framework/`lib` missing or wrong ABI |
| No face / no document | Lighting, crop, distance; try still gallery image first |
| Liveness / authenticity empty | License flag off — request the matching entitlement |
| Camera black / crash | Use a **physical** device; grant camera permission |
| Docker license fails after bare-metal license | Machine codes differ — re-license the container |

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


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

The following is adapted from the shipping repository README for screenshots, exact commands, and platform-specific notes.

## <img src="https://cdn.simpleicons.org/apple/000000" width="32" height="32" alt="" /> Identixia Face Recognition — iOS

**On-device face recognition SDK** for iPhone: enroll, **1:N identification**, capture, attributes, and optional **passive face liveness**. Face template matching stays on device — Identixia cloud never sees your biometric frames. Built for private KYC selfie flows and on-device galleries.

Demo modes: **Enroll · Identify · Capture · Attribute**.

<p><img src="https://img.shields.io/badge/On-device-0F766E?style=flat-square" alt="On-device" /> <img src="https://img.shields.io/badge/1%3AN%20identification-0F766E?style=flat-square" alt="1%3AN%20identification" /> <img src="https://img.shields.io/badge/Passive%20liveness-0F766E?style=flat-square" alt="Passive%20liveness" /> <img src="https://img.shields.io/badge/Face%20templates-0F766E?style=flat-square" alt="Face%20templates" /> <img src="https://img.shields.io/badge/KYC%20ready-5A6573?style=flat-square" alt="KYC%20ready" /></p>

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Read this once before cloning. Mobile demos ship a **bundled license** for the sample application / bundle id. Production apps need a new key from Identixia. [Initial commands](#-initial-commands) lists clone → place runtime → run → activate options.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face recognition SDK** for iOS |
| **Modes** | Enroll · Identify (1:N) · Capture · Attribute · optional passive liveness |
| **Runtime zip** | Three frameworks at repo root from Drive zip `PENDING` |
| **Demo id / license** | `com.identixia.facerecognitionsdk` — use the sample id with the bundled demo license |
| **Activate** | Sample app: keep the demo id and bundled key. Your app: new applicationId / bundle id → [contact](#-contact) → call the SDK activate API (see docs). |
| **Tools** | **Xcode 15+** · physical **iPhone** |
| **UI** | Four demo modes after Ready |
| **Privacy** | Templates stay on device — no Identixia cloud |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

Clone the sample, place the runtime, and run it.

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Clone and place the runtime

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS.git
cd FaceRecognition-LivenessDetection-iOS
```

Download the runtime zip (`PENDING`) and place at repo root:

```text
facerecognitionsdk.framework
FaceRecognitionEngine.framework
onnxruntime.framework
```

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Run the demo

Open `FaceRecognitionSDK.xcodeproj` → Signing Team → Run on a physical iPhone.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> Activate / license

Please [contact us](#-contact) to get a license for your own app. The sample already includes a demo license for its application id.

### <img src="https://img.shields.io/badge/-4-0F766E?style=for-the-badge" alt="" /> First capture

Wait until Home status = **Ready**, then use Camera / Gallery (or the face mode tiles). Confirm Result / About shows a licensed state before integrating into your own app.

---

## <img src="https://api.iconify.design/lucide/list-checks.svg?color=%230F766E" width="24" height="24" alt="" /> What you get

| Capability | What it does |
| --- | --- |
| <img src="https://api.iconify.design/lucide/user-plus.svg?color=%230F766E" width="16" height="16" alt="" /> Enroll | Capture face templates into an on-device gallery |
| <img src="https://api.iconify.design/lucide/users.svg?color=%230F766E" width="16" height="16" alt="" /> Identify (1:N) | Match a live or still face against enrolled templates |
| <img src="https://api.iconify.design/lucide/aperture.svg?color=%230F766E" width="16" height="16" alt="" /> Capture | Guided still capture with quality feedback |
| <img src="https://api.iconify.design/lucide/sliders.svg?color=%230F766E" width="16" height="16" alt="" /> Attribute | Age / gender / expression-style attributes when enabled |
| <img src="https://api.iconify.design/lucide/shield.svg?color=%230F766E" width="16" height="16" alt="" /> Passive liveness | Optional face PAD (and deepfake checks when licensed on server) |
| <img src="https://api.iconify.design/lucide/fingerprint.svg?color=%230F766E" width="16" height="16" alt="" /> Templates | Compact face template extraction + similarity / matching |

---

## <img src="https://api.iconify.design/lucide/app-window.svg?color=%230F766E" width="24" height="24" alt="" /> Demo modes

| Mode | What to try |
| --- | --- |
| **Enroll** | Store an on-device face template |
| **Identify** | Live 1:N against enrolled people |
| **Capture** | Guided still capture |
| **Attribute** | Attribute readout when enabled |

---

## <img src="https://api.iconify.design/lucide/pc-case.svg?color=%230F766E" width="24" height="24" alt="" /> Requirements

| | |
| --- | --- |
| Device | Physical **iPhone** |
| Tools | **Xcode 15+** |
| Demo bundle id | `com.identixia.facerecognitionsdk` |
| Frameworks | `facerecognitionsdk` · `FaceRecognitionEngine` · `onnxruntime` |

---

## <img src="https://api.iconify.design/lucide/package.svg?color=%230F766E" width="24" height="24" alt="" /> Runtime zip

> **Google Drive (single zip):** `PENDING`

Unzip to the repo root (siblings of the Xcode project):

```text
facerecognitionsdk.framework
FaceRecognitionEngine.framework
onnxruntime.framework
```

---

## <img src="https://api.iconify.design/lucide/rocket.svg?color=%230F766E" width="24" height="24" alt="" /> Run

```text
1. git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS.git
2. Place the three frameworks at the repo root
3. Open FaceRecognitionSDK.xcodeproj → set Signing Team
4. Keep bundle id com.identixia.facerecognitionsdk for the demo license
5. Run on a physical iPhone → Enroll / Identify / Capture / Attribute
```

---

## <img src="https://api.iconify.design/lucide/key-round.svg?color=%230F766E" width="24" height="24" alt="" /> License

| | |
| --- | --- |
| Demo bundle id | `com.identixia.facerecognitionsdk` |
| Capabilities | Face recognition and/or passive face liveness |

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/blob/a83d7d82046d388e6d58c78579f0453d4b4d141a/FaceRecognitionSDK/Home/ViewController.swift#L8-L10](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/blob/a83d7d82046d388e6d58c78579f0453d4b4d141a/FaceRecognitionSDK/Home/ViewController.swift#L8-L10)

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/blob/a83d7d82046d388e6d58c78579f0453d4b4d141a/FaceRecognitionSDK/Home/ViewController.swift#L167-L191](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/blob/a83d7d82046d388e6d58c78579f0453d4b4d141a/FaceRecognitionSDK/Home/ViewController.swift#L167-L191)

Please [contact us](#-contact) to get a license for **your own app**.

---

## <img src="https://api.iconify.design/lucide/puzzle.svg?color=%230F766E" width="24" height="24" alt="" /> Use in your app

Link the three frameworks, activate → init, then detect / template / match (and liveness when licensed). Do not ship a production key against the demo bundle id. See [docs](https://doc.identixia.com).

---

## <img src="https://api.iconify.design/lucide/images.svg?color=%230F766E" width="24" height="24" alt="" /> Screenshots

<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/home.png" width="160" alt="Face recognition home — detect, attribute, quality, landmarks, match, liveness, enroll, identity" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/capture.png" width="160" alt="Identity camera — move closer" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/enroll.png" width="160" alt="Enroll result" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/identify.png" width="160" alt="1:N identify result" />
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/detect.png" width="160" alt="Face detect result" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute.png" width="160" alt="Face attribute result" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute-quality.png" width="160" alt="Image quality result" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/landmarks.png" width="160" alt="68-point landmarks" />
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/match.png" width="160" alt="1:1 match result" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute-liveness.png" width="160" alt="Liveness result" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/settings.png" width="160" alt="Settings — camera, landmarks, thresholds" />
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/about.png" width="160" alt="About, license, and application id" />
</p>

---

## <img src="https://api.iconify.design/lucide/layers.svg?color=%230F766E" width="24" height="24" alt="" /> Platforms

| | Platform | Repo |
| --- | --- | --- |
| <img src="https://cdn.simpleicons.org/android/3DDC84" width="18" height="18" alt="" /> | Android | [FaceRecognition-LivenessDetection-Android](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| <img src="https://cdn.simpleicons.org/apple/000000" width="18" height="18" alt="" /> | iOS | [FaceRecognition-LivenessDetection-iOS](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| <img src="https://cdn.simpleicons.org/flutter/02569B" width="18" height="18" alt="" /> | Flutter | [FaceRecognition-LivenessDetection-Flutter](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| <img src="https://cdn.simpleicons.org/react/61DAFB" width="18" height="18" alt="" /> | React Native | [FaceRecognition-LivenessDetection-React-Native](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) |
| <img src="https://cdn.simpleicons.org/ionic/3880FF" width="18" height="18" alt="" /> | Ionic Capacitor | [FaceRecognition-LivenessDetection-Ionic-Capacitor](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| <img src="https://cdn.simpleicons.org/apachecordova/E8E8E8" width="18" height="18" alt="" /> | Ionic Cordova | [FaceRecognition-LivenessDetection-Ionic-Cordova](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| <img src="https://cdn.simpleicons.org/windows/0078D4" width="18" height="18" alt="" /> | Windows | [FaceRecognition-LivenessDetection-Windows](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) |
| <img src="https://cdn.simpleicons.org/docker/2496ED" width="18" height="18" alt="" /> | Linux / Docker | [FaceRecognition-LivenessDetection-Docker](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) |

---
