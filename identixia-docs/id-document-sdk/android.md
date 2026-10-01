---
description: >-
  On-device ID document recognition SDK for Android. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.
---

# ID Document SDK — Android


## Overview

On-device ID document recognition SDK for Android. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `ID-Document-Recognition-Liveness-Detection-Android` |
| **Platform** | Android |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


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

See [Result JSON](result-json.md) and [Security check fields](security-fields.md).

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

## Screenshots

<figure><img src="../.gitbook/assets/document-desktop-status.png" alt="Status" width="420"><figcaption>Status</figcaption></figure>

<figure><img src="../.gitbook/assets/document-desktop-fields-visual.png" alt="Visual fields" width="420"><figcaption>Visual fields</figcaption></figure>

<figure><img src="../.gitbook/assets/document-desktop-checks-validity.png" alt="Validity checks" width="420"><figcaption>Validity checks</figcaption></figure>

<figure><img src="../.gitbook/assets/document-desktop-checks-liveness.png" alt="Liveness checks" width="420"><figcaption>Liveness checks</figcaption></figure>

<figure><img src="../.gitbook/assets/document-desktop-images.png" alt="Images" width="420"><figcaption>Images</figcaption></figure>


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

Adapted from the shipping repository README for exact commands and platform-specific notes. Screenshots above use the current Identixia asset pack.

## Identixia ID Document Recognition and Liveness Detection — Android

**On-device ID document recognition** for Android: passports, national IDs, and driver licenses with passport MRZ OCR, ID card barcode reading, live camera capture, and optional document liveness / authenticity. Built for KYC and eKYC — **identity data stays on the phone**; nothing is uploaded to Identixia cloud.

Use the sample app to evaluate capture UX and the one-scroll Result screen, then add the same `install.gradle` line to your app.

---

## Basics

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

## Initial commands

Clone the sample, place the runtime, and run it.

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android.git
cd ID-Document-Recognition-Liveness-Detection-Android
```

The sample applies `install.gradle`. When `libdocsdk/documentreadersdk.aar` is already in the clone, that is the engine the app builds with.

Open this folder in **Android Studio** (JDK 17) → Run on a physical **arm64** device.

Please [contact us](#-contact) to get a license for your own app. The sample already includes a demo license for its application id.

Wait until Home status = **Ready**, then use Camera / Gallery (or the face mode tiles). Confirm Result / About shows a licensed state before integrating into your own app.

---

## What you get

| Capability | What it does |
| --- | --- |

---

## Requirements

| | |
| --- | --- |
| OS / device | Physical **arm64** Android phone (emulator is not supported for full camera demos) |
| Tools | Android Studio, **JDK 17**, AGP 8.5+ |
| minSdk / compileSdk | **24** / **34** |
| Demo `applicationId` | `com.identixia.documentreader` |

---

## Install

The sample builds with the AAR already in `libdocsdk/`. Your own app adds one line to the app module:

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/main/install.gradle'
```

That one line pulls the **engine** (`documentreadersdk.aar`) and the reusable **kit** (`libdockey`: `DocSdkSession`, `DocumentGuideView`, `ResultParser`, …).

Keep `minSdk 24`, `abiFilters` `arm64-v8a`, and `packaging { jniLibs { useLegacyPackaging = true } }`.

---

## Run

```text
1. git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android.git
2. Open the cloned folder in Android Studio (JDK 17)
3. Run on a physical arm64 device
4. Wait until Home status = Ready → tap Camera or Gallery
```

---

## License

| | |
| --- | --- |
| Demo id | `com.identixia.documentreader` |
| Bundled demo license | Valid until **12 Aug 2027** for that `applicationId` |
| Capabilities | Document recognition and/or document liveness (authenticity), per key |

The code below shows how to use the license:

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/d474f2496acc59fc438352c5c7d157315623eaaf/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L31-L33](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/d474f2496acc59fc438352c5c7d157315623eaaf/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L31-L33)

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/d474f2496acc59fc438352c5c7d157315623eaaf/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L76-L77](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/d474f2496acc59fc438352c5c7d157315623eaaf/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L76-L77)

Please [contact us](#-contact) to get a license for **your own app**.

---

## Use in your app

1. In the app module, apply `install.gradle` from tag `v1.0.0` (see Install above) — engine + `libdockey`.
2. Activate → init → recognize (prefer kit helpers over raw engine calls).
3. Keep the demo `applicationId` only while using the sample license.

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

Document liveness only: [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

---
