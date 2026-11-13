---
description: >-
  Face recognition and liveness for iOS. Enrollment, templates, and 1:N search run on the device. Passive liveness runs when the license includes it.
---

# Face Recognition and Liveness Detection SDK for iOS


## Overview

| | |
| --- | --- |
| **Repository** | [`FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) · [Releases](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/tag/runtime) |
| **Platform** | iOS |
| **Runs** | On the device. Images stay in the app. |

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

Native engines and model databases are **not** stored in git. Open the `runtime` GitHub Release and place each file in the path below.

| | |
| --- | --- |
| **Release asset** | `facefull.zip` from this repository’s `runtime` Release |
| **Local path** | `repository root` |
| **Databases** | Required packs: `recognition.xdb`, `recognition-common.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb`, and when licensed `recognition-liveness.xdb` + `recognition-deepfake.xdb`. |

[Download the runtime](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/tag/runtime)

Download [`facefull.zip`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/tag/runtime) from this repository’s [Releases](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/tag/runtime). Unzip it at the repository root so the frameworks and database packs land in the sample folders, not inside an extra directory.

Extract so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. An unavailable check is not a pass.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS.git
cd FaceRecognition-LivenessDetection-iOS
```

### 2. Download and place the runtime

Download [`facefull.zip`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/tag/runtime) from this repository’s [Releases](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS/releases/tag/runtime). Unzip it at the repository root so the frameworks and database packs land in the sample folders, not inside an extra directory.

See [Download and place the runtime](#download-and-place-the-runtime).

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

Prefer **`FaceRecognitionClient`** (Android kit) / the matching iOS kit wrappers. Flutter, React Native, and Ionic expose the **same method names** as Android (`detect`, `faceDetection`, `match`, …). Serialize all engine calls on **one background thread**.

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
| `setVideoWorkerEventHandler` | Receive track / match events (JSON) |
| `stopVideoWorker()` | Stop session |
| `makeTrackingConfig` / `makeIdentityConfig` | Build configs |

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

Call the same method names exposed by the plugin bridge (`activate` → `init` → `detect` / `match` / `enroll`). Keep camera preview on the UI thread; keep engine calls on a single background isolate / queue.

### Integration checklist

1. Download the `runtime` GitHub Release and extract it into the sample folder.
2. `FaceRecognitionClient.get(context).activate(license) { code -> … }` (or `setActivation` → `init` on plugins).
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

Keep the same license product line across stacks. From the [Face SDK](README.md) hub:

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

![iOS home](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/home.png)

![iOS capture](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/capture.png)

![iOS identify](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/identify.jpg)

![iOS attributes](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/attribute.png)

![iOS liveness](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/attribute-liveness.png)

![iOS about](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/ios/about.png)


## Support

{% include "../.gitbook/includes/contact.md" %}
