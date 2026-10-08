---
description: >-
  Face recognition SDK for Flutter on Android and iOS. Enrollment, 1:N identification, and face attributes for KYC, plus passive liveness when licensed.
icon: layer-group
---

# Face SDK — Flutter


## Overview

Face recognition SDK for Flutter on Android and iOS. Enrollment, 1:N identification, and face attributes for KYC, plus passive liveness when licensed.

Processing runs **on the device**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`FaceRecognition-LivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| **Platform** | Flutter |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter" %}

[`identixia-IDV/FaceRecognition-LivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) · [Releases](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Face detection | Bounding box, landmarks, and pose |
| Attributes | Age, gender, and related traits when enabled |
| Quality | ICAO-style image and face quality scores |
| Templates | Compact feature vectors stored in **your** database |
| 1:1 match | Compare two images or two templates |
| 1:N identify | Enroll a gallery and search (mobile VideoWorker / server gallery) |
| Passive liveness + deepfake | PAD and deepfake together when the license includes `liveness`; REAL only if both pass |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Flutter | Stable channel, recent SDK |
| Android | JDK 17, physical arm64 device |
| iOS | Xcode + CocoaPods; physical iPhone |
| Bootstrap | Run the sample `tool/bootstrap.dart` / `pod install` as documented in the repo |

## Download and place the runtime

Native engines and model databases are **not** stored in git. Every product ships `scripts/get_runtime.py`, which downloads the correct GitHub Release assets and places them where the sample expects.

### Download (recommended)

```bash
python scripts/get_runtime.py
```

To pin a specific Release tag:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

| | |
| --- | --- |
| **Release asset** | Android `facefullsdk.aar` zip + iOS face zip (from the paired Android / iOS product Releases) |
| **Local path after download** | See the sample paths in the repository README (`example/android/libfacesdk/facefullsdk.aar`, `ios/Frameworks/…`) |
| **Databases** | Do not skip database packs — `get_runtime.py` verifies required `*.xdb` files after download. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter/releases/latest/download/<asset>
```

Unzip so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter.git
cd FaceRecognition-LivenessDetection-Flutter
```

### 2. Download and place the runtime

See [Download and place the runtime](#download-and-place-the-runtime) below. From the repository root:

```bash
python scripts/get_runtime.py
```

### 3. Run the demo

```bash
dart run tool/bootstrap.dart
cd example && flutter run
```

Use a physical device for camera demos.

### 4. Activate and try every mode

1. Confirm Home / About shows a licensed **Ready** state (sample apps ship a demo key for the sample application id only).
2. Exercise each demo tile once (enroll, identify, capture, attribute, liveness, document front/back, result).
3. For your own app: request a license for **your** application id / bundle id, then call activate → init on a background thread.


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

Prefer **`FaceRecognitionClient`** (Android kit) / the matching iOS kit wrappers. Flutter, React Native, and Ionic expose the **same method names** as Android (`detect`, `faceDetection`, `liveness`, `livenessAll`, …). Serialize all engine calls on **one background thread**.

### Lifecycle

| API | Purpose |
| --- | --- |
| `setActivation(license)` / kit `activate(license)` | Activate (+ init) on a worker thread |
| `init()` | Load models when not bundled into activate |
| `deinit()` / `deactivate()` / `release()` | Tear down engine |
| `getMachineCode()` | Offline machine / app fingerprint helpers |
| `getLicenseStatus()` | Current license flags |
| `allowsRecognition()` / `allowsLiveness()` | Capability checks |

### Still-image recognition

| API | Purpose | Closest HTTP route |
| --- | --- | --- |
| `detect(image, crop?, flags?)` | Detect faces; JSON with regions / landmarks / traits | `POST /api/face/analyze` |
| `faceDetection(image, param?)` | Typed `FaceBox` list / JSON boxes | `POST /api/face/boxes` |
| `faceDetect` / `faceAttribute` / `imageQuality` / `landmarks` | Focused still helpers (plugin channels) | `/api/face/traits`, `/image-quality`, `/landmarks` |
| `match(image1, image2)` | 1:1 image compare | `POST /api/face/compare` |
| `templateExtraction(image, face)` | Template bytes for one face box | `POST /api/face/template` |
| `extractFeature(image)` | Feature bytes (largest / primary face) | `POST /api/face/template` |
| `similarity(feature1, feature2)` | 1:1 score between templates | `POST /api/face/score` |
| `quality(image, crop?)` | Quality attributes JSON | `POST /api/face/quality` |
| `setLandmarkMode(14\|68)` | Landmark density | — |

### Passive liveness + deepfake (when licensed)

| API | Purpose | Closest HTTP route |
| --- | --- | --- |
| `liveness(image)` | PAD + deepfake | `POST /api/face/liveness` |
| `livenessAll(image)` | Same as `liveness`, high-accuracy pack | `POST /api/face/liveness` |
| `deepfake(image)` | Deepfake-only still check | `POST /api/face/deepfake` |

Treat authenticity as **REAL** only when both PAD and deepfake say real. Without the entitlement, treat missing scores as **not run**, not as pass.

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
| `addFrame` / live-frame helpers | Push camera frames |
| `setVideoWorkerEventHandler` | Receive track / match / liveness events (JSON) |
| `stopVideoWorker()` | Stop session |
| `makeTrackingConfig` / `makeIdentityConfig` | Build configs (passive / active liveness options when licensed) |

### Usage example (Android kit)

```kotlin
val client = FaceRecognitionClient.get(context)
client.activate(licenseKey) { code ->
    if (code != 0) return@activate
    // Worker thread: detect + match
    val json = client.detect(bitmap, /* crop */ false, /* flags */ 0)
    val score = client.match(bitmapA, bitmapB)
    val live = client.liveness(bitmap) // when licensed
}
```

### Usage example (plugin / Flutter / React Native / Ionic)

Call the same method names exposed by the plugin bridge (`activate` → `init` → `detect` / `match` / `liveness` / `enroll`). Keep camera preview on the UI thread; keep engine calls on a single background isolate / queue.

### Integration checklist

1. Download runtime with `python scripts/get_runtime.py` (or `install.gradle` on Android).
2. `FaceRecognitionClient.get(context).activate(license) { code -> … }` (or `setActivation` → `init` on plugins).
3. On `0`, enable camera modes.
4. Enroll → Identify, or Capture / Attribute / Liveness for still flows.
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

Keep the same license product line across stacks. From the [Face SDK](https://docs.identixia.com/face-sdk) hub:

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
| Function guides | [Recognition](https://docs.identixia.com/face-sdk/recognition) · [Liveness](https://docs.identixia.com/face-sdk/liveness) |

## Screenshots

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/flutter/camera.png" alt="Flutter camera" width="200"><figcaption>Flutter camera</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/flutter/result.png" alt="Flutter result" width="200"><figcaption>Flutter result</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/home.png" alt="Android home (same product family)" width="160"><figcaption>Android home (same product family)</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/identify.png" alt="Android identify" width="160"><figcaption>Android identify</figcaption></figure>

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/FaceRecognition-LivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter/releases/latest) |
| **Runtime helper** | `python scripts/get_runtime.py` in the product clone |
| **Documentation site** | [docs.identixia.com](https://docs.identixia.com) |
| **SDK Server (HTTP)** | [SDK Server](https://docs.identixia.com/sdk-server) |
| **Website** | [identixia.com](https://identixia.com) |
| **Hugging Face** | [huggingface.co/Identixia](https://huggingface.co/Identixia) |
| **Docker Hub** | [hub.docker.com/u/identixia](https://hub.docker.com/u/identixia) |
| **Playground** | [playground.identixia.com](https://playground.identixia.com/) |
| **License & support** | [Request a license](https://docs.identixia.com/guides/request-a-license-and-support) · [Contact](https://docs.identixia.com/guides/contact-us) |

Postman collections live under each product repository’s `postman/` folder (and the monorepo `postman/Identixia-API.postman_collection.json` for all HTTP routes).

## Next steps

1. Complete **Integration guide — start the project** until the sample shows **Ready**.
2. Confirm runtime files and databases are in place (`python scripts/get_runtime.py`).
3. Activate with a license issued for **your** application id or machine code.
4. Call only the APIs your license allows; treat missing flags as “not evaluated”, not as pass.
5. Return to the [Face SDK](https://docs.identixia.com/face-sdk) hub for recognition, liveness, and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use images from the identixia-assets repository.

## Identixia Face Recognition — Flutter

**On-device face recognition SDK** plugin: enroll, **1:N identification**, guided capture, attributes, and optional **passive face liveness + deepfake** (authenticity REAL only if both pass). Face template matching runs on the device — **no** biometric frames uploaded to Identixia cloud. Ideal for KYC selfie checks and private galleries inside your mobile app.

Package: `face_recognition_sdk`. Demo modes: **Enroll · Identify · Capture · Attribute**.

> For setup, integration, and API guides, see the [Identixia documentation](https://docs.identixia.com/developers/face-sdk/flutter). This page covers the sample repository.

## Basics

Read this once before cloning. Plugin demos ship a **bundled license** for the sample Android / iOS ids. Production apps need a new key. [Initial commands](#-initial-commands) lists clone → place runtime → run → activate options.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face recognition** Flutter plugin |
| **Modes** | Enroll · Identify (1:N) · Capture · Attribute |
| **API** | Detect · templates · identify · optional passive liveness |
| **Runtime** | Local example engines, or the `v1.0.0` GitHub Release when missing |
| **Demo id** | `com.identixia.facefullsdk` / `com.identixia.facefullsdk.app` |
| **Tools** | Flutter 3.44+ · physical arm64 Android / iPhone |
| **UI** | Four demo modes after Ready · package kit `FaceCapture` |
| **Privacy** | Templates stay on device — no Identixia cloud |

---

## Initial commands

Run **one** platform. Android and iOS are separate commands. Pasting both into one shell does not test both phones.

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter.git
cd FaceRecognition-LivenessDetection-Flutter
```

Native engines are already in the clone when this repository includes them. If a library file is missing, download the GitHub Release into the folders this sample expects:

```bash
python scripts/get_runtime.py
```

On macOS, if `python` is not found, run `python3 scripts/get_runtime.py`.

### Android

Use a physical **arm64** Android phone with USB debugging on. Flutter 3.44 or newer. The camera sample does not run on an emulator.

From the repository root:

```bash
dart run tool/bootstrap.dart
cd example
flutter devices
flutter run -d android
```

`flutter devices` prints the id of each connected phone. When more than one Android device is listed, pass that id instead of `android`.

### iOS

Use a Mac with Xcode, CocoaPods, and a physical **iPhone**. The camera sample does not run in the Simulator.

From the repository root:

```bash
dart run tool/bootstrap.dart
cd example
cd ios && pod install && cd ..
flutter devices
flutter run -d ios
```

When more than one iPhone is listed, pass that device id instead of `ios`.

Please [contact us](#-contact) to get a license for your own app. The sample already includes a demo license for its application id.

Wait until Home = **Ready**, then Enroll / Identify / Capture / Attribute.

---

## What you get

| Capability | What it does |
| --- | --- |

## Requirements

| | |
| --- | --- |
| Devices | Physical **arm64** Android and/or **iPhone** |
| Package | `face_recognition_sdk` |
| Runtimes | Local example engines, or the `v1.0.0` GitHub Release when they are missing |

---

## Install

The example builds with native runtimes already in the clone when present. Run `python scripts/get_runtime.py` (or pin `--tag 1.0.0`) to fetch GitHub Release engines when missing. Gradle may also download Latest when a file is absent.

- AAR → `example/android/libfacefullsdk/facefullsdk.aar`
- iOS → `ios/Frameworks/` (`facefullsdk`, `FaceRecognitionEngine`, `onnxruntime`)

Customer apps depend on `face_recognition_sdk` from this repo at tag `v1.0.0` (Flutter: git dependency; React Native / Ionic: npm / github package). Do **not** use a monorepo `path:` dependency in shipping apps.

Android: keep `packaging { jniLibs { useLegacyPackaging = true } }` so `libFaceRecognitionEngine.so` is extracted for `nativeInitEngine`.

---

## Run

Run **one** platform from the repository root. These are the same commands as [Initial commands](#-initial-commands).

**Android** — physical arm64 phone, USB debugging on:

```bash
dart run tool/bootstrap.dart
cd example
flutter devices
flutter run -d android
```

**iOS** — Mac, Xcode, CocoaPods, physical iPhone (not the Simulator):

```bash
dart run tool/bootstrap.dart
cd example
cd ios && pod install && cd ..
flutter devices
flutter run -d ios
```

---

## License

Demo ids: Android `com.identixia.facefullsdk` · iOS `com.identixia.facefullsdk.app`.

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter/blob/0126a661c391c61c1ac9e51314ef76579da1d7b4/example/lib/core/constants/license.dart#L6-L14](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter/blob/0126a661c391c61c1ac9e51314ef76579da1d7b4/example/lib/core/constants/license.dart#L6-L14)

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter/blob/0126a661c391c61c1ac9e51314ef76579da1d7b4/example/lib/services/sdk_service.dart#L28-L39](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter/blob/0126a661c391c61c1ac9e51314ef76579da1d7b4/example/lib/services/sdk_service.dart#L28-L39)

Capabilities: face recognition (detect / templates / match) and/or passive face liveness + deepfake. Please [contact us](#-contact) to get a license for **your own app**.

## API

The sample and your app use the same method names.

| API | What it returns |
| --- | --- |
| `activate(license)` then `init()` | Load the engine. Call both on one background thread. |
| `getLicenseStatus()` | Read flags before opening the camera. |
| `detect` / `faceAttribute` / `landmarks` | Still-image face, attributes, and landmarks. |
| `templateExtraction` / `similarity` | Template bytes and a 1:1 score. |
| `enroll` / `bestMatch` | On-device gallery and 1:N search. |
| `liveness` / `deepfake` | PAD and deepfake. REAL only if both pass. |

Camera frames stay on the UI thread. Engine calls stay on one background thread. The engine is not concurrent.

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

---

{% include "../.gitbook/includes/footer.md" %}
