---
description: >-
  Integrate Identixia face liveness detection on iOS. Follow setup and license activation steps for passive anti-spoofing and deepfake checks.
icon: shield-halved
---

# Face Liveness Detection SDK for iOS


## Overview

Passive face liveness SDK for iOS. On-device presentation-attack and deepfake checks for KYC. A face is REAL only when both pass. Sample app and docs included.

Processing runs **on the device**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) |
| **Platform** | iOS |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |


## Repository

{% embed url="https://github.com/identixia-IDV/FaceLivenessDetection-iOS" %}

[`identixia-IDV/FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) · [Releases](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/releases/latest)

## Capabilities

| Capability | Description |
| --- | --- |
| Passive face liveness + deepfake | Check a color face image for presentation attacks and deepfakes; report REAL only when both checks pass |
| License gating | Liveness / deepfake run only when the license includes `liveness` |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| IDE | Xcode (recent stable) |
| Device | Physical iPhone for camera demos |
| Deployment | iOS 13+ (see sample project) |
| Frameworks | Vendored `.framework` / `.xcframework` from Release or Drive pack |

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
| **Release asset** | `facerecognitionsdk-ios.zip` (frameworks + `databases/*.xdb`) |
| **Local path after download** | Repository root / `Frameworks/` + `databases/*.xdb` |
| **Databases** | Place every `*.xdb` from the Release next to the frameworks (or under `databases/`). |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceLivenessDetection-iOS/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-iOS.git
cd FaceLivenessDetection-iOS
```

### 2. Download and place the runtime

See [Download and place the runtime](#download-and-place-the-runtime) below. From the repository root:

```bash
python scripts/get_runtime.py
```

### 3. Run the demo

Open the Xcode project, set your signing **Team**, and run on a physical iPhone.

Wait until Home status shows **Ready** before opening camera modes.

### 4. Activate and try every mode

1. Confirm Home / About shows a licensed **Ready** state (sample apps ship a demo key for the sample application id only).
2. Exercise each demo tile once (enroll, identify, capture, attribute, liveness, document front/back, result).
3. For your own app: request a license for **your** application id / bundle id, then call activate → init on a background thread.


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

Run native SDK calls sequentially on **one background thread**. The engine does not support simultaneous calls.


## API reference — mobile face liveness

Android, iOS, Flutter, React Native, and Ionic share the same customer methods.

| API | Purpose | Closest HTTP route |
| --- | --- | --- |
| `setActivation(license)` → `init()` | License then load models (background thread) | `POST /api/activate` |
| `getMachineCode()` / `getLicenseStatus()` | License helpers | `/api/machinecode`, `/api/licenseStatus` |
| `liveness(image)` | PAD + deepfake | `POST /api/face/liveness` |
| `livenessAll(image)` | Same as `liveness`, high-accuracy pack | `POST /api/face/liveness` |
| `deepfake(image)` | Deepfake-only still check | `POST /api/face/deepfake` |
| VideoWorker / capture kit | Live camera HUD; authenticity REAL only if PAD and deepfake both pass | `/api/face/track/*` |

Without a liveness entitlement the score is omitted — treat as **not evaluated**, not pass.

### Usage example

```text
1. python scripts/get_runtime.py
2. activate(license) on a background thread → init()
3. liveness(bitmap) or start the capture / VideoWorker UI
4. Treat authenticity as REAL only when PAD and deepfake both pass
```


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

![Mobile liveness result](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/mobile/liveness.png)

![Desktop liveness demo](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/desktop/demo-ui.png)

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/releases/latest) |
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
5. Return to the [Face SDK](https://docs.identixia.com/face-sdk) hub for recognition, liveness, and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use images from the identixia-assets repository.

## Face Liveness Detection SDK for iOS — Sample App | Identixia

Integrate **face liveness detection and anti-spoofing** with the **Identixia iOS SDK**. This repository provides a native iOS sample app for passive face liveness detection and deepfake detection. Use presentation attack detection (PAD) to check for face spoofing and deepfake detection to check for manipulated face images. The combined authenticity result is REAL only when both checks pass. Face recognition and matching are not included.

Use the sample to add selfie liveness checks to remote onboarding and biometric identity verification alongside a separate face matching service. Processing runs on the device; images are not sent to the Identixia cloud.

> For setup, integration, and API guides, see the [Face Liveness Detection SDK documentation for iOS](https://docs.identixia.com/developers/face-sdk/liveness-ios). This page covers the sample repository.

## SDK overview

The sample includes a demo license. Your own application requires a key issued for its application identifier.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face liveness detection** for iOS |
| **Demo tiles** | Liveness · Settings · About |
| **Runtime** | `facelivenesssdk.framework`, `FaceLivenessEngine.framework`, `onnxruntime.framework` plus database packs from the Release |
| **Demo bundle id** | `com.identixia.faceliveness.app` |
| **Tools** | Xcode · physical iPhone |
| **Privacy** | All processing on device — no Identixia cloud |

---

## Quick start

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-iOS.git
cd FaceLivenessDetection-iOS
python scripts/get_runtime.py
```

Open `FaceLivenessSDK.xcodeproj` in **Xcode**, set your Team, and run on a physical iPhone. Home status should show ready, then **Liveness / Settings / About** unlock.

The sample includes a demo license for its existing application identifier. Keep that identifier and the bundled key when running the demo. For your own app, request a key from [contact@identixia.com](mailto:contact@identixia.com), replace the demo key, and rebuild. See [SDK license and activation](#-sdk-license-and-activation) below for the source files and activation steps.

Wait for the Home screen to show **Ready**, then select a demo feature. Check the license status on the Result or About screen before integrating the SDK into your own app.

---

## Features

| Capability | What it does |
| --- | --- |
| **Liveness** | Live camera PAD + deepfake with face overlay and authenticity metrics |
| **Settings** | Camera lens and liveness threshold |
| **About** | SDK status and on-device anti-spoofing summary |

## System requirements

| | |
| --- | --- |
| Device | Physical iPhone |
| Tools | Xcode with your signing Team |
| Demo bundle id | `com.identixia.faceliveness.app` |

---

## SDK installation

Run the following script to download the native SDK libraries and model files from this repository’s GitHub Releases. The script places each file in the folder used by the sample.

```bash
python scripts/get_runtime.py
```

To select a release explicitly, pass its tag with `--tag`. For example:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

After `python scripts/get_runtime.py`, the frameworks and database packs should sit at the repository root (or under `Frameworks/` / `databases/` as the Release layout provides).

---

## Run

Open `FaceLivenessSDK.xcodeproj` in **Xcode**, set your Team, and run on a physical iPhone. Home status should show ready, then **Liveness / Settings / About** unlock.

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

- iOS bundle identifier: `com.identixia.faceliveness.app`.

To use the SDK in your own app, email [contact@identixia.com](mailto:contact@identixia.com) with your platform, application ID or bundle identifier, and the SDK features you need. Request a key for your app, replace the demo key in the source file below, and rebuild the app. For apps targeting both Android and iOS, use the key issued for each platform.

Activate the license before initializing the SDK, following the sample’s startup code. Check the license status before using SDK features. If activation fails, verify that the key matches your app identifier and contact Identixia if you need a replacement.

[Demo license definition](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/main/FaceLivenessSDK/Home/ViewController.swift#L8-L11)

[SDK activation call](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/blob/main/FaceLivenessSDK/Home/ViewController.swift#L154-L154)

## API

The following SDK methods are used by the sample and can also be called from your application.

| API | Purpose |
| --- | --- |
| `activate(license)` then `init()` | Activate the license, then initialize the engine. Run these calls in order on one background thread. |
| `getLicenseStatus()` | Check the license status and enabled features before opening the camera. |
| `liveness` / `deepfake` | Run presentation attack detection and deepfake checks. Report REAL only when both pass. |
| Enroll / 1:N | Not included. Use a Face Recognition repository for templates. |

Keep camera preview updates on the UI thread. Run SDK operations sequentially on a single background thread; the engine does not support simultaneous calls.

---

## SDKs for other platforms

| | Platform | Repo |
| --- | --- | --- |

---

{% include "../.gitbook/includes/footer.md" %}
