---
description: >-
  ID document liveness for Flutter. Presentation-attack checks for passports and ID cards run on the device, separate from OCR.
---

# ID Document Liveness Detection SDK for Flutter


## Overview

| | |
| --- | --- |
| **Repository** | [`ID-Document-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Flutter) · [Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Flutter/releases/latest) |
| **Platform** | Flutter |
| **Runs** | On the device. Images stay in the app. |

## Capabilities

| Capability | Description |
| --- | --- |
| Document authenticity API | Checks against screen replay, printout, and substitution |
| Separate from OCR | Complements ID Document Recognition; does not replace it |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Flutter | Stable channel, recent SDK |
| Android | JDK 17, physical arm64 device |
| iOS | Xcode + CocoaPods; physical iPhone |
| Bootstrap | Run the sample `tool/bootstrap.dart` / `pod install` as documented in the repo |

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
| **Release asset** | Android `documentlivenesssdk.aar` + iOS `docsdk.xcframework.zip` (from the paired native product Releases) |
| **Local path after download** | See the sample paths in the repository README (`example/android/libdocsdk/documentlivenesssdk.aar`, `ios/Frameworks/…`) |
| **Databases** | Document Android embeds `document.xdb` in the AAR; iOS embeds it in the framework bundle. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Flutter/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Flutter.git
cd ID-Document-Liveness-Detection-Flutter
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


## API reference — mobile document liveness

This sample checks presentation attacks. It does not read MRZ, barcodes, or visual fields.

| API | Purpose |
| --- | --- |
| `setActivation(license)` | Activate license (background thread) |
| `init()` | Load models |
| `deinit()` | Unload engine |
| `getMachineCode()` / `getLicenseStatus()` | License helpers |
| `documentLiveness(front, back?)` | Authenticity / PAD |

A missing authenticity result is not a pass. See [Security check fields](security-fields.md).

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

![Liveness checks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png)

![Status card](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png)


## Support

{% include "../.gitbook/includes/contact.md" %}
