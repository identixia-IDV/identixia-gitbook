#!/usr/bin/env python3
"""Platform page builders for customer-facing Identixia GitBook docs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProductCtx:
    name: str
    owner: str
    description: str
    title: str
    platform: str  # Android, iOS, Flutter, ReactNative, Ionic, Ionic-Cordova, Windows, Linux, Hub
    family: str  # face_combined, face_recog, face_liveness, document, document_liveness, hub


STATUS_CODES = """
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
"""

CONTACT = """
### Support

{% include "../../.gitbook/includes/contact.md" %}
"""

# Fix include path - pages are at different depths. Use absolute-from-root style for GitBook.
CONTACT_ROOT = """
## Support

{% include "./.gitbook/includes/contact.md" %}
"""

CONTACT_NESTED = """
## Support

{% include "../.gitbook/includes/contact.md" %}
"""


def github_block(owner: str, name: str) -> str:
    return f"""
## Repository

{{% embed url="https://github.com/{owner}/{name}" %}}

[`{owner}/{name}`](https://github.com/{owner}/{name}) · [Releases](https://github.com/{owner}/{name}/releases/latest)
"""


def overview(ctx: ProductCtx) -> str:
    where = (
        "on the device"
        if ctx.platform
        not in ("Windows", "Linux", "Hub")
        else "on your server (or in your container)"
    )
    return f"""
## Overview

{ctx.description}

Processing runs **{where}**. Identixia does **not** receive biometric images, templates, or document scans.

| | |
| --- | --- |
| **Repository** | [`{ctx.name}`](https://github.com/{ctx.owner}/{ctx.name}) |
| **Platform** | {ctx.platform} |
| **Documentation** | [docs.identixia.com](https://docs.identixia.com) |
"""


def what_you_can_do(ctx: ProductCtx) -> str:
    if ctx.family in ("face_combined", "face_recog"):
        rows = [
            "| Face detection | Bounding box, landmarks, and pose |",
            "| Attributes | Age, gender, and related traits when enabled |",
            "| Quality | ICAO-style image and face quality scores |",
            "| Templates | Compact feature vectors stored in **your** database |",
            "| 1:1 match | Compare two images or two templates |",
        ]
        if ctx.family == "face_combined":
            rows.append(
                "| 1:N identify | Enroll a gallery and search (mobile VideoWorker / server gallery) |"
            )
            rows.append(
                "| Passive liveness + deepfake | PAD and deepfake together when the license includes `liveness`; REAL only if both pass |"
            )
        return (
            "## Capabilities\n\n| Capability | Description |\n| --- | --- |\n"
            + "\n".join(rows)
            + "\n"
        )
    if ctx.family == "face_liveness":
        return """## Capabilities

| Capability | Description |
| --- | --- |
| Passive face liveness + deepfake | Score one RGB face for PAD and deepfake; REAL only when both engines say real |
| License gating | Liveness / deepfake run only when the license includes `liveness` |
"""
    if ctx.family == "document":
        return """## Capabilities

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Visual-zone fields (name, document number, dates, and related data) |
| MRZ | Machine-readable zone parse and checksum checks |
| Barcode / QR | Extracted when present on the document |
| Front and back | Capture both sides when your workflow requires it |
| Document authenticity | Anti-spoof checks when the license includes `authenticity` |
| Structured JSON | Same result model on mobile and server — see Result JSON |
"""
    if ctx.family == "document_liveness":
        return """## Capabilities

| Capability | Description |
| --- | --- |
| Document authenticity API | Checks against screen replay, printout, and substitution |
| Separate from OCR | Complements ID Document Recognition; does not replace it |
"""
    return "## Capabilities\n\nSee the linked platform pages for the full capability list.\n"


def prerequisites(ctx: ProductCtx) -> str:
    if ctx.platform == "Android":
        return """## Prerequisites

| Requirement | Detail |
| --- | --- |
| IDE | Android Studio |
| JDK | **17** |
| Device | Physical **arm64** phone for camera demos |
| minSdk | 24+ |
| ABIs | `arm64-v8a`, `armeabi-v7a` |
| Packaging | `jniLibs { useLegacyPackaging = true }` |
"""
    if ctx.platform == "iOS":
        return """## Prerequisites

| Requirement | Detail |
| --- | --- |
| IDE | Xcode (recent stable) |
| Device | Physical iPhone for camera demos |
| Deployment | iOS 13+ (see sample project) |
| Frameworks | Vendored `.framework` / `.xcframework` from Release or Drive pack |
"""
    if ctx.platform == "Flutter":
        return """## Prerequisites

| Requirement | Detail |
| --- | --- |
| Flutter | Stable channel, recent SDK |
| Android | JDK 17, physical arm64 device |
| iOS | Xcode + CocoaPods; physical iPhone |
| Bootstrap | Run the sample `tool/bootstrap.dart` / `pod install` as documented in the repo |
"""
    if ctx.platform == "ReactNative":
        return """## Prerequisites

| Requirement | Detail |
| --- | --- |
| Node | 18+ |
| Package manager | Yarn (recommended) |
| Android | JDK 17, physical arm64 device |
| iOS | Xcode + CocoaPods; physical iPhone |
| Env | Follow [React Native environment setup](https://reactnative.dev/docs/environment-setup) |
"""
    if ctx.platform in ("Ionic", "Ionic-Cordova"):
        return """## Prerequisites

| Requirement | Detail |
| --- | --- |
| Node | 18+ |
| Ionic CLI | Current stable |
| Android / iOS | Native toolchains as for Capacitor or Cordova |
| Device | Physical phone for camera capture |
"""
    if ctx.platform == "Windows":
        return """## Prerequisites

| Requirement | Detail |
| --- | --- |
| OS | Windows 10/11 x64 |
| Runtime | Product `lib/` (CPU) next to the server |
| Python | As required by the sample server (see repo README) |
| Port | Full face **14103** · recognition-only **14104** · face liveness **14105** · document **14102** · document liveness **14107** |
| License | `.env` `LICENSE=` or `POST /api/activate` |
"""
    if ctx.platform == "Linux":
        return """## Prerequisites

| Requirement | Detail |
| --- | --- |
| Host | Linux x86_64 or any Docker host |
| Docker | Optional — same repository builds the image |
| Port | Full face **14103** · recognition-only **14104** · face liveness **14105** · document **14102** · document liveness **14107** |
| Machine code | Different for bare metal vs container — license the environment you ship |
"""
    return "## Prerequisites\n\nSee the product README for toolchain details.\n"


def _android_aar(name: str) -> str:
    """AAR file name. Distinct for recognition, liveness, and both."""
    if "Document" in name:
        if "Recognition" in name and "Liveness" in name:
            return "documentfullsdk.aar"
        if name.startswith("ID-Document-Liveness"):
            return "documentlivenesssdk.aar"
        return "documentreadersdk.aar"
    if "Recognition" in name and "Liveness" in name:
        return "facefullsdk.aar"
    if name.startswith("FaceLiveness"):
        return "facelivenessdk.aar"
    return "facerecognitionsdk.aar"


def _windows_dll(name: str) -> str:
    """Windows wrapper DLL. Distinct for recognition, liveness, and both."""
    if "Document" in name:
        if "Recognition" in name and "Liveness" in name:
            return "DocumentFullSDK.dll"
        if name.startswith("ID-Document-Liveness"):
            return "DocumentLivenessSDK.dll"
        return "DocumentReaderSDK.dll"
    if "Recognition" in name and "Liveness" in name:
        return "FaceFullSDK.dll"
    if name.startswith("FaceLiveness"):
        return "FaceLivenessSDK.dll"
    return "FaceRecognitionSDK.dll"


def _runtime_paths(ctx: ProductCtx) -> tuple[str, str, str]:
    """Return (asset_hint, local_path, databases_note)."""
    if ctx.platform == "Android" and ctx.family in ("face_combined", "face_recog", "face_liveness"):
        aar = _android_aar(ctx.name)
        stem = aar[: -len(".aar")]
        if ctx.family == "face_liveness" or ctx.name.startswith("FaceLiveness"):
            note = "Required packs: `liveness.xdb` and `recognition-deepfake.xdb`."
        else:
            note = (
                "Required packs: `recognition.xdb`, `recognition-common.xdb`, `recognition-attr.xdb`, "
                "`recognition-quality.xdb`, and when licensed `recognition-liveness.xdb` + `recognition-deepfake.xdb`."
            )
        return (
            f"`{stem}-android.zip` (contains `{aar}` + `databases/*.xdb`)",
            f"`libfacesdk/{aar}` and `libfacesdk/databases/*.xdb`",
            note,
        )
    if ctx.platform == "Android" and ctx.family in ("document", "document_liveness"):
        aar = _android_aar(ctx.name)
        return (
            f"`{aar}`",
            f"`libdocsdk/{aar}`",
            "`document.xdb` is embedded inside the AAR (`assets/document.xdb`).",
        )
    if ctx.platform == "iOS" and ctx.family in ("face_combined", "face_recog", "face_liveness"):
        return (
            "`facerecognitionsdk-ios.zip` (frameworks + `databases/*.xdb`)",
            "Repository root / `Frameworks/` + `databases/*.xdb`",
            "Place every `*.xdb` from the Release next to the frameworks (or under `databases/`).",
        )
    if ctx.platform == "iOS" and ctx.family in ("document", "document_liveness"):
        return (
            "`docsdk.xcframework.zip`",
            "`docsdk.xcframework` / `docsdk.framework` (includes `document.xdb` in the bundle)",
            "If the framework is missing `document.xdb`, add it from the paired SDK pack before shipping.",
        )
    if ctx.platform in ("Flutter", "ReactNative", "Ionic", "Ionic-Cordova"):
        if "Document" in ctx.name or ctx.family.startswith("document"):
            aar = _android_aar(ctx.name)
            return (
                f"Android `{aar}` + iOS `docsdk.xcframework.zip` (from the paired native product Releases)",
                f"See the sample paths in the repository README (`example/android/libdocsdk/{aar}`, `ios/Frameworks/…`)",
                "Document Android embeds `document.xdb` in the AAR; iOS embeds it in the framework bundle.",
            )
        return (
            f"Android `{_android_aar(ctx.name)}` zip + iOS face zip (from the paired Android / iOS product Releases)",
            f"See the sample paths in the repository README (`example/android/libfacesdk/{_android_aar(ctx.name)}`, `ios/Frameworks/…`)",
            "Do not skip database packs — `get_runtime.py` verifies required `*.xdb` files after download.",
        )
    if ctx.platform in ("Windows", "Linux"):
        asset = "GitHub Release `*-windows.zip` / `*-linux.zip`"
        return (
            asset,
            f"`lib/cpu/` (`{_windows_dll(ctx.name)}` on Windows, or the `.so` files on Linux, **and** every required `*.xdb` at the top level)",
            "Face recognition needs the full `recognition*.xdb` set; face liveness needs "
            "`recognition-common.xdb`, `recognition-liveness.xdb`, `recognition-deepfake.xdb`; "
            "document products need `document.xdb`.",
        )
    return (
        "GitHub Release assets for this repository",
        "Paths documented in the product README",
        "Always download database packs with the engine — never ship binaries alone.",
    )


def _run_commands_mobile(ctx: ProductCtx) -> str:
    if ctx.platform == "Android":
        return (
            "Open this folder in **Android Studio** (JDK **17**) and run on a physical **arm64** phone.\n\n"
            "Wait until Home status shows **Ready** before opening camera modes."
        )
    if ctx.platform == "iOS":
        return (
            "Open the Xcode project, set your signing **Team**, and run on a physical iPhone.\n\n"
            "Wait until Home status shows **Ready** before opening camera modes."
        )
    if ctx.platform == "Flutter":
        return (
            "```bash\n"
            "dart run tool/bootstrap.dart\n"
            "cd example && flutter run\n"
            "```\n\n"
            "Use a physical device for camera demos."
        )
    if ctx.platform == "ReactNative":
        return (
            "```bash\nyarn\ncd example && yarn android\n```\n\n"
            "On iOS: `cd example/ios && pod install && cd .. && yarn ios --device`."
        )
    if ctx.platform == "Ionic":
        return (
            "```bash\nnpm install\nnpm run build\nnpx cap sync\nnpx cap run android\n```\n\n"
            "On iOS: `npx cap open ios` after sync, then run from Xcode."
        )
    if ctx.platform == "Ionic-Cordova":
        return (
            "```bash\nnpm install\nnpm run setup:android && npm run android\n```\n\n"
            "On iOS: `npm run setup:ios && npm run ios`."
        )
    return "Follow the repository **Run** section."


def runtime_download_section(ctx: ProductCtx) -> str:
    asset, path, dbs = _runtime_paths(ctx)
    hint_open = '{% hint style="warning" %}'
    hint_close = "{% endhint %}"
    return f"""## Download and place the runtime

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
| **Release asset** | {asset} |
| **Local path after download** | {path} |
| **Databases** | {dbs} |

### Manual download (optional)

Open the repository **Releases** page and download the asset named above:

```text
https://github.com/{ctx.owner}/{ctx.name}/releases/latest/download/<asset>
```

Unzip so files land in the documented path — **not** nested inside an extra folder.

{hint_open}
If databases are missing, activate/init may succeed but recognition, liveness, or OCR will fail at runtime. `get_runtime.py` checks required packs after download.
{hint_close}
"""


def quick_start_mobile(ctx: ProductCtx) -> str:
    clone = f"https://github.com/{ctx.owner}/{ctx.name}.git"
    run_cmds = _run_commands_mobile(ctx)

    install = ""
    if ctx.platform == "Android" and ctx.family in ("face_combined", "face_liveness"):
        install = f"""
### Add the SDK to your own Android app

In the **app** module `build.gradle`:

```gradle
apply from: 'https://raw.githubusercontent.com/{ctx.owner}/{ctx.name}/main/install.gradle'
```

That line pulls the engine and, for face recognition, the reusable **kit** (`libfacekit`: `FaceRecognitionClient`, camera helpers, JSON parsers). Prefer the kit over calling the raw SDK class directly.
"""
    elif ctx.platform == "Android" and ctx.family == "document":
        install = f"""
### Add the SDK to your own Android app

```gradle
apply from: 'https://raw.githubusercontent.com/{ctx.owner}/{ctx.name}/main/install.gradle'
```

Keep `{_android_aar(ctx.name)}` available (Release download or `libdocsdk/`). Use the sample kit helpers for guide crop + `recognize`.
"""

    return f"""## Integration guide — start the project

### 1. Clone the sample

```bash
git clone {clone}
cd {ctx.name}
```

### 2. Download and place the runtime

See [Download and place the runtime](#download-and-place-the-runtime) below. From the repository root:

```bash
python scripts/get_runtime.py
```

### 3. Run the demo

{run_cmds}

### 4. Activate and try every mode

1. Confirm Home / About shows a licensed **Ready** state (sample apps ship a demo key for the sample application id only).
2. Exercise each demo tile once (enroll, identify, capture, attribute, liveness, document front/back, result).
3. For your own app: request a license for **your** application id / bundle id, then call activate → init on a background thread.
{install}
"""


def quick_start_server(ctx: ProductCtx) -> str:
    port = "14103"
    if ctx.family == "document":
        port = "14102"
    elif ctx.family == "document_liveness":
        port = "14107"
    elif ctx.family == "face_liveness":
        port = "14105"
    elif ctx.family == "face_recog":
        port = "14104"

    analyze = ""
    if ctx.family in ("face_combined", "face_recog"):
        analyze = f"""
### Try a process call

```bash
curl -s -X POST http://127.0.0.1:{port}/api/face/analyze \\
  -H "Content-Type: application/json" \\
  -d "{{\\"image\\":\\"BASE64_JPEG\\"}}"
```
"""
    elif ctx.family == "face_liveness":
        analyze = f"""
### Try liveness

```bash
curl -s -X POST http://127.0.0.1:{port}/api/face/liveness \\
  -H "Content-Type: application/json" \\
  -d "{{\\"image\\":\\"BASE64_JPEG\\"}}"
```
"""
    elif ctx.family == "document":
        analyze = f"""
### Try document process

```bash
curl -s -X POST http://127.0.0.1:{port}/api/document/process \\
  -H "Content-Type: application/json" \\
  -d "{{\\"images\\":[{{\\"image\\":\\"BASE64_JPEG\\"}}]}}"
```
"""
    elif ctx.family == "document_liveness":
        analyze = f"""
### Try document liveness

```bash
curl -s -X POST http://127.0.0.1:{port}/api/document/liveness \\
  -H "Content-Type: application/json" \\
  -d "{{\\"images\\":[\\"BASE64_JPEG\\"]}}"
```
"""

    docker = ""
    if ctx.platform == "Linux":
        docker = """
### Docker (when the repo ships an image)

```bash
# See the repository README for the exact image name and tags (CPU/GPU).
docker compose up -d   # or the documented docker run line
curl -s http://127.0.0.1:PORT/api/health
```
"""

    start = "python run_server.py" if ctx.platform == "Windows" else "python3 run_server.py"
    return f"""## Integration guide — start the project

Default API port for this product family: **`{port}`**. Gradio demo (when shipped) uses **`{int(port)+100}`**.

### 1. Clone the sample

```bash
git clone https://github.com/{ctx.owner}/{ctx.name}.git
cd {ctx.name}
```

### 2. Download and place the runtime

Native libraries and `*.xdb` databases are not in git. From the repository root:

```bash
python scripts/get_runtime.py
```

Files must land under `lib/cpu/` (DLLs or `.so` files **and** every required database pack). See [Download and place the runtime](#download-and-place-the-runtime).

### 3. Configure and start the server

```bash
cp -n .env.example .env   # Windows: copy .env.example .env
pip install -r requirements.txt
{start}
```

Configuration lives in **`.env`**: `PORT`, `LICENSE`, `API_BASE`, `DEMO_PORT`. Shell / Compose environment variables still win over `.env`.

### 4. Machine code → license → activate

```bash
curl -s http://127.0.0.1:{port}/api/machinecode
```

Send `data.machinecode` to Identixia and receive a license. Then either set `LICENSE=` in `.env` and restart, or:

```bash
curl -s -X POST http://127.0.0.1:{port}/api/activate \\
  -H "Content-Type: application/json" \\
  -d '{{\\"license\\":\\"YOUR_KEY\\"}}'
curl -s http://127.0.0.1:{port}/api/licenseStatus
curl -s http://127.0.0.1:{port}/api/health
```

Prefer `.env` (`LICENSE=`) for the key — do not use a separate `license.txt`.
{analyze}{docker}
"""


def license_section(ctx: ProductCtx) -> str:
    if ctx.platform in ("Windows", "Linux"):
        return """## License and activation (server)

1. Start the API (it stays up even without a key so you can read the machine code).
2. `GET /api/machinecode` → copy `data.machinecode`.
3. Contact Identixia with that code (Docker and bare metal codes differ).
4. `POST /api/activate` with the key **or** set `LICENSE=` in `.env` and restart.
5. `GET /api/licenseStatus` → check capability flags (`recognition`, `liveness` / `authenticity`).

Control routes return the envelope `{success, code, message, request_id, data}`. Process routes return **engine / process JSON** (not the control envelope).
"""
    demo_id = {
        "face_combined": "`com.identixia.facerecognitionsdk` (Android) / matching iOS bundle id in the sample",
        "face_liveness": "Sample application / bundle id shipped in the repo",
        "document": "Sample application / bundle id shipped in the repo (document reader demo)",
    }.get(ctx.family, "Sample application / bundle id in the repository")

    return f"""## License and activation (mobile)

| | |
| --- | --- |
| **Demo id** | {demo_id} |
| **Demo key** | Bundled for the sample id only |
| **Your app** | New applicationId / bundle id → request a new license |

### Activate → init (concept)

1. Call activate with your license string (background thread).
2. On success, call init (unpacks on-device models; may take a few seconds the first time).
3. Gate UI on Ready / license status before camera modes.
4. Never paste the demo key into a production app id.

{STATUS_CODES}
"""


def face_mobile_api() -> str:
    return """## API reference — mobile face SDK

Prefer **`FaceRecognitionClient`** (Android kit) / the matching iOS kit wrappers. Flutter, React Native, and Ionic expose the **same method names** as Android (`detect`, `faceDetection`, `liveness`, `livenessAll`, …). Serialize all engine calls on **one background thread**.

### Lifecycle

| API | Purpose |
| --- | --- |
| `setActivation(license)` / kit `activate(license)` | Activate (+ init) on a worker thread |
| `init()` | Load models when not bundled into activate |
| `deinit()` / `deactivate()` / `release()` | Tear down engine |
| `getMachineCode()` | Offline machine / app fingerprint helpers |
| `getLicenseStatus()` | Current license flags |
| `allowsRecognition()` / `allowsLiveness()` | Capability checks |

### Still-image recognition

| API | Purpose | Closest HTTP route |
| --- | --- | --- |
| `detect(image, crop?, flags?)` | Detect faces; JSON with regions / landmarks / traits | `POST /api/face/analyze` |
| `faceDetection(image, param?)` | Typed `FaceBox` list / JSON boxes | `POST /api/face/boxes` |
| `faceDetect` / `faceAttribute` / `imageQuality` / `landmarks` | Focused still helpers (plugin channels) | `/api/face/traits`, `/image-quality`, `/landmarks` |
| `match(image1, image2)` | 1:1 image compare | `POST /api/face/compare` |
| `templateExtraction(image, face)` | Template bytes for one face box | `POST /api/face/template` |
| `extractFeature(image)` | Feature bytes (largest / primary face) | `POST /api/face/template` |
| `similarity(feature1, feature2)` | 1:1 score between templates | `POST /api/face/score` |
| `quality(image, crop?)` | Quality attributes JSON | `POST /api/face/quality` |
| `setLandmarkMode(14\\|68)` | Landmark density | — |

### Passive liveness + deepfake (when licensed)

| API | Purpose | Closest HTTP route |
| --- | --- | --- |
| `liveness(image)` | PAD + deepfake | `POST /api/face/liveness` |
| `livenessAll(image)` | Same as `liveness`, high-accuracy pack | `POST /api/face/liveness` |
| `deepfake(image)` | Deepfake-only still check | `POST /api/face/deepfake` |

Treat authenticity as **REAL** only when both PAD and deepfake say real. Without the entitlement, treat missing scores as **not run**, not as pass.

### Gallery (on-device 1:N)

| API | Purpose |
| --- | --- |
| `enroll(name, feature, thumbnail?)` | Store person locally |
| `bestMatch(feature, threshold)` | 1:N search |
| `enrolledPeople()` / `removeEnrolled` / `clearEnrolled` | Gallery management |
| `syncDatabase(matchThreshold)` | Push templates into VideoWorker DB |

### Live camera (VideoWorker)

| API | Purpose |
| --- | --- |
| `startVideoWorker(config)` | Start tracking / identify session |
| `addFrame` / live-frame helpers | Push camera frames |
| `setVideoWorkerEventHandler` | Receive track / match / liveness events (JSON) |
| `stopVideoWorker()` | Stop session |
| `makeTrackingConfig` / `makeIdentityConfig` | Build configs (passive / active liveness options when licensed) |

### Usage example (Android kit)

```kotlin
val client = FaceRecognitionClient.get(context)
client.activate(licenseKey) { code ->
    if (code != 0) return@activate
    // Worker thread: detect + match
    val json = client.detect(bitmap, /* crop */ false, /* flags */ 0)
    val score = client.match(bitmapA, bitmapB)
    val live = client.liveness(bitmap) // when licensed
}
```

### Usage example (plugin / Flutter / React Native / Ionic)

Call the same method names exposed by the plugin bridge (`activate` → `init` → `detect` / `match` / `liveness` / `enroll`). Keep camera preview on the UI thread; keep engine calls on a single background isolate / queue.

### Integration checklist

1. Download runtime with `python scripts/get_runtime.py` (or `install.gradle` on Android).
2. `FaceRecognitionClient.get(context).activate(license) { code -> … }` (or `setActivation` → `init` on plugins).
3. On `0`, enable camera modes.
4. Enroll → Identify, or Capture / Attribute / Liveness for still flows.
5. Persist templates in **your** database if you leave the demo gallery.
"""


def face_http_api(combined: bool) -> str:
    port = "14103" if combined else "14104"
    live = ""
    if combined:
        live = """
| `POST` | `/api/face/liveness` | `{ "image": "<b64>" }` | PAD + deepfake (`liveness_all`); REAL when both pass |
| `POST` | `/api/face/deepfake` | `{ "image": "<b64>" }` | Deepfake-only score when enabled |
"""
    gallery = """
| `POST` | `/api/face/enroll` | `{ "image", "name" }` | Server gallery enroll |
| `POST` | `/api/face/search` | `{ "image", "threshold" }` | 1:N search |
| `GET` | `/api/face/gallery` | — | List gallery |
| `DELETE` | `/api/face/gallery/{id}` | — | Remove gallery entry |
"""
    return f"""## API reference — HTTP (Windows / Linux / Docker)

Base URL: `http://{{host}}:{port}`

There is **no** legacy `/api/detect`, `/api/match`, or `/api/liveness` on this stack — use `/api/face/*` only.

### Control routes (envelope)

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Process up (no license required) |
| `GET` | `/api/backend` | Backend / SDK info |
| `GET` | `/api/machinecode` | Machine fingerprint for licensing |
| `GET` | `/api/licenseStatus` | Flags: `recognition`, `liveness` |
| `POST` | `/api/activate` | License text, JSON `{{"license":"…"}}`, or multipart |

### Process routes (engine / process JSON)

Same path accepts JSON (base64 fields) or `multipart/form-data` (`image`, `image1`, `image2`, …).

| Method | Path | Body (summary) | Description |
| --- | --- | --- | --- |
| `POST` | `/api/face/analyze` | `image`, optional `cropImage` | Full analyze |
| `POST` | `/api/face/boxes` | `image` | Face boxes |
| `POST` | `/api/face/traits` | `image` | Attributes |
| `POST` | `/api/face/image-quality` | `image` | Image quality |
| `POST` | `/api/face/landmarks` | `image`, `mode` `14` or `68` | Landmarks |
| `POST` | `/api/face/quality` | `image` | Face quality |
| `POST` | `/api/face/template` | `image` | Template / feature |
| `POST` | `/api/face/compare` | `image1`, `image2` | 1:1 image match |
| `POST` | `/api/face/score` | `feature1`, `feature2` | Template similarity |
{live}{gallery}
### Live track (when enabled)

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/face/track/start` | Start a tracking session |
| `POST` | `/api/face/track/frame` | Push a frame (base64) |
| `GET` | `/api/face/track/events` | Poll track / match / liveness events |
| `POST` | `/api/face/track/stop` | Stop the session |

### Example — analyze one image

```bash
curl -s -X POST http://127.0.0.1:{port}/api/face/analyze \\
  -H "Content-Type: application/json" \\
  -d '{{"image":"BASE64_JPEG","cropImage":false}}'
```

### Example — compare two images

```bash
curl -s -X POST http://127.0.0.1:{port}/api/face/compare \\
  -H "Content-Type: application/json" \\
  -d '{{"image1":"BASE64_JPEG","image2":"BASE64_JPEG"}}'
```

### Example — template similarity

```bash
curl -s -X POST http://127.0.0.1:{port}/api/face/score \\
  -H "Content-Type: application/json" \\
  -d '{{"feature1":"<b64>","feature2":"<b64>"}}'
```

### Example — Python analyze

```python
import base64, json, urllib.request
from pathlib import Path

image = base64.b64encode(Path("photo.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:{port}/api/face/analyze",
    data=json.dumps({{"image": image, "cropImage": False}}).encode(),
    headers={{"Content-Type": "application/json"}},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

**Postman:** import `postman/Identixia-API.postman_collection.json` (monorepo) or the product `postman/` collection, and set `baseUrl` to `http://127.0.0.1:{port}`.
"""


def face_liveness_http_api() -> str:
    return """## API reference — face liveness HTTP

Base URL: `http://{host}:14105`

Liveness-only products expose `/api/face/liveness` and `/api/face/deepfake` (same paths as the full Face stack). There is **no** `/api/liveness` / `/api/check_liveness` alias on this release.

`POST /api/face/liveness` runs **PAD + deepfake** (`FaceSDK_liveness_all`). Demo UIs treat authenticity as **REAL** only when both traits say real. Use `/api/face/deepfake` for a deepfake-only score.

| Method | Path | Body | Description |
| --- | --- | --- | --- |
| `GET` | `/api/health` | — | Health |
| `GET` | `/api/machinecode` | — | License machine code |
| `GET` | `/api/licenseStatus` | — | Liveness entitlement |
| `POST` | `/api/activate` | license bytes / JSON | Activate |
| `POST` | `/api/face/liveness` | `{ "image": "<b64>" }` | PAD + deepfake (combined authenticity) |
| `POST` | `/api/face/deepfake` | `{ "image": "<b64>" }` | Deepfake-only score when enabled |

```bash
curl -s -X POST http://127.0.0.1:14105/api/face/liveness \\
  -H "Content-Type: application/json" \\
  -d '{"image":"BASE64_JPEG"}'
```

**Postman:** import `postman/FaceLiveness-API.postman_collection.json` from the product repo.
"""


def document_mobile_api() -> str:
    return """## API reference — mobile document SDK

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
"""


def document_http_api() -> str:
    return """## API reference — document HTTP (Windows / Linux / Docker)

Base URL: `http://{host}:14102`

### Control routes

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/backend` | Backend info |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | `recognition`, `authenticity` flags |
| `POST` | `/api/activate` | Activate license |

### Process routes

| Method | Path | Body | Description |
| --- | --- | --- | --- |
| `POST` | `/api/document/process` | `{ "images":[…], "rfid"?, "response"? }` | Full process (OCR + optional authenticity) |
| `POST` | `/api/document/recognition` | `{ "images":[…] }` | Recognition only |
| `POST` | `/api/document/liveness` | `{ "images":[…] }` | Authenticity / liveness only |
| `POST` | `/api/document/general` | `{ "image", "options"? }` | General process helper |

`images` entries are objects with base64 `image` (and optional metadata) or raw base64 strings depending on binding — see the sample Postman collection in the repo `postman/` folder.

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/process \\
  -H "Content-Type: application/json" \\
  -d '{"images":[{"image":"BASE64_JPEG"}]}'
```
"""


def document_liveness_http_api() -> str:
    return """## API reference — document liveness HTTP

Base URL: `http://{host}:14107` (dedicated product; Document Recognition on **14102** also exposes `/api/document/liveness` when licensed).

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | Entitlement |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/document/liveness` | `{ "images": ["<b64>", ...] }` |

This product is **PAD / authenticity**, not OCR. Pair with ID Document Recognition when you need fields.

**Postman:** import `postman/DocumentLiveness-API.postman_collection.json` from the product repo.
"""


def troubleshooting(ctx: ProductCtx) -> str:
    common = """## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Invalid license | Application / bundle id must match the key; server needs the correct machine code |
| Init failed | Runtime AAR/framework/`lib` missing or wrong ABI |
| No face / no document | Lighting, crop, distance; try still gallery image first |
| Liveness / authenticity empty | License flag off — request the matching entitlement |
| Camera black / crash | Use a **physical** device; grant camera permission |
| Docker license fails after bare-metal license | Machine codes differ — re-license the container |
"""
    if ctx.platform in ("Windows", "Linux"):
        common += """
| Port in use | Change host port or stop the other Identixia server |
| Multipart vs JSON | Field names must match (`image`, `image1`, `images`) |
| Envelope vs process JSON | Only control routes use `{success,code,…}`; process routes return engine JSON |
"""
    return common


def _asset(name: str, alt: str, width: int = 180) -> str:
    """GitBook-local asset (copied into identixia-docs/.gitbook/assets/)."""
    return (
        f'<figure><img src="../.gitbook/assets/{name}" alt="{alt}" width="{width}">'
        f"<figcaption>{alt}</figcaption></figure>"
    )


def _asset_root(name: str, alt: str, width: int = 180) -> str:
    return (
        f'<figure><img src=".gitbook/assets/{name}" alt="{alt}" width="{width}">'
        f"<figcaption>{alt}</figcaption></figure>"
    )


def screenshots_section(ctx: ProductCtx, *, nested: bool = True) -> str:
    """Modern product screenshots shipped in .gitbook/assets (not remote hotlinks)."""
    a = _asset if nested else _asset_root

    # Face liveness product / hub
    if ctx.family == "face_liveness" or ctx.name == "Face-Liveness-Detection-SDK":
        imgs = [
            a("liveness-mobile.png", "Mobile liveness result", 220),
            a("liveness-desktop.png", "Desktop liveness demo", 480),
        ]
        return "## Screenshots\n\n" + "\n\n".join(imgs) + "\n"

    # Document products / hub — use split desktop gallery (no tall stacked duplicate).
    if ctx.family in ("document", "document_liveness") or "Document" in ctx.name:
        imgs = [
            a("document-desktop-status.png", "Status", 420),
            a("document-desktop-fields-visual.png", "Visual fields", 420),
            a("document-desktop-checks-validity.png", "Validity checks", 420),
            a("document-desktop-checks-liveness.png", "Liveness checks", 420),
            a("document-desktop-images.png", "Images", 420),
        ]
        if ctx.family == "document_liveness":
            imgs = [
                a("document-desktop-checks-liveness.png", "Liveness checks", 420),
                a("document-desktop-status.png", "Status card", 420),
            ]
        return "## Screenshots\n\n" + "\n\n".join(imgs) + "\n"

    # Face recognition (combined, recognition-only, hub)
    if ctx.family in ("face_combined", "face_recog") or ctx.name == "Face-Recognition-SDK":
        if ctx.platform == "iOS":
            imgs = [
                a("face-ios-home.png", "iOS home", 160),
                a("face-ios-capture.png", "iOS capture", 160),
                a("face-ios-identify.jpg", "iOS identify", 160),
                a("face-ios-attribute.png", "iOS attributes", 160),
                a("face-ios-liveness.png", "iOS liveness", 160),
                a("face-ios-about.png", "iOS about", 160),
            ]
        elif ctx.platform == "Flutter":
            imgs = [
                a("face-flutter-camera.png", "Flutter camera", 200),
                a("face-flutter-result.png", "Flutter result", 200),
                a("face-android-home.png", "Android home (same product family)", 160),
                a("face-android-identify.png", "Android identify", 160),
            ]
        elif ctx.platform in ("Windows", "Linux"):
            imgs = [
                a("face-desktop-detect.png", "Desktop detect", 360),
                a("face-desktop-match.png", "Desktop 1:1 match", 360),
                a("face-desktop-liveness.png", "Desktop liveness", 360),
                a("face-desktop-identify.png", "Desktop identify", 360),
            ]
        elif ctx.platform == "Hub":
            imgs = [
                a("face-android-home.png", "Android home", 160),
                a("face-android-identify.png", "Identify", 160),
                a("face-android-match.png", "1:1 match", 160),
                a("face-desktop-detect.png", "Desktop detect", 280),
            ]
        else:
            imgs = [
                a("face-android-home.png", "Home", 150),
                a("face-android-capture.png", "Capture", 150),
                a("face-android-enroll.png", "Enroll", 150),
                a("face-android-identify.png", "Identify", 150),
                a("face-android-detect.png", "Detect", 150),
                a("face-android-attribute.png", "Attributes", 150),
                a("face-android-quality.png", "Quality", 150),
                a("face-android-landmarks.png", "Landmarks", 150),
                a("face-android-match.png", "Match", 150),
                a("face-android-liveness.png", "Liveness", 150),
                a("face-android-settings.png", "Settings", 150),
                a("face-android-about.png", "About", 150),
            ]
        return "## Screenshots\n\n" + "\n\n".join(imgs) + "\n"

    return ""


def readme_appendix(readme_body: str) -> str:
    if not readme_body.strip():
        return ""
    return (
        "## Repository README\n\n"
        "The following notes are adapted from the shipping repository README "
        "(exact commands and platform-specific details). Screenshots on this page "
        "use the Identixia documentation asset pack.\n\n"
        + readme_body.strip()
        + "\n"
    )


def resources_section(ctx: ProductCtx) -> str:
    return f"""## Resources

| Resource | Link |
| --- | --- |
| **This repository** | [`{ctx.owner}/{ctx.name}`](https://github.com/{ctx.owner}/{ctx.name}) |
| **GitHub Releases (runtime)** | [Latest download](https://github.com/{ctx.owner}/{ctx.name}/releases/latest) |
| **Runtime helper** | `python scripts/get_runtime.py` in the product clone |
| **Documentation site** | [docs.identixia.com](https://docs.identixia.com) |
| **SDK Server (HTTP)** | [SDK Server](../sdk-server/README.md) |
| **Website** | [identixia.com](https://identixia.com) |
| **Hugging Face** | [huggingface.co/Identixia](https://huggingface.co/Identixia) |
| **Docker Hub** | [hub.docker.com/u/identixia](https://hub.docker.com/u/identixia) |
| **Playground** | [playground.identixia.com](https://playground.identixia.com/) |
| **License & support** | [Request a license](../request-a-license-and-support.md) · [Contact](../contact-us.md) |

Postman collections live under each product repository’s `postman/` folder (and the monorepo `postman/Identixia-API.postman_collection.json` for all HTTP routes).
"""


def next_steps(ctx: ProductCtx) -> str:
    lines = [
        "## Next steps",
        "",
        "1. Complete **Integration guide — start the project** until the sample shows **Ready**.",
        "2. Confirm runtime files and databases are in place (`python scripts/get_runtime.py`).",
        "3. Activate with a license issued for **your** application id or machine code.",
        "4. Call only the APIs your license allows; treat missing flags as “not evaluated”, not as pass.",
    ]
    if ctx.family in ("face_combined", "face_recog", "face_liveness"):
        lines.append(
            "5. Return to the [Face SDK](README.md) hub for recognition, liveness, and related platforms."
        )
    elif ctx.family in ("document", "document_liveness"):
        lines.append(
            "5. Return to the [ID Document SDK](README.md) hub for Result JSON and related platforms."
        )
    else:
        lines.append("5. Open the product hub that matches your license.")
    return "\n".join(lines) + "\n"


def cross_platform_face() -> str:
    return """## Related platforms

Keep the same license product line across stacks. From the [Face SDK](README.md) hub:

| Platform | Docs |
| --- | --- |
| Android (full) | [Android](android.md) |
| iOS (full) | [iOS](ios.md) |
| Flutter (full) | [Flutter](flutter.md) |
| React Native (full) | [React Native](react-native.md) |
| Ionic Capacitor (full) | [Ionic Capacitor](ionic-capacitor.md) |
| Ionic Cordova (full) | [Ionic Cordova](ionic-cordova.md) |
| Windows (full) | [Windows](windows.md) |
| Linux / Docker (full) | [Linux / Docker](linux-docker.md) |
| Windows (recognition only) | [Recognition Windows](recognition-windows.md) |
| Linux (recognition only) | [Recognition Linux / Docker](recognition-linux-docker.md) |
| Liveness-only | [Android](liveness-android.md) · [iOS](liveness-ios.md) · [Windows](liveness-windows.md) · [Docker](liveness-linux-docker.md) |
| Function guides | [Recognition](recognition.md) · [Liveness](liveness.md) |
"""


def build_page_body(ctx: ProductCtx, readme_body: str) -> str:
    parts: list[str] = []
    parts.append(overview(ctx))
    parts.append(github_block(ctx.owner, ctx.name))
    parts.append(what_you_can_do(ctx))
    parts.append(prerequisites(ctx))

    if ctx.family == "hub":
        parts.append(
            "## Start here\n\n"
            "Open the platform page that matches your license and stack. "
            "Each page includes quick start, activation, full API reference, and troubleshooting.\n"
        )
        if "Face-Recognition" in ctx.name or ctx.name == "Face-Recognition-SDK":
            parts.append(cross_platform_face())
        parts.append(screenshots_section(ctx, nested=True))
        parts.append(CONTACT_NESTED)
        parts.append(readme_appendix(readme_body))
        return "\n".join(p for p in parts if p)

    parts.append(runtime_download_section(ctx))

    if ctx.platform in ("Windows", "Linux"):
        parts.append(quick_start_server(ctx))
        parts.append(license_section(ctx))
        if ctx.family == "face_combined":
            parts.append(face_http_api(combined=True))
        elif ctx.family == "face_recog":
            parts.append(face_http_api(combined=False))
        elif ctx.family == "face_liveness":
            parts.append(face_liveness_http_api())
        elif ctx.family == "document":
            parts.append(document_http_api())
        elif ctx.family == "document_liveness":
            parts.append(document_liveness_http_api())
    else:
        parts.append(quick_start_mobile(ctx))
        parts.append(license_section(ctx))
        if ctx.family in ("face_combined", "face_recog"):
            parts.append(face_mobile_api())
        elif ctx.family == "face_liveness":
            parts.append(
                "## API reference — mobile face liveness\n\n"
                "Android, iOS, Flutter, React Native, and Ionic share the same customer methods.\n\n"
                "| API | Purpose | Closest HTTP route |\n"
                "| --- | --- | --- |\n"
                "| `setActivation(license)` → `init()` | License then load models (background thread) | `POST /api/activate` |\n"
                "| `getMachineCode()` / `getLicenseStatus()` | License helpers | `/api/machinecode`, `/api/licenseStatus` |\n"
                "| `liveness(image)` | PAD + deepfake | `POST /api/face/liveness` |\n"
                "| `livenessAll(image)` | Same as `liveness`, high-accuracy pack | `POST /api/face/liveness` |\n"
                "| `deepfake(image)` | Deepfake-only still check | `POST /api/face/deepfake` |\n"
                "| VideoWorker / capture kit | Live camera HUD; authenticity REAL only if PAD and deepfake both pass | `/api/face/track/*` |\n\n"
                "Without a liveness entitlement the score is omitted — treat as **not evaluated**, not pass.\n\n"
                "### Usage example\n\n"
                "```text\n"
                "1. python scripts/get_runtime.py\n"
                "2. activate(license) on a background thread → init()\n"
                "3. liveness(bitmap) or start the capture / VideoWorker UI\n"
                "4. Treat authenticity as REAL only when PAD and deepfake both pass\n"
                "```\n"
            )
            parts.append(STATUS_CODES)
        elif ctx.family in ("document", "document_liveness"):
            parts.append(document_mobile_api())

    parts.append(troubleshooting(ctx))
    if ctx.family in ("face_combined", "face_recog"):
        parts.append(cross_platform_face())
    parts.append(screenshots_section(ctx, nested=True))
    parts.append(resources_section(ctx))
    parts.append(next_steps(ctx))
    parts.append(CONTACT_NESTED)
    parts.append(readme_appendix(readme_body))
    return "\n".join(p for p in parts if p)


def classify(name: str, platform: str | None) -> tuple[str, str]:
    """Return (platform_label, family)."""
    plat = platform or "Hub"
    if name.endswith("-SDK") or name in {
        "Face-Recognition-SDK",
        "Face-Liveness-Detection-SDK",
        "ID-Document-Recognition-Liveness-Detection-SDK",
    }:
        return "Hub", "hub"
    if name.startswith("ID-Document-Liveness"):
        return plat if plat != "?" else "Linux", "document_liveness"
    if "Document" in name or name.startswith("ID-Document"):
        return plat, "document"
    if name.startswith("FaceLiveness") or "Face-Liveness" in name:
        return plat, "face_liveness"
    if name in ("FaceRecognition-Windows", "FaceRecognition-Docker"):
        return plat, "face_recog"
    if "FaceRecognition" in name:
        return plat, "face_combined"
    return plat, "hub"
