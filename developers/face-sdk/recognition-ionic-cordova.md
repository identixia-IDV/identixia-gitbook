---
description: >-
  Face recognition for Ionic Cordova. Detection, attributes, quality, templates, and 1:1 match run on the device. This build does not include liveness.
icon: file
---

# Face Recognition SDK for Ionic Cordova

## Overview

| | |
| --- | --- |
| **Repository** | [`FaceRecognition-Ionic-Cordova`](https://github.com/identixia-IDV/FaceRecognition-Ionic-Cordova) · [Releases](https://github.com/identixia-IDV/FaceRecognition-Ionic-Cordova/releases/latest) |
| **Platform** | Ionic-Cordova |
| **Runs** | On the device. Images stay in the app. |

## Capabilities

| Capability | Description |
| --- | --- |
| Face detection | Bounding box, landmarks, and pose |
| Attributes | Age, gender, and related traits when enabled |
| Quality | ICAO-style image and face quality scores |
| Templates | Numerical representations of faces that you can store in **your** database for comparison |
| 1:1 match | Compare two images or two templates |
| 1:N identify | Enroll a gallery and search. This sample does not return a liveness score. |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Node | 18+ |
| Ionic CLI | Current stable |
| Android / iOS | Native toolchains as for Capacitor or Cordova |
| Device | Physical phone for camera capture |

## Download and place the runtime

Download the runtime zip from GitHub Releases and unzip it into the folder listed for that platform.

| | |
| --- | --- |
| **Release asset** | Android `facerecognitionsdk.aar` zip + iOS face zip (from the paired Android / iOS product Releases) |
| **Local path after download** | See the sample paths in the repository README (`example/android/libfacesdk/facerecognitionsdk.aar`, `ios/Frameworks/…`) |

### Download

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceRecognition-Ionic-Cordova/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-Ionic-Cordova.git
cd FaceRecognition-Ionic-Cordova
```

### 2. Download and place the runtime

Download the runtime zip from GitHub Releases and unzip it into the path in [Download and place the runtime](#download-and-place-the-runtime).

### 3. Run the demo

```bash
npm install
npm run setup:android && npm run android
```

On iOS: `npm run setup:ios && npm run ios`.

### 4. Activate and try every mode

1. Confirm Home / About shows a licensed **Ready** state (sample apps ship a demo key for the sample application id only).
2. Exercise each demo tile once (enroll, identify, capture, attribute, liveness, document front/back, result).
3. For your own app: request a license for **your** application id / bundle id, then call activate → init on a background thread.

## License and activation (mobile)

| | |
| --- | --- |
| **Demo id** | Sample application / bundle id in the repository |
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

This repository does not include face liveness. Do not call `liveness` or `/api/face/liveness`.

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
}
```

### Usage example (plugin / Flutter / React Native / Ionic)

Call the same method names exposed by the plugin bridge (`activate` → `init` → `detect` / `match` / `enroll`). Keep camera preview on the UI thread; keep engine calls on a single background isolate / queue.

### Integration checklist

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

![Home](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/home.png)

![Capture](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/capture.png)

![Enroll](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/enroll.png)

![Identify](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/identify.png)

![Detect](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/detect.png)

![Attributes](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute.png)

![Quality](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute-quality.png)

![Landmarks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/landmarks.png)

![Match](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/match.png)

![Liveness](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/attribute-liveness.png)

![Settings](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/settings.png)

![About](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/about.png)

## Support

{% include "../.gitbook/includes/contact.md" %}

{% include "../.gitbook/includes/footer.md" %}
