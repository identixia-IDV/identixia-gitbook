---
description: >-
  Face recognition SDK for Android. On-device enrollment, 1:N identification, and face attributes for KYC, plus passive liveness when the license includes it.
icon: mobile
---

# Face SDK — Android


## Overview

Face recognition SDK for Android. On-device enrollment, 1:N identification, and face attributes for KYC, plus passive liveness when the license includes it.

Processing runs **on the device**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`FaceRecognition-LivenessDetection-Android`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| **Platform** | Android |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android" %}

[`identixia-IDV/FaceRecognition-LivenessDetection-Android`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) · [Releases](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/releases/latest)

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
| IDE | Android Studio |
| JDK | **17** |
| Device | Physical **arm64** phone for camera demos |
| minSdk | 24+ |
| ABIs | `arm64-v8a`, `armeabi-v7a` |
| Packaging | `jniLibs { useLegacyPackaging = true }` |

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
| **Release asset** | `facefullsdk-android.zip` (contains `facefullsdk.aar` + `databases/*.xdb`) |
| **Local path after download** | `libfacesdk/facefullsdk.aar` and `libfacesdk/databases/*.xdb` |
| **Databases** | Required packs: `recognition.xdb`, `recognition-common.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb`, and when licensed `recognition-liveness.xdb` + `recognition-deepfake.xdb`. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/releases/latest/download/<asset>
```

Unzip so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android.git
cd FaceRecognition-LivenessDetection-Android
```

### 2. Download and place the runtime

See [Download and place the runtime](#download-and-place-the-runtime) below. From the repository root:

```bash
python scripts/get_runtime.py
```

### 3. Run the demo

Open this folder in **Android Studio** (JDK **17**) and run on a physical **arm64** phone.

Wait until Home status shows **Ready** before opening camera modes.

### 4. Activate and try every mode

1. Confirm Home / About shows a licensed **Ready** state (sample apps ship a demo key for the sample application id only).
2. Exercise each demo tile once (enroll, identify, capture, attribute, liveness, document front/back, result).
3. For your own app: request a license for **your** application id / bundle id, then call activate → init on a background thread.

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

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/home.png" alt="Home" width="150"><figcaption>Home</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/capture.png" alt="Capture" width="150"><figcaption>Capture</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/enroll.png" alt="Enroll" width="150"><figcaption>Enroll</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/identify.png" alt="Identify" width="150"><figcaption>Identify</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/detect.png" alt="Detect" width="150"><figcaption>Detect</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute.png" alt="Attributes" width="150"><figcaption>Attributes</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute-quality.png" alt="Quality" width="150"><figcaption>Quality</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/landmarks.png" alt="Landmarks" width="150"><figcaption>Landmarks</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/match.png" alt="Match" width="150"><figcaption>Match</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute-liveness.png" alt="Liveness" width="150"><figcaption>Liveness</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/settings.png" alt="Settings" width="150"><figcaption>Settings</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/about.png" alt="About" width="150"><figcaption>About</figcaption></figure>

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/FaceRecognition-LivenessDetection-Android`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/releases/latest) |
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

## Identixia Face Recognition — Android

**On-device face recognition SDK** for Android: enroll, **1:N identification**, guided capture, attributes, and optional **passive face liveness + deepfake** (authenticity REAL only if both pass). Face template matching and images stay on the phone — nothing is sent to Identixia cloud. Use it for KYC selfie checks, workforce access, or private 1:N galleries without a biometrics SaaS hop.

Modes in the demo: **Enroll · Identify · Capture · Attribute**.

> For setup, integration, and API guides, see the [Identixia documentation](https://docs.identixia.com/developers/face-sdk/android). This page covers the sample repository.

## Basics

Read this once before cloning. Mobile demos ship a **bundled license** for the sample application / bundle id. Production apps need a new key from Identixia. [Initial commands](#-initial-commands) lists clone → place runtime → run → activate options.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face recognition SDK** for Android |
| **Modes** | Enroll · Identify (1:N) · Capture · Attribute · optional passive liveness |
| **Runtime zip** | `install.gradle` uses `libfacefullsdk/` when `facefullsdk.aar` is already in this repo |
| **Demo id / license** | `com.identixia.facefullsdk` — use the sample id with the bundled demo license |
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
python scripts/get_runtime.py
```

The sample applies `install.gradle`. When `libfacefullsdk/facefullsdk.aar` is already in the clone, that is the engine the app builds with.

Open this folder in **Android Studio** (JDK 17) → Run on a physical **arm64** device.

Please [contact us](#-contact) to get a license for your own app. The sample already includes a demo license for its application id.

Wait until Home status = **Ready**, then use Camera / Gallery (or the face mode tiles). Confirm Result / About shows a licensed state before integrating into your own app.

---

## What you get

| Capability | What it does |
| --- | --- |

## Requirements

| | |
| --- | --- |
| Device | Physical **arm64** Android phone (camera demos) |
| Tools | Android Studio, **JDK 17** |
| Demo `applicationId` | `com.identixia.facefullsdk` |
| Runtime | `facefullsdk.aar` in `libfacefullsdk/` |

---

## Install

The sample builds with the AAR already in `libfacefullsdk/`. Your own app adds one line to the app module:

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/main/install.gradle'
```

That one line pulls the **engine** (`facefullsdk.aar`) and the reusable **kit** (`libfacekit`: `FaceRecognitionClient`, `CameraPreview`, `ModeAnalyzer`, `FaceJson`, …). Prefer the kit over calling `FaceFullSDK` directly.

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
| Demo id | `com.identixia.facefullsdk` |
| Capabilities | Face recognition (detect / templates / match) and/or passive face liveness + deepfake |

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/e8782d9082a02bddd139bf90abcc8ac737ecda4b/app/src/main/java/com/identixia/facefullsdk/ui/MainActivity.kt#L34-L36](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/e8782d9082a02bddd139bf90abcc8ac737ecda4b/app/src/main/java/com/identixia/facefullsdk/ui/MainActivity.kt#L34-L36)

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/e8782d9082a02bddd139bf90abcc8ac737ecda4b/app/src/main/java/com/identixia/facefullsdk/ui/MainActivity.kt#L105-L122](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android/blob/e8782d9082a02bddd139bf90abcc8ac737ecda4b/app/src/main/java/com/identixia/facefullsdk/ui/MainActivity.kt#L105-L122)

Please [contact us](#-contact) to get a license for **your own app**.

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
