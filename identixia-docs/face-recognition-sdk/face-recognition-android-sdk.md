---
description: >-
  On-device face recognition SDK for Android: enrollment, 1:N identification, and face attributes. Passive liveness is available when the license allows it.
---

# Face Recognition Android SDK


## Overview

On-device face recognition SDK for Android: enrollment, 1:N identification, and face attributes. Passive liveness is available when the license allows it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `FaceRecognition-LivenessDetection-Android` |
| **Platform** | Android |
| **Docs site** | [doc.identixia.com](https://doc.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android" %}

Source: [`identixia-IDV/FaceRecognition-LivenessDetection-Android`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android)

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
| IDE | Android Studio |
| JDK | **17** |
| Device | Physical **arm64** phone for camera demos |
| minSdk | 24+ |
| ABIs | `arm64-v8a`, `armeabi-v7a` |
| Packaging | `jniLibs { useLegacyPackaging = true }` |

## Quick start

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android.git
cd FaceRecognition-LivenessDetection-Android
```

### 2. Place the runtime

Engine zip/AAR/framework from GitHub Releases (`/releases/latest/download/…`) or the files already under `libfacesdk` / Frameworks when present.

Clients should download versioned assets via:

```text
https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/releases/latest/download/<asset>
```

### 3. Run the demo

Follow the repository **Run** section (Android Studio / Xcode / `flutter run` / `yarn android` / Ionic). Wait until status shows **Ready** before opening camera modes.

### 4. Try every demo mode

Use each tile / screen once (enroll, identify, capture, document front/back, result, about). Confirm license state on the About / Result screen.

### Add the SDK to your own Android app

In the **app** module `build.gradle`:

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/main/install.gradle'
```

That line pulls the engine and, for face recognition, the reusable **kit** (`libfacekit`: `FaceRecognitionClient`, camera helpers, JSON parsers). Prefer the kit over calling the raw SDK class directly.


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

## <img src="https://cdn.simpleicons.org/android/3DDC84" width="32" height="32" alt="" /> Identixia Face Recognition — Android

**On-device face recognition SDK** for Android: enroll, **1:N identification**, guided capture, attributes, and optional **passive face liveness**. Face template matching and images stay on the phone — nothing is sent to Identixia cloud. Use it for KYC selfie checks, workforce access, or private 1:N galleries without a biometrics SaaS hop.

Modes in the demo: **Enroll · Identify · Capture · Attribute**.

<p><img src="https://img.shields.io/badge/On-device-0F766E?style=flat-square" alt="On-device" /> <img src="https://img.shields.io/badge/1%3AN%20identification-0F766E?style=flat-square" alt="1%3AN%20identification" /> <img src="https://img.shields.io/badge/Passive%20liveness-0F766E?style=flat-square" alt="Passive%20liveness" /> <img src="https://img.shields.io/badge/Face%20templates-0F766E?style=flat-square" alt="Face%20templates" /> <img src="https://img.shields.io/badge/KYC%20ready-5A6573?style=flat-square" alt="KYC%20ready" /></p>

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Read this once before cloning. Mobile demos ship a **bundled license** for the sample application / bundle id. Production apps need a new key from Identixia. [Initial commands](#-initial-commands) lists clone → place runtime → run → activate options.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face recognition SDK** for Android |
| **Modes** | Enroll · Identify (1:N) · Capture · Attribute · optional passive liveness |
| **Runtime zip** | `install.gradle` uses `libfacesdk/` when `facerecognitionsdk.aar` is already in this repo |
| **Demo id / license** | `com.identixia.facerecognitionsdk` — use the sample id with the bundled demo license |
| **Activate** | Sample app: keep the demo id and bundled key. Your app: new applicationId / bundle id → [contact](#-contact) → call the SDK activate API (see docs). |
| **Tools** | Android Studio · **JDK 17** · physical **arm64** phone |
| **UI** | Four demo modes after SDK Ready |
| **Privacy** | Templates stay on device — no Identixia cloud |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

Clone the sample, place the runtime, and run it.

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Clone and place the runtime

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android.git
cd FaceRecognition-LivenessDetection-Android
```

The sample applies `install.gradle`. When `libfacesdk/facerecognitionsdk.aar` is already in the clone, that is the engine the app builds with.

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Run the demo

Open this folder in **Android Studio** (JDK 17) → Run on a physical **arm64** device.

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
| **Enroll** | Capture a face and store a template + thumbnail on device |
| **Identify** | Live 1:N search against the enrolled gallery |
| **Capture** | Guided still capture with quality feedback |
| **Attribute** | Read attribute scores when enabled by the engine / license |

---

## <img src="https://api.iconify.design/lucide/pc-case.svg?color=%230F766E" width="24" height="24" alt="" /> Requirements

| | |
| --- | --- |
| Device | Physical **arm64** Android phone (camera demos) |
| Tools | Android Studio, **JDK 17** |
| Demo `applicationId` | `com.identixia.facerecognitionsdk` |
| Runtime | `facerecognitionsdk.aar` in `libfacesdk/` |

---

## <img src="https://api.iconify.design/lucide/package.svg?color=%230F766E" width="24" height="24" alt="" /> Install

The sample builds with the AAR already in `libfacesdk/`. Your own app adds one line to the app module:

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/main/install.gradle'
```

That one line pulls the **engine** (`facerecognitionsdk.aar`) and the reusable **kit** (`libfacekit`: `FaceRecognitionClient`, `CameraPreview`, `ModeAnalyzer`, `FaceJson`, …). Prefer the kit over calling `FaceRecognitionSDK` directly.

Keep `minSdk 24`, `abiFilters` `arm64-v8a` and `armeabi-v7a`, and `packaging { jniLibs { useLegacyPackaging = true } }`. Then `FaceRecognitionClient.activate` → modes / detect / template / identify. The license key must match the app `applicationId`.

---

## <img src="https://api.iconify.design/lucide/rocket.svg?color=%230F766E" width="24" height="24" alt="" /> Run

```text
1. git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android.git
2. Open the cloned folder in Android Studio (JDK 17)
3. Run on a physical arm64 device
4. Wait until the SDK is Ready → Enroll / Identify / Capture / Attribute
```

---

## <img src="https://api.iconify.design/lucide/key-round.svg?color=%230F766E" width="24" height="24" alt="" /> License

| | |
| --- | --- |
| Demo id | `com.identixia.facerecognitionsdk` |
| Capabilities | Face recognition (detect / templates / match) and/or passive face liveness |

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/0548789a620a66936b15bb30d297557cb10b03d3/app/src/main/java/com/identixia/facerecognitionsdk/ui/MainActivity.kt#L34-L36](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/0548789a620a66936b15bb30d297557cb10b03d3/app/src/main/java/com/identixia/facerecognitionsdk/ui/MainActivity.kt#L34-L36)

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/0548789a620a66936b15bb30d297557cb10b03d3/app/src/main/java/com/identixia/facerecognitionsdk/ui/MainActivity.kt#L105-L122](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/0548789a620a66936b15bb30d297557cb10b03d3/app/src/main/java/com/identixia/facerecognitionsdk/ui/MainActivity.kt#L105-L122)

Please [contact us](#-contact) to get a license for **your own app**.

---

## <img src="https://api.iconify.design/lucide/puzzle.svg?color=%230F766E" width="24" height="24" alt="" /> Use in your app

1. In the app module, apply `install.gradle` (see Install above) — engine + `libfacekit`.
2. Activate with your license → init.
3. Prefer kit capture / identify helpers; call detect / template / similarity when you need lower-level APIs.
4. Keep the demo `applicationId` only while using the sample license.

See [docs](https://doc.identixia.com).

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
