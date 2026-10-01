#!/usr/bin/env python3
"""Rebuild Identixia GitBook docs: Face SDK · ID Document SDK · IDV.

Sources:
  - repositories/* product READMEs + catalog/github_about.json (Face + Document)
  - IDV/* (platform overview; no handbook dump)

  python gitbook-push/generate.py
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_lib as C  # noqa: E402

ABOUT_PATH = ROOT / "catalog" / "github_about.json"
NAMES_PATH = ROOT / "catalog" / "repository_names.json"
REPOS_DIR = ROOT / "repositories"
ASSETS_SRC = REPOS_DIR / "identixia-assets"
IDV_DIR = ROOT / "IDV"
OUT = Path(__file__).resolve().parent / "identixia-docs"
DOCS_BASE = "https://docs.identixia.com"
GH = "https://github.com/identixia-IDV"

# Flattened local names under .gitbook/assets/ (one copy each).
ASSET_COPY: list[tuple[str, str]] = [
    ("brand/logo.png", "brand-logo.png"),
    ("brand/mark.png", "brand-mark.png"),
    ("screenshots/face-recognition/android/home.png", "face-android-home.png"),
    ("screenshots/face-recognition/android/capture.png", "face-android-capture.png"),
    ("screenshots/face-recognition/android/enroll.png", "face-android-enroll.png"),
    ("screenshots/face-recognition/android/identify.png", "face-android-identify.png"),
    ("screenshots/face-recognition/android/detect.png", "face-android-detect.png"),
    ("screenshots/face-recognition/android/attribute.png", "face-android-attribute.png"),
    ("screenshots/face-recognition/android/attribute-quality.png", "face-android-quality.png"),
    ("screenshots/face-recognition/android/landmarks.png", "face-android-landmarks.png"),
    ("screenshots/face-recognition/android/match.png", "face-android-match.png"),
    ("screenshots/face-recognition/android/attribute-liveness.png", "face-android-liveness.png"),
    ("screenshots/face-recognition/android/settings.png", "face-android-settings.png"),
    ("screenshots/face-recognition/android/about.png", "face-android-about.png"),
    ("screenshots/face-recognition/ios/home.png", "face-ios-home.png"),
    ("screenshots/face-recognition/ios/capture.png", "face-ios-capture.png"),
    ("screenshots/face-recognition/ios/identify.jpg", "face-ios-identify.jpg"),
    ("screenshots/face-recognition/ios/attribute.png", "face-ios-attribute.png"),
    ("screenshots/face-recognition/ios/attribute-liveness.png", "face-ios-liveness.png"),
    ("screenshots/face-recognition/ios/about.png", "face-ios-about.png"),
    ("screenshots/face-recognition/flutter/camera.png", "face-flutter-camera.png"),
    ("screenshots/face-recognition/flutter/result.png", "face-flutter-result.png"),
    ("screenshots/face-recognition/desktop/demo-ui-detect.png", "face-desktop-detect.png"),
    ("screenshots/face-recognition/desktop/demo-ui-match.png", "face-desktop-match.png"),
    ("screenshots/face-recognition/desktop/demo-ui-liveness.png", "face-desktop-liveness.png"),
    ("screenshots/face-recognition/desktop/demo-ui-identify.png", "face-desktop-identify.png"),
    ("screenshots/face-liveness/mobile/liveness.png", "liveness-mobile.png"),
    ("screenshots/face-liveness/desktop/demo-ui.png", "liveness-desktop.png"),
    ("screenshots/document-reader/desktop/demo-ui-status.png", "document-desktop-status.png"),
    ("screenshots/document-reader/desktop/demo-ui-fields-visual.png", "document-desktop-fields-visual.png"),
    ("screenshots/document-reader/desktop/demo-ui-fields-code.png", "document-desktop-fields-code.png"),
    ("screenshots/document-reader/desktop/demo-ui-checks-validity.png", "document-desktop-checks-validity.png"),
    ("screenshots/document-reader/desktop/demo-ui-checks-liveness.png", "document-desktop-checks-liveness.png"),
    ("screenshots/document-reader/desktop/demo-ui-images.png", "document-desktop-images.png"),
]

BRAND_EXTRA: list[tuple[Path, str]] = [
    (IDV_DIR / "license" / "admin" / "brand" / "favicon.ico", "favicon.ico"),
    (IDV_DIR / "license" / "admin" / "brand" / "favicon.png", "favicon.png"),
    (IDV_DIR / "license" / "admin" / "brand" / "apple-touch-icon.png", "apple-touch-icon.png"),
    (IDV_DIR / "docs" / "audit-console.png", "idv-audit-console.png"),
    (IDV_DIR / "docs" / "device-idv-screen.png", "idv-device-screen.png"),
]

# Catalog homepage leaf → human title (section hubs use README.md).
TITLES: dict[str, str] = {
    "face-sdk": "Face SDK",
    "recognition": "Face recognition",
    "liveness": "Face liveness",
    "android": "Android",
    "ios": "iOS",
    "flutter": "Flutter",
    "react-native": "React Native",
    "ionic-capacitor": "Ionic Capacitor",
    "ionic-cordova": "Ionic Cordova",
    "windows": "Windows (recognition + liveness)",
    "linux-docker": "Linux / Docker (recognition + liveness)",
    "recognition-windows": "Windows (recognition only)",
    "recognition-linux-docker": "Linux / Docker (recognition only)",
    "liveness-android": "Android (liveness only)",
    "liveness-ios": "iOS (liveness only)",
    "liveness-windows": "Windows (liveness only)",
    "liveness-linux-docker": "Linux / Docker (liveness only)",
    "id-document-sdk": "ID Document SDK",
    "result-json": "Result JSON",
    "security-fields": "Security check fields",
    "idv": "IDV platform",
    "architecture": "Architecture",
    "quick-start": "Quick start",
    "walkthrough": "End-to-end walkthrough",
    "project-structure": "Project structure",
    "initial-setup": "Initial setup process",
    "session-states": "Session states",
    "api": "Creating a session (API)",
    "production": "Production",
    "engines": "Prerequisites: engines",
    "components": "Components & clients",
}

# Catalog hubs: custom section/concept pages win (do not dump product README over them).
HUB_REPOS = {
    "Face-Recognition-SDK",  # -> face-sdk/
    "Face-Liveness-Detection-SDK",  # -> face-sdk/liveness (concept page)
    "ID-Document-Recognition-Liveness-Detection-SDK",  # -> id-document-sdk/
}

PLATFORM_MAP = {
    "Android": "Android",
    "iOS": "iOS",
    "Flutter": "Flutter",
    "ReactNative": "ReactNative",
    "Ionic": "Ionic",
    "Ionic-Cordova": "Ionic-Cordova",
    "Windows": "Windows",
    "Linux": "Linux",
}


def load_catalog() -> tuple[dict, dict[str, dict]]:
    about = json.loads(ABOUT_PATH.read_text(encoding="utf-8"))
    names = {
        item["name"]: item
        for item in json.loads(NAMES_PATH.read_text(encoding="utf-8"))["repositories"]
        if isinstance(item, dict) and "name" in item
    }
    return about, names


def homepage_rel(url: str) -> str | None:
    if not url.startswith(DOCS_BASE):
        return None
    return url[len(DOCS_BASE) :].lstrip("/") or None


def title_for(rel: str) -> str:
    leaf = rel.rsplit("/", 1)[-1]
    return TITLES.get(leaf) or TITLES.get(rel) or re.sub(r"[-_]+", " ", leaf).title()


def rewrite_links(text: str, owner: str) -> str:
    text = text.replace("https://doc.identixia.com", DOCS_BASE)
    text = text.replace("https://docs.identixia.com", DOCS_BASE)
    text = text.replace("https://github.com/identixiaAI/", f"https://github.com/{owner}/")
    return text


def _plain_heading(line: str) -> str:
    m = re.match(r"^(#{1,6})\s+(.*)$", line)
    if not m:
        return line
    level, rest = m.group(1), m.group(2)
    rest = re.sub(r"<img\b[^>]*>\s*", "", rest, flags=re.I)
    rest = re.sub(r"<[^>]+>", "", rest).strip()
    rest = re.sub(r"\s+", " ", rest)
    return f"{level} {rest}" if rest else line


def strip_readme_noise(body: str) -> str:
    lines = body.splitlines()
    out: list[str] = []
    started = False
    skip_screenshots = False
    for line in lines:
        if not started:
            if re.match(r"^#+\s+", line):
                started = True
                line = _plain_heading(line)
                if line.startswith("# "):
                    out.append("## " + line[2:])
                else:
                    out.append(line)
            continue
        if line.strip() in {"</div>", '<div align="center">', "<div align='center'>"}:
            continue
        if re.search(r"Contact\s*$", line) and (
            "mail.svg" in line or line.strip().startswith("##")
        ):
            break
        if re.match(r"^##+\s+.*Screenshots", line, flags=re.I):
            skip_screenshots = True
            continue
        if skip_screenshots:
            if re.match(r"^##+\s+", line):
                skip_screenshots = False
            else:
                continue
        if "contact@identixia.com" in line and "img.shields.io" in line:
            continue
        if "cdn.simpleicons.org" in line or "api.iconify.design" in line:
            if re.match(r"^#+\s+", line):
                out.append(_plain_heading(line))
            continue
        if "img.shields.io" in line and (
            line.strip().startswith("<p>")
            or line.strip().startswith("<img")
            or "badge/-" in line
        ):
            continue
        line = line.replace(
            "raw.githubusercontent.com/identixiaAI/identixia-assets",
            "raw.githubusercontent.com/identixia-IDV/identixia-assets",
        )
        if re.match(r"^#+\s+", line):
            line = _plain_heading(line)
        out.append(line)
    text = "\n".join(out).strip() + "\n"
    text = re.sub(r"<p>\s*</p>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def frontmatter(description: str) -> str:
    desc = description.replace("\n", " ").strip()
    if len(desc) > 280:
        desc = desc[:277] + "..."
    return f"---\ndescription: >-\n  {desc}\n---\n\n"


def write_page(path: Path, title: str, description: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        frontmatter(description) + f"# {title}\n\n" + body.rstrip() + "\n",
        encoding="utf-8",
        newline="\n",
    )


def sync_assets() -> None:
    dest = OUT / ".gitbook" / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    # Remove stale flattened copies we no longer map (keep includes elsewhere).
    keep = {dst for _, dst in ASSET_COPY} | {dst for _, dst in BRAND_EXTRA}
    for p in dest.iterdir():
        if p.is_file() and p.name not in keep:
            p.unlink()
    for src_rel, dst_name in ASSET_COPY:
        src = ASSETS_SRC / src_rel
        if not src.is_file():
            print(f"WARN missing asset: {src_rel}")
            continue
        shutil.copy2(src, dest / dst_name)
    for src, dst_name in BRAND_EXTRA:
        if src.is_file():
            shutil.copy2(src, dest / dst_name)
        else:
            print(f"WARN missing brand: {src}")


def out_path_for(rel: str) -> Path:
    if "/" not in rel:
        return OUT / rel / "README.md"
    section, leaf = rel.split("/", 1)
    return OUT / section / f"{leaf}.md"


def build_product_page(owner: str, item: dict, rel: str, by_name: dict[str, dict]) -> Path | None:
    name = item["name"]
    if name in HUB_REPOS:
        return None
    desc = item["description"]
    title = title_for(rel)
    # Prefer clear platform titles for product pages
    if "/" in rel:
        leaf = rel.split("/", 1)[1]
        title = TITLES.get(leaf, title)
        # Prefix with product family for clarity
        if rel.startswith("face-sdk/"):
            if leaf.startswith("liveness-"):
                title = f"Face liveness — {title.split('(')[0].strip()}"
            elif leaf.startswith("recognition-"):
                title = f"Face recognition — {title.split('(')[0].strip()}"
            elif leaf in ("recognition", "liveness"):
                title = TITLES[leaf]
            else:
                title = f"Face SDK — {title}"
        elif rel.startswith("id-document-sdk/"):
            if leaf.startswith("liveness-"):
                title = f"Document liveness — {title.split('(')[0].strip()}"
            elif leaf in ("recognition", "liveness", "result-json", "security-fields"):
                title = TITLES[leaf]
            else:
                title = f"ID Document SDK — {title}"

    meta = by_name.get(name, {})
    plat_raw = meta.get("platform")
    plat_label, family = C.classify(name, PLATFORM_MAP.get(plat_raw, plat_raw))
    ctx = C.ProductCtx(
        name=name,
        owner=owner,
        description=desc,
        title=title,
        platform=plat_label,
        family=family,
    )
    readme_path = REPOS_DIR / name / "README.md"
    readme_body = ""
    if readme_path.is_file():
        raw = rewrite_links(readme_path.read_text(encoding="utf-8", errors="replace"), owner)
        readme_body = strip_readme_noise(raw)
    body = C.build_page_body(ctx, readme_body)
    out = out_path_for(rel)
    write_page(out, title, desc, body)
    return out


def write_face_hub() -> None:
    body = f"""
<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>

## Overview

The **Face SDK** runs entirely on the device or on your server. It covers two independently licensed functions:

| Function | Capabilities | License flag |
| --- | --- | --- |
| **Recognition** | Detect faces, attributes, quality, templates, 1:1 match, 1:N identify | `recognition` |
| **Liveness** | Passive presentation-attack score (live person vs photo or screen) | `liveness` |

Choose a **repository that matches your license**. A recognition-only build does not return liveness scores.

## Product lines

| Requirement | Start here |
| --- | --- |
| Recognition **and** liveness in one app or API | [Full product](full-product.md) (Android through Docker) |
| Recognition only | [Windows](recognition-windows.md) · [Linux / Docker](recognition-linux-docker.md) |
| Liveness only | [Android](liveness-android.md) · [iOS](liveness-ios.md) · [Windows](liveness-windows.md) · [Linux / Docker](liveness-linux-docker.md) |

Function guides:

* [Face recognition](recognition.md) — detect, templates, gallery, match
* [Face liveness](liveness.md) — when scores appear and how to gate UX

## Full product (recognition + liveness)

| Platform | Repository | Docs |
| --- | --- | --- |
| Android | [`FaceRecognition-LivenessDetection-Android`]({GH}/FaceRecognition-LivenessDetection-Android) | [Android](android.md) |
| iOS | [`FaceRecognition-LivenessDetection-iOS`]({GH}/FaceRecognition-LivenessDetection-iOS) | [iOS](ios.md) |
| Flutter | [`FaceRecognition-LivenessDetection-Flutter`]({GH}/FaceRecognition-LivenessDetection-Flutter) | [Flutter](flutter.md) |
| React Native | [`FaceRecognition-LivenessDetection-React-Native`]({GH}/FaceRecognition-LivenessDetection-React-Native) | [React Native](react-native.md) |
| Ionic Capacitor | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`]({GH}/FaceRecognition-LivenessDetection-Ionic-Capacitor) | [Ionic Capacitor](ionic-capacitor.md) |
| Ionic Cordova | [`FaceRecognition-LivenessDetection-Ionic-Cordova`]({GH}/FaceRecognition-LivenessDetection-Ionic-Cordova) | [Ionic Cordova](ionic-cordova.md) |
| Windows | [`FaceRecognition-LivenessDetection-Windows`]({GH}/FaceRecognition-LivenessDetection-Windows) | [Windows](windows.md) |
| Linux / Docker | [`FaceRecognition-LivenessDetection-Docker`]({GH}/FaceRecognition-LivenessDetection-Docker) | [Linux / Docker](linux-docker.md) |

<figure><img src="../.gitbook/assets/face-android-home.png" alt="Face SDK Android home" width="160"><figcaption>Android demo home</figcaption></figure>

## Integration path

1. Open the platform page for your stack.
2. Clone the sample, place engine binaries from GitHub Releases, and run until status shows **Ready**.
3. Activate with **your** application id or machine code (demo keys work only for demo ids).
4. Call recognition and liveness APIs on a **background** thread (mobile) or over HTTP (server).

{{% hint style="info" %}}
Biometric images and templates stay on **your** device or server. Identixia does not host them.
{{% endhint %}}
""".strip()
    write_page(
        OUT / "face-sdk" / "README.md",
        "Face SDK",
        "On-premise Face SDK: recognition and passive liveness for mobile and server platforms.",
        body + "\n",
    )


def write_face_concepts() -> None:
    write_page(
        OUT / "face-sdk" / "recognition.md",
        "Face recognition",
        "What Identixia face recognition does, which APIs to call, and which repositories ship it.",
        f"""
## Overview

Face **recognition** turns a camera image into data you can store and compare:

1. **Detect** the face (box, landmarks, pose).
2. **Describe** it (optional attributes and quality).
3. **Encode** it as a compact **template** (feature vector).
4. **Compare** templates (1:1) or search a gallery (1:N).

You own the gallery database. The SDK does not upload faces to Identixia.

## Typical mobile flow

```text
activate(license) → initSDK()
        │
        ├─ detect / attributes / quality / landmarks
        ├─ template (enroll) → save in YOUR database
        ├─ match (1:1) two images or two templates
        └─ identify (1:N) probe against enrolled people
```

## Typical server flow (HTTP)

Control routes use `{{success, code, message, request_id, data}}`. Process routes return engine JSON.

| Step | Route (examples) |
| --- | --- |
| Health | `GET /api/health` |
| Machine code | `GET /api/machinecode` |
| Activate | `POST /api/activate` |
| Detect / analyze | `POST /api/face/analyze` or `/api/face/boxes` |
| Template | `POST /api/face/template` |
| 1:1 | `POST /api/face/compare` |
| 1:N | `POST /api/face/enroll` · `/api/face/search` · `/api/face/gallery` |

### Example — 1:1 compare (Linux / Windows)

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/compare \\
  -H "Content-Type: application/json" \\
  -d '{{"image1":"BASE64_A","image2":"BASE64_B"}}'
```

Parse the process JSON for score / match decision. Do not scrape the demo UI.

## Repositories that include recognition

| Variant | Platforms |
| --- | --- |
| Full (recognition + liveness) | [Android](android.md) · [iOS](ios.md) · [Flutter](flutter.md) · [React Native](react-native.md) · [Ionic](ionic-capacitor.md) · [Windows](windows.md) · [Docker](linux-docker.md) |
| Recognition only | [Windows](recognition-windows.md) · [Docker](recognition-linux-docker.md) |

Hub pack: [`Face-Recognition-SDK`]({GH}/Face-Recognition-SDK)

## License

Without `recognition` entitlement, detect/template/match calls fail or return empty results. Check `GET /api/licenseStatus` (server) or the kit license status (mobile).
""".strip()
        + "\n",
    )
    write_page(
        OUT / "face-sdk" / "liveness.md",
        "Face liveness",
        "Passive face liveness: when it runs, which products include it, and how to read the score.",
        f"""
## Overview

Face **liveness** answers whether the subject is a live person or a photo, screen, or replay.

It is **passive**: the user looks at the camera. The core API does not require smile or blink challenges.

## When a score appears

| Situation | Result |
| --- | --- |
| License includes `liveness` | Engine returns a liveness score / decision |
| License is recognition-only | No liveness score — treat as “not evaluated”, not as “pass” |
| Wrong product repo | Use a **liveness** or **full** repository, not recognition-only |

## Products

| Product line | Docs |
| --- | --- |
| Full Face SDK (recognition + liveness) | Platform pages under [Face SDK](README.md) |
| Liveness-only | [Android](liveness-android.md) · [iOS](liveness-ios.md) · [Windows](liveness-windows.md) · [Docker](liveness-linux-docker.md) |

Hub pack: [`Face-Liveness-Detection-SDK`]({GH}/Face-Liveness-Detection-SDK)

## Server example

Default Face API port is **14103** (confirm in the product README).

```bash
# Full / recognition+liveness Docker stack
curl -s -X POST http://127.0.0.1:14103/api/face/liveness \\
  -H "Content-Type: application/json" \\
  -d '{{"image":"BASE64_JPEG"}}'
```

Liveness-only Docker uses the path documented on [Linux / Docker (liveness only)](liveness-linux-docker.md) (often `/api/liveness`).

## Mobile tip

Run activate → init → liveness on a **background** thread. Keep the camera preview on the UI thread. If VideoWorker / tracking is used, start it when the camera screen appears and stop it when the screen closes.

<figure><img src="../.gitbook/assets/liveness-mobile.png" alt="Mobile liveness" width="200"><figcaption>Mobile liveness result</figcaption></figure>
""".strip()
        + "\n",
    )


def write_document_hub() -> None:
    body = f"""
<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>

## Overview

The **ID Document SDK** reads passports, national IDs, and driver licenses **on-premise**. Two independently licensed functions:

| Function | Capabilities | License flag |
| --- | --- | --- |
| **Recognition** | Locate, OCR, MRZ, barcode, cropped images | `recognition` |
| **Liveness / authenticity** | Anti-spoof checks (screen, printout, substitution) | `authenticity` |

Full product repositories run **both** when the license allows. A **liveness-only** Linux / Docker API is available when you need authenticity without the full OCR surface.

## Start here

1. [Document recognition](recognition.md) — fields, MRZ, images
2. [Document liveness](liveness.md) — authenticity checks versus OCR
3. [Result JSON](result-json.md) — shared shape for mobile and server
4. [Security check fields](security-fields.md) — how to read authenticity results

## Full product (recognition + liveness)

| Platform | Repository | Docs |
| --- | --- | --- |
| Android | [`ID-Document-Recognition-Liveness-Detection-Android`]({GH}/ID-Document-Recognition-Liveness-Detection-Android) | [Android](android.md) |
| iOS | [`ID-Document-Recognition-Liveness-Detection-iOS`]({GH}/ID-Document-Recognition-Liveness-Detection-iOS) | [iOS](ios.md) |
| Flutter | [`ID-Document-Recognition-Liveness-Detection-Flutter`]({GH}/ID-Document-Recognition-Liveness-Detection-Flutter) | [Flutter](flutter.md) |
| React Native | [`ID-Document-Recognition-Liveness-Detection-React-Native`]({GH}/ID-Document-Recognition-Liveness-Detection-React-Native) | [React Native](react-native.md) |
| Ionic Capacitor | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) | [Ionic Capacitor](ionic-capacitor.md) |
| Ionic Cordova | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) | [Ionic Cordova](ionic-cordova.md) |
| Windows | [`ID-Document-Recognition-Liveness-Detection-Windows`]({GH}/ID-Document-Recognition-Liveness-Detection-Windows) | [Windows](windows.md) |
| Linux / Docker | [`ID-Document-Recognition-Liveness-Detection-Docker`]({GH}/ID-Document-Recognition-Liveness-Detection-Docker) | [Linux / Docker](linux-docker.md) |

## Liveness-only API

| Platform | Repository | Docs |
| --- | --- | --- |
| Linux / Docker | [`ID-Document-Liveness-Detection-Docker`]({GH}/ID-Document-Liveness-Detection-Docker) | [Document liveness Docker](liveness-linux-docker.md) |

<figure><img src="../.gitbook/assets/document-desktop-status.png" alt="Document demo status" width="480"><figcaption>Desktop demo — status</figcaption></figure>

{{% hint style="info" %}}
Document images and OCR fields stay on **your** device or server. Parse [Result JSON](result-json.md) — do not scrape the Result UI.
{{% endhint %}}
""".strip()
    write_page(
        OUT / "id-document-sdk" / "README.md",
        "ID Document SDK",
        "On-premise ID Document SDK: recognition (OCR/MRZ) and document liveness for mobile and server.",
        body + "\n",
    )


def write_document_concepts() -> None:
    write_page(
        OUT / "id-document-sdk" / "recognition.md",
        "Document recognition",
        "OCR, MRZ, barcode, and images from ID documents — APIs and repositories.",
        f"""
## Overview

Document **recognition** finds the card in the frame and extracts:

* Visual-zone fields (name, document number, dates, and related data)
* **MRZ** (machine-readable zone)
* Barcode / QR when present
* Cropped images (portrait, document, signature, and related crops)

## Capture tips

* Prefer a **physical** device for camera demos.
* Align the document inside the guide; capture front (and back when required).
* On mobile, call locate → capture → `recognize` on a **background** thread.

## Server routes (full Document Docker / Windows)

Default full-product API port is **14102** (confirm in the README).

| Route | Role |
| --- | --- |
| `POST /api/documentProcess` | Full process (recognition + authenticity when licensed) |
| `POST /api/documentRecognition` | OCR / MRZ / barcode only |
| `POST /api/documentLiveness` | Authenticity only |

### Example — recognition-only call

```bash
curl -s -X POST http://127.0.0.1:14102/api/documentRecognition \\
  -H "Content-Type: application/json" \\
  -d '{{"images":["BASE64_FRONT","BASE64_BACK"]}}'
```

Response shape: [Result JSON](result-json.md).

## Repositories

Full mobile + server samples are listed on the [ID Document SDK](README.md) hub.  
Packaging hub: [`ID-Document-Recognition-Liveness-Detection-SDK`]({GH}/ID-Document-Recognition-Liveness-Detection-SDK)
""".strip()
        + "\n",
    )
    write_page(
        OUT / "id-document-sdk" / "liveness.md",
        "Document liveness",
        "Document authenticity / anti-spoofing — separate from OCR, license-gated.",
        f"""
## Overview

Document **liveness** (authenticity) checks whether the ID is likely a physical document versus:

* A screen replay
* A printout or paper copy
* Portrait or document substitution (when the engine supports it)

It does **not** replace OCR. You can run authenticity alone or together with recognition.

## License rule

| License | What you get |
| --- | --- |
| `authenticity` present | `security` / related checks populate in result JSON |
| Missing | Empty or omitted security — **not** a pass |

See [Security check fields](security-fields.md).

## Where it ships

| Product | Docs |
| --- | --- |
| Full Document SDK (mobile + server) | Platform pages on [ID Document SDK](README.md) |
| Liveness-only Linux / Docker | [Document liveness Docker](liveness-linux-docker.md) |

### Example — authenticity-only (full server)

```bash
curl -s -X POST http://127.0.0.1:14102/api/documentLiveness \\
  -H "Content-Type: application/json" \\
  -d '{{"images":["BASE64_FRONT"]}}'
```

<figure><img src="../.gitbook/assets/document-desktop-checks-liveness.png" alt="Liveness checks UI" width="480"><figcaption>Desktop demo — liveness checks</figcaption></figure>
""".strip()
        + "\n",
    )
    write_page(
        OUT / "id-document-sdk" / "result-json.md",
        "Result JSON",
        "Customer process JSON for mobile recognize and server document APIs.",
        """
## Purpose

Mobile `recognize` and server `POST /api/documentProcess` (also recognition / liveness routes) return one **customer process JSON**. Parse this object in your app — do not scrape the demo Result UI.

Allowed top-level keys:

| Key | Role |
| --- | --- |
| `identity` | Document class, country, overall score |
| `readings` | OCR / MRZ / barcode field rows |
| `tests` | Validity, capture, and authenticity checks |
| `images` | Crops (face, document pages, …) as base64 |
| `session` | Job id, status code, detail, timestamp |

There is **no** separate top-level `security` object. Authenticity lives in `tests` rows with `group: "authenticity"`.

## Field shapes

### `identity`

| Field | Example | Meaning |
| --- | --- | --- |
| `class` / `type` | `"Passport"` | Document class |
| `country` | `"UTO"` | Issuing country |
| `score` | `0.91` | Overall document confidence when present |

### `readings[]`

| Field | Example | Meaning |
| --- | --- | --- |
| `name` | `"familyName"`, `"firstNames"`, `"docNumber"` | Canonical field id |
| `value` | `"DOE"` | Extracted text |
| `origin` / `source` | `"visual"`, `"zone"`, `"code"`, `"chip"` | Visual OCR, MRZ zone, barcode, RFID |
| `score` | `0.97` | Optional confidence |

Kits may still emit legacy names (`surname`, `mrz`, …). Prefer the sample `ResultParser` / `ix_payload` helpers when present.

### `tests[]`

| Field | Example | Meaning |
| --- | --- | --- |
| `name` | `"expiry"`, `"focus"`, `"foilCheck"` | Check id |
| `group` / `kind` | `"validity"`, `"capture"`, `"authenticity"` | Category |
| `outcome` / `result` | `"pass"`, `"fail"`, `"hold"` | Decision (`hold` ≈ skip / not evaluated) |
| `page` | `0` / `1` | Front / back when applicable |
| `score` | `0.88` | Optional numeric score |
| `note` / `reason` | `"expired"` | Optional explanation |

Overall UI grouping uses **most-severe-wins** within each kind: `fail` > `hold` > `pass`.

### `images[]`

| Field | Meaning |
| --- | --- |
| `name` / `id` | Crop role (`face`, document page, …) |
| `page` | Page index when multi-page |
| `data` / `image` | Base64 payload |

### `session`

| Field | Meaning |
| --- | --- |
| `jobId` | Transaction / job id |
| `code` | `0` = ready / success; non-zero = failure |
| `detail` | Short status (`ready`, `failed`, …) |
| `at` | ISO timestamp |

## Example (contract fixture)

```json
{
  "identity": { "class": "Passport", "country": "UTO", "score": 0.91 },
  "readings": [
    { "name": "familyName", "value": "DOE", "origin": "visual", "score": 0.97 },
    { "name": "firstNames", "value": "JOHN", "origin": "visual", "score": 0.96 },
    { "name": "docNumber", "value": "123456789", "origin": "zone", "score": 0.99 }
  ],
  "tests": [
    { "name": "expiry", "group": "validity", "outcome": "pass" },
    { "name": "focus", "group": "capture", "outcome": "pass", "score": 0.9 },
    { "name": "foilCheck", "group": "authenticity", "page": 0, "outcome": "pass", "score": 0.88 }
  ],
  "images": [
    { "name": "face", "page": 0, "data": "<base64>" }
  ],
  "session": {
    "jobId": "identixia_0123456789abcdef0123456789abcdef",
    "code": 0,
    "detail": "ready",
    "at": "2026-09-14T00:55:12Z"
  }
}
```

## Related

* [Security check fields](security-fields.md) — authenticity rows in detail
* [Document recognition](recognition.md) · [Document liveness](liveness.md)
""".strip()
        + "\n",
    )
    write_page(
        OUT / "id-document-sdk" / "security-fields.md",
        "Security check fields",
        "How to read document authenticity / liveness checks inside Result JSON tests[].",
        """
## Where authenticity lives

Document authenticity (document liveness) is **not** a separate top-level `security` object in the customer process JSON. It appears as rows in `tests[]` where:

```text
group == "authenticity"   // also accepted: kind, or legacy "security" / "liveness"
```

Parent shape: [Result JSON](result-json.md).

## When rows appear

| Situation | Meaning |
| --- | --- |
| No authenticity rows | Feature **not licensed**, **not requested**, or engine omitted them — **not a pass** |
| Rows with `outcome: "fail"` | Treat as authenticity reject per your risk policy |
| Rows with `outcome: "hold"` | Not evaluated / skipped — do not treat as pass |
| Recognition-only license | Use OCR/MRZ (`readings` + validity/capture tests) only |

## Row fields

| Field | Meaning |
| --- | --- |
| `name` | Check id (e.g. `foilCheck`; legacy `hologramIntegrity` maps to the same idea) |
| `group` | Must resolve to `authenticity` |
| `outcome` | `pass` · `fail` · `hold` |
| `page` | `0` = front, `1` = back |
| `score` | Optional float (demo UI may show six decimals) |
| `note` / `reason` | Optional human-readable detail |

### Example authenticity row

```json
{
  "name": "foilCheck",
  "group": "authenticity",
  "page": 0,
  "outcome": "pass",
  "score": 0.88
}
```

### Example summary logic (same idea as the desktop demo)

```text
authenticity_rows = tests where group == "authenticity"
if none → "not evaluated"
else count pass / fail / hold → apply your policy (any fail ⇒ reject is common)
```

## License rule

| License | What you get |
| --- | --- |
| `authenticity` present | Authenticity `tests` populate when the route requests them |
| Missing | Empty authenticity set — never invent a pass |

Server routes: `POST /api/documentLiveness` (authenticity only) or `POST /api/documentProcess` (OCR + authenticity when licensed).
""".strip()
        + "\n",
    )


def write_idv_pages() -> None:
    write_page(
        OUT / "idv" / "README.md",
        "IDV platform",
        "Self-host identity verification platform: setup guide, sessions, APIs, and webhooks.",
        f"""
<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>
<p align="center"><img src="../.gitbook/assets/favicon.png" alt="Identixia mark" width="48"></p>

## What IDV is

**IDV** is Identixia’s self-host identity-verification platform. It uses your on-premise **Document** and **Face** SDK HTTP engines as the biometric backend. It does not replace those SDKs — it orchestrates them between your company systems and applicant capture apps.

## Project components

| Component | Role | Folder · port |
| --- | --- | --- |
| **Platform (Admin)** | Tenant API, reviews, Identity Console | `platform/server/` · `:14187` · UI `:14188` / `/admin` |
| **Company (Merchant)** | Holds service credentials; starts sessions | `company/backend/` · `:14195` · Admin `:14189` |
| **Applicant (User)** | Web / mobile capture apps | `client/` · e.g. web `:5175` |
| **Engines** | Document + Face HTTP APIs | Document `:14102` · Face `:14103` |

```text
Applicant app ──► Company backend :14195 ──► IDV server :14187 ──► Face / Document engines
                      │                         │
               Company Admin :14189      Identity Console /admin
```

## Read this guide (in order)

1. [Project structure](project-structure.md)
2. [Prerequisites: engines](engines.md) — start and activate Document + Face first
3. [Project setup](environment.md) — `.env`, tokens, storage
4. [Initial setup process](initial-setup.md) — first console login, settings, webhook secret
5. [Quick start](quick-start.md) · [End-to-end walkthrough](walkthrough.md)
6. [Session states](session-states.md)
7. [Creating a session (API)](api.md)
8. [Webhook integration](company-webhooks.md)
9. [Applicant clients](components-clients.md) · [Production](production.md)

<figure><img src="../.gitbook/assets/idv-audit-console.png" alt="Identity Console" width="520"><figcaption>Identity Console</figcaption></figure>
<figure><img src="../.gitbook/assets/idv-device-screen.png" alt="Applicant capture" width="220"><figcaption>Applicant capture</figcaption></figure>

{{% hint style="danger" %}}
**Safety:** Keep the company **service bearer** on the company backend only. Capture apps receive a short-lived **capture token**. Never commit secrets. `IDV_OPEN_API=1` / bearer `demo` is for **localhost demos only**. License Admin (`:14190`) stays on a private host.
{{% endhint %}}
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "architecture.md",
        "Architecture",
        "IDV runtime flow across company backend, platform server, engines, and consoles.",
        """
## Runtime flow

```text
Company backend :14195              Capture app (web / mobile)
       │                                      │
       │  service bearer → POST /v1/sessions  │
       │  mint capture token / launch URL     │
       ├─────────────────────────────────────►│
       │                                      │ submissions (+ step headers)
       │                                      ▼
       │                               IDV Server :14187
       │                          engines → decision → store
       │                                      │
       │◄──────── webhooks (session.*) ───────┤
       ▼                                      ▼
 Company Admin :14189                 Identity Console /admin
```

1. **Company backend** holds the service credentials and starts a verification session on IDV.
2. It returns a **capture token** / launch URL to the applicant app (or operator UI).
3. The **capture client** submits step bundles to IDV (`/submissions`).
4. IDV calls **Document** and **Face** HTTP engines, evaluates trust, may open review.
5. IDV notifies the company via **webhooks**; operators use Identity Console and Company Admin.

## Authority

| Concern | Owner |
| --- | --- |
| Document OCR / face match / liveness scores | Document SDK + Face SDK |
| Tenant policy, sessions, reviews, API auth | `platform/server` |
| Holding service tokens, starting sessions for apps | **Your** backend (sample: `company/backend`) |
| Hybrid entitlement metering on customer host | `license/license_v2` inside `platform/server` |
| Issuing Hybrid licences | `license/admin` (Identixia) |

## Decision rule

Trust aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing or error signals never auto-accept (`platform/server/idv/decision/`).
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "quick-start.md",
        "Quick start",
        "Run IDV server, Identity Console, company backend/admin, and licence admin locally.",
        """
## Order that works locally

1. Complete [Project setup](environment.md) (`.env`)
2. Document engine `:14102` + Face engine `:14103` — [Prerequisites: engines](engines.md)
3. Run `python IDV/scripts/start_local.py` **or** start services manually below
4. [Initial setup process](initial-setup.md) — console, company settings, webhook
5. [End-to-end walkthrough](walkthrough.md)

## Helper (recommended)

```bash
# Engines must already be healthy on :14102 and :14103
python IDV/scripts/start_local.py
```

Preflight checks engine health, starts IDV server + company backend, and prints URLs. It does **not** start License Admin and does **not** mean the stack is production-ready when `IDV_OPEN_API=1`.

## Storage defaults

| Project | Default SQLite |
| --- | --- |
| `platform/server` | `platform/server/database/idv.sqlite` (or `IDV_SQLITE_PATH`) |
| `company/backend` | `company/backend/database/company.sqlite` |
| `license/admin` | `license/admin/database/` |

PostgreSQL / media / Valkey / RabbitMQ: `python setup_database.py` from `IDV/`. See [Project setup](environment.md).

## Manual commands

```bash
# Platform (localhost demo auth only)
cd IDV/platform/server && python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
# → http://127.0.0.1:14187/v1  and  /admin/

# Identity Console (develop)
cd IDV/platform/console && npm install && npm run dev
# → http://127.0.0.1:14188/

# Company server + admin UI
cd IDV/company/backend && pip install -r requirements.txt
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
# → http://127.0.0.1:14195/  (built admin at /admin/)

cd IDV/company/admin && npm install && npm run dev
# → http://127.0.0.1:14189/

# Licence issuer (localhost / private network only — never public)
cd IDV/license/admin && pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
# → http://127.0.0.1:14190/
```
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "engines.md",
        "Prerequisites: engines",
        "Start and activate Document and Face HTTP engines before running IDV.",
        """
## Why this comes first

IDV calls Identixia **Document** and **Face** HTTP APIs for OCR, authenticity, match, and liveness. Start and activate those engines **before** the IDV server and company sample.

When `IDV_ENGINES=http`, the platform uses:

| Role | Default URL | Example paths |
| --- | --- | --- |
| Document Reader | `http://127.0.0.1:14102` | `/api/documentProcess`, `/api/documentRecognition`, `/api/documentLiveness` |
| Face Recognition + liveness | `http://127.0.0.1:14103` | `/api/face/compare`, `/api/face/boxes`, `/api/face/template`, `/api/face/score`, `/api/face/liveness` |

Child pages: [Document engine](engines-document.md) · [Face engine](engines-face.md).

Same process APIs as [ID Document SDK](../id-document-sdk/) and [Face SDK](../face-sdk/). Document responses follow [Result JSON](../id-document-sdk/result-json.md).

## Numbered setup

1. Run the Document server (Windows or Docker) on **14102** — see [ID Document SDK → Server](../id-document-sdk/full-server.md).
2. Run the Face server on **14103** — see [Face SDK → Server](../face-sdk/full-server.md).
3. Activate each engine with **its** machine code (`GET /api/machinecode` → send to Identixia → `POST /api/activate` or `license.txt`). Docker and bare metal codes differ.
4. Confirm health:

```bash
curl -s http://127.0.0.1:14102/api/health
curl -s http://127.0.0.1:14103/api/health
```

5. Set `IDV_ENGINES=http`, `DOCUMENT_API_URL`, and `FACE_API_URL` in `IDV/.env` (see [Project setup](environment.md)).
6. Continue with [Initial setup process](initial-setup.md) or `python IDV/scripts/start_local.py`.

## Session create (platform API)

Usually the **company backend** calls this with the service bearer (not the capture app):

```http
POST /v1/sessions
Authorization: Bearer demo
X-Tenant-Id: ten_demo
Idempotency-Key: <unique>
Content-Type: application/json

{ "workflow_id": "onboarding_standard" }
```

Then mint a capture token and hand it to the applicant app. Full flow: [Creating a session (API)](api.md) · [Walkthrough](walkthrough.md).

## Matching note

Face 1:1 uses the **Face SDK matcher**. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "components.md",
        "Map of components",
        "Index of every major IDV folder and where it is documented.",
        f"""
## Top-level layout (`IDV/`)

| Path | Role | Docs |
| --- | --- | --- |
| `platform/server/` | Platform API + workers (`:14187`) | [Platform server](platform-server.md) |
| `platform/console/` | Identity Console (`:14188` / `/admin`) | [Identity Console](platform-console.md) |
| `company/backend/` | Sample **company server** (`:14195`) | [Company backend](company-backend.md) |
| `company/admin/` | Company operator UI (`:14189`) | [Company Admin](company-admin.md) |
| `license/admin/` | Hybrid issuer + brand (`:14190`) | [License Admin](license-admin.md) |
| `app/` | Applicant SDKs + demos | [Applicant clients](components-clients.md) |
| `packages/` | Shared UI / decision / licence libs | [Shared packages](shared-packages.md) |
| `license/license_v2/` | Shared Hybrid protocol | [Hybrid protocol](license-protocol.md) |
| `docs/` | Offline handbook + API notes | [Reference](reference.md) |

## Brand

One pack only: `IDV/license/admin/brand/` → `/brand/*` and docs `.gitbook/assets/`.

Org: [`identixia-IDV`]({GH}).
""".strip()
        + "\n",
    )


def write_static_pages() -> None:
    write_page(
        OUT / "request-a-license-and-support.md",
        "Request a License & Support",
        "How to request an Identixia license for Face SDK, ID Document SDK, and IDV.",
        """
## Mobile SDK (Face / Document)

1. Build with **your** applicationId or bundle id (not the demo id).
2. Contact us with that id and the product (Face recognition, Face liveness, Document recognition, or Document authenticity).
3. Activate and initialize as shown on the platform page.

Demo keys work only for demo application ids.

## Server SDK (Windows / Linux / Docker)

1. Start the API once.
2. Call `GET /api/machinecode` and copy `data.machinecode`.
3. Send that code to Identixia. Docker and bare-metal machine codes differ — license the environment you ship.
4. Call `POST /api/activate`, or place `license.txt` and restart.
5. Confirm with `GET /api/licenseStatus`.

## IDV

IDV uses Hybrid licensing via `license/admin` and `license/license_v2`. The issuer UI listens on `:14190` (localhost). Company systems use `company/backend` (sample `:14195`) to hold the service token and start sessions — see [Company integration](idv/company.md).

## Support

{% include "./.gitbook/includes/contact.md" %}
""".strip()
        + "\n",
    )
    write_page(
        OUT / "contact-us.md",
        "Contact",
        "Contact Identixia for licenses and technical support.",
        """
## Support channels

We are available 24/7 for license requests and technical support.

{% include "./.gitbook/includes/contact.md" %}
""".strip()
        + "\n",
    )
    (OUT / ".gitbook" / "includes").mkdir(parents=True, exist_ok=True)
    (OUT / ".gitbook" / "includes" / "contact.md").write_text(
        """
<div align="center">

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>

</div>
""".lstrip(),
        encoding="utf-8",
        newline="\n",
    )


def write_welcome() -> None:
    body = """
<p align="center"><img src=".gitbook/assets/brand-logo.png" alt="Identixia" width="280"></p>

## Introduction

Identixia documentation covers **three products**. All biometric processing runs on **your** device or server.

| Product | Source in monorepo | What you get |
| --- | --- | --- |
| [**Face SDK**](face-sdk/) | `repositories/Face*` | Face recognition and passive face liveness |
| [**ID Document SDK**](id-document-sdk/) | `repositories/ID-Document*` | Document OCR/MRZ and document authenticity |
| [**IDV**](idv/) | `IDV/` | Verification platform that orchestrates the two SDKs |

## How to use these docs

The sidebar is multi-level: product → function → product line → channel → platform.

1. Open the **product** (Face SDK, ID Document SDK, or IDV).
2. Open **Recognition** or **Liveness** (for IDV: Getting started, Engines, or Components).
3. Choose **full product**, **recognition-only**, or **liveness-only**, then **Mobile** or **Server**.
4. Open your **platform** page → Quick start → Ready → API reference.
5. For IDV, start the Document and Face engines, then the IDV server and a client demo.

{% hint style="info" %}
Native engine binaries ship on GitHub Releases (`/releases/latest/download/…`). They are not committed to git. Demo UIs are optional — call the SDK or HTTP API directly in production.
{% endhint %}

## Products

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>Face SDK</strong></td><td>Detect, templates, 1:1 / 1:N, and passive liveness when licensed. Mobile and server repositories under <code>repositories/</code>.</td><td><a href=".gitbook/assets/face-android-home.png">face-android-home.png</a></td><td></td><td><a href="face-sdk/">face-sdk</a></td></tr>
<tr><td><strong>ID Document SDK</strong></td><td>Passport and ID OCR, MRZ, barcode, and document authenticity when licensed.</td><td><a href=".gitbook/assets/document-desktop-status.png">document-desktop-status.png</a></td><td></td><td><a href="id-document-sdk/">id-document-sdk</a></td></tr>
<tr><td><strong>IDV platform</strong></td><td>Sessions, capture clients, Identity Console, company sample, and Hybrid licensing — uses Face and Document engines over HTTP.</td><td><a href=".gitbook/assets/brand-mark.png">brand-mark.png</a></td><td></td><td><a href="idv/">idv</a></td></tr>
</tbody></table>

## Shared conventions

| Topic | Summary |
| --- | --- |
| Control vs process (HTTP) | `/api/health`, `/api/machinecode`, `/api/activate`, `/api/licenseStatus` return `{success,code,message,request_id,data}`. Process routes return engine JSON. |
| Threading (mobile) | Activate, init, detect, and recognize on a **background** thread. |
| License flags | Face: `recognition` / `liveness`. Document: `recognition` / `authenticity`. A missing flag means the feature is not evaluated. |
| Brand | Logo and favicons live in docs `.gitbook/assets/`; IDV consoles use `IDV/license/admin/brand/`. |

## Links

* [Request a license & support](request-a-license-and-support.md)
* [Contact](contact-us.md)
* [identixia.com](https://identixia.com)
* GitHub: [identixia-IDV](https://github.com/identixia-IDV)
""".strip()
    write_page(
        OUT / "README.md",
        "Welcome to Identixia",
        "Identixia documentation for Face SDK, ID Document SDK, and the IDV platform.",
        body + "\n",
    )


def write_nav_hubs() -> None:
    """Intermediate sidebar pages (levels 3–4). Leaf platform URLs stay catalog-stable."""

    def hub(rel: str, title: str, desc: str, body: str) -> None:
        write_page(OUT / rel, title, desc, body.strip() + "\n")

    # —— Face SDK ——
    hub(
        "face-sdk/full-product.md",
        "Full product (recognition + liveness)",
        "Face SDK repositories that ship recognition and passive liveness together.",
        """
## When to use this line

Choose **full product** when one application or one HTTP API must provide both:

* Face recognition (detect, template, 1:1, 1:N)
* Passive face liveness (when the license includes `liveness`)

## Channels

| Channel | Page |
| --- | --- |
| Phones and cross-platform | [Mobile](full-mobile.md) |
| Windows and Docker | [Server](full-server.md) |

Function guides: [Recognition](recognition.md) · [Liveness](liveness.md)

Return to the [Face SDK](README.md) hub for product-line selection.
""",
    )
    hub(
        "face-sdk/full-mobile.md",
        "Mobile & cross-platform",
        "Full Face SDK samples for Android, iOS, Flutter, React Native, and Ionic.",
        f"""
## Platforms

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`FaceRecognition-LivenessDetection-Android`]({GH}/FaceRecognition-LivenessDetection-Android) |
| iOS | [iOS](ios.md) | [`FaceRecognition-LivenessDetection-iOS`]({GH}/FaceRecognition-LivenessDetection-iOS) |
| Flutter | [Flutter](flutter.md) | [`FaceRecognition-LivenessDetection-Flutter`]({GH}/FaceRecognition-LivenessDetection-Flutter) |
| React Native | [React Native](react-native.md) | [`FaceRecognition-LivenessDetection-React-Native`]({GH}/FaceRecognition-LivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`]({GH}/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`FaceRecognition-LivenessDetection-Ionic-Cordova`]({GH}/FaceRecognition-LivenessDetection-Ionic-Cordova) |

## Integration path

1. Open the platform page for your stack.
2. Complete **Quick start** until the sample shows **Ready**.
3. Activate with a license issued for **your** application id.
4. Call SDK APIs on a **background** thread; keep the camera preview on the UI thread.

Parent: [Full product](full-product.md).
""",
    )
    hub(
        "face-sdk/full-server.md",
        "Server (Windows & Docker)",
        "Full Face SDK HTTP APIs for Windows and Linux/Docker.",
        f"""
## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](windows.md) | [`FaceRecognition-LivenessDetection-Windows`]({GH}/FaceRecognition-LivenessDetection-Windows) | 14103 |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`FaceRecognition-LivenessDetection-Docker`]({GH}/FaceRecognition-LivenessDetection-Docker) | 14103 |

## HTTP contract

| Route type | Shape |
| --- | --- |
| Control (`/api/health`, `/api/machinecode`, `/api/activate`, `/api/licenseStatus`) | `{{success, code, message, request_id, data}}` |
| Process (`/api/face/*`) | Engine JSON (scores, templates, boxes) |

Confirm the bind address and port in the product README before production.

Parent: [Full product](full-product.md).
""",
    )
    hub(
        "face-sdk/recognition-only.md",
        "Recognition-only products",
        "Face recognition without liveness packs — Windows and Linux/Docker.",
        f"""
## When to use

Use these repositories when your license is **recognition only** (no `liveness` entitlement).

| Platform | Docs | Repository |
| --- | --- | --- |
| Windows | [Windows (recognition only)](recognition-windows.md) | [`FaceRecognition-Windows`]({GH}/FaceRecognition-Windows) |
| Linux / Docker | [Linux / Docker (recognition only)](recognition-linux-docker.md) | [`FaceRecognition-Docker`]({GH}/FaceRecognition-Docker) |

For recognition **with** liveness in one build, use the [full product](full-product.md) instead.

Concept guide: [Face recognition](recognition.md).
""",
    )
    hub(
        "face-sdk/liveness-only.md",
        "Liveness-only products",
        "Standalone face liveness SDKs without the full recognition gallery stack.",
        """
## When to use

Score a face for presentation-attack detection without shipping the full enroll / 1:N stack.

| Channel | Page |
| --- | --- |
| Mobile | [Liveness-only — mobile](liveness-only-mobile.md) |
| Server | [Liveness-only — server](liveness-only-server.md) |

Concept guide: [Face liveness](liveness.md). For recognition plus liveness together, use the [full product](full-product.md).
""",
    )
    hub(
        "face-sdk/liveness-only-mobile.md",
        "Liveness-only — mobile",
        "Android and iOS standalone face liveness samples.",
        f"""
## Platforms

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](liveness-android.md) | [`FaceLivenessDetection-Android`]({GH}/FaceLivenessDetection-Android) |
| iOS | [iOS](liveness-ios.md) | [`FaceLivenessDetection-iOS`]({GH}/FaceLivenessDetection-iOS) |

## Integration path

1. Clone the sample and place the liveness runtime from GitHub Releases.
2. Run until status shows **Ready**, then open the camera flow.
3. Activate with a license that includes `liveness`.
4. Treat a missing score as “not evaluated”, not as pass.

Parent: [Liveness-only products](liveness-only.md).
""",
    )
    hub(
        "face-sdk/liveness-only-server.md",
        "Liveness-only — server",
        "Windows and Linux/Docker standalone face liveness APIs.",
        f"""
## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](liveness-windows.md) | [`FaceLivenessDetection-Windows`]({GH}/FaceLivenessDetection-Windows) | 14103 |
| Linux / Docker | [Linux / Docker](liveness-linux-docker.md) | [`FaceLivenessDetection-Docker`]({GH}/FaceLivenessDetection-Docker) | 14103 |

Process path is typically `POST /api/liveness` (confirm in the product README). Control routes use the standard `{{success, code, message, request_id, data}}` envelope.

Parent: [Liveness-only products](liveness-only.md).
""",
    )

    # —— ID Document SDK ——
    hub(
        "id-document-sdk/full-product.md",
        "Full product (recognition + liveness)",
        "Document repositories that ship OCR/MRZ and authenticity together.",
        """
## When to use

Choose **full product** when one sample or API must provide document **recognition** and document **authenticity** (when licensed).

| Channel | Page |
| --- | --- |
| Phones and cross-platform | [Mobile](full-mobile.md) |
| Windows and Docker | [Server](full-server.md) |

Guides: [Recognition](recognition.md) · [Liveness](liveness.md) · [Result JSON](result-json.md)

Return to the [ID Document SDK](README.md) hub for product-line selection.
""",
    )
    hub(
        "id-document-sdk/full-mobile.md",
        "Mobile & cross-platform",
        "Full Document SDK samples for Android, iOS, Flutter, React Native, and Ionic.",
        f"""
## Platforms

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`ID-Document-Recognition-Liveness-Detection-Android`]({GH}/ID-Document-Recognition-Liveness-Detection-Android) |
| iOS | [iOS](ios.md) | [`ID-Document-Recognition-Liveness-Detection-iOS`]({GH}/ID-Document-Recognition-Liveness-Detection-iOS) |
| Flutter | [Flutter](flutter.md) | [`ID-Document-Recognition-Liveness-Detection-Flutter`]({GH}/ID-Document-Recognition-Liveness-Detection-Flutter) |
| React Native | [React Native](react-native.md) | [`ID-Document-Recognition-Liveness-Detection-React-Native`]({GH}/ID-Document-Recognition-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |

## Integration path

1. Open the platform page for your stack.
2. Complete **Quick start** until the sample shows **Ready**.
3. Activate with a license issued for **your** application id.
4. Capture front (and back when required); parse [Result JSON](result-json.md) in your app.

Parent: [Full product](full-product.md).
""",
    )
    hub(
        "id-document-sdk/full-server.md",
        "Server (Windows & Docker)",
        "Full Document SDK HTTP APIs for Windows and Linux/Docker.",
        f"""
## Platforms

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Windows | [Windows](windows.md) | [`ID-Document-Recognition-Liveness-Detection-Windows`]({GH}/ID-Document-Recognition-Liveness-Detection-Windows) | 14102 |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`ID-Document-Recognition-Liveness-Detection-Docker`]({GH}/ID-Document-Recognition-Liveness-Detection-Docker) | 14102 |

## Routes

| Route | Role |
| --- | --- |
| `POST /api/documentProcess` | Full process (recognition + authenticity when licensed) |
| `POST /api/documentRecognition` | OCR / MRZ / barcode only |
| `POST /api/documentLiveness` | Authenticity only |

Control routes use `{{success, code, message, request_id, data}}`. Response shape: [Result JSON](result-json.md).

Parent: [Full product](full-product.md).
""",
    )
    hub(
        "id-document-sdk/liveness-only.md",
        "Liveness-only products",
        "Document authenticity API without the full OCR product surface.",
        f"""
## When to use

You need document anti-spoofing (authenticity) without shipping a full OCR UI.

| Platform | Docs | Repository | Default port |
| --- | --- | --- | ---: |
| Linux / Docker | [Document liveness Docker](liveness-linux-docker.md) | [`ID-Document-Liveness-Detection-Docker`]({GH}/ID-Document-Liveness-Detection-Docker) | 14106 |

Concept guide: [Document liveness](liveness.md). For OCR plus authenticity together, use the [full product](full-product.md).
""",
    )
    hub(
        "id-document-sdk/reference.md",
        "Reference",
        "Shared Document SDK result shapes and security fields.",
        """
## Topics

| Topic | Page |
| --- | --- |
| Process / recognize JSON | [Result JSON](result-json.md) |
| Authenticity fields | [Security check fields](security-fields.md) |

Parse JSON in your application. Do not scrape the demo Result screen.

Return to the [ID Document SDK](README.md) hub for platform samples.
""",
    )

    # —— IDV ——
    hub(
        "idv/getting-started.md",
        "Getting started",
        "IDKIT-style setup path: structure, engines, env, first admin, sessions, API, webhooks.",
        """
## Setup guide (follow in order)

1. [Project structure](project-structure.md) — Admin / Company / Applicant / Engines
2. [Prerequisites: engines](engines.md) — Document `:14102` + Face `:14103`
3. [Project setup](environment.md) — `.env`, tokens, storage
4. [Initial setup process](initial-setup.md) — consoles, settings, webhook secret
5. [Quick start](quick-start.md) · helper `python IDV/scripts/start_local.py`
6. [End-to-end walkthrough](walkthrough.md)
7. [Session states](session-states.md)
8. [Creating a session (API)](api.md)
9. [Webhook integration](company-webhooks.md)
10. [Applicant clients](components-clients.md)
11. [Production](production.md) before go-live

Architecture deep-dive: [Architecture](architecture.md). Offline handbook: `IDV/docs/` (not duplicated here).
""",
    )
    hub(
        "idv/project-structure.md",
        "Project structure",
        "IDV folders mapped to Admin, Company, Applicant, and Engines roles.",
        """
## Components

IDV is a self-host KYC platform that uses Identixia **SDK-integrated HTTP engines** as the biometric backend.

| Role | What it is | Folder | Typical port |
| --- | --- | --- | ---: |
| **Admin (platform)** | Tenant API, workers, Identity Console | `platform/server/`, `platform/console/` | 14187 · 14188 |
| **Company (merchant)** | Your backend sample + operator UI | `company/backend/`, `company/admin/` | 14195 · 14189 |
| **Applicant (user)** | Capture SDKs and demo apps | `app/` | e.g. 5175 |
| **Engines** | Document + Face recognition / liveness | Face / Document SDK repos | 14102 · 14103 |

## Supporting folders

| Path | Role |
| --- | --- |
| `license/admin/` | Hybrid licence **issuer** (Identixia ops) — `:14190`, private only |
| `license/license_v2/` | Shared Hybrid protocol sources |
| `packages/` | Shared admin UI / decision / licence helpers |
| `docs/` | Offline handbook + API notes |

## Data flow

```text
Applicant (client) → Company backend (:14195) → IDV server (:14187) → Engines (:14102 / :14103)
                         ↑                              ↓
                  Company Admin                  Identity Console
```

Next: [Prerequisites: engines](engines.md).
""",
    )
    hub(
        "idv/walkthrough.md",
        "End-to-end walkthrough",
        "Run one verification: engines, IDV server, company backend, capture, webhook, review.",
        """
## Goal

Complete one `onboarding_standard` verification locally and see a `session.completed` webhook plus an identity in Identity Console.

## 1. Start engines

| Service | URL |
| --- | --- |
| Document | `http://127.0.0.1:14102` — activate, then `GET /api/health` |
| Face | `http://127.0.0.1:14103` — activate, then `GET /api/health` |

## 2. Start platform + company

```bash
# IDV server
cd IDV/platform/server && set IDV_OPEN_API=1 && python app.py
# → http://127.0.0.1:14187/v1  and  /admin/

# Company backend
cd IDV/company/backend
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
# → http://127.0.0.1:14195/
```

Optional UIs: Identity Console `:14188` (or `/admin` on the server), Company Admin `:14189`.

## 3. Register a webhook

1. Company Admin → Settings → webhook URL  
   `http://127.0.0.1:14195/demo/webhooks/idv`
2. Identity Console → Webhooks → add that URL for `session.created` and `session.completed`
3. Copy the one-time `whsec_…` into Company Admin Settings

Details: [Company webhooks](company-webhooks.md).

## 4. Start verification (company API)

```bash
curl -s -X POST http://127.0.0.1:14195/demo/start-verification \\
  -H "Content-Type: application/json" \\
  -d '{"workflow_id":"onboarding_standard"}'
```

Response includes `sessionId`, `captureToken`, `launchUrl`, and `next_step`. Hand the **capture token** (or launch URL) to the applicant app — never the service bearer.

## 5. Capture steps

1. `GET /v1/sessions/{id}` with `Authorization: Bearer <captureToken>` → read `next_step.id`
2. `POST /v1/sessions/{id}/submissions` with headers:
   * `Authorization: Bearer <captureToken>`
   * `Idempotency-Key: <unique>`
   * `X-IDV-Step-ID: <next_step.id>`
   * `X-IDV-Attempt: 1`
   * Body: `{ "images": ["<base64>"] }` (or the shape the step expects)
3. Repeat until the session completes (typical: document then face)

Use a [client demo](components-clients.md) or Postman (`IDV/platform/server/postman/IDV-Public.postman_collection.json`).

## 6. Confirm outcome

| Check | Where |
| --- | --- |
| Webhook delivery | Company Admin → Webhooks · or `GET /demo/webhooks/events` |
| Session + identity | Identity Console · or `GET /v1/sessions/{id}` / `GET /v1/identities/{id}` |
| Trust decision | Identity `trust_state` / `trust_factors` · webhook `payload.decision` |

Decision aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing engine signals never auto-accept.

## 7. Optional review

If trust is `review`, claim the case in Identity Console (or `POST /v1/review-cases/{identity_id}/claim`) and transition with `accept` / `reject`.

API details: [Creating a session (API)](api.md). Production hardening: [Production](production.md).
""",
    )
    hub(
        "idv/api.md",
        "Creating a session (API)",
        "Create a verification session, mint a capture token, and hand launchUrl to the applicant.",
        """
## Step 1 — Get a service credential

| Environment | Credential |
| --- | --- |
| Local demo (`IDV_OPEN_API=1`) | Bearer `demo`, tenant `ten_demo` |
| Production | Real service token issued for your tenant — stored **only** on the company backend |

Never put the service bearer in a mobile/web applicant app.

## Step 2 — Recommended: company shortcut

Your merchant backend (sample `:14195`) creates the session and mint token together:

```bash
curl -s -X POST http://127.0.0.1:14195/demo/start-verification \\
  -H "Content-Type: application/json" \\
  -d '{"workflow_id":"onboarding_standard"}'
```

Response includes `sessionId`, `captureToken`, `launchUrl`, and `next_step`. Give **`launchUrl` / `captureToken`** to the applicant.

| Method | Path | Role |
| --- | --- | --- |
| `POST` | `/demo/start-verification` | Session + capture token |
| `GET` | `/demo/sessions/{id}` | Status refresh |
| `POST` | `/demo/sessions/{id}/cancel` | Cancel (service side) |
| `GET` | `/demo/workflows` | List workflows |

## Step 3 — Platform API (same result, two calls)

Use these from the **company backend** only:

```http
POST /v1/sessions
Authorization: Bearer <service>
X-Tenant-Id: <tenant>
Idempotency-Key: <unique>
Content-Type: application/json

{ "workflow_id": "onboarding_standard" }
```

```http
POST /v1/sessions/{session_id}/capture-token
Authorization: Bearer <service>
X-Tenant-Id: <tenant>
```

### Submit a capture step (applicant)

```http
POST /v1/sessions/{session_id}/submissions
Authorization: Bearer <captureToken>
Idempotency-Key: <unique>
X-IDV-Step-ID: <next_step.id>
X-IDV-Attempt: 1
Content-Type: application/json

{ "images": ["BASE64_JPEG"] }
```

Use the exact `next_step.id` from the session (e.g. `step_document_capture`, `step_face_capture`).

## Auth summary

| Caller | Credential |
| --- | --- |
| Company backend | Service bearer · `X-Tenant-Id` |
| Capture app | Capture token as Bearer |

Mutating calls often require `Idempotency-Key`.

## Other useful routes

| Method | Path | Role |
| --- | --- | --- |
| `GET` | `/v1/sessions` · `/v1/sessions/{id}` | List / poll session |
| `POST` | `/v1/sessions/{id}/cancel` | Cancel (service only) |
| `GET` | `/v1/identities` · `/v1/identities/{id}` | Finished record + `trust_state` |
| `POST` | `/v1/identities/{id}/transitions` | `accept` / `reject` / `reset_to_review` |
| `GET` | `/v1/workflows` | Includes `onboarding_standard` |

## Webhooks

Register in Identity Console. Events today: `session.created`, `session.completed`. See [Webhook integration](company-webhooks.md).

## Postman

| Collection | Path |
| --- | --- |
| Public | `IDV/platform/server/postman/IDV-Public.postman_collection.json` |
| Company sample | `IDV/platform/server/postman/Company-Backend-Sample.postman_collection.json` |
| Local env | `IDV/platform/server/postman/IDV-Local.postman_environment.json` |

Full persistence notes: `IDV/docs/API.md` in source. Session meanings: [Session states](session-states.md).
""",
    )
    hub(
        "idv/production.md",
        "Production",
        "Hardening checklist: auth, TLS, databases, engines, and what not to expose.",
        """
## Checklist

| Area | Guidance |
| --- | --- |
| Demo auth | Set `IDV_OPEN_API=0` (or unset). Issue real service tokens per tenant. |
| Capture secrets | Keep `IDV_SERVICE_TOKEN` on the **company backend** only. Apps use capture tokens. |
| TLS | Terminate HTTPS on a reverse proxy in front of `:14187` (and company `:14195` if public). |
| License Admin | Keep `:14190` on **localhost** / private network. Do not publish the issuer UI. |
| Engines | Point IDV at internal Document `:14102` and Face `:14103` URLs; activate each host/container with its own machine code. |
| Database | Prefer PostgreSQL via `python IDV/setup_database.py` (or `--yes` for a guided default). SQLite is fine for local demos only. |
| Memory store | `IDV_FORCE_MEMORY` / `COMPANY_FORCE_MEMORY` are for tests — not production. |
| Webhooks | Require `whsec_…` HMAC verification; idempotent handlers; poll session API if a delivery is missed. |
| Brand | Serve `/brand/*` from `license/admin/brand/` (or the configured `IDV_BRAND_DIR`). |

## Reverse proxy (sketch)

```text
Internet clients
      │
      ▼
 HTTPS terminator  ──►  platform/server :14187  (/v1, /admin)
      │
      └──►  company/backend :14195  (merchant APIs + /admin)
                 │
                 ├──► platform/server (service bearer)
                 └──► (optional) capture CDN / static hosting

Internal only:
  document-engine :14102
  face-engine     :14103
  license/admin   :14190   ← Identixia / ops, not public
```

## Database

```bash
cd IDV
python setup_database.py --check   # inspect current config
python setup_database.py --yes     # non-interactive recommended local/prod bootstrap
```

Writes `IDV/.env` and creates schema. Production authority is **PostgreSQL**; media / Valkey / RabbitMQ options appear in the same wizard when you need them.

## Engine URLs

Configure IDV to reach engines on your private network (not `127.0.0.1` from another host). Confirm:

```bash
curl -s https://doc-engine.internal/api/health
curl -s https://face-engine.internal/api/health
```

Machine codes differ for bare metal vs Docker — license the environment you ship.

## Go-live smoke test

1. Health on IDV, company backend, both engines
2. Start verification → capture document + face → `session.completed` webhook
3. Inspect identity `trust_state` in Identity Console
4. Confirm License Admin and issuer ports are not internet-facing

Related: [Project setup](environment.md) · [Walkthrough](walkthrough.md) · [Creating a session (API)](api.md).
""",
    )
    hub(
        "idv/environment.md",
        "Project setup",
        "Configure IDV .env, engine URLs, tokens, and storage — keep secrets out of apps and git.",
        """
## 1. Copy environment file

```bash
cd IDV
copy .env.example .env
# or: cp .env.example .env
```

Edit `IDV/.env`. Restart servers after changes.

## 2. Required keys for a real engine demo

| Key | Local demo value | Notes |
| --- | --- | --- |
| `IDV_ENGINES` | `http` | Use `fake` only for UI smoke tests without engines |
| `DOCUMENT_API_URL` | `http://127.0.0.1:14102` | Internal Document engine |
| `FACE_API_URL` | `http://127.0.0.1:14103` | Internal Face engine |
| `IDV_PORT` / `IDV_BASE_URL` | `14187` / `http://127.0.0.1:14187` | Platform listen URL |
| `IDV_OPEN_API` | `1` locally only | Demo bearer `demo` — **off in production** |

Company backend (process env or its own config):

| Key | Local demo | Notes |
| --- | --- | --- |
| `IDV_BASE_URL` | `http://127.0.0.1:14187` | Platform URL |
| `IDV_SERVICE_TOKEN` | `demo` with open API | Real token in production — **never in client apps** |
| `IDV_TENANT_ID` | `ten_demo` | Tenant scope |

## 3. Folder overrides

| Env key | Default |
| --- | --- |
| `IDV_SERVER_DIR` | `platform/server` |
| `IDV_SERVER_UI_DIST` | `platform/console/dist` |
| `IDV_BRAND_DIR` | `license/admin/brand` |
| `COMPANY_ADMIN_DIST` | `company/admin/dist` |
| `COMPANY_ADMIN_DIR` | `company/admin` |
| `LICENSE_ADMIN_DIR` | `license/admin` |

## 4. Storage

| Project | Default |
| --- | --- |
| `platform/server` | SQLite under `database/` (tenant-separated rows) |
| `company/backend` | `company/backend/database/company.sqlite` |
| `license/admin` | `license/admin/database/` (issuer ledger) |

Production: `python IDV/setup_database.py` (or `--yes`) for PostgreSQL / media / Valkey / RabbitMQ. Memory stores are for tests only (`IDV_FORCE_MEMORY` / `COMPANY_FORCE_MEMORY`).

## 5. Security rules (non-negotiable)

| Rule | Why |
| --- | --- |
| Do not commit `.env` or licence files | Secrets and machine-bound keys |
| Service bearer stays on company backend | Capture apps use capture tokens only |
| No open “allow all” auth | Unlike public test-mode cloud rules — deny by default |
| License Admin on localhost / private net | Issuer must not be internet-facing |

Next: [Initial setup process](initial-setup.md).
""",
    )
    hub(
        "idv/initial-setup.md",
        "Initial setup process",
        "First Identity Console access, company settings, and webhook secret — after engines and .env.",
        """
## Before you start

1. Engines healthy — [Prerequisites: engines](engines.md)
2. `.env` configured — [Project setup](environment.md)
3. Platform + company running — `python IDV/scripts/start_local.py` or [Quick start](quick-start.md)

## 1. Open Identity Console

| Mode | URL |
| --- | --- |
| Production build (served by server) | http://127.0.0.1:14187/admin/ |
| Develop UI | http://127.0.0.1:14188/ |

Confirm the console can reach the API (meta / sessions list loads). With `IDV_OPEN_API=1`, local demo auth uses bearer `demo` and tenant `ten_demo`.

## 2. Company Admin settings

1. Open Company Admin: http://127.0.0.1:14189/ (or `:14195/admin/` when built-in).
2. Confirm **Overview** shows IDV reachable.
3. Note the webhook receiver URL:  
   `http://127.0.0.1:14195/demo/webhooks/idv`

## 3. Register webhook + store secret

1. Identity Console → **Webhooks** → add the company URL.
2. Select `session.created` and `session.completed`.
3. Copy the one-time `whsec_…` secret.
4. Paste it into Company Admin → **Settings** and save.

Details: [Webhook integration](company-webhooks.md).

{{% hint style="danger" %}}
Treat `whsec_…` like a password. Do not put it in applicant apps or public repos.
{{% endhint %}}

## 4. Service credential reminder

| Credential | Where it lives |
| --- | --- |
| `IDV_SERVICE_TOKEN` | Company backend only |
| Capture token / `launchUrl` | Returned to the applicant app for one session |

## 5. First verification

Use Company Admin → **Start verification** (workflow `onboarding_standard`) or:

```bash
curl -s -X POST http://127.0.0.1:14195/demo/start-verification \\
  -H "Content-Type: application/json" \\
  -d '{"workflow_id":"onboarding_standard"}'
```

Share `launchUrl` or `captureToken` with the applicant — not the service bearer.

Next: [Session states](session-states.md) · [Creating a session (API)](api.md) · [Walkthrough](walkthrough.md).
""",
    )
    hub(
        "idv/session-states.md",
        "Session states",
        "Session status and identity trust_state through an Identixia IDV verification.",
        """
## Session status

Each verification **session** moves through:

| Status | Meaning |
| --- | --- |
| `created` | Session row exists; capture may not have started |
| `capturing` | Waiting for / receiving applicant step submissions |
| `processing` | Engines / pipeline evaluating the latest submission |
| `completed` | Finalized — identity created or linked; see trust state |
| `cancelled` | Stopped by the company (service bearer) |
| `expired` | Timed out before completion |
| `technical_error` | Unrecoverable platform / pipeline error |

## Identity trust state

When a session completes, the **identity** carries the decision:

| `trust_state` | Meaning |
| --- | --- |
| `incomplete` | Not finished evaluating |
| `review` | Needs human review in Identity Console |
| `accepted` | Auto-accepted or accepted after review |
| `rejected` | Auto-rejected or rejected after review |
| `anonymized` | Personal data erased |

Aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing engine signals never auto-accept.

## Starting a verification (operator)

Like a “create session + share link” flow:

1. Company Admin → **Start verification** (or `POST /demo/start-verification`).
2. Copy **`launchUrl`** (or show a QR of that URL in your own UI) and/or **`captureToken`**.
3. Applicant opens the link / app; session stays `capturing` until steps finish.
4. On completion, webhook `session.completed` fires; Identity Console shows the identity.

Each capture token / launch URL is session-scoped. Start a **new** verification for each applicant attempt.

## Reviewer path

If `trust_state` is `review`:

1. Open Identity Console → review cases / identity detail.
2. Claim the case if required.
3. Transition with `accept` or `reject` ([Creating a session (API)](api.md) · identities section).

Next: [Creating a session (API)](api.md) · [Webhook integration](company-webhooks.md).
""",
    )
    hub(
        "idv/platform.md",
        "Platform",
        "Identixia IDV platform server and Identity Console.",
        """
The **platform** is what tenants call for sessions, submissions, reviews, and workflows.

| Piece | Docs |
| --- | --- |
| API + workers | [IDV server](platform-server.md) |
| Operator console | [Identity Console](platform-console.md) |
| Customer routes | [Creating a session (API)](api.md) |
| Hardening | [Production](production.md) |

<figure><img src="../.gitbook/assets/idv-audit-console.png" alt="Identity Console" width="480"><figcaption>Identity Console</figcaption></figure>

Company systems integrate **through** this platform — see [Company integration](company.md).
""",
    )
    hub(
        "idv/platform-server.md",
        "IDV server",
        "platform/server: platform API, workers, storage, and /admin mount.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/platform/server/` |
| API | `http://127.0.0.1:14187/v1` |
| Admin (production build) | `http://127.0.0.1:14187/admin/` |
| Postman | `IDV/platform/server/postman/` |
| OpenAPI notes | `IDV/docs/API.md` |

```bash
cd IDV/platform/server
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
```

`IDV_OPEN_API=1` enables the local demo bearer (`demo` / `ten_demo`). Disable it outside local demos — see [Production](production.md).

Integrator routes: [Creating a session (API)](api.md). Decision code: `platform/server/idv/decision/`.
""",
    )
    hub(
        "idv/platform-console.md",
        "Identity Console",
        "platform/console — tenant operators: sessions, reviews, webhooks, workflows.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/platform/console/` |
| Develop | `http://127.0.0.1:14188/` (proxies API to `:14187`) |
| Production | `npm run build` → served from `platform/server` at `/admin/` |

```bash
cd IDV/platform/console
npm install && npm run dev
```

Use this console to register company webhook URLs, inspect identities/sessions, and run manual review.
""",
    )
    hub(
        "idv/company.md",
        "Company integration",
        "Sample merchant company server and admin UI that talk to IDV.",
        """
Your **company** (bank, fintech, marketplace) owns applicant UX launch and service credentials.

The sample in this repo:

| Piece | Folder | Port |
| --- | --- | --- |
| Company server | `company/backend/` | 14195 |
| Company Admin UI | `company/admin/` | 14189 (dev) · built into `:14195/admin` |

| Page | Topic |
| --- | --- |
| [Company backend](company-backend.md) | Start sessions, health, webhook ingest |
| [Company Admin](company-admin.md) | Operator UI |
| [Webhooks](company-webhooks.md) | Wire Identity Console → company receiver |

{{% hint style="info" %}}
Keep `IDV_SERVICE_TOKEN` on the company server only. Capture apps must not embed it.
{{% endhint %}}
""",
    )
    hub(
        "idv/company-backend.md",
        "Company backend (server)",
        "Sample company/backend: holds the service bearer and starts IDV sessions.",
        """
## Role

`IDV/company/backend/` is the **sample company server**. It:

* Holds `IDV_SERVICE_TOKEN` / tenant id
* Starts verifications against IDV (`POST` session flows)
* Exposes demo APIs for capture apps (`POST /demo/start-verification`)
* Receives IDV webhooks (`POST /demo/webhooks/idv`)
* Serves the built Company Admin at `/admin/`

| Surface | URL |
| --- | --- |
| Health | `http://127.0.0.1:14195/health` |
| Start verification | `POST /demo/start-verification` |
| Webhook ingest | `POST /demo/webhooks/idv` |
| Admin UI (built) | `http://127.0.0.1:14195/admin/` |

## Run

```bash
cd IDV/company/backend
pip install -r requirements.txt
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
```

Storage: `company/backend/database/company.sqlite` by default.

### Example — start via company backend (JS sketch)

```js
const start = await IdvApi.startViaCompanyBackend({
  companyBackendUrl: "http://127.0.0.1:14195",
});
// use start.captureToken / launch URL in the applicant app
```
""",
    )
    hub(
        "idv/company-admin.md",
        "Company Admin UI",
        "company/admin React UI for operators on the sample company backend.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/company/admin/` |
| Develop | `http://127.0.0.1:14189/` |
| Production | `npm run build` → `company/backend` serves `/admin/` |

```bash
cd IDV/company/admin
npm install && npm run dev
```

## Operator areas (sample)

| Area | What it does |
| --- | --- |
| Overview | IDV reachability, session/webhook counts |
| Start verification | Pick workflow, external ref, customer; copy capture token / URL |
| Sessions | Refresh status from IDV, cancel, inspect payload |
| Workflows | List published workflows from `/v1/workflows` |
| Webhooks | Recent deliveries + settings for webhook URL/secret |

Shared React helpers: `IDV/packages/admin-ui`.
""",
    )
    hub(
        "idv/company-webhooks.md",
        "Webhook integration",
        "Subscribe to session events, verify HMAC signatures, and handle deliveries safely.",
        """
## Subscribe to events

1. Expose an HTTPS endpoint on **your** company server (sample: `POST /demo/webhooks/idv` on `:14195`).
2. In **Identity Console → Webhooks**, register that URL.
3. Select events: `session.created`, `session.completed` (only these are emitted today).
4. Store the one-time `whsec_…` secret in Company Admin **Settings** (or your secret manager).

Local sample URL: `http://127.0.0.1:14195/demo/webhooks/idv`.

## Handle webhooks

Your endpoint receives `POST` JSON:

```json
{
  "eventId": "evt_...",
  "eventType": "session.completed",
  "occurredAt": "2026-09-24T12:00:00+00:00",
  "payload": {
    "sessionId": "ses_...",
    "decision": "review"
  }
}
```

Headers include `X-IDV-Event` and `X-IDV-Signature`.

## Security verification

```text
X-IDV-Signature: sha256=<HMAC-SHA256 of the raw body>
```

Compute HMAC-SHA256 over the **raw** request body with `whsec_…` and compare in constant time. Leave the secret blank only for an unsigned **local** trial.

{{% hint style="danger" %}}
In production always verify the signature, reject bad signatures, and make handlers idempotent. Poll `GET /v1/sessions/{id}` if a delivery is missing.
{{% endhint %}}

## Test the integration

Use Identity Console → Webhooks → **Send test**, or finish a verification. Company Admin **Webhooks** (or `GET /demo/webhooks/events`) lists deliveries.

## Event types (supported)

| Event | When |
| --- | --- |
| `session.created` | New verification session started |
| `session.completed` | Verification finished (see `payload.decision` / identity trust) |

Related: [Initial setup process](initial-setup.md) · [Creating a session (API)](api.md) · [Session states](session-states.md).
""",
    )
    hub(
        "idv/licensing.md",
        "Licensing",
        "Hybrid licence issuer and protocol used by the IDV platform.",
        """
IDV uses **Hybrid** licensing: day-to-day metering on the customer host, issuance by Identixia.

| Piece | Docs |
| --- | --- |
| Issuer UI / APIs | [License Admin](license-admin.md) |
| Shared protocol | [Hybrid protocol (`license/license_v2`)](license-protocol.md) |
| Production exposure | Keep issuer on localhost — [Production](production.md) |

## Operator exchange

| Action | Customer sends | You return |
| --- | --- | --- |
| First issue | `license_request.txt` | `license.txt` |
| Same host again | — | Used count kept (no restore) |

The issuer never sees ID images or biometrics. Brand files for consoles live under `license/admin/brand/`.
""",
    )
    hub(
        "idv/license-admin.md",
        "License Admin",
        "Identixia Hybrid issuer (license/admin) on localhost :14190.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/license/admin/` |
| UI | `http://127.0.0.1:14190/` (**localhost only**) |
| Brand | `license/admin/brand/` → `/brand/*` |

```bash
cd IDV/license/admin
pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
```

First sign-in enrols an authenticator for the seeded `admin` operator.

### Operator exchange

| Action | Customer sends | You return |
| --- | --- | --- |
| First issue | `license_request.txt` | `license.txt` |
| Same host again | — | Used count kept (no restore) |

`POST /api/v2/online/report` may be exposed via reverse proxy for customer sync; do **not** expose the operator UI off-box.
""",
    )
    hub(
        "idv/license-protocol.md",
        "Hybrid licence protocol",
        "license_v2 shared protocol used by platform/server and license/admin.",
        """
## Overview

IDV uses a **Hybrid** licence model: day-to-day entitlement metering runs on the customer host; Identixia issues and renews licence files.

| Path | Role |
| --- | --- |
| `IDV/license/license_v2/` | Canonical protocol sources and tests |
| Vendored copies | Inside `platform/server/` and `license/admin/` for self-contained runs |
| `IDV/packages/license-core` | Helper package for consoles and shared libraries |

## Operating model

| Step | Where it happens |
| --- | --- |
| Issue / renew `license.txt` | [License Admin](license-admin.md) (Identixia) |
| Enforce usage on the host | `license/license_v2` inside `platform/server` |
| Sync usage receipts | USB export or `POST /api/v2/online/report` (when exposed) |

There is one commercial Hybrid product. Operators do not choose STRICT/LENIENT tiers in the issuer UI. The issuer never receives ID images or biometrics.

Parent: [Licensing](licensing.md).
""",
    )
    hub(
        "idv/shared-packages.md",
        "Shared packages",
        "IDV/packages libraries shared by platform and company UIs.",
        """
| Package | Role |
| --- | --- |
| `admin-ui` | Shared React helpers for Identity Console and Company Admin |
| `decision-core` | Trust / decision helpers |
| `license-core` | Hybrid licence helpers |
| `contracts` / `db` | Shared contracts and DB helpers when used by kits |

Applicant SDKs are **not** here — they live under `IDV/app/packages/`.
""",
    )
    hub(
        "idv/reference.md",
        "Reference",
        "Where to find IDV API tables, Postman, and the offline handbook.",
        """
| Resource | Location |
| --- | --- |
| Integrator summary (this site) | [Creating a session (API)](api.md) · [Walkthrough](walkthrough.md) · [Production](production.md) |
| Endpoint / persistence notes | `IDV/docs/API.md` |
| Offline handbook (chapters) | `IDV/docs/handbook/` · `IDV/docs/index.html` |
| Postman (public / private / company) | `IDV/platform/server/postman/` |
| Architecture notes | `IDV/docs/architecture.md` |

GitBook covers the integrator path. Deep handbook chapters stay in `IDV/docs/` and are not duplicated page-for-page here.
""",
    )
    hub(
        "idv/engines-document.md",
        "Document engine",
        "How IDV calls the ID Document SDK HTTP API.",
        """
## Default configuration

| Setting | Value |
| --- | --- |
| Base URL | `http://127.0.0.1:14102` |
| Modes | `documentProcess` · `documentRecognition` · `documentLiveness` |

IDV selects recognition, authenticity, or full process based on workflow steps and licence flags. Parse engine responses as [Result JSON](../id-document-sdk/result-json.md).

## Related docs

* [ID Document SDK → Server](../id-document-sdk/full-server.md)
* Parent: [Engines](engines.md)
""",
    )
    hub(
        "idv/engines-face.md",
        "Face engine",
        "How IDV calls the Face SDK HTTP API.",
        """
## Default configuration

| Setting | Value |
| --- | --- |
| Base URL | `http://127.0.0.1:14103` |
| Modes | compare · boxes · template · score · liveness |

IDV uses the Face SDK matcher for 1:1 and related steps. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.

## Related docs

* [Face SDK → Server](../face-sdk/full-server.md)
* Parent: [Engines](engines.md)
""",
    )
    hub(
        "idv/components-clients.md",
        "Applicant clients",
        "IDV client SDKs and demo apps under IDV/app/.",
        """
Capture SDKs and demos. The **service token stays on the company backend**; apps use capture tokens.

## Packages (`IDV/app/packages/`)

| Package | Role |
| --- | --- |
| `idv-web` | Embeddable web capture UI |
| `idv-react` | React wrapper |
| `idv-android` | Android SDK (CameraX) |
| `idv-ios` | Swift package `IdvSdk` |

## Demo hosts

| App | Docs |
| --- | --- |
| Web | [Web demo](client-web.md) |
| Android | [Android demo](client-android.md) |
| iOS | [iOS demo](client-ios.md) |
| Flutter / React Native | [Other demos](client-other.md) |

```bash
python IDV/app/tools/refresh_client.py
```
""",
    )
    hub(
        "idv/client-web.md",
        "Web demo",
        "Run the IDV web applicant demo.",
        """
## Run locally

```bash
cd IDV/app/demos/web
npm install && npm run dev
# http://127.0.0.1:5175/
```

## Integration rule

Start verification through the [company backend](company-backend.md) (or your own server). Do not embed the company service bearer in the browser.

Parent: [Applicant clients](components-clients.md).
""",
    )
    hub(
        "idv/client-android.md",
        "Android demo",
        "Build the IDV Android applicant demo.",
        """
## Build

```bash
cd IDV/app/packages/idv-android
./gradlew publishToMavenLocal
cd ../../app/android
./gradlew :app:assembleDebug
```

Use a capture token from the company backend. Package sources: `IDV/app/packages/idv-android`.

Parent: [Applicant clients](components-clients.md).
""",
    )
    hub(
        "idv/client-ios.md",
        "iOS demo",
        "Run the IDV iOS applicant demo.",
        """
## Run

Open `IDV/app/demos/ios/IdvClient.xcodeproj` and run the **IdvClient** scheme on a physical device when testing camera capture.

Session client package: `IDV/app/packages/idv-ios`.

Parent: [Applicant clients](components-clients.md).
""",
    )
    hub(
        "idv/client-other.md",
        "Flutter & React Native demos",
        "Other IDV applicant demo hosts.",
        """
## Demo hosts

| App | Path |
| --- | --- |
| Flutter | `IDV/app/demos/flutter` |
| React Native | `IDV/app/demos/react_native` |

React Native capture helpers align with `packages/idv-web`. See `IDV/app/README.md` for bootstrap details.

Parent: [Applicant clients](components-clients.md).
""",
    )


def write_summary(_structure: dict[str, list[tuple[str, str]]] | None = None) -> None:
    """4–5 level GitBook sidebar. Leaf platform files keep stable catalog URLs."""
    lines = [
        "# Table of contents",
        "",
        "",
        "* [Welcome to Identixia](README.md)",
        "* [Face SDK](face-sdk/README.md)",
        "  * [Recognition](face-sdk/recognition.md)",
        "    * [Full product (recognition + liveness)](face-sdk/full-product.md)",
        "      * [Mobile & cross-platform](face-sdk/full-mobile.md)",
        "        * [Android](face-sdk/android.md)",
        "        * [iOS](face-sdk/ios.md)",
        "        * [Flutter](face-sdk/flutter.md)",
        "        * [React Native](face-sdk/react-native.md)",
        "        * [Ionic Capacitor](face-sdk/ionic-capacitor.md)",
        "        * [Ionic Cordova](face-sdk/ionic-cordova.md)",
        "      * [Server (Windows & Docker)](face-sdk/full-server.md)",
        "        * [Windows](face-sdk/windows.md)",
        "        * [Linux / Docker](face-sdk/linux-docker.md)",
        "    * [Recognition-only products](face-sdk/recognition-only.md)",
        "      * [Windows](face-sdk/recognition-windows.md)",
        "      * [Linux / Docker](face-sdk/recognition-linux-docker.md)",
        "  * [Liveness](face-sdk/liveness.md)",
        "    * [In the full product](face-sdk/full-product.md)",
        "      * [Mobile & cross-platform](face-sdk/full-mobile.md)",
        "      * [Server (Windows & Docker)](face-sdk/full-server.md)",
        "    * [Liveness-only products](face-sdk/liveness-only.md)",
        "      * [Mobile](face-sdk/liveness-only-mobile.md)",
        "        * [Android](face-sdk/liveness-android.md)",
        "        * [iOS](face-sdk/liveness-ios.md)",
        "      * [Server](face-sdk/liveness-only-server.md)",
        "        * [Windows](face-sdk/liveness-windows.md)",
        "        * [Linux / Docker](face-sdk/liveness-linux-docker.md)",
        "* [ID Document SDK](id-document-sdk/README.md)",
        "  * [Recognition](id-document-sdk/recognition.md)",
        "    * [Full product (recognition + liveness)](id-document-sdk/full-product.md)",
        "      * [Mobile & cross-platform](id-document-sdk/full-mobile.md)",
        "        * [Android](id-document-sdk/android.md)",
        "        * [iOS](id-document-sdk/ios.md)",
        "        * [Flutter](id-document-sdk/flutter.md)",
        "        * [React Native](id-document-sdk/react-native.md)",
        "        * [Ionic Capacitor](id-document-sdk/ionic-capacitor.md)",
        "        * [Ionic Cordova](id-document-sdk/ionic-cordova.md)",
        "      * [Server (Windows & Docker)](id-document-sdk/full-server.md)",
        "        * [Windows](id-document-sdk/windows.md)",
        "        * [Linux / Docker](id-document-sdk/linux-docker.md)",
        "  * [Liveness](id-document-sdk/liveness.md)",
        "    * [In the full product](id-document-sdk/full-product.md)",
        "      * [Mobile & cross-platform](id-document-sdk/full-mobile.md)",
        "      * [Server (Windows & Docker)](id-document-sdk/full-server.md)",
        "    * [Liveness-only products](id-document-sdk/liveness-only.md)",
        "      * [Linux / Docker](id-document-sdk/liveness-linux-docker.md)",
        "  * [Reference](id-document-sdk/reference.md)",
        "    * [Result JSON](id-document-sdk/result-json.md)",
        "    * [Security check fields](id-document-sdk/security-fields.md)",
        "* [IDV platform](idv/README.md)",
        "  * [Getting started](idv/getting-started.md)",
        "    * [Project structure](idv/project-structure.md)",
        "    * [Prerequisites: engines](idv/engines.md)",
        "      * [Document engine](idv/engines-document.md)",
        "      * [Face engine](idv/engines-face.md)",
        "    * [Project setup](idv/environment.md)",
        "    * [Initial setup process](idv/initial-setup.md)",
        "    * [Quick start](idv/quick-start.md)",
        "    * [End-to-end walkthrough](idv/walkthrough.md)",
        "  * [Session states](idv/session-states.md)",
        "  * [Creating a session (API)](idv/api.md)",
        "  * [Webhook integration](idv/company-webhooks.md)",
        "  * [Applicant clients](idv/components-clients.md)",
        "    * [Web demo](idv/client-web.md)",
        "    * [Android demo](idv/client-android.md)",
        "    * [iOS demo](idv/client-ios.md)",
        "    * [Flutter & React Native](idv/client-other.md)",
        "  * [Architecture](idv/architecture.md)",
        "  * [Platform](idv/platform.md)",
        "    * [IDV server](idv/platform-server.md)",
        "    * [Identity Console](idv/platform-console.md)",
        "  * [Company integration](idv/company.md)",
        "    * [Company backend (server)](idv/company-backend.md)",
        "    * [Company Admin UI](idv/company-admin.md)",
        "  * [Licensing](idv/licensing.md)",
        "    * [License Admin](idv/license-admin.md)",
        "    * [Hybrid licence protocol](idv/license-protocol.md)",
        "  * [Production](idv/production.md)",
        "  * [Shared packages](idv/shared-packages.md)",
        "  * [Map of components](idv/components.md)",
        "  * [Reference](idv/reference.md)",
        "* [Request a License & Support](request-a-license-and-support.md)",
        "* [Contact](contact-us.md)",
        "",
    ]
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_gitbook_yaml() -> None:
    """Space icon uses Identixia favicon (single brand pack)."""
    (OUT / ".gitbook.yaml").write_text(
        "root: .\n\n"
        "# Brand (copied into .gitbook/assets/ by generate.py)\n"
        "# Configure the space icon/favicon in GitBook UI to favicon.png if needed.\n",
        encoding="utf-8",
        newline="\n",
    )


def clean_obsolete_trees() -> None:
    """Remove old section folders and leftover duplicate pages."""
    obsolete = [
        "face-recognition-sdk",
        "liveness-detection-sdk",
        "id-document-recognition-sdk",
        "id-document-liveness-sdk",
        "palm-recognition-sdk",
    ]
    for name in obsolete:
        p = OUT / name
        if p.is_dir():
            shutil.rmtree(p)
            print(f"removed obsolete {name}/")


def summary_label(rel: str) -> str:
    leaf = rel.rsplit("/", 1)[-1]
    return TITLES.get(leaf, title_for(rel))


def main() -> int:
    about, by_name = load_catalog()
    owner = (about.get("publish_owner") or about.get("owner") or "identixia-IDV").strip()
    OUT.mkdir(parents=True, exist_ok=True)
    sync_assets()
    clean_obsolete_trees()

    structure: dict[str, list[tuple[str, str]]] = {
        "face-sdk": [],
        "id-document-sdk": [],
        "idv": [],
    }

    write_face_hub()
    write_face_concepts()
    write_document_hub()
    write_document_concepts()
    write_idv_pages()
    write_nav_hubs()
    write_static_pages()
    write_gitbook_yaml()

    for item in about["repositories"]:
        name = item["name"]
        if name == "identixia-assets":
            continue
        rel = homepage_rel(item["homepage"])
        if not rel:
            print(f"SKIP non-docs homepage: {name}")
            continue
        path = build_product_page(owner, item, rel, by_name)
        if path is None:
            print(f"HUB {name} -> section README (custom)")
            continue
        print(f"OK {name} -> {path.relative_to(OUT.parent)} ({path.stat().st_size} bytes)")
        if "/" in rel:
            section, leaf = rel.split("/", 1)
            structure.setdefault(section, []).append((summary_label(rel), f"{leaf}.md"))

    write_welcome()
    write_summary(structure)
    print(f"Wrote docs under {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
