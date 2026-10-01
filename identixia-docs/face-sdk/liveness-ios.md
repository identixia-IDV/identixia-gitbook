---
description: >-
  On-device passive face liveness SDK for iOS. Scores a camera frame for presentation-attack detection when the license allows it.
---

# Face liveness — iOS


## Overview

On-device passive face liveness SDK for iOS. Scores a camera frame for presentation-attack detection when the license allows it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `FaceLivenessDetection-iOS` |
| **Platform** | iOS |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/FaceLivenessDetection-iOS" %}

Source: [`identixia-IDV/FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS)

## What you can do

| Capability | Description |
| --- | --- |
| Passive face liveness | Score one RGB face image / frame for presentation-attack detection |
| License gating | Liveness runs only when the license allows it |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| IDE | Xcode (recent stable) |
| Device | Physical iPhone for camera demos |
| Deployment | iOS 13+ (see sample project) |
| Frameworks | Vendored `.framework` / `.xcframework` from Release or Drive pack |

## Quick start

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-iOS.git
cd FaceLivenessDetection-iOS
```

### 2. Place the runtime

Liveness runtime AAR/framework as documented in the sample `libfacesdk` / Frameworks folder.

Clients should download versioned assets via:

```text
https://github.com/identixia-IDV/FaceLivenessDetection-iOS/releases/latest/download/<asset>
```

### 3. Run the demo

Follow the repository **Run** section (Android Studio / Xcode / `flutter run` / `yarn android` / Ionic). Wait until status shows **Ready** before opening camera modes.

### 4. Try every demo mode

Use each tile / screen once (enroll, identify, capture, document front/back, result, about). Confirm license state on the About / Result screen.


## License and activation (mobile)

| | |
| --- | --- |
| **Demo id** | Sample application / bundle id shipped in the repo |
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


## API reference — mobile face liveness

Activate → init, then score a camera frame or gallery still with the liveness API exposed by the sample (see kit / SDK class in the repo). Without a liveness entitlement the score is omitted.


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

<figure><img src="../.gitbook/assets/liveness-mobile.png" alt="Mobile liveness result" width="220"><figcaption>Mobile liveness result</figcaption></figure>

<figure><img src="../.gitbook/assets/liveness-desktop.png" alt="Desktop liveness demo" width="480"><figcaption>Desktop liveness demo</figcaption></figure>


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

Adapted from the shipping repository README for exact commands and platform-specific notes. Screenshots above use the current Identixia asset pack.

## Identixia Face Liveness Detection SDK — iOS (Fully On-Premise)

> **Ready in ~10 minutes (after framework download):**
> Unzip Drive frameworks into this folder → Run on a phone

---

## Quick start checklist

- [ ] Clone `https://github.com/identixia-IDV/FaceLivenessDetection-iOS`
- [ ] Download the `.zip` files from [Google Drive](#get-the-framework)
- [ ] Unzip into this folder (`facelivenessdk.framework`, `FaceLivenessEngine.framework`, `onnxruntime.framework`)
- [ ] Open `FaceLivenessSDK.xcodeproj` → set **your** Team → Run on a **physical** iPhone
- [ ] Home status shows ready → **Liveness / Settings / About** unlock

> **Your own app?** Skip to [Setup on your own app](#setup-on-your-own-app). Full API: [docs.identixia.com](https://docs.identixia.com).

---

## Introduction

Identixia **Face Liveness Detection SDK for iOS** is an on-device passive liveness check for KYC. No extra hardware and no cloud. The check runs only after the license is activated.

All processing stays on the iPhone. **No** biometric data leaves the device.

This repository is the **iOS demo app**. Runtime frameworks download from Google Drive. No other Identixia repository is required.

### Features

| Demo tile | What it does |
| --------- | ------------ |
| **Liveness** | Live camera anti-spoofing with face overlay + liveness metrics |
| **Settings** | Camera lens, liveness threshold |
| **About** | Identixia Face Liveness SDK — on-device anti-spoofing |

## Before you start

| Step | What you need |
| ---- | ------------- |
| 1 | Xcode 15+ and a **physical iPhone** |
| 2 | Unzipped frameworks in this folder — see [Get the framework](#get-the-framework) |
| 3 | Paste a Face Liveness license for bundle id `com.identixia.faceliveness.app` (product `741777`) into `ViewController.swift` — see [SDK License](#sdk-license) |

### System requirements

| Item | Minimum | Recommended |
| ---- | ------- | ----------- |
| iOS | 13.0 | 16 or newer |
| Device | Physical iPhone | Same; simulator is not for camera / liveness |

---

## Get the framework

Frameworks are stubs on GitHub because the binaries are too large. On Drive they ship as **zips** — unzip after download.

### Where to download

**[FaceLivenessSDK iOS (Google Drive)](https://drive.google.com/drive/folders/1HzREOmFg9kBLbuso1e57j8Hk5Jk41kyr)** — `facelivenessdk.framework.zip`, `FaceLivenessEngine.framework.zip`, `onnxruntime.framework.zip`

### How to place it

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-iOS.git
cd FaceLivenessDetection-iOS
```

Unzip and place frameworks at the **repo root** (next to `FaceLivenessSDK.xcodeproj`):

```text
FaceLivenessDetection-iOS/
├── FaceLivenessSDK.xcodeproj
├── FaceLivenessKit/
├── FaceLivenessSDK/
├── facelivenessdk.framework/
├── FaceLivenessEngine.framework/
└── onnxruntime.framework/
```

---

## Run the demo

1. Open **FaceLivenessSDK.xcodeproj** in Xcode.
2. Set your **Team** for signing.
3. Paste your Face Liveness `licenseKey` for `com.identixia.faceliveness.app`, then run on a device.

Keep bundle id **`com.identixia.faceliveness.app`** so the key matches the binary (product `741777` only).

## SDK License

Licenses are **offline** and bound to your bundle identifier.

`licenseKey` in `ViewController.swift` is empty until you paste a key issued for `com.identixia.faceliveness.app` (product `741777`). A Face Recognition demo key will not activate this framework.

### How to get a license

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/bee2f1bfef8c91cb0ef8f94c4212a8a9ddf57d20/FaceLivenessSDK/Home/ViewController.swift#L7-L8](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/bee2f1bfef8c91cb0ef8f94c4212a8a9ddf57d20/FaceLivenessSDK/Home/ViewController.swift#L7-L8)

[https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/bee2f1bfef8c91cb0ef8f94c4212a8a9ddf57d20/FaceLivenessSDK/Home/ViewController.swift#L150-L158](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/bee2f1bfef8c91cb0ef8f94c4212a8a9ddf57d20/FaceLivenessSDK/Home/ViewController.swift#L150-L158)

Please [contact us](#contact) to get a license for **your own app**.

---

## Setup on your own app

Minimal integration (details: [docs.identixia.com](https://docs.identixia.com)):

1. Add `facelivenessdk.framework`, `FaceLivenessEngine.framework`, and `onnxruntime.framework` (Embed & Sign).
2. Optionally copy **FaceLivenessKit** for `FaceLivenessClient` helpers.
3. Activate once at launch (off the main thread): `FaceLivenessClient.shared.activate(license: "") { code in … }` (`0` = success).
4. Add `NSCameraUsageDescription` in `Info.plist`.

Request a license for **your** bundle id, not the demo’s.

---

## About SDK

Use **FaceLivenessKit** (`FaceLivenessClient.shared`) or call the native SDK from Objective-C++. Call **once per process**: activate → init. Serialize native work. Full reference: [docs.identixia.com](https://docs.identixia.com).

| Code | Meaning |
| ---- | ------- |
| 0 | Success |
| 1 | Invalid license |
| 2 | License expired |
| 3 | License not activated |
| 4 | Engine failed to start |

---
