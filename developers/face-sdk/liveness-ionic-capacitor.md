---
description: >-
  Passive face liveness for Ionic Capacitor. Presentation-attack and deepfake checks run on the device. A face is REAL only when both pass.
icon: file
---

# Face Liveness Detection SDK for Ionic Capacitor

## Overview

| | |
| --- | --- |
| **Repository** | [`FaceLivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Capacitor) · [Releases](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Capacitor/releases/latest) |
| **Platform** | Ionic |
| **Runs** | On the device. Images stay in the app. |

## Capabilities

| Capability | Description |
| --- | --- |
| Passive face liveness + deepfake | Check a color face image for presentation attacks and deepfakes; report REAL only when both checks pass |
| License gating | Liveness / deepfake run only when the license includes `liveness` |

## Prerequisites

| Requirement | Detail |
| --- | --- |
| Node | 18+ |
| Ionic CLI | Current stable |
| Android / iOS | Native toolchains as for Capacitor or Cordova |
| Device | Physical phone for camera capture |

## Download and place the runtime

Download the runtime zip from GitHub Releases and unzip it into the folder listed for that platform.

| | |
| --- | --- |
| **Release asset** | Android `facelivenessdk.aar` zip + iOS face zip (from the paired Android / iOS product Releases) |
| **Local path after download** | See the sample paths in the repository README (`example/android/libfacesdk/facelivenessdk.aar`, `ios/Frameworks/…`) |

### Download

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Capacitor/releases/latest/download/<asset>
```

Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.

## Integration guide — start the project

### 1. Clone the sample

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Capacitor.git
cd FaceLivenessDetection-Ionic-Capacitor
```

### 2. Download and place the runtime

Download the runtime zip from GitHub Releases and unzip it into the path in [Download and place the runtime](#download-and-place-the-runtime).

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

## Support

{% include "../.gitbook/includes/contact.md" %}

{% include "../.gitbook/includes/footer.md" %}
