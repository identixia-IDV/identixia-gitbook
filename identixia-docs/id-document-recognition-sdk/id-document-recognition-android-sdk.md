---
description: >-
  On-device ID document recognition SDK for Android. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.
---

# ID Document Recognition Android SDK


## Overview

On-device ID document recognition SDK for Android. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `ID-Document-Recognition-Liveness-Detection-Android` |
| **Platform** | Android |
| **Docs site** | [doc.identixia.com](https://doc.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android" %}

Source: [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android)

## What you can do

| Capability | Description |
| --- | --- |
| Locate & crop | Find the ID document in a camera frame or still |
| OCR | Visual-zone fields (name, document number, dates, …) |
| MRZ | Machine-readable zone parse + checks |
| Barcode / QR | When present on the document |
| Front + back | Capture both sides when required |
| Document liveness | Authenticity / PAD checks when the license includes it |
| Structured JSON | Same result idea on mobile and server |

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
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android.git
cd ID-Document-Recognition-Liveness-Detection-Android
```

### 2. Place the runtime

Engine AAR / `docsdk` framework from Releases (`documentreadersdk.aar` / `docsdk.xcframework.zip`) or local `libdocsdk`.

Clients should download versioned assets via:

```text
https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/releases/latest/download/<asset>
```

### 3. Run the demo

Follow the repository **Run** section (Android Studio / Xcode / `flutter run` / `yarn android` / Ionic). Wait until status shows **Ready** before opening camera modes.

### 4. Try every demo mode

Use each tile / screen once (enroll, identify, capture, document front/back, result, about). Confirm license state on the About / Result screen.

### Add the SDK to your own Android app

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/main/install.gradle'
```

Keep `documentreadersdk.aar` available (Release download or `libdocsdk/`). Use the sample kit helpers for guide crop + `recognize`.


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

Serialize native SDK calls on **one background thread**. The engine is not concurrent.


## API reference — mobile document SDK

### Lifecycle

| API | Purpose |
| --- | --- |
| Activate + init | License then load models (background thread) |
| License status | Recognition / authenticity flags |
| Session helpers | `startNewSession` / gallery session before recognize |

### Capture and recognize

| API | Purpose |
| --- | --- |
| Guide / crop helpers | Align document in frame (`DocumentGuideView` / kit crop) |
| `recognize(front, back?)` | Run OCR + MRZ + barcode (+ liveness when licensed) |
| Result parser | Map engine JSON → identity, fields, checks, images |

### Result JSON (shared idea)

Top-level concepts (names may be normalized per platform):

| Area | Contents |
| --- | --- |
| Identity | Document type, country, overall score |
| Fields / readings | OCR, MRZ, barcode field rows |
| Checks / tests | Verification + image quality + security |
| Images | Portrait / document crops (base64) |

See [Document result JSON](document-result-json.md) and [Document security check fields](document-security-check-fields.md).

### Integration checklist

1. Apply `install.gradle` or vendor iOS `docsdk`.
2. Activate with your app id license.
3. Capture front (and back when needed) → `recognize`.
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


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

The following is adapted from the shipping repository README for screenshots, exact commands, and platform-specific notes.

## <img src="https://cdn.simpleicons.org/android/3DDC84" width="32" height="32" alt="" /> Identixia ID Document Recognition and Liveness Detection — Android

**On-device ID document recognition** for Android: passports, national IDs, and driver licenses with passport MRZ OCR, ID card barcode reading, live camera capture, and optional document liveness / authenticity. Built for KYC and eKYC — **identity data stays on the phone**; nothing is uploaded to Identixia cloud.

Use the sample app to evaluate capture UX and the one-scroll Result screen, then add the same `install.gradle` line to your app.

<p><img src="https://img.shields.io/badge/On-device-0F766E?style=flat-square" alt="On-device" /> <img src="https://img.shields.io/badge/Passport%20MRZ%20OCR-0F766E?style=flat-square" alt="Passport%20MRZ%20OCR" /> <img src="https://img.shields.io/badge/ID%20barcode-0F766E?style=flat-square" alt="ID%20barcode" /> <img src="https://img.shields.io/badge/Document%20liveness-0F766E?style=flat-square" alt="Document%20liveness" /> <img src="https://img.shields.io/badge/KYC%20%2F%20eKYC-5A6573?style=flat-square" alt="KYC%20%2F%20eKYC" /></p>

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Read this once before cloning. Mobile demos ship a **bundled license** for the sample application / bundle id. Production apps need a new key from Identixia. [Initial commands](#-initial-commands) lists clone → place runtime → run → activate options.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **ID document recognition SDK** for Android (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · passport MRZ · barcode / QR · optional document liveness |
| **Runtime zip** | `install.gradle` uses `libdocsdk/` when `documentreadersdk.aar` is already in this repo |
| **Demo id / license** | `com.identixia.documentreader` — bundled demo license until **12 Aug 2027** |
| **Activate** | Sample app: keep the demo id and bundled key. Your app: new applicationId / bundle id → [contact](#-contact) → call the SDK activate API (see docs). |
| **Tools** | Android Studio · **JDK 17** · physical **arm64** phone (emulator is not enough for full camera demos) |
| **UI** | Wide Camera Home · Gallery / About · one-scroll Result |
| **Privacy** | All processing on device — no Identixia cloud for document data |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

Clone the sample, place the runtime, and run it.

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Clone and place the runtime

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android.git
cd ID-Document-Recognition-Liveness-Detection-Android
```

The sample applies `install.gradle`. When `libdocsdk/documentreadersdk.aar` is already in the clone, that is the engine the app builds with.

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Run the demo

Open this folder in **Android Studio** (JDK 17) → Run on a physical **arm64** device.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> Activate / license

Please [contact us](#-contact) to get a license for your own app. The sample already includes a demo license for its application id.

### <img src="https://img.shields.io/badge/-4-0F766E?style=for-the-badge" alt="" /> First capture

Wait until Home status = **Ready**, then use Camera / Gallery (or the face mode tiles). Confirm Result / About shows a licensed state before integrating into your own app.

---

## <img src="https://api.iconify.design/lucide/list-checks.svg?color=%230F766E" width="24" height="24" alt="" /> What you get

| Capability | What it does |
| --- | --- |
| <img src="https://api.iconify.design/lucide/id-card.svg?color=%230F766E" width="16" height="16" alt="" /> Passport / ID / DL | On-device ID document recognition for passports, national IDs, and driver licenses |
| <img src="https://api.iconify.design/lucide/scan-text.svg?color=%230F766E" width="16" height="16" alt="" /> Passport MRZ OCR | Machine-readable zone OCR for ICAO travel documents |
| <img src="https://api.iconify.design/lucide/scan-barcode.svg?color=%230F766E" width="16" height="16" alt="" /> ID card barcode | PDF417 / barcode extraction on supported cards |
| <img src="https://api.iconify.design/lucide/camera.svg?color=%230F766E" width="16" height="16" alt="" /> Live capture | Camera locate + Capture; gallery front / optional back |
| <img src="https://api.iconify.design/lucide/shield.svg?color=%230F766E" width="16" height="16" alt="" /> Document liveness | Optional authenticity / PAD (screen, print, photo-swap) when licensed |
| <img src="https://api.iconify.design/lucide/scroll-text.svg?color=%230F766E" width="16" height="16" alt="" /> Result UI | One scroll: identity → fields → checks → images → Raw JSON |
| <img src="https://api.iconify.design/lucide/house.svg?color=%230F766E" width="16" height="16" alt="" /> Home UI | Wide Camera tile + Gallery / About |

---

## <img src="https://api.iconify.design/lucide/pc-case.svg?color=%230F766E" width="24" height="24" alt="" /> Requirements

| | |
| --- | --- |
| OS / device | Physical **arm64** Android phone (emulator is not supported for full camera demos) |
| Tools | Android Studio, **JDK 17**, AGP 8.5+ |
| minSdk / compileSdk | **24** / **34** |
| Demo `applicationId` | `com.identixia.documentreader` |

---

## <img src="https://api.iconify.design/lucide/package.svg?color=%230F766E" width="24" height="24" alt="" /> Install

The sample builds with the AAR already in `libdocsdk/`. Your own app adds one line to the app module:

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/main/install.gradle'
```

That one line pulls the **engine** (`documentreadersdk.aar`) and the reusable **kit** (`libdockey`: `DocSdkSession`, `DocumentGuideView`, `ResultParser`, …).

Keep `minSdk 24`, `abiFilters` `arm64-v8a`, and `packaging { jniLibs { useLegacyPackaging = true } }`.

---

## <img src="https://api.iconify.design/lucide/rocket.svg?color=%230F766E" width="24" height="24" alt="" /> Run

```text
1. git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android.git
2. Open the cloned folder in Android Studio (JDK 17)
3. Run on a physical arm64 device
4. Wait until Home status = Ready → tap Camera or Gallery
```

---

## <img src="https://api.iconify.design/lucide/key-round.svg?color=%230F766E" width="24" height="24" alt="" /> License

| | |
| --- | --- |
| Demo id | `com.identixia.documentreader` |
| Bundled demo license | Valid until **12 Aug 2027** for that `applicationId` |
| Capabilities | Document recognition and/or document liveness (authenticity), per key |

The code below shows how to use the license:

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/f33138b5fb7ca69529f5ca3bdd2cf3dede084b79/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L31-L33](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/f33138b5fb7ca69529f5ca3bdd2cf3dede084b79/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L31-L33)

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/f33138b5fb7ca69529f5ca3bdd2cf3dede084b79/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L76-L77](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/f33138b5fb7ca69529f5ca3bdd2cf3dede084b79/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L76-L77)

Please [contact us](#-contact) to get a license for **your own app**.

---

## <img src="https://api.iconify.design/lucide/puzzle.svg?color=%230F766E" width="24" height="24" alt="" /> Use in your app

1. In the app module, apply `install.gradle` from tag `v1.0.0` (see Install above) — engine + `libdockey`.
2. Activate → init → recognize (prefer kit helpers over raw engine calls).
3. Keep the demo `applicationId` only while using the sample license.

---

## <img src="https://api.iconify.design/lucide/images.svg?color=%230F766E" width="24" height="24" alt="" /> Screenshots

<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-result.png" width="720" alt="ID document recognition Gradio demo — front and back capture, fields, and cropped images" />
</p>

---

## <img src="https://api.iconify.design/lucide/layers.svg?color=%230F766E" width="24" height="24" alt="" /> Platforms

| | Platform | Repo |
| --- | --- | --- |
| <img src="https://cdn.simpleicons.org/android/3DDC84" width="18" height="18" alt="" /> | Android | [ID-Document-Recognition-Liveness-Detection-Android](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) |
| <img src="https://cdn.simpleicons.org/apple/000000" width="18" height="18" alt="" /> | iOS | [ID-Document-Recognition-Liveness-Detection-iOS](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS) |
| <img src="https://cdn.simpleicons.org/flutter/02569B" width="18" height="18" alt="" /> | Flutter | [ID-Document-Recognition-Liveness-Detection-Flutter](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Flutter) |
| <img src="https://cdn.simpleicons.org/react/61DAFB" width="18" height="18" alt="" /> | React Native | [ID-Document-Recognition-Liveness-Detection-React-Native](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-React-Native) |
| <img src="https://cdn.simpleicons.org/ionic/3880FF" width="18" height="18" alt="" /> | Ionic Capacitor | [ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| <img src="https://cdn.simpleicons.org/apachecordova/E8E8E8" width="18" height="18" alt="" /> | Ionic Cordova | [ID-Document-Recognition-Liveness-Detection-Ionic-Cordova](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| <img src="https://cdn.simpleicons.org/windows/0078D4" width="18" height="18" alt="" /> | Windows | [ID-Document-Recognition-Liveness-Detection-Windows](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) |
| <img src="https://cdn.simpleicons.org/docker/2496ED" width="18" height="18" alt="" /> | Linux / Docker | [ID-Document-Recognition-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) |

Document liveness only: [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

---
