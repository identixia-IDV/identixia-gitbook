---
description: >-
  On-device passive face liveness SDK for Android. Scores a camera frame for presentation-attack detection when the license allows it.
---

# Liveness Detection Android SDK

On-device passive face liveness SDK for Android. Scores a camera frame for presentation-attack detection when the license allows it.

### Repository

{% embed url="https://github.com/identixia-IDV/FaceLivenessDetection-Android" %}

[`identixia-IDV/FaceLivenessDetection-Android`](https://github.com/identixia-IDV/FaceLivenessDetection-Android)

### From the product README

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

> **Your own app?** Skip to [Setup on your own app](#setup-on-your-own-app). Full API: [docs.identixia.com](https://doc.identixia.com).

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

### Screenshots

<p align="center">
<img src="https://raw.githubusercontent.com/identixiaAI/identixia-assets/main/screenshots/face-liveness/mobile/liveness.png" alt="Liveness result" width="220"/>
</p>

---

## SDK License

Licenses are **offline** and bound to your `applicationId`.

`LICENSE_KEY` in `MainActivity.kt` is empty until you paste a key issued for `com.identixia.faceliveness` (product `741777`). A Face Recognition demo key will not activate this AAR.

### How to get a license

The code below shows how to use the license:

[https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/main/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L21-L22](https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/main/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L21-L22)

[https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/main/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L50-L55](https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/main/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L50-L55)

Please [contact us](#contact) to get a license for **your own app**.

### License capabilities

After activation, `FaceLivenessSDK.getLicenseStatus()` (and `LicenseStatus.current()` in the demo kit) reports what the key unlocks:

- **Liveness only** / **Recognition + Liveness** — Liveness tile
- **Recognition only** — liveness stays unavailable on this App
- **No license** — tile stays locked until you activate

---

## Setup on your own app

Minimal integration (details: [docs.identixia.com](https://doc.identixia.com)):

1. Copy `libfacesdk/` into your project and place `facelivenessdk.aar` inside it.
2. `settings.gradle`: `include ':libfacesdk'`
3. `app/build.gradle`: `implementation project(':libfacesdk')`, `minSdk 24`, `abiFilters 'arm64-v8a', 'armeabi-v7a'`, and `packaging { jniLibs { useLegacyPackaging = true } }`
4. Add `CAMERA` permission.
5. On a **background** thread: `FaceLivenessSDK.setActivation(context, "")` → `FaceLivenessSDK.init(context)` (`0` = success).

Optional: copy `app/.../kit/` (`FaceLivenessClient`) for demo-style threading / camera helpers.

Request a license for **your** `applicationId`, not the demo’s.

---

## About SDK

Public class: `com.identixia.facelivenessdk.FaceLivenessSDK`. Call **once per process** on a background thread: `setActivation` → `init`. Serialize native calls. Full reference: [docs.identixia.com](https://doc.identixia.com).

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
