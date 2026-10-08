---
description: >-
  Passive face liveness SDK for Android. On-device presentation-attack and deepfake checks for KYC. A face is REAL only when both pass. Sample app and docs included.
icon: shield-halved
---

# Face liveness — Android


## Overview

Passive face liveness SDK for Android. On-device presentation-attack and deepfake checks for KYC. A face is REAL only when both pass. Sample app and docs included.

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
| Passive face liveness + deepfake | Score one RGB face for PAD and deepfake; REAL only when both engines say real |
| License gating | Liveness / deepfake run only when the license includes `liveness` |

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
| **Release asset** | `facelivenessdk-android.zip` (contains `facelivenessdk.aar` + `databases/*.xdb`) |
| **Local path after download** | `libfacesdk/facelivenessdk.aar` and `libfacesdk/databases/*.xdb` |
| **Databases** | Required packs: `liveness.xdb` and `recognition-deepfake.xdb`. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceLivenessDetection-Android/releases/latest/download/<asset>
```

Unzip so files land in the documented path — **not** nested inside an extra folder.

{% hint style="warning" %}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{% endhint %}

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Android.git
cd FaceLivenessDetection-Android
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

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/mobile/liveness.png" alt="Mobile liveness result" width="220"><figcaption>Mobile liveness result</figcaption></figure>

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-liveness/desktop/demo-ui.png" alt="Desktop liveness demo" width="480"><figcaption>Desktop liveness demo</figcaption></figure>

## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`identixia-IDV/FaceLivenessDetection-Android`](https://github.com/identixia-IDV/FaceLivenessDetection-Android) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/identixia-IDV/FaceLivenessDetection-Android/releases/latest) |
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

## Identixia Face Liveness Detection — Android

**On-device face liveness SDK** for Android: passive face PAD and deepfake checks (authenticity is **REAL** only if both pass). All processing stays on the phone — no biometric data is sent to Identixia cloud. Ready after you download the AAR and databases (about 10 minutes once the runtime is in place).

> For setup, integration, and API guides, see the [Identixia documentation](https://docs.identixia.com/developers/face-sdk/liveness-android). This page covers the sample repository.

## Basics

Read this once before cloning. Mobile demos may ship a **bundled license** for the sample application id. Production apps need a new key from Identixia.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face liveness detection** for Android |
| **Demo tiles** | Liveness · Settings · About |
| **Runtime** | `libfacelivenesssdk/facelivenesssdk.aar` plus `libfacelivenesssdk/databases/*.xdb` |
| **Demo application id** | `com.identixia.faceliveness` |
| **Tools** | Android Studio · physical arm64 phone |
| **Privacy** | All processing on device — no Identixia cloud |

---

## Initial commands

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Android.git
cd FaceLivenessDetection-Android
python scripts/get_runtime.py
```

Open this folder in **Android Studio** and run on a physical phone. Home status should show **Ready**, then **Liveness / Settings / About** unlock.

Please [contact us](#-contact) to get a license for your own app. The sample may already include a demo license for its application id.

Wait until Home status shows **Ready**, then try the demo tiles. Confirm Result / About shows a licensed state before integrating into your own app.

---

## What you get

| Capability | What it does |
| --- | --- |
| **Liveness** | Live camera PAD + deepfake with face box and authenticity metrics |
| **Settings** | Camera lens (front / back) and liveness threshold |
| **About** | SDK status and on-device anti-spoofing summary |

## Requirements

| | |
| --- | --- |
| Android | API 24 (7.0) minimum; API 29+ recommended |
| ABI | `arm64-v8a`, `armeabi-v7a` |
| Camera | Physical device (emulator is not recommended) |
| Demo application id | `com.identixia.faceliveness` |

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

Place files like this after download:

```text
FaceLivenessDetection-Android/
└── libfacelivenesssdk/
    ├── build.gradle
    ├── facelivenesssdk.aar
    └── databases/
        ├── liveness.xdb
        └── recognition-deepfake.xdb
```

Google Drive folder (alternate download): [FaceLivenessSDK Android](https://drive.google.com/drive/folders/1x3jt02f-YHsk4WD_QlnKJSx5uQ5Ds4xH).

---

## Run

Open this folder in **Android Studio** and run on a physical phone. Home status should show **Ready**, then **Liveness / Settings / About** unlock.

---

## License

Licenses are offline and bound to your `applicationId`. Paste a Face Liveness key for `com.identixia.faceliveness` into the sample. A Face Recognition demo key will not activate this AAR.

Please [contact us](#-contact) to get a license for **your own app**.

After activation, `FaceLivenessSDK.getLicenseStatus()` reports what the key unlocks:

- **Liveness only** / **Recognition + Liveness** — Liveness tile available
- **Recognition only** — liveness stays unavailable on this app
- **No license** — tiles stay locked until you activate

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

{% include "../.gitbook/includes/footer.md" %}
