---
description: >-
  Face recognition and liveness for iOS. Enrollment, templates, and 1:N search run on the device. Passive liveness runs when the license includes it.
icon: mobile-screen
---

# Face Recognition and Liveness Detection SDK for iOS


## Overview

Face recognition SDK for iOS. On-device enrollment, 1:N identification, and face attributes for KYC, plus passive liveness when the license includes it.

Processing runs **on the device**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| **Platform** | iOS |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS" %}

[`identixia-IDV/FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) · [Releases](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Face detection | Bounding box, landmarks, and pose |
| Attributes | Age, gender, and related traits when enabled |
| Quality | ICAO-style image and face quality scores |
| Templates | Numerical representations of faces that you can store in **your** database for comparison |
| 1:1 match | Compare two images or two templates |
| 1:N identify | Save face templates in a gallery, then search for the closest match using the platform's gallery API |
| Passive liveness + deepfake | Run presentation attack detection (PAD) and deepfake checks when the license includes `liveness`; report REAL only when both pass |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| IDE | Xcode (recent stable) |
| Device | Physical iPhone for camera demos |
| Deployment | iOS 13+ (see sample project) |
| Frameworks | Vendored `.framework` / `.xcframework` from Release or Drive pack |

## Download and place the runtime

Download the native SDK libraries and model files before running the sample. Use `scripts/get_runtime.py` to retrieve the required GitHub Release assets and place them in the sample's expected folders.

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
| **Release asset** | `facerecognitionsdk-ios.zip` (frameworks + `databases/*.xdb`) |
| **Local path after download** | Repository root / `Frameworks/` + `databases/*.xdb` |
| **Databases** | Place every `*.xdb` from the Release next to the frameworks (or under `databases/`). |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS.git
cd FaceRecognition-LivenessDetection-iOS
```

### 2. Download and place the runtime

See [Download and place the runtime](#download-and-place-the-runtime) below. From the repository root:

```bash
python scripts/get_runtime.py
```

### 3. Run the demo

Open the Xcode project, set your signing **Team**, and run on a physical iPhone.

Wait until Home status shows **Ready** before opening camera modes.

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

Run native SDK calls sequentially on **one background thread**. The engine does not support simultaneous calls.


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

![iOS home](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/home.png)

![iOS capture](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/capture.png)

![iOS identify](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/identify.jpg)

![iOS attributes](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/attribute.png)

![iOS liveness](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/attribute-liveness.png)

![iOS about](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/about.png)

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/latest) |
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

## Face Recognition and Liveness Detection SDK for iOS — Sample App | Identixia

Integrate **face recognition and liveness detection** with the **Identixia iOS SDK**. This repository provides a native iOS sample app for face detection, face template extraction, and face matching. Face templates are numerical representations used to compare faces. Enroll faces in a local gallery and search for a match with one-to-many (1:N) identification. Passive liveness, also called presentation attack detection (PAD), and deepfake detection are available when licensed. The combined authenticity result is REAL only when both checks pass.

Use the sample as a starting point for biometric identity verification, face-based access control, and customer onboarding. Processing runs on the device; images are not sent to the Identixia cloud.

Demo modes: **Enroll · Identify · Capture · Attribute**.

> For setup, integration, and API guides, see the [Face Recognition and Liveness Detection SDK documentation for iOS](https://docs.identixia.com/developers/face-sdk/ios). This page covers the sample repository.

## SDK overview

The sample includes a demo license. Your own application requires a key issued for its application identifier.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face recognition SDK** for iOS |
| **Modes** | Enroll · Identify (1:N) · Capture · Attribute · optional passive liveness |
| **Runtime zip** | Place the three frameworks listed below in the repository root after downloading the SDK runtime |
| **Demo id / license** | `com.identixia.facefullsdk.app` — use the sample id with the bundled demo license |
| **Activate** | Keep the sample’s application identifier and bundled key for evaluation. For your own app, request a key for its Android application ID or iOS bundle identifier and activate it before initializing the SDK. |
| **Tools** | **Xcode 15+** · physical **iPhone** |
| **UI** | Four demo modes become available after SDK initialization completes |
| **Privacy** | Templates stay on device — no Identixia cloud |

---

## Quick start

Clone the sample, place the runtime, and run it.

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS.git
cd FaceRecognition-LivenessDetection-iOS
python scripts/get_runtime.py
```

Download the runtime zip (`PENDING`) and place at repo root:

```text
facefullsdk.framework
FaceRecognitionEngine.framework
onnxruntime.framework
```

Open `FaceFullSDK.xcodeproj` → Signing Team → Run on a physical iPhone.

The sample runs with its bundled demo key. Keep the sample application id.

For your own app:

1. Email your Android application id or iOS bundle id, and the product name, to [contact@identixia.com](mailto:contact@identixia.com).
2. Replace the demo key in the sample source with the key you receive.
3. Rebuild. The sample activates that key before it initializes the SDK.

Wait for the Home screen to show **Ready**, then select a capture option. Check the license status on the Result or About screen before integrating the SDK into your own app.

---

## Features

| Capability | What it does |
| --- | --- |

## System requirements

| | |
| --- | --- |
| Device | Physical **iPhone** |
| Tools | **Xcode 15+** |
| Demo bundle id | `com.identixia.facefullsdk.app` |
| Frameworks | `facefullsdk` · `FaceRecognitionEngine` · `onnxruntime` |

---

## SDK installation

> **GitHub Release:** `python scripts/get_runtime.py` (or `--tag 1.0.0`)

Unzip to the repo root (siblings of the Xcode project):

```text
facefullsdk.framework
FaceRecognitionEngine.framework
onnxruntime.framework
```

---

## Run

```text
1. git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS.git
2. Place the three frameworks at the repo root
3. Open FaceFullSDK.xcodeproj → set Signing Team
4. Keep bundle id com.identixia.facefullsdk.app for the demo license
5. Run on a physical iPhone → Enroll / Identify / Capture / Attribute
```

---

## SDK license and activation

1. Run the sample with the bundled key and the sample id below.
2. For your own app, email [contact@identixia.com](mailto:contact@identixia.com) with the platform, your application id or bundle id, and the features you need.
3. Put the key you receive in the same place as the demo key.
4. Rebuild. Activation runs before SDK init. If it fails, the key does not match that id.

Sample id:

- `com.identixia.facefullsdk.app`

Set the key, then activate:

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/blob/main/FaceFullSDK/Home/ViewController.swift#L7-L8](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/blob/main/FaceFullSDK/Home/ViewController.swift#L7-L8)

[https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/blob/main/FaceFullSDK/Home/ViewController.swift#L266-L266](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/blob/main/FaceFullSDK/Home/ViewController.swift#L266-L266)

## API

The following SDK methods are used by the sample and can also be called from your application.

| API | Purpose |
| --- | --- |
| `activate(license)` then `init()` | Activate the license, then initialize the engine. Run these calls in order on one background thread. |
| `getLicenseStatus()` | Check the license status and enabled features before opening the camera. |
| `detect` / `faceAttribute` / `landmarks` | Detect faces in an image and return facial attributes and landmark coordinates. |
| `templateExtraction` / `similarity` | Create a numerical representation of a face and compare two faces to obtain a similarity score. |
| `enroll` / `bestMatch` | Save faces in a local gallery and search it for the closest match. |
| `liveness` / `deepfake` | Run presentation attack detection and deepfake checks. Report REAL only when both pass. |

Keep camera preview updates on the UI thread. Run SDK operations sequentially on a single background thread; the engine does not support simultaneous calls.

---

## SDKs for other platforms

| | Platform | Repo |
| --- | --- | --- |

---

{% include "../.gitbook/includes/footer.md" %}
