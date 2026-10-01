---
description: >-
  On-device face recognition SDK for Android: enrollment, 1:N identification, and face attributes. Passive liveness is available when the license allows it.
---

# Face SDK — Android


## Overview

On-device face recognition SDK for Android: enrollment, 1:N identification, and face attributes. Passive liveness is available when the license allows it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `FaceRecognition-LivenessDetection-Android` |
| **Platform** | Android |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


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
| Android (full) | [Android](android.md) |
| iOS (full) | [iOS](ios.md) |
| Flutter (full) | [Flutter](flutter.md) |
| React Native (full) | [React Native](react-native.md) |
| Ionic Capacitor (full) | [Ionic Capacitor](ionic-capacitor.md) |
| Ionic Cordova (full) | [Ionic Cordova](ionic-cordova.md) |
| Windows (full) | [Windows](windows.md) |
| Linux / Docker (full) | [Linux / Docker](linux-docker.md) |
| Windows (recognition only) | [Recognition Windows](recognition-windows.md) |
| Linux (recognition only) | [Recognition Linux / Docker](recognition-linux-docker.md) |
| Liveness-only | [Android](liveness-android.md) · [iOS](liveness-ios.md) · [Windows](liveness-windows.md) · [Docker](liveness-linux-docker.md) |
| Function guides | [Recognition](recognition.md) · [Liveness](liveness.md) |

## Screenshots

<figure><img src="../.gitbook/assets/face-android-home.png" alt="Home" width="150"><figcaption>Home</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-capture.png" alt="Capture" width="150"><figcaption>Capture</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-enroll.png" alt="Enroll" width="150"><figcaption>Enroll</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-identify.png" alt="Identify" width="150"><figcaption>Identify</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-detect.png" alt="Detect" width="150"><figcaption>Detect</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-attribute.png" alt="Attributes" width="150"><figcaption>Attributes</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-quality.png" alt="Quality" width="150"><figcaption>Quality</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-landmarks.png" alt="Landmarks" width="150"><figcaption>Landmarks</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-match.png" alt="Match" width="150"><figcaption>Match</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-liveness.png" alt="Liveness" width="150"><figcaption>Liveness</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-settings.png" alt="Settings" width="150"><figcaption>Settings</figcaption></figure>

<figure><img src="../.gitbook/assets/face-android-about.png" alt="About" width="150"><figcaption>About</figcaption></figure>


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

Adapted from the shipping repository README for exact commands and platform-specific notes. Screenshots above use the current Identixia asset pack.

## Identixia Face Recognition — Android

**On-device face recognition SDK** for Android: enroll, **1:N identification**, guided capture, attributes, and optional **passive face liveness**. Face template matching and images stay on the phone — nothing is sent to Identixia cloud. Use it for KYC selfie checks, workforce access, or private 1:N galleries without a biometrics SaaS hop.

Modes in the demo: **Enroll · Identify · Capture · Attribute**.

---

## Basics

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

## Initial commands

Clone the sample, place the runtime, and run it.

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android.git
cd FaceRecognition-LivenessDetection-Android
```

The sample applies `install.gradle`. When `libfacesdk/facerecognitionsdk.aar` is already in the clone, that is the engine the app builds with.

Open this folder in **Android Studio** (JDK 17) → Run on a physical **arm64** device.

Please [contact us](#-contact) to get a license for your own app. The sample already includes a demo license for its application id.

Wait until Home status = **Ready**, then use Camera / Gallery (or the face mode tiles). Confirm Result / About shows a licensed state before integrating into your own app.

---

## What you get

| Capability | What it does |
| --- | --- |

---

## Demo modes

| Mode | What to try |
| --- | --- |
| **Enroll** | Capture a face and store a template + thumbnail on device |
| **Identify** | Live 1:N search against the enrolled gallery |
| **Capture** | Guided still capture with quality feedback |
| **Attribute** | Read attribute scores when enabled by the engine / license |

---

## Requirements

| | |
| --- | --- |
| Device | Physical **arm64** Android phone (camera demos) |
| Tools | Android Studio, **JDK 17** |
| Demo `applicationId` | `com.identixia.facerecognitionsdk` |
| Runtime | `facerecognitionsdk.aar` in `libfacesdk/` |

---

## Install

The sample builds with the AAR already in `libfacesdk/`. Your own app adds one line to the app module:

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/main/install.gradle'
```

That one line pulls the **engine** (`facerecognitionsdk.aar`) and the reusable **kit** (`libfacekit`: `FaceRecognitionClient`, `CameraPreview`, `ModeAnalyzer`, `FaceJson`, …). Prefer the kit over calling `FaceRecognitionSDK` directly.

Keep `minSdk 24`, `abiFilters` `arm64-v8a` and `armeabi-v7a`, and `packaging { jniLibs { useLegacyPackaging = true } }`. Then `FaceRecognitionClient.activate` → modes / detect / template / identify. The license key must match the app `applicationId`.

---

## Run

```text
1. git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android.git
2. Open the cloned folder in Android Studio (JDK 17)
3. Run on a physical arm64 device
4. Wait until the SDK is Ready → Enroll / Identify / Capture / Attribute
```

---

## License

| | |
| --- | --- |
| Demo id | `com.identixia.facerecognitionsdk` |
| Capabilities | Face recognition (detect / templates / match) and/or passive face liveness |

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/2f42e2b49afea2ae5accb93a23a365b04ddbffbe/app/src/main/java/com/identixia/facerecognitionsdk/ui/MainActivity.kt#L34-L36](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/2f42e2b49afea2ae5accb93a23a365b04ddbffbe/app/src/main/java/com/identixia/facerecognitionsdk/ui/MainActivity.kt#L34-L36)

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/2f42e2b49afea2ae5accb93a23a365b04ddbffbe/app/src/main/java/com/identixia/facerecognitionsdk/ui/MainActivity.kt#L105-L122](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/2f42e2b49afea2ae5accb93a23a365b04ddbffbe/app/src/main/java/com/identixia/facerecognitionsdk/ui/MainActivity.kt#L105-L122)

Please [contact us](#-contact) to get a license for **your own app**.

---

## Use in your app

1. In the app module, apply `install.gradle` (see Install above) — engine + `libfacekit`.
2. Activate with your license → init.
3. Prefer kit capture / identify helpers; call detect / template / similarity when you need lower-level APIs.
4. Keep the demo `applicationId` only while using the sample license.

See [docs](https://docs.identixia.com).

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

---
