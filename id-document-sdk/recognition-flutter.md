---
description: >-
  ID document recognition for Flutter. Passport, national ID, and driver license OCR, MRZ, and barcode reading run on the device. This build does not include document liveness.
---

# ID Document Recognition and OCR SDK for Flutter


## Overview

| | |
| --- | --- |
| **Repository** | [`ID-Document-Recognition-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Flutter) · [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Android/releases/tag/runtime) |
| **Platform** | Flutter |
| **Runs** | On the device. Images stay in the app. |

## Capabilities

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Read printed document fields such as the name, document number, and dates using optical character recognition |
| MRZ | Read the machine-readable zone (MRZ) and validate its check digits |
| Barcode / QR | Extracted when present on the document |
| Front and back | Capture both sides when your workflow requires it |
| Structured JSON | Same result model on mobile and server — see Result JSON |

This sample does not include document liveness. It does not serve `/api/document/liveness` and it does not call `documentLiveness`.

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Flutter | Stable channel, recent SDK |
| Android | JDK 17, physical arm64 device |
| iOS | Xcode + CocoaPods; physical iPhone |
| Bootstrap | Run the sample `tool/bootstrap.dart` / `pod install` as documented in the repo |

## Download and place the runtime

Native engines and model databases are **not** stored in git. Open the `runtime` GitHub Release and place each file in the path below.

| | |
| --- | --- |
| **Release asset** | `documentrecognitionsdk.aar`, `documentrecognitionsdk.framework.zip` from `ID-Document-Recognition-Android` `runtime`, `ID-Document-Recognition-iOS` `runtime` |
| **Local path** | `example/android/libdocumentrecognitionsdk/documentrecognitionsdk.aar/`, `ios/Frameworks/` |
| **Databases** | `document.xdb` ships inside the AAR or the iOS framework bundle (Windows/Linux: next to the DLL/`.so` in `lib/cpu/`). |

[Download the runtime](https://github.com/identixia-IDV/ID-Document-Recognition-Android/releases/tag/runtime)

Download [`documentrecognitionsdk.aar`](https://github.com/identixia-IDV/ID-Document-Recognition-Android/releases/tag/runtime) from the [ID-Document-Recognition-Android Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Android/releases/tag/runtime). Save the file as `example/android/libdocumentrecognitionsdk/documentrecognitionsdk.aar`.

Download [`documentrecognitionsdk.framework.zip`](https://github.com/identixia-IDV/ID-Document-Recognition-iOS/releases/tag/runtime) from the [ID-Document-Recognition-iOS Releases](https://github.com/identixia-IDV/ID-Document-Recognition-iOS/releases/tag/runtime). Unzip it into `ios/Frameworks/`. The files should sit in that folder, not inside an extra directory.

Extract so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. An unavailable check is not a pass.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Flutter.git
cd ID-Document-Recognition-Flutter
```

### 2. Download and place the runtime

Download [`documentrecognitionsdk.aar`](https://github.com/identixia-IDV/ID-Document-Recognition-Android/releases/tag/runtime) from the [ID-Document-Recognition-Android Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Android/releases/tag/runtime). Save the file as `example/android/libdocumentrecognitionsdk/documentrecognitionsdk.aar`.

Download [`documentrecognitionsdk.framework.zip`](https://github.com/identixia-IDV/ID-Document-Recognition-iOS/releases/tag/runtime) from the [ID-Document-Recognition-iOS Releases](https://github.com/identixia-IDV/ID-Document-Recognition-iOS/releases/tag/runtime). Unzip it into `ios/Frameworks/`. The files should sit in that folder, not inside an extra directory.

See [Download and place the runtime](#download-and-place-the-runtime).

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


## API reference — mobile document SDK

This repository does not include document liveness. Do not call `documentLiveness` or `/api/document/liveness`.

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
| `recognize(front, back?, authenticity?)` | OCR + MRZ + barcode |
| `documentRecognition(front, back?)` | Recognition path |

### Result JSON (shared idea)

Top-level concepts (names may be normalized per platform):

| Area | Contents |
| --- | --- |
| Identity | Document type, country, overall score |
| Fields / readings | OCR, MRZ, barcode field rows |
| Checks / tests | Verification + image quality |
| Images | Portrait / document crops (base64) |
| Session | Process / request metadata when present |

See [Result JSON](result-json.md) and [Security check fields](security-fields.md).

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
