---
description: >-
  Passive face liveness for Android. Presentation-attack and deepfake checks run on the device. A face is REAL only when both pass.
icon: shield
---

# Face Liveness Detection SDK for Android


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
| Passive face liveness + deepfake | Check a color face image for presentation attacks and deepfakes; report REAL only when both checks pass |
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
| **Release asset** | `facelivenessdk-android.zip` (contains `facelivenessdk.aar` + `databases/*.xdb`) |
| **Local path after download** | `libfacesdk/facelivenessdk.aar` and `libfacesdk/databases/*.xdb` |
| **Databases** | Required packs: `liveness.xdb` and `recognition-deepfake.xdb`. |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceLivenessDetection-Android/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

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

## Face Liveness Detection SDK for Android — Sample App | Identixia

Integrate **face liveness detection and anti-spoofing** with the **Identixia Android SDK**. This repository provides a native Android sample app for passive face liveness detection and deepfake detection. Use presentation attack detection (PAD) to check for face spoofing and deepfake detection to check for manipulated face images. The combined authenticity result is REAL only when both checks pass. Face recognition and matching are not included.

Use the sample to add selfie liveness checks to remote onboarding and biometric identity verification alongside a separate face matching service. Processing runs on the device; images are not sent to the Identixia cloud.

> For setup, integration, and API guides, see the [Face Liveness Detection SDK documentation for Android](https://docs.identixia.com/developers/face-sdk/liveness-android). This page covers the sample repository.

## SDK overview

The sample includes a demo license. Your own application requires a key issued for its application identifier.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **face liveness detection** for Android |
| **Demo tiles** | Liveness · Settings · About |
| **Runtime** | `libfacelivenesssdk/facelivenesssdk.aar` plus `libfacelivenesssdk/databases/*.xdb` |
| **Demo application id** | `com.identixia.faceliveness` |
| **Tools** | Android Studio · physical arm64 phone |
| **Privacy** | All processing on device — no Identixia cloud |

---

## Quick start

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Android.git
cd FaceLivenessDetection-Android
python scripts/get_runtime.py
```

Open this folder in **Android Studio** and run on a physical phone. Home status should show **Ready**, then **Liveness / Settings / About** unlock.

The sample runs with its bundled demo key. Keep the sample application id.

For your own app:

1. Email your Android application id or iOS bundle id, and the product name, to [contact@identixia.com](mailto:contact@identixia.com).
2. Replace the demo key in the sample source with the key you receive.
3. Rebuild. The sample activates that key before it initializes the SDK.

Wait for the Home screen to show **Ready**, then select a demo feature. Check the license status on the Result or About screen before integrating the SDK into your own app.

---

## Features

| Capability | What it does |
| --- | --- |
| **Liveness** | Live camera PAD + deepfake with face box and authenticity metrics |
| **Settings** | Camera lens (front / back) and liveness threshold |
| **About** | SDK status and on-device anti-spoofing summary |

## System requirements

| | |
| --- | --- |
| Android | API 24 (7.0) minimum; API 29+ recommended |
| ABI | `arm64-v8a`, `armeabi-v7a` |
| Camera | Physical device (emulator is not recommended) |
| Demo application id | `com.identixia.faceliveness` |

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

## SDK license and activation

1. Run the sample with the bundled key and the sample id below.
2. For your own app, email [contact@identixia.com](mailto:contact@identixia.com) with the platform, your application id or bundle id, and the features you need.
3. Put the key you receive in the same place as the demo key.
4. Rebuild. Activation runs before SDK init. If it fails, the key does not match that id.

Sample id:

- `com.identixia.faceliveness`

Set the key, then activate:

[https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/main/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L21-L22](https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/main/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L21-L22)

[https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/main/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L55-L55](https://github.com/identixia-IDV/FaceLivenessDetection-Android/blob/main/app/src/main/java/com/identixia/faceliveness/ui/MainActivity.kt#L55-L55)

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
