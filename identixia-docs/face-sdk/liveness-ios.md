---
description: >-
  Passive face liveness SDK for iOS. On-device presentation-attack and deepfake checks for KYC. A face is REAL only when both pass. Sample app and docs included.
---

# Face liveness — iOS


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
| Passive face liveness + deepfake | Score one RGB face for PAD and deepfake; REAL only when both engines say real |
| License gating | Liveness / deepfake run only when the license includes `liveness` |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| IDE | Xcode (recent stable) |
| Device | Physical iPhone for camera demos |
| Deployment | iOS 13+ (see sample project) |
| Frameworks | Vendored `.framework` / `.xcframework` from Release or Drive pack |

## Download and place the runtime

Native engines and model databases are **not** stored in git. Every product ships `scripts/get_runtime.py`, which downloads the correct GitHub Release assets and places them where the sample expects.

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

Unzip so files land in the documented path — **not** nested inside an extra folder.

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

Serialize native SDK calls on **one background thread**. The engine is not concurrent.


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

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/releases/latest) |
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
5. Return to the [Face SDK](README.md) hub for recognition, liveness, and related platforms.


## Support

{% include "../.gitbook/includes/contact.md" %}

## Repository README

The following notes are adapted from the shipping repository README (exact commands and platform-specific details). Screenshots on this page use the Identixia documentation asset pack.

## Identixia Face Liveness Detection — iOS

**On-device face liveness SDK** for iOS: passive face PAD and deepfake checks (authenticity is **REAL** only if both pass). All processing stays on the iPhone — no biometric data is sent to Identixia cloud.

---

## Develop

Use this repository for passive face presentation-attack and deepfake checks, without a recognition gallery. Processing stays on the phone. Identixia does not receive camera frames, templates, or document images.

| | |
| --- | --- |
| **Architecture** | [Where the engine runs](#-architecture) |
| **Quick start** | Follow [Initial commands](#-initial-commands), then [Run](#-run). |
| **Initialize** | [Activate, then init](#-initialize) |
| **Process** | [Camera or a still image](#-process) |
| **Results** | [What to read back](#-results) |
| **Requirements** | [Requirements](#-requirements) |

---

## Resources

| Resource | Where |
| --- | --- |
| **Sample** | This repository — [FaceLivenessDetection-iOS](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) |
| **Client library** | the sample project in this repository |
| **Runtime** | [`python scripts/get_runtime.py`](#-install) · [Releases](https://github.com/identixia-IDV/FaceLivenessDetection-iOS/releases/latest) |
| **API** | [Method list](#-api) |
| **Develop docs** | [docs.identixia.com/face-sdk/liveness-ios](https://docs.identixia.com/face-sdk/liveness-ios) |
| **License** | [License](#-license) · [Contact](#-contact) |
| **Other platforms** | [Platforms](#-platforms) |

---

## Basics

Read this once before cloning. Mobile demos may ship a **bundled license** for the sample application id. Production apps need a new key from Identixia.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face liveness detection** for iOS |
| **Demo tiles** | Liveness · Settings · About |
| **Runtime** | `facelivenesssdk.framework`, `FaceLivenessEngine.framework`, `onnxruntime.framework` plus database packs from the Release |
| **Demo bundle id** | `com.identixia.faceliveness.app` |
| **Tools** | Xcode · physical iPhone |
| **Privacy** | All processing on device — no Identixia cloud |

---

## Initial commands

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-iOS.git
cd FaceLivenessDetection-iOS
python scripts/get_runtime.py
```

Open `FaceLivenessSDK.xcodeproj` in **Xcode**, set your Team, and run on a physical iPhone. Home status should show ready, then **Liveness / Settings / About** unlock.

Please [contact us](#-contact) to get a license for your own app. The sample may already include a demo license for its application id.

Wait until Home status shows **Ready**, then try the demo tiles. Confirm Result / About shows a licensed state before integrating into your own app.

---

## What you get

| Capability | What it does |
| --- | --- |
| **Liveness** | Live camera PAD + deepfake with face overlay and authenticity metrics |
| **Settings** | Camera lens and liveness threshold |
| **About** | SDK status and on-device anti-spoofing summary |

---

## Demo modes

| Mode | What to try |
| --- | --- |
| **Liveness** | Run passive PAD + deepfake on a live face |
| **Settings** | Switch camera lens and adjust the liveness threshold |
| **About** | Confirm license and SDK ready state |

---

## Requirements

| | |
| --- | --- |
| Device | Physical iPhone |
| Tools | Xcode with your signing Team |
| Demo bundle id | `com.identixia.faceliveness.app` |

---

## Install

Download the native engine files from this repository’s GitHub Release. The helper script places libraries and database packs in the correct folders.

```bash
python scripts/get_runtime.py
```

To download a specific Release tag instead of the latest build:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

After `python scripts/get_runtime.py`, the frameworks and database packs should sit at the repository root (or under `Frameworks/` / `databases/` as the Release layout provides).

---

## Run

Open `FaceLivenessSDK.xcodeproj` in **Xcode**, set your Team, and run on a physical iPhone. Home status should show ready, then **Liveness / Settings / About** unlock.

---

## License

Licenses are offline and bound to your bundle id. Please [contact us](#-contact) to get a license for **your own app**. Keep the sample bundle id only while using the bundled demo key.

---

## Use in your app

Add the frameworks to your Xcode app, ship the database packs with the app bundle, then activate → init on a background queue before starting the camera. Full reference: [docs.identixia.com](https://docs.identixia.com).

---

## Architecture

The native engine runs inside the app process. The first successful activate unpacks model databases onto the device. Keep `useLegacyPackaging = true` on Android when the engine loads `.so` files from the AAR.

## Initialize

The sample application id is already licensed. For your own id, request a new key, then call activate and init on a background thread. Open the camera only after the status is Ready. Do not reuse the sample key with a different application id.

| Code | Meaning |
| ---: | --- |
| `0` | Success |
| `1` / `-1` | Invalid license |
| `2` / `-2` | License was issued for a different application id |
| `3` / `-3` | License expired |
| `4` / `-4` | Not activated |
| `-5` | Models failed to load. Run `python scripts/get_runtime.py` and confirm the database packs are present. |
| `-12` | No face in the image |
| `-13` | No document in the image |

## Process

Capture one still or a live frame of the subject. Do not enroll a gallery in this build.

## Results

Read the liveness decision. A face or document is REAL only when every required check passes. A missing score means the check did not run.

## API

The sample and your app use the same method names.

| API | What it returns |
| --- | --- |
| `activate(license)` then `init()` | Load the engine. Call both on one background thread. |
| `getLicenseStatus()` | Read flags before opening the camera. |
| `liveness` / `deepfake` | PAD and deepfake. REAL only if both pass. |
| Enroll / 1:N | Not included. Use a Face Recognition repository for templates. |

Camera frames stay on the UI thread. Engine calls stay on one background thread. The engine is not concurrent.

---

## Platforms

| | Platform | Repo |
| --- | --- | --- |

---
