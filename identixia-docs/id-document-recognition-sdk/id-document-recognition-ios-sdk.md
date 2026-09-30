---
description: >-
  On-device ID document recognition SDK for iOS. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.
---

# ID Document Recognition iOS SDK


## Overview

On-device ID document recognition SDK for iOS. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `ID-Document-Recognition-Liveness-Detection-iOS` |
| **Platform** | iOS |
| **Docs site** | [docs.identixia.com](https://docs.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS" %}

Source: [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS)

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
| IDE | Xcode (recent stable) |
| Device | Physical iPhone for camera demos |
| Deployment | iOS 13+ (see sample project) |
| Frameworks | Vendored `.framework` / `.xcframework` from Release or Drive pack |

## Quick start

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS.git
cd ID-Document-Recognition-Liveness-Detection-iOS
```

### 2. Place the runtime

Engine AAR / `docsdk` framework from Releases (`documentreadersdk.aar` / `docsdk.xcframework.zip`) or local `libdocsdk`.

Clients should download versioned assets via:

```text
https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/releases/latest/download/<asset>
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

## Screenshots

<figure><img src="../.gitbook/assets/document-desktop-result.png" alt="Document recognition result UI" width="520"><figcaption>Document recognition result UI</figcaption></figure>

<figure><img src="../.gitbook/assets/document-docker-result.png" alt="Docker document result" width="520"><figcaption>Docker document result</figcaption></figure>


## Support

{% include "../.gitbook/includes/contact.md" %}

## Product README (reference)

Adapted from the shipping repository README for exact commands and platform-specific notes. Screenshots above use the current Identixia asset pack.

## Identixia ID Document Recognition and Liveness Detection — iOS

**On-device ID document recognition** for iPhone: passports, national IDs, and driver licenses with passport MRZ OCR, ID card barcode, live capture, and optional document liveness / authenticity. Designed for KYC and eKYC — **all recognition runs on device**; Identixia never receives your document images.

---

## Basics

Read this once before cloning. Mobile demos ship a **bundled license** for the sample application / bundle id. Production apps need a new key from Identixia. [Initial commands](#-initial-commands) lists clone → place runtime → run → activate options.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **ID document recognition SDK** for iOS (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · passport MRZ · barcode / QR · optional document liveness |
| **Runtime zip** | `docsdk.framework` from Google Drive zip `PENDING` |
| **Demo id / license** | `com.identixia.documentreader.app` — bundled demo license until **12 Aug 2027** |
| **Activate** | Sample app: keep the demo id and bundled key. Your app: new applicationId / bundle id → [contact](#-contact) → call the SDK activate API (see docs). |
| **Tools** | **Xcode 15+** · physical **iPhone** |
| **UI** | Wide Camera Home · Gallery / About · one-scroll Result |
| **Privacy** | All processing on device — no Identixia cloud for document data |

---

## Initial commands

Clone the sample, place the runtime, and run it.

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS.git
cd ID-Document-Recognition-Liveness-Detection-iOS
```

Download the runtime zip (`PENDING`) and place:

```text
docsdk.framework
```

Open `DocumentReader.xcodeproj` in **Xcode 15+** → set Signing Team → Run on a physical iPhone.

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
| Device | Physical **iPhone** (camera demos) |
| Tools | **Xcode 15+**, CocoaPods not required for the framework demo |
| Demo bundle id | `com.identixia.documentreader.app` |

---

## Runtime zip

> **Google Drive (single zip):** `PENDING`

Unzip `docsdk.framework` next to `DocumentReader.xcodeproj` at the repo root:

```text
docsdk.framework
DocumentReader.xcodeproj
```

---

## Run

```text
1. git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS.git
2. Place docsdk.framework at the repo root (from the runtime zip)
3. Open DocumentReader.xcodeproj in Xcode 15+
4. Set your Signing Team; keep bundle id com.identixia.documentreader.app for the demo license
5. Run on a physical iPhone → Home Ready → Camera / Gallery
```

---

## License

| | |
| --- | --- |
| Demo bundle id | `com.identixia.documentreader.app` |
| Bundled demo license | Until **12 Aug 2027** for that id |
| Capabilities | Recognition and/or document liveness per key |

The code below shows how to use the license:

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/blob/be88a3a057808ed15a4a1e74f5828a33df7d2dcd/DocumentReader/ViewController.swift#L14-L15](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/blob/be88a3a057808ed15a4a1e74f5828a33df7d2dcd/DocumentReader/ViewController.swift#L14-L15)

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/blob/be88a3a057808ed15a4a1e74f5828a33df7d2dcd/DocumentReader/ViewController.swift#L147-L149](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/blob/be88a3a057808ed15a4a1e74f5828a33df7d2dcd/DocumentReader/ViewController.swift#L147-L149)

Please [contact us](#-contact) to get a license for **your own app**.

---

## Use in your app

Embed `docsdk.framework`, activate with your license string, init, then recognize. See [docs](https://docs.identixia.com). Do not ship the demo bundle id with a production key mismatch.

Typical KYC path: Home Ready → Camera (or Gallery front/back) → one-scroll Result → Raw JSON for your backend mapping.

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

Document liveness only: [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

---
