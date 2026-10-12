---
description: >-
  ID document recognition and liveness for Android. Passport, national ID, and driver license OCR, MRZ, and barcode reading run on the device. Document liveness runs when the license includes it.
icon: mobile-screen
---

# ID Document OCR and Liveness Detection SDK for Android


## Overview

| | |
| --- | --- |
| **Repository** | [`ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) · [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/releases/latest) |
| **Platform** | Android |
| **Runs** | On the device. Images stay in the app. |

## Capabilities

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Read printed document fields such as the name, document number, and dates using optical character recognition |
| MRZ | Read the machine-readable zone (MRZ) and validate its check digits |
| Barcode / QR | Extracted when present on the document |
| Front and back | Capture both sides when your workflow requires it |
| Document authenticity | Anti-spoof checks when the license includes `authenticity` |
| Structured JSON | Same result model on mobile and server — see Result JSON |

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

Native engines and model databases are **not** stored in git. Download the runtime zip from [GitHub Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/releases/latest) and unzip it into the path below.

| | |
| --- | --- |
| **Release asset** | `documentfullsdk.aar` |
| **Local path** | `libdocsdk/documentfullsdk.aar` |
| **Databases** | `document.xdb` is embedded inside the AAR (`assets/document.xdb`). |

```text
https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/releases/latest
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. An unavailable check is not a pass.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android.git
cd ID-Document-Recognition-Liveness-Detection-Android
```

### 2. Download and place the runtime

Download the runtime zip from [GitHub Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/releases/latest) and unzip it into the path in [Download and place the runtime](#download-and-place-the-runtime).

### 3. Run the demo

Open this folder in **Android Studio** (JDK **17**) and run on a physical **arm64** phone.

Wait until Home status shows **Ready** before opening camera modes.

### 4. Activate and try every mode

1. Confirm Home / About shows a licensed **Ready** state (sample apps ship a demo key for the sample application id only).
2. Exercise each demo tile once (enroll, identify, capture, attribute, liveness, document front/back, result).
3. For your own app: request a license for **your** application id / bundle id, then call activate → init on a background thread.

### Add the SDK to your own Android app

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/main/install.gradle'
```

Keep `documentfullsdk.aar` available (Release download or `libdocsdk/`). Use the sample kit helpers for guide crop + `recognize`.


## License and activation (mobile)

| | |
| --- | --- |
| **Demo id** | Sample application / bundle id shipped in the repo (document reader demo) |
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


## API reference — mobile document SDK

Android, iOS, Flutter, React Native, and Ionic share the **same customer method names** and the same process JSON idea (`identity` / `readings` / `tests` / `images` / `session`).

### Lifecycle

| API | Purpose |
| --- | --- |
| `setActivation(license)` | Activate license (background thread) |
| `init()` | Load models |
| `deinit()` | Unload engine |
| `getMachineCode()` / `getLicenseStatus()` | License helpers |
| `startNewSession(optionsJson?)` | Open a process session before recognize |

### Capture and process

| API | Purpose |
| --- | --- |
| Guide / crop helpers | Align document in frame (`DocumentGuideView` / kit crop) |
| `locateDocument(image)` | Find document bounds in a frame / still |
| `recognize(front, back?, authenticity?)` | OCR + MRZ + barcode (+ authenticity when licensed) |
| `documentRecognition(front, back?)` | Recognition path |

| `documentLiveness(front, back?)` | Authenticity / PAD-only path |
| `documentProcess(imagesJson, rfidJson, optionsJson)` | Combined pipeline (same idea as `POST /api/document/process`) |
| `faceLiveness(image, mode?)` | Optional face PAD helper on document products that ship it |

### Result JSON (shared idea)

Top-level concepts (names may be normalized per platform):

| Area | Contents |
| --- | --- |
| Identity | Document type, country, overall score |
| Fields / readings | OCR, MRZ, barcode field rows |
| Checks / tests | Verification + image quality |
| Images | Portrait / document crops (base64) |
| Session | Process / request metadata when present |

See [Result JSON](https://docs.identixia.com/id-document-sdk/result-json) and [Security check fields](https://docs.identixia.com/id-document-sdk/security-fields).

### Integration checklist

1. Apply `install.gradle` or vendor iOS `docsdk`.
2. Activate with your app id license → `init`.
3. Capture front (and back when needed) → `recognize` or `documentRecognition`.
4. Parse JSON in your app — do not depend on the demo Result UI.
5. Store fields you need in **your** database.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Invalid license | Application / bundle id must match the key; server needs the correct machine code |
| Init failed | Runtime AAR/framework/`lib` missing or wrong ABI |
| No face / no document | Lighting, crop, distance; try still gallery image first |
| Liveness / authenticity empty | License flag off — request the matching entitlement |
| Camera black / crash | Use a **physical** device; grant camera permission |
| Docker license fails after bare-metal license | Machine codes differ — re-license the container |

## Screenshots

![Status](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png)

![Visual fields](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-fields-visual.png)

![Validity checks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-validity.png)

![Liveness checks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png)

![Images](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-images.png)


## Support

{% include "../.gitbook/includes/contact.md" %}

{% include "../.gitbook/includes/footer.md" %}
