---
description: >-
  On-device passive face liveness SDK for iOS. Scores a camera frame for presentation-attack detection when the license allows it.
---

# Liveness Detection iOS SDK

On-device passive face liveness SDK for iOS. Scores a camera frame for presentation-attack detection when the license allows it.

### Repository

{% embed url="https://github.com/identixia-IDV/FaceLivenessDetection-iOS" %}

[`identixia-IDV/FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS)

### From the product README

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

> **Your own app?** Skip to [Setup on your own app](#setup-on-your-own-app). Full API: [docs.identixia.com](https://doc.identixia.com).

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

### Screenshots

<p align="center">
<img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-liveness/mobile/liveness.png" alt="Liveness result" width="220"/>
</p>

---

## SDK License

Licenses are **offline** and bound to your bundle identifier.

`licenseKey` in `ViewController.swift` is empty until you paste a key issued for `com.identixia.faceliveness.app` (product `741777`). A Face Recognition demo key will not activate this framework.

### How to get a license

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/main/FaceLivenessSDK/Home/ViewController.swift#L7-L8](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/main/FaceLivenessSDK/Home/ViewController.swift#L7-L8)

[https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/main/FaceLivenessSDK/Home/ViewController.swift#L150-L158](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/main/FaceLivenessSDK/Home/ViewController.swift#L150-L158)

Please [contact us](#contact) to get a license for **your own app**.

---

## Setup on your own app

Minimal integration (details: [docs.identixia.com](https://doc.identixia.com)):

1. Add `facelivenessdk.framework`, `FaceLivenessEngine.framework`, and `onnxruntime.framework` (Embed & Sign).
2. Optionally copy **FaceLivenessKit** for `FaceLivenessClient` helpers.
3. Activate once at launch (off the main thread): `FaceLivenessClient.shared.activate(license: "") { code in … }` (`0` = success).
4. Add `NSCameraUsageDescription` in `Info.plist`.

Request a license for **your** bundle id, not the demo’s.

---

## About SDK

Use **FaceLivenessKit** (`FaceLivenessClient.shared`) or call the native SDK from Objective-C++. Call **once per process**: activate → init. Serialize native work. Full reference: [docs.identixia.com](https://doc.identixia.com).

| Code | Meaning |
| ---- | ------- |
| 0 | Success |
| 1 | Invalid license |
| 2 | License expired |
| 3 | License not activated |
| 4 | Engine failed to start |

---

## Contact

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}
