---
description: >-
  Ionic Capacitor ID document recognition plugin for Android and iOS. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.
---

# ID Document Recognition Ionic Capacitor SDK


## Overview

Ionic Capacitor ID document recognition plugin for Android and iOS. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor` |
| **Platform** | Ionic |
| **Docs site** | [doc.identixia.com](https://doc.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor" %}

Source: [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor)

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
| Node | 18+ |
| Ionic CLI | Current stable |
| Android / iOS | Native toolchains as for Capacitor or Cordova |
| Device | Physical phone for camera capture |

## Quick start

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor.git
cd ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor
```

### 2. Place the runtime

Engine AAR / `docsdk` framework from Releases (`documentreadersdk.aar` / `docsdk.xcframework.zip`) or local `libdocsdk`.

Clients should download versioned assets via:

```text
https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/releases/latest/download/<asset>
```

### 3. Run the demo

Follow the repository **Run** section (Android Studio / Xcode / `flutter run` / `yarn android` / Ionic). Wait until status shows **Ready** before opening camera modes.

### 4. Try every demo mode

Use each tile / screen once (enroll, identify, capture, document front/back, result, about). Confirm license state on the About / Result screen.


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

## <img src="https://cdn.simpleicons.org/ionic/3880FF" width="32" height="32" alt="" /> Identixia ID Document Recognition and Liveness Detection — Ionic Capacitor

**On-device ID document recognition** plugin for Android and iOS: passport MRZ OCR, ID card barcode, live capture, and optional document liveness / authenticity for KYC and eKYC. Processing stays on the device — **no** document images go to Identixia cloud.

Package: `document-reader-capacitor`.

<p><img src="https://img.shields.io/badge/On-device-0F766E?style=flat-square" alt="On-device" /> <img src="https://img.shields.io/badge/Android%20%2B%20iOS-0F766E?style=flat-square" alt="Android%20%2B%20iOS" /> <img src="https://img.shields.io/badge/MRZ%20OCR-0F766E?style=flat-square" alt="MRZ%20OCR" /> <img src="https://img.shields.io/badge/Document%20liveness-0F766E?style=flat-square" alt="Document%20liveness" /> <img src="https://img.shields.io/badge/Plugin-5A6573?style=flat-square" alt="Plugin" /></p>

**Capacitor** (not Cordova). Cordova: [ID-Document-Recognition-Liveness-Detection-Ionic-Cordova](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova).

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Read this once before cloning. Plugin demos ship a **bundled license** for the sample Android / iOS ids. Production apps need a new key. [Initial commands](#-initial-commands) lists clone → place runtime → run → activate options.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **ID document recognition** Ionic Capacitor plugin (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license |
| **Extracts** | OCR · passport MRZ · barcode / QR · optional document liveness |
| **Runtime** | Android AAR + iOS framework from Drive zips `PENDING` |
| **Demo id** | `com.identixia.documentreader` / `.app` (until **12 Aug 2027**) |
| **Tools** | npm · Capacitor · physical arm64 Android / iPhone |
| **UI** | Wide Camera Home · Gallery / About · one-scroll Result |
| **Privacy** | All processing on device — no Identixia cloud for document data |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

Must-know path for the sample / example app.

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Clone, place runtime, run

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor.git
cd ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor
npm install && npm run build
cd example && npm install
# place Android + iOS runtimes
npm run build && npx cap sync
npx cap open android   # or: npx cap open ios
```

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Activate / license

Please [contact us](#-contact) to get a license for your own app. The sample already includes a demo license for its application id.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> First capture

Wait until Home = **Ready**, then Camera / Gallery. Confirm Result / About shows a licensed state.

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
| Devices | Physical **arm64** Android and/or **iPhone** |
| Demo Android id | `com.identixia.documentreader` |
| Demo iOS id | `com.identixia.documentreader.app` |
| Package | `document-reader-capacitor` |

---

## <img src="https://api.iconify.design/lucide/package.svg?color=%230F766E" width="24" height="24" alt="" /> Install

The example builds with native runtimes already in the clone when present. Missing files are fetched from the `v1.0.0` GitHub Releases.

| | Path after unzip |
| --- | --- |
| <img src="https://cdn.simpleicons.org/android/3DDC84" width="14" height="14" alt="" /> Android | `example/android/libdocsdk/documentreadersdk.aar` |
| <img src="https://cdn.simpleicons.org/apple/000000" width="14" height="14" alt="" /> iOS | `ios/Frameworks/docsdk.framework` |

Customer apps depend on `document-reader-capacitor` from this repo at tag `v1.0.0` (Flutter: git; React Native / Ionic: npm / github). Do **not** use a monorepo `path:` dependency in shipping apps.

Prefer package kits (`DocumentCapture`, `ResultParser`) for the same camera / Result path as the sample. Keep `useLegacyPackaging = true` on Android when required by the engine.

---

## <img src="https://api.iconify.design/lucide/rocket.svg?color=%230F766E" width="24" height="24" alt="" /> Run

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor.git
cd ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor
npm install && npm run build
cd example && npm install
# place Android + iOS runtimes
npm run build && npx cap sync
npx cap open android   # or: npx cap open ios
```

`ionic serve` alone is not enough — open the native project and run on a physical device.

---

## <img src="https://api.iconify.design/lucide/key-round.svg?color=%230F766E" width="24" height="24" alt="" /> License

Demo ids: Android `com.identixia.documentreader` · iOS `com.identixia.documentreader.app`. Demo license until **12 Aug 2027**.

The code below shows how to use the license:

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/blob/d9f1feaff33d7d18d36aea500b239402b3fb0ced/example/src/license.ts#L7-L17](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/blob/d9f1feaff33d7d18d36aea500b239402b3fb0ced/example/src/license.ts#L7-L17)

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/blob/d9f1feaff33d7d18d36aea500b239402b3fb0ced/example/src/SdkContext.tsx#L60-L70](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/blob/d9f1feaff33d7d18d36aea500b239402b3fb0ced/example/src/SdkContext.tsx#L60-L70)

Capabilities: document recognition and/or document liveness. Please [contact us](#-contact) to get a license for **your own app**.

---

## <img src="https://api.iconify.design/lucide/puzzle.svg?color=%230F766E" width="24" height="24" alt="" /> Use in your app

Install `document-reader-capacitor`, sync Cap native projects with the AAR + framework, then call the plugin activate / init / recognize APIs from your Ionic app.

Depend on `document-reader-capacitor` via **git** `ref: v1.0.0` (not a monorepo `path:`). Ship or download the AAR + framework, then activate → init → recognize.

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

---
