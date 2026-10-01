---
description: >-
  On-device passive face liveness SDK for Android. Scores a camera frame for presentation-attack detection when the license allows it.
---

# Face liveness — Android


## Overview

On-device passive face liveness SDK for Android. Scores a camera frame for presentation-attack detection when the license allows it.

Processing runs **on the device**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`FaceLivenessDetection-Android`](https://github.com/identixia-IDV/FaceLivenessDetection-Android) |
| **Platform** | Android |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/FaceLivenessDetection-Android" %}

[`identixia-IDV/FaceLivenessDetection-Android`](https://github.com/identixia-IDV/FaceLivenessDetection-Android) · [Releases](https://github.com/identixia-IDV/FaceLivenessDetection-Android/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Passive face liveness | Score one RGB face image or camera frame for presentation-attack detection |
| License gating | Liveness runs only when the license includes `liveness` |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| IDE | Android Studio |
| JDK | **17** |
| Device | Physical **arm64** phone for camera demos |
| minSdk | 24+ |
| ABIs | `arm64-v8a`, `armeabi-v7a` |
| Packaging | `jniLibs { useLegacyPackaging = true }` |

## Quick start

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Android.git
cd FaceLivenessDetection-Android
```

### 2. Place the runtime

Liveness runtime AAR/framework as documented in the sample `libfacesdk` / Frameworks folder.

Clients should download versioned assets via:

```text
https://github.com/identixia-IDV/FaceLivenessDetection-Android/releases/latest/download/<asset>
```

### 3. Run the demo

Follow the repository **Run** section (Android Studio / Xcode / `flutter run` / `yarn android` / Ionic). Wait until status shows **Ready** before opening camera modes.

### 4. Try every demo mode

Use each tile / screen once (enroll, identify, capture, document front/back, result, about). Confirm license state on the About / Result screen.

### Add the SDK to your own Android app

In the **app** module `build.gradle`:

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/FaceLivenessDetection-Android/main/install.gradle'
```

That line pulls the engine and, for face recognition, the reusable **kit** (`libfacekit`: `FaceRecognitionClient`, camera helpers, JSON parsers). Prefer the kit over calling the raw SDK class directly.


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

## Next steps

1. Complete **Quick start** until the sample shows **Ready**.
2. Activate with a license issued for **your** application id or machine code.
3. Call only the APIs your license allows; treat missing flags as “not evaluated”, not as pass.
4. Return to the [Face SDK](README.md) hub for recognition, liveness, and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use the Identixia documentation asset pack.

## Identixia Face Liveness Detection SDK — Android (Fully On-Premise)

> **Ready in ~10 minutes (after AAR download):**
> Drop `facelivenessdk.aar` into `libfacesdk/` → Run on a phone

---

## Quick start checklist

- [ ] Clone `https://github.com/identixia-IDV/FaceLivenessDetection-Android`
- [ ] Download `facelivenessdk.aar` from [Google Drive](#get-the-aar-libfacesdk)
- [ ] Place it in `libfacesdk/` (next to `libfacesdk/build.gradle`)
- [ ] Open this folder in Android Studio → Run on a **physical** phone
- [ ] Home status shows **Ready** → **Liveness / Settings / About** unlock

> **Your own app?** Skip to [Setup on your own app](#setup-on-your-own-app). Full API: [docs.identixia.com](https://docs.identixia.com).

---

## Introduction

Identixia **Face Liveness Detection SDK for Android** is an on-device passive liveness check for KYC. No extra hardware and no cloud. The check runs only after the license is activated.

All processing stays on the phone. **No** biometric data leaves the device.

This repository is the **Android demo app**. Runtime is `libfacesdk/facelivenessdk.aar` (download from Google Drive). No other Identixia repository is required.

### Features

| Demo tile | What it does |
| --------- | ------------ |
| **Liveness** | Live camera anti-spoofing with face box + track / liveness / luminance HUD |
| **Settings** | Camera lens (front / back), liveness threshold |
| **About** | Identixia Face Liveness SDK — on-device anti-spoofing |

## Before you start

| Step | What you need |
| ---- | ------------- |
| 1 | Android Studio + a **real device** (emulator is not recommended) |
| 2 | `facelivenessdk.aar` in `./libfacesdk/` — see [Get the AAR](#get-the-aar-libfacesdk) |
| 3 | Paste a Face Liveness license for `applicationId` `com.identixia.faceliveness` (product `741777`) into `MainActivity.kt` — see [SDK License](#sdk-license) |

### System requirements

| Item | Minimum | Recommended |
| ---- | ------- | ----------- |
| Android | API 24 (7.0) | API 29 (10) or newer |
| ABI | `arm64-v8a`, `armeabi-v7a` | `arm64-v8a` |
| Camera | Front or rear | Physical device |

---

## Get the AAR (`libfacesdk`)

`libfacesdk/facelivenessdk.aar` is empty on GitHub because the binary is too large.

### Where to download

**[FaceLivenessSDK Android (Google Drive)](https://drive.google.com/drive/folders/1x3jt02f-YHsk4WD_QlnKJSx5uQ5Ds4xH)**

### How to place it

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Android.git
cd FaceLivenessDetection-Android
```

Download `facelivenessdk.aar` and put it here:

```text
FaceLivenessDetection-Android/
└── libfacesdk/
    ├── build.gradle
    └── facelivenessdk.aar
```

---

## Run the demo

1. Open **this** folder in Android Studio.
2. Paste your Face Liveness `LICENSE_KEY` for `com.identixia.faceliveness`, then run on a device.

Keep `applicationId` **`com.identixia.faceliveness`** so the key matches the binary (product `741777` only).

## SDK License

Licenses are **offline** and bound to your `applicationId`.

`LICENSE_KEY` in `MainActivity.kt` is empty until you paste a key issued for `com.identixia.faceliveness` (product `741777`). A Face Recognition demo key will not activate this AAR.

### How to get a license

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/18e5ebacd71b3959df56a2ad082c96abe13cdbb9/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L21-L22](https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/18e5ebacd71b3959df56a2ad082c96abe13cdbb9/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L21-L22)

[https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/18e5ebacd71b3959df56a2ad082c96abe13cdbb9/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L50-L55](https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/18e5ebacd71b3959df56a2ad082c96abe13cdbb9/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L50-L55)

Please [contact us](#contact) to get a license for **your own app**.

### License capabilities

After activation, `FaceLivenessSDK.getLicenseStatus()` (and `LicenseStatus.current()` in the demo kit) reports what the key unlocks:

- **Liveness only** / **Recognition + Liveness** — Liveness tile
- **Recognition only** — liveness stays unavailable on this App
- **No license** — tile stays locked until you activate

---

## Setup on your own app

Minimal integration (details: [docs.identixia.com](https://docs.identixia.com)):

1. Copy `libfacesdk/` into your project and place `facelivenessdk.aar` inside it.
2. `settings.gradle`: `include ':libfacesdk'`
3. `app/build.gradle`: `implementation project(':libfacesdk')`, `minSdk 24`, `abiFilters 'arm64-v8a', 'armeabi-v7a'`, and `packaging { jniLibs { useLegacyPackaging = true } }`
4. Add `CAMERA` permission.
5. On a **background** thread: `FaceLivenessSDK.setActivation(context, "")` → `FaceLivenessSDK.init(context)` (`0` = success).

Optional: copy `app/.../kit/` (`FaceLivenessClient`) for demo-style threading / camera helpers.

Request a license for **your** `applicationId`, not the demo’s.

---

## About SDK

Public class: `com.identixia.facelivenessdk.FaceLivenessSDK`. Call **once per process** on a background thread: `setActivation` → `init`. Serialize native calls. Full reference: [docs.identixia.com](https://docs.identixia.com).

| Code | Meaning |
| ---- | ------- |
| 0 | Success |
| 1 | Invalid license |
| 2 | License expired |
| 3 | License not activated |
| 4 | Engine failed to start |

---
