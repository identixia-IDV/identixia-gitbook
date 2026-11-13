---
description: >-
  ID document liveness for Android. Presentation-attack checks for passports and ID cards run on the device, separate from OCR.
---

# ID Document Liveness Detection SDK for Android


## Overview

| | |
| --- | --- |
| **Repository** | [`ID-Document-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android) · [Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime) |
| **Platform** | Android |
| **Runs** | On the device. Images stay in the app. |

## Capabilities

| Capability | Description |
| --- | --- |
| Document authenticity API | Checks against screen replay, printout, and substitution |
| Separate from OCR | Complements ID Document Recognition; does not replace it |

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

Native engines and model databases are **not** stored in git. Open the `runtime` GitHub Release and place each file in the path below.

| | |
| --- | --- |
| **Release asset** | `documentlivenesssdk.aar` from this repository’s `runtime` Release |
| **Local path** | `libdocumentlivenesssdk/documentlivenesssdk.aar/` |
| **Databases** | `document.xdb` ships inside the AAR or the iOS framework bundle (Windows/Linux: next to the DLL/`.so` in `lib/cpu/`). |

[Download the runtime](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime)

Download [`documentlivenesssdk.aar`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime) from this repository’s [Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime). Save the file as `libdocumentlivenesssdk/documentlivenesssdk.aar`.

Extract so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. An unavailable check is not a pass.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android.git
cd ID-Document-Liveness-Detection-Android
```

### 2. Download and place the runtime

Download [`documentlivenesssdk.aar`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime) from this repository’s [Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime). Save the file as `libdocumentlivenesssdk/documentlivenesssdk.aar`.

See [Download and place the runtime](#download-and-place-the-runtime).

### 3. Run the demo

Open this folder in **Android Studio** (JDK **17**) and run on a physical **arm64** phone.

Wait until Home status shows **Ready** before opening camera modes.

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
