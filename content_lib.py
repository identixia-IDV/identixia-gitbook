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
                "| Passive liveness | Presentation-attack score when the license includes `liveness` |"
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
| Passive face liveness | Score one RGB face image or camera frame for presentation-attack detection |
| License gating | Liveness runs only when the license includes `liveness` |
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
| Port | Face **14103** · Document **14102** (default) |
| License | `license.txt` or `POST /api/activate` |
"""
    if ctx.platform == "Linux":
        return """## Prerequisites

| Requirement | Detail |
| --- | --- |
| Host | Linux x86_64 or any Docker host |
| Docker | Optional — same repository builds the image |
| Port | Face **14103** · Document **14102** · Document liveness **14106** (product-specific) |
| Machine code | Different for bare metal vs container — license the environment you ship |
"""
    return "## Prerequisites\n\nSee the product README for toolchain details.\n"


def quick_start_mobile(ctx: ProductCtx) -> str:
    clone = f"https://github.com/{ctx.owner}/{ctx.name}.git"
    runtime_note = {
        "face_combined": "Engine zip/AAR/framework from GitHub Releases (`/releases/latest/download/…`) or the files already under `libfacesdk` / Frameworks when present.",
        "face_liveness": "Liveness runtime AAR/framework as documented in the sample `libfacesdk` / Frameworks folder.",
        "document": "Engine AAR / `docsdk` framework from Releases (`documentreadersdk.aar` / `docsdk.xcframework.zip`) or local `libdocsdk`.",
    }.get(ctx.family, "Follow the repository README for the runtime path.")

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

Keep `documentreadersdk.aar` available (Release download or `libdocsdk/`). Use the sample kit helpers for guide crop + `recognize`.
"""

    return f"""## Quick start

### 1. Clone the sample

```bash
git clone {clone}
cd {ctx.name}
```

### 2. Place the runtime

{runtime_note}

Clients should download versioned assets via:

```text
https://github.com/{ctx.owner}/{ctx.name}/releases/latest/download/<asset>
```

### 3. Run the demo

Follow the repository **Run** section (Android Studio / Xcode / `flutter run` / `yarn android` / Ionic). Wait until status shows **Ready** before opening camera modes.

### 4. Try every demo mode

Use each tile / screen once (enroll, identify, capture, document front/back, result, about). Confirm license state on the About / Result screen.
{install}
"""


def quick_start_server(ctx: ProductCtx) -> str:
    port = "14103"
    if ctx.family == "document":
        port = "14102"
    elif ctx.family == "document_liveness":
        port = "14106"
    elif ctx.family == "face_liveness":
        port = "14103"

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
curl -s -X POST http://127.0.0.1:{port}/api/liveness \\
  -H "Content-Type: application/json" \\
  -d "{{\\"image\\":\\"BASE64_JPEG\\"}}"
```
"""
    elif ctx.family == "document":
        analyze = f"""
### Try document process

```bash
curl -s -X POST http://127.0.0.1:{port}/api/documentProcess \\
  -H "Content-Type: application/json" \\
  -d "{{\\"images\\":[{{\\"image\\":\\"BASE64_JPEG\\"}}]}}"
```
"""
    elif ctx.family == "document_liveness":
        analyze = f"""
### Try document liveness

```bash
curl -s -X POST http://127.0.0.1:{port}/api/documentLiveness \\
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

    return f"""## Quick start (server)

Default API port for this product family: **`{port}`**.

### 1. Clone and start

```bash
git clone https://github.com/{ctx.owner}/{ctx.name}.git
cd {ctx.name}
# Follow README: place lib/ runtime, then start the HTTP server / demo UI
```

### 2. Machine code → license → activate

```bash
curl -s http://127.0.0.1:{port}/api/machinecode
# Send data.machinecode to Identixia → receive license
curl -s -X POST http://127.0.0.1:{port}/api/activate \\
  -H "Content-Type: text/plain" \\
  --data-binary @license.txt
curl -s http://127.0.0.1:{port}/api/licenseStatus
curl -s http://127.0.0.1:{port}/api/health
```

You can also drop `license.txt` next to the server and restart.
{analyze}{docker}
"""


def license_section(ctx: ProductCtx) -> str:
    if ctx.platform in ("Windows", "Linux"):
        return """## License and activation (server)

1. Start the API (it stays up even without a key so you can read the machine code).
2. `GET /api/machinecode` → copy `data.machinecode`.
3. Contact Identixia with that code (Docker and bare metal codes differ).
4. `POST /api/activate` with the license file/bytes **or** place `license.txt` and restart.
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

Prefer **`FaceRecognitionClient`** (Android kit) / the matching iOS kit wrappers. Serialize all engine calls on one queue.

### Lifecycle

| API | Purpose |
| --- | --- |
| `activate(license)` | Activate + init on a worker thread; completion returns status code |
| `deactivate()` / `release()` | Tear down engine |
| `getLicenseStatus()` | Current license flags |
| `allowsRecognition()` / `allowsLiveness()` | Capability checks |

### Still-image recognition

| API | Purpose |
| --- | --- |
| `detect(bitmap, crop?, flags?)` | Detect faces; JSON string with regions / landmarks / traits |
| `faceDetection(bitmap, param?)` | Typed `FaceBox` list |
| `templateExtraction(bitmap, face)` | Template bytes for one face box |
| `extractFeature(bitmap)` | Feature bytes (largest / primary face helpers) |
| `similarity(feature1, feature2)` | 1:1 score between templates |
| `quality(bitmap, crop?)` | Quality attributes JSON |
| `setLandmarkMode(14\\|68)` | Landmark density |

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
| `addFrame(bitmap)` | Push camera frames |
| `setVideoWorkerEventHandler` | Receive track / match / liveness events (JSON) |
| `stopVideoWorker()` | Stop session |
| `makeTrackingConfig` / `makeIdentityConfig` | Build configs (passive / active liveness options when licensed) |

### Passive liveness

When the license includes liveness, still-image detect/quality paths and VideoWorker configs can return passive 2D scores. Use `passive2DVerdict` helpers in the kit. Without the entitlement, treat missing scores as **not run**, not as pass.

### Integration checklist

1. Apply `install.gradle` (Android) or vendor iOS frameworks from Release.
2. `FaceRecognitionClient.get(context).activate(license) { code -> … }`.
3. On `0`, enable camera modes.
4. Enroll → Identify, or Capture / Attribute for still flows.
5. Persist templates in **your** database if you leave the demo gallery.
"""


def face_http_api(combined: bool) -> str:
    live = ""
    if combined:
        live = """
| `POST` | `/api/face/liveness` | `{ "image": "<b64>" }` | Passive liveness (license-gated) |
| `POST` | `/api/face/deepfake` | `{ "image": "<b64>" }` | Deepfake score when enabled |
| `POST` | `/api/face/enroll` | `{ "image", "name" }` | Server gallery enroll |
| `POST` | `/api/face/search` | `{ "image", "threshold" }` | 1:N search |
| `DELETE` | `/api/face/gallery/{id}` | — | Remove gallery entry |
"""
    return f"""## API reference — HTTP (Windows / Linux / Docker)

Base URL: `http://{{host}}:14103`

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
{live}
### Example — compare two images

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/compare \\
  -H "Content-Type: application/json" \\
  -d '{{"image1":"BASE64_JPEG","image2":"BASE64_JPEG"}}'
```

### Example — template similarity

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/score \\
  -H "Content-Type: application/json" \\
  -d '{{"feature1":"<b64>","feature2":"<b64>"}}'
```
"""


def face_liveness_http_api() -> str:
    return """## API reference — face liveness HTTP

Base URL: `http://{host}:14103` (confirm in the product README).

| Method | Path | Body | Description |
| --- | --- | --- | --- |
| `GET` | `/api/health` | — | Health |
| `GET` | `/api/machinecode` | — | License machine code |
| `GET` | `/api/licenseStatus` | — | Liveness entitlement |
| `POST` | `/api/activate` | license bytes / JSON | Activate |
| `POST` | `/api/liveness` | `{ "image": "<b64>", "algorithm": "all" }` | Passive liveness |
| `POST` | `/api/check_liveness` | same | Alias |

```bash
curl -s -X POST http://127.0.0.1:14103/api/liveness \\
  -H "Content-Type: application/json" \\
  -d '{"image":"BASE64_JPEG","algorithm":"all"}'
```
"""


def document_mobile_api() -> str:
    return """## API reference — mobile document SDK

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
| `POST` | `/api/documentProcess` | `{ "images":[…], "rfid"?, "response"? }` | Full process (OCR + optional authenticity) |
| `POST` | `/api/documentRecognition` | `{ "images":[…] }` | Recognition only |
| `POST` | `/api/documentLiveness` | `{ "images":[…] }` | Authenticity / liveness only |
| `POST` | `/api/generalProcess` | `{ "image", "options"? }` | General process helper |

`images` entries are objects with base64 `image` (and optional metadata) or raw base64 strings depending on binding — see the sample Postman collection in the repo `postman/` folder.

```bash
curl -s -X POST http://127.0.0.1:14102/api/documentProcess \\
  -H "Content-Type: application/json" \\
  -d '{"images":[{"image":"BASE64_JPEG"}]}'
```
"""


def document_liveness_http_api() -> str:
    return """## API reference — document liveness HTTP

Base URL: `http://{host}:14106` (dedicated product; Document Recognition on **14102** also exposes `/api/documentLiveness` when licensed).

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | Entitlement |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/documentLiveness` | `{ "images": ["<b64>", ...] }` |

This product is **PAD / authenticity**, not OCR. Pair with ID Document Recognition when you need fields.
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


def next_steps(ctx: ProductCtx) -> str:
    lines = [
        "## Next steps",
        "",
        "1. Complete **Quick start** until the sample shows **Ready**.",
        "2. Activate with a license issued for **your** application id or machine code.",
        "3. Call only the APIs your license allows; treat missing flags as “not evaluated”, not as pass.",
    ]
    if ctx.family in ("face_combined", "face_recog", "face_liveness"):
        lines.append(
            "4. Return to the [Face SDK](README.md) hub for recognition, liveness, and related platforms."
        )
    elif ctx.family in ("document", "document_liveness"):
        lines.append(
            "4. Return to the [ID Document SDK](README.md) hub for Result JSON and related platforms."
        )
    else:
        lines.append("4. Open the product hub that matches your license.")
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
                "Activate → init, then score a camera frame or gallery still with the "
                "liveness API exposed by the sample (see kit / SDK class in the repo). "
                "Without a liveness entitlement the score is omitted.\n"
            )
            parts.append(STATUS_CODES)
        elif ctx.family == "document":
            parts.append(document_mobile_api())

    parts.append(troubleshooting(ctx))
    if ctx.family in ("face_combined", "face_recog"):
        parts.append(cross_platform_face())
    parts.append(screenshots_section(ctx, nested=True))
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
