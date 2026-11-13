---
description: >-
  ID document liveness for Ionic Capacitor. Presentation-attack checks for passports and ID cards run on the device, separate from OCR.
---

# ID Document Liveness Detection SDK for Ionic Capacitor


## Overview

| | |
| --- | --- |
| **Repository** | [`ID-Document-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Capacitor) · [Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime) |
| **Platform** | Ionic |
| **Runs** | On the device. Images stay in the app. |

## Capabilities

| Capability | Description |
| --- | --- |
| Document authenticity API | Checks against screen replay, printout, and substitution |
| Separate from OCR | Complements ID Document Recognition; does not replace it |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Node | 18+ |
| Ionic CLI | Current stable |
| Android / iOS | Native toolchains as for Capacitor or Cordova |
| Device | Physical phone for camera capture |

## Download and place the runtime

Native engines and model databases are **not** stored in git. Open the `runtime` GitHub Release and place each file in the path below.

| | |
| --- | --- |
| **Release asset** | `documentlivenesssdk.aar`, `documentlivenesssdk.framework.zip` from `ID-Document-Liveness-Detection-Android` `runtime`, `ID-Document-Liveness-Detection-iOS` `runtime` |
| **Local path** | `example/android/libdocumentlivenesssdk/documentlivenesssdk.aar/`, `ios/Frameworks/` |
| **Databases** | `document.xdb` ships inside the AAR or the iOS framework bundle (Windows/Linux: next to the DLL/`.so` in `lib/cpu/`). |

[Download the runtime](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime)

Download [`documentlivenesssdk.aar`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime) from the [ID-Document-Liveness-Detection-Android Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime). Save the file as `example/android/libdocumentlivenesssdk/documentlivenesssdk.aar`.

Download [`documentlivenesssdk.framework.zip`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-iOS/releases/tag/runtime) from the [ID-Document-Liveness-Detection-iOS Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-iOS/releases/tag/runtime). Unzip it into `ios/Frameworks/`. The files should sit in that folder, not inside an extra directory.

Extract so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. An unavailable check is not a pass.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Capacitor.git
cd ID-Document-Liveness-Detection-Ionic-Capacitor
```

### 2. Download and place the runtime

Download [`documentlivenesssdk.aar`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime) from the [ID-Document-Liveness-Detection-Android Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android/releases/tag/runtime). Save the file as `example/android/libdocumentlivenesssdk/documentlivenesssdk.aar`.

Download [`documentlivenesssdk.framework.zip`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-iOS/releases/tag/runtime) from the [ID-Document-Liveness-Detection-iOS Releases](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-iOS/releases/tag/runtime). Unzip it into `ios/Frameworks/`. The files should sit in that folder, not inside an extra directory.

See [Download and place the runtime](#download-and-place-the-runtime).

### 3. Run the demo

```bash
npm install
npm run build
npx cap sync
npx cap run android
```

On iOS: `npx cap open ios` after sync, then run from Xcode.

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
