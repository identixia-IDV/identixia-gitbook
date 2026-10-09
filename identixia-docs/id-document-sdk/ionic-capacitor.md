---
description: >-
  ID document recognition and liveness for Ionic Capacitor. Passport, national ID, and driver license OCR, MRZ, and barcode reading run on the device. Document liveness runs when the license includes it.
---

# ID Document OCR and Liveness Detection SDK for Ionic Capacitor


## Overview

ID document recognition SDK for Ionic Capacitor on Android and iOS. Passport, ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when licensed.

Processing runs **on the device**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| **Platform** | Ionic |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor" %}

[`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) · [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/releases/latest)

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
| Node | 18+ |
| Ionic CLI | Current stable |
| Android / iOS | Native toolchains as for Capacitor or Cordova |
| Device | Physical phone for camera capture |

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
| **Release asset** | Android `documentfullsdk.aar` + iOS `docsdk.xcframework.zip` (from the paired native product Releases) |
| **Local path after download** | See the sample paths in the repository README (`example/android/libdocsdk/documentfullsdk.aar`, `ios/Frameworks/…`) |
| **Databases** | Document Android embeds `document.xdb` in the AAR; iOS embeds it in the framework bundle. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor.git
cd ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor
```

### 2. Download and place the runtime

See [Download and place the runtime](#download-and-place-the-runtime) below. From the repository root:

```bash
python scripts/get_runtime.py
```

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

See [Result JSON](result-json.md) and [Security check fields](security-fields.md).

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
| **This repository** | [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/releases/latest) |
| **Runtime helper** | `python scripts/get_runtime.py` in the product clone |
| **Documentation site** | [docs.identixia.com](https://docs.identixia.com) |
| **SDK Server (HTTP)** | [SDK Server](../sdk-server/README.md) |
| **Website** | [identixia.com](https://identixia.com) |
| **Hugging Face** | [huggingface.co/Identixia](https://huggingface.co/Identixia) |
| **Docker Hub** | [hub.docker.com/u/identixia](https://hub.docker.com/u/identixia) |
| **Playground** | [playground.identixia.com](https://playground.identixia.com/) |
| **License & support** | [Request a license](../request-a-license-and-support.md) · [Contact](../contact-us.md) |

Postman collections live under each product repository’s `postman/` folder (and the monorepo `postman/Identixia-API.postman_collection.json` for all HTTP routes).

## Next steps

1. Complete **Integration guide — start the project** until the sample shows **Ready**.
2. Confirm runtime files and databases are in place (`python scripts/get_runtime.py`).
3. Activate with a license issued for **your** application id or machine code.
4. Call only the APIs your license allows; treat missing flags as “not evaluated”, not as pass.
5. Return to the [ID Document SDK](README.md) hub for Result JSON and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use images from the identixia-assets repository.

## ID Document Recognition and Liveness Detection SDK for Ionic Capacitor — Plugin and Sample App | Identixia

Integrate **ID document OCR and liveness detection** with the **Identixia Ionic Capacitor SDK**. This repository provides a Ionic Capacitor plugin for Android and iOS for reading passports, national ID cards, and driver licenses. Extract identity fields using optical character recognition (OCR), read the machine-readable zone (MRZ), and decode supported document barcodes. Add document liveness checks for screen replays, printed copies, and replaced photos when enabled by your license.

Use the sample to build document capture and data extraction into customer onboarding, Know Your Customer (KYC), and electronic KYC (eKYC) workflows. Processing runs on the device; images are not sent to the Identixia cloud.

Package: `document-reader-capacitor`.

**Capacitor** (not Cordova). Cordova: [ID-Document-Recognition-Liveness-Detection-Ionic-Cordova](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova).

> For setup, integration, and API guides, see the [ID Document Recognition and Liveness Detection SDK documentation for Ionic Capacitor](https://docs.identixia.com/developers/id-document-sdk/ionic-capacitor). This page covers the sample repository.

## SDK overview

The sample includes a demo license. Your own application requires a key issued for its application identifier.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **ID document recognition** Ionic Capacitor plugin (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license |
| **Extracts** | OCR · passport MRZ · barcode / QR · optional document liveness |
| **Runtime** | Android AAR + iOS framework via `python scripts/get_runtime.py` (GitHub Release) |
| **Demo id** | `com.identixia.documentreader` / `.app` (until **12 Aug 2027**) |
| **Tools** | npm · Capacitor · physical arm64 Android / iPhone |
| **UI** | Home screen with Camera, Gallery, and About options; results on one scrollable screen |
| **Privacy** | All processing on device — no Identixia cloud for document data |

---

## Quick start

Choose the instructions for your device below. Run the Android and iOS steps separately; iOS builds require a Mac.

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor.git
cd ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor
```

If the required native SDK libraries are missing from your checkout, run the following script to download them from this repository’s GitHub Releases and place them in the expected folders:

```bash
python scripts/get_runtime.py
```

On macOS, if `python` is not found, run `python3 scripts/get_runtime.py`.

### Android

`ionic serve` and the browser preview do not load the native engine. Use a physical **arm64** Android phone.

From the repository root:

```bash
npm install
npm run build
cd example
npm install
npm run sync
npm run android
```

`npm run android` opens Android Studio. Select the physical arm64 device and press Run.

### iOS

Use a Mac with Xcode and a physical **iPhone**. `ionic serve` does not load the native engine. Do not use the Simulator for the camera sample.

From the repository root:

```bash
npm install
npm run build
cd example
npm install
npm run sync
npm run ios
```

`npm run ios` opens Xcode. Select the physical iPhone and press Run.

The sample runs with its bundled demo key. Keep the sample application id.

For your own app:

1. Email your Android application id or iOS bundle id, and the product name, to [contact@identixia.com](mailto:contact@identixia.com).
2. Replace the demo key in the sample source with the key you receive.
3. Rebuild. The sample activates that key before it initializes the SDK.

Wait for the Home screen to show **Ready**, then choose **Camera** to capture a document or **Gallery** to select an image. Check the license status on the Result or About screen.

---

## Features

| Capability | What it does |
| --- | --- |

---

## System requirements

| | |
| --- | --- |
| Devices | Physical **arm64** Android and/or **iPhone** |
| Demo Android id | `com.identixia.documentreader` |
| Demo iOS id | `com.identixia.documentreader.app` |
| Package | `document-reader-capacitor` |

---

## SDK installation

The example builds with native runtimes already in the clone when present. Missing files are fetched from the `v1.0.0` GitHub Releases.

| | Path after unzip |
| --- | --- |

For your own app, add `document-reader-capacitor` as a dependency from this repository and pin it to the `v1.0.0` tag. Use your package manager’s GitHub dependency syntax. Avoid dependencies on local folders when distributing the app.

Use `DocumentCapture` and `ResultParser` to reuse the sample’s capture and result-handling components. Keep `useLegacyPackaging = true` in the Android build configuration when the engine requires it.

---

## Run

Start in the repository root and follow the commands for your target platform. These commands are also listed in [Quick start](#-quick-start).

**Android** — physical arm64 phone. This opens Android Studio; press Run on that device:

```bash
npm install
npm run build
cd example
npm install
npm run sync
npm run android
```

**iOS** — Mac, Xcode, physical iPhone. This opens Xcode; press Run on that iPhone:

```bash
npm install
npm run build
cd example
npm install
npm run sync
npm run ios
```

---

## SDK license and activation

1. Run the sample with the bundled key and the sample id below.
2. For your own app, email [contact@identixia.com](mailto:contact@identixia.com) with the platform, your application id or bundle id, and the features you need.
3. Put the key you receive in the same place as the demo key.
4. Rebuild. Activation runs before SDK init. If it fails, the key does not match that id.

Sample id:

- `com.identixia.documentreader`
- `com.identixia.documentreader.app`

Set the key, then activate:

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/blob/main/example/src/license.ts#L13-L19](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/blob/main/example/src/license.ts#L13-L19)

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/blob/main/example/src/SdkContext.tsx#L73-L73](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor/blob/main/example/src/SdkContext.tsx#L73-L73)

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

---
