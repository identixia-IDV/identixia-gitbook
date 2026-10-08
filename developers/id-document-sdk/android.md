---
description: >-
  Integrate Identixia ID document OCR and liveness detection on Android. Follow setup and license activation steps for passport and ID card OCR, MRZ, and barcode reading.
icon: mobile-screen
---

# ID Document OCR and Liveness Detection SDK for Android


## Overview

ID document recognition SDK for Android. On-device passport, national ID, and driver license OCR, MRZ, and barcode capture for KYC. Document liveness runs when licensed.

Processing runs **on the device**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) |
| **Platform** | Android |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android" %}

[`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) · [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Read printed document fields such as the name, document number, and dates using optical character recognition |
| MRZ | Read the machine-readable zone (MRZ) and validate its check digits |
| Barcode / QR | Extracted when present on the document |
| Front and back | Capture both sides when your workflow requires it |
| Document authenticity | Anti-spoof checks when the license includes `authenticity` |
| Structured JSON | Same result model on mobile and server — see Result JSON |

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

Download the native SDK libraries and model files before running the sample. Use `scripts/get_runtime.py` to retrieve the required GitHub Release assets and place them in the sample's expected folders.

### Download (recommended)

```bash
python scripts/get_runtime.py
```

To pin a specific Release tag:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

| | |
| --- | --- |
| **Release asset** | `documentfullsdk.aar` |
| **Local path after download** | `libdocsdk/documentfullsdk.aar` |
| **Databases** | `document.xdb` is embedded inside the AAR (`assets/document.xdb`). |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android.git
cd ID-Document-Recognition-Liveness-Detection-Android
```

### 2. Download and place the runtime

See [Download and place the runtime](#download-and-place-the-runtime) below. From the repository root:

```bash
python scripts/get_runtime.py
```

### 3. Run the demo

Open this folder in **Android Studio** (JDK **17**) and run on a physical **arm64** phone.

Wait until Home status shows **Ready** before opening camera modes.

### 4. Activate and try every mode

1. Confirm Home / About shows a licensed **Ready** state (sample apps ship a demo key for the sample application id only).
2. Exercise each demo tile once (enroll, identify, capture, attribute, liveness, document front/back, result).
3. For your own app: request a license for **your** application id / bundle id, then call activate → init on a background thread.

### Add the SDK to your own Android app

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/main/install.gradle'
```

Keep `documentfullsdk.aar` available (Release download or `libdocsdk/`). Use the sample kit helpers for guide crop + `recognize`.


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

Run native SDK calls sequentially on **one background thread**. The engine does not support simultaneous calls.


## API reference — mobile document SDK

Android, iOS, Flutter, React Native, and Ionic share the **same customer method names** and the same process JSON idea (`identity` / `readings` / `tests` / `images` / `session`).

### Lifecycle

| API | Purpose |
| --- | --- |
| `setActivation(license)` | Activate license (background thread) |
| `init()` | Load models |
| `deinit()` | Unload engine |
| `getMachineCode()` / `getLicenseStatus()` | License helpers |
| `startNewSession(optionsJson?)` | Open a process session before recognize |

### Capture and process

| API | Purpose |
| --- | --- |
| Guide / crop helpers | Align document in frame (`DocumentGuideView` / kit crop) |
| `locateDocument(image)` | Find document bounds in a frame / still |
| `recognize(front, back?, authenticity?)` | OCR + MRZ + barcode (+ authenticity when licensed) |
| `documentRecognition(front, back?)` | Recognition-only path |
| `documentLiveness(front, back?)` | Authenticity / PAD-only path |
| `documentProcess(imagesJson, rfidJson, optionsJson)` | Combined pipeline (same idea as `POST /api/document/process`) |
| `faceLiveness(image, mode?)` | Optional face PAD helper on document products that ship it |

### Result JSON (shared idea)

Top-level concepts (names may be normalized per platform):

| Area | Contents |
| --- | --- |
| Identity | Document type, country, overall score |
| Fields / readings | OCR, MRZ, barcode field rows |
| Checks / tests | Verification + image quality + security |
| Images | Portrait / document crops (base64) |
| Session | Process / request metadata when present |

See [Result JSON](https://docs.identixia.com/id-document-sdk/result-json) and [Security check fields](https://docs.identixia.com/id-document-sdk/security-fields).

### Integration checklist

1. Apply `install.gradle` or vendor iOS `docsdk`.
2. Activate with your app id license → `init`.
3. Capture front (and back when needed) → `recognize` or `documentProcess`.
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

![Status](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png)

![Visual fields](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-fields-visual.png)

![Validity checks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-validity.png)

![Liveness checks](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png)

![Images](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-images.png)

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/releases/latest) |
| **Runtime helper** | `python scripts/get_runtime.py` in the product clone |
| **Documentation site** | [docs.identixia.com](https://docs.identixia.com) |
| **SDK Server (HTTP)** | [SDK Server](https://docs.identixia.com/sdk-server) |
| **Website** | [identixia.com](https://identixia.com) |
| **Hugging Face** | [huggingface.co/Identixia](https://huggingface.co/Identixia) |
| **Docker Hub** | [hub.docker.com/u/identixia](https://hub.docker.com/u/identixia) |
| **Playground** | [playground.identixia.com](https://playground.identixia.com/) |
| **License & support** | [Request a license](https://docs.identixia.com/guides/request-a-license-and-support) · [Contact](https://docs.identixia.com/guides/contact-us) |

Postman collections live under each product repository’s `postman/` folder (and the monorepo `postman/Identixia-API.postman_collection.json` for all HTTP routes).

## Next steps

1. Complete **Integration guide — start the project** until the sample shows **Ready**.
2. Confirm runtime files and databases are in place (`python scripts/get_runtime.py`).
3. Activate with a license issued for **your** application id or machine code.
4. Call only the APIs your license allows; treat missing flags as “not evaluated”, not as pass.
5. Return to the [ID Document SDK](https://docs.identixia.com/id-document-sdk) hub for Result JSON and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use images from the identixia-assets repository.

## ID Document Recognition and Liveness Detection SDK for Android — Sample App | Identixia

Integrate **ID document OCR and liveness detection** with the **Identixia Android SDK**. This repository provides a native Android sample app for reading passports, national ID cards, and driver licenses. Extract identity fields using optical character recognition (OCR), read the machine-readable zone (MRZ), and decode supported document barcodes. Add document liveness checks for screen replays, printed copies, and replaced photos when enabled by your license.

Use the sample to build document capture and data extraction into customer onboarding, Know Your Customer (KYC), and electronic KYC (eKYC) workflows. Processing runs on the device; images are not sent to the Identixia cloud.

Use the sample to try image capture and review the results screen. To integrate the SDK into your Android app, add the `install.gradle` line shown below.

> For setup, integration, and API guides, see the [ID Document Recognition and Liveness Detection SDK documentation for Android](https://docs.identixia.com/developers/id-document-sdk/android). This page covers the sample repository.

## SDK overview

The sample includes a demo license. Your own application requires a key issued for its application identifier.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **ID document recognition SDK** for Android (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · passport MRZ · barcode / QR · optional document liveness |
| **Runtime zip** | `install.gradle` uses `libdocumentfullsdk/` when `documentfullsdk.aar` is already in this repo |
| **Demo id / license** | `com.identixia.documentreader` — bundled demo license until **12 Aug 2027** |
| **Activate** | Keep the sample’s application identifier and bundled key for evaluation. For your own app, request a key for its Android application ID or iOS bundle identifier and activate it before initializing the SDK. |
| **Tools** | Android Studio · **JDK 17** · physical **arm64** phone (emulator is not enough for full camera demos) |
| **UI** | Home screen with Camera, Gallery, and About options; results on one scrollable screen |
| **Privacy** | All processing on device — no Identixia cloud for document data |

---

## Quick start

Clone the sample, place the runtime, and run it.

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android.git
cd ID-Document-Recognition-Liveness-Detection-Android
python scripts/get_runtime.py
```

The sample applies `install.gradle`. When `libdocumentfullsdk/documentfullsdk.aar` is already in the clone, that is the engine the app builds with.

Open this folder in **Android Studio** (JDK 17) → Run on a physical **arm64** device.

The sample includes a demo license for its existing application identifier. Keep that identifier and the bundled key when running the demo. For your own app, request a key from [contact@identixia.com](mailto:contact@identixia.com), replace the demo key, and rebuild. See [SDK license and activation](#-sdk-license-and-activation) below for the source files and activation steps.

Wait for the Home screen to show **Ready**, then select a capture option. Check the license status on the Result or About screen before integrating the SDK into your own app.

---

## Features

| Capability | What it does |
| --- | --- |

---

## System requirements

| | |
| --- | --- |
| OS / device | Physical **arm64** Android phone (emulator is not supported for full camera demos) |
| Tools | Android Studio, **JDK 17**, AGP 8.5+ |
| minSdk / compileSdk | **24** / **34** |
| Demo `applicationId` | `com.identixia.documentreader` |

---

## SDK installation

The sample builds with the AAR already in `libdocumentfullsdk/`. Your own app adds one line to the app module:

```gradle
apply from: 'https://raw.githubusercontent.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/main/install.gradle'
```

That one line pulls the **engine** (`documentfullsdk.aar`) and the reusable **kit** (`libdockey`: `DocSdkSession`, `DocumentGuideView`, `ResultParser`, …).

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

## SDK license and activation

<p align="center">
<a href="#-contact"><img src="https://img.shields.io/badge/Your%20app-Request%20a%20key-0F766E?style=for-the-badge&logo=gmail&logoColor=white" alt="Request a key" /></a>
</p>

<p align="center">
</p>

<p align="center"><img src="https://img.shields.io/badge/Sample%20code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="Sample code" /></p>

The sample includes a demo license tied to its application identifier. Keep the sample’s identifier and bundled key when evaluating the app. License validation runs locally.

The demo uses these identifiers:

- Android application ID: `com.identixia.documentreader`.

To use the SDK in your own app, email [contact@identixia.com](mailto:contact@identixia.com) with your platform, application ID or bundle identifier, and the SDK features you need. Request a key for your app, replace the demo key in the source file below, and rebuild the app. For apps targeting both Android and iOS, use the key issued for each platform.

Activate the license before initializing the SDK, following the sample’s startup code. Check the license status before using SDK features. If activation fails, verify that the key matches your app identifier and contact Identixia if you need a replacement.

[Demo license definition](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/main/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L30-L31)

[SDK activation call](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android/blob/main/app/src/main/java/com/identixia/documentreader/MainActivity.kt#L62-L62)

## API

The following SDK methods are used by the sample and can also be called from your application.

| API | Purpose |
| --- | --- |
| `activate(license)` then `init()` | Activate the license, then initialize the engine. Run these calls in order on one background thread. |
| Camera | Live capture from the sample Home screen. |
| Gallery | Still image of a passport, national ID, or driver license. |
| `recognize` / document process | Identity, MRZ, barcode, and field text. |
| Document liveness | Presentation-attack result when the license includes it. |

---

## SDKs for other platforms

| | Platform | Repo |
| --- | --- | --- |

Document liveness only: [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

---

{% include "../.gitbook/includes/footer.md" %}
