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
    (IDV_DIR / "license-admin" / "brand" / "favicon.ico", "favicon.ico"),
    (IDV_DIR / "license-admin" / "brand" / "favicon.png", "favicon.png"),
    (IDV_DIR / "license-admin" / "brand" / "apple-touch-icon.png", "apple-touch-icon.png"),
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
    "engines": "Document & Face engines",
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
        "Shared document process JSON for mobile recognize and server document APIs.",
        """
## Purpose

Mobile `recognize` and server `POST /api/documentProcess` (plus recognition / liveness routes) return the **same idea**: one JSON object your app parses.

## Top-level fields

| Field | Meaning |
| --- | --- |
| `errorCode` / process `metadata.status` | Engine / process status |
| Document type / country | Identity class and issuing country |
| `ocr` / field readings | Visual-zone fields |
| `mrz` | Machine-readable zone |
| `barcode` | Barcode / QR fields |
| `images` | Crops (portrait, document, …) |
| `tests` / `verification` | Field and document checks |
| `security` | Authenticity / document liveness (license-gated) |
| `session` | Session metadata when provided |

### Example (trimmed)

```json
{
  "identity": { "documentType": "Passport", "country": "UTO" },
  "readings": [{ "field": "surname", "value": "DOE", "source": "mrz" }],
  "tests": [{ "name": "mrzChecksum", "result": "passed" }],
  "images": [{ "role": "portrait", "data": "…" }],
  "session": { "scenario": "FullProcess" }
}
```

Exact nesting can vary slightly by platform kit — prefer the sample `ResultParser` when present. Values `0` / `1` / `2` in verification rows usually mean pass / fail / not checked.

## Related

* [Security check fields](security-fields.md)
* [Document recognition](recognition.md) · [Document liveness](liveness.md)
""".strip()
        + "\n",
    )
    write_page(
        OUT / "id-document-sdk" / "security-fields.md",
        "Security check fields",
        "How to read document authenticity / liveness fields in result JSON.",
        """
## When security fields appear

If the license includes document authenticity, the result includes `security` (and related `tests` rows) for anti-spoof checks.

| Situation | Meaning |
| --- | --- |
| `security` missing / empty | Feature **not licensed** or **not requested** — not a pass |
| Checks present with fail | Treat as authenticity reject per your risk policy |
| Recognition-only license | Use OCR/MRZ only; do not invent security passes |

Parent object: [Result JSON](result-json.md).
""".strip()
        + "\n",
    )


def write_idv_pages() -> None:
    write_page(
        OUT / "idv" / "README.md",
        "IDV platform",
        "Identixia IDV: platform server, company integration, licensing, engines, and applicant clients.",
        f"""
<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>
<p align="center"><img src="../.gitbook/assets/favicon.png" alt="Identixia mark" width="48"></p>

## Overview

**IDV** is the Identixia identity-verification **platform** (`IDV/` in the monorepo). It does not replace the Face or Document SDKs — it **orchestrates** them between your company systems and applicant capture apps.

## Who runs what

| Role | Folders | Typical ports |
| --- | --- | --- |
| **Platform** (tenant API, workers, reviews) | `idv-server/`, `idv-server-ui/` | 14187 · 14188 |
| **Company / merchant sample** | `company-backend/`, `company-admin/` | 14195 · 14189 |
| **Identixia licence issuer** | `license-admin/` (+ brand) | 14190 |
| **Applicant capture** | `client/` | e.g. web 5175 |
| **Shared libraries** | `packages/`, `license_v2/` | — |
| **Biometric engines** | Face SDK + Document SDK (HTTP) | 14103 · 14102 |

```text
Applicant app ──► Company backend :14195 ──► IDV server :14187 ──► Face/Document engines
                      │                         │
               Company Admin :14189      Identity Console :14188 /admin
                                                    │
                                           License Admin :14190 (issuer)
```

## Read next

1. [Architecture](architecture.md)
2. [Getting started](getting-started.md) → [Quick start](quick-start.md)
3. [Platform](platform.md) · [Company integration](company.md) · [Licensing](licensing.md)
4. [Engines](engines.md) · [Applicant clients](components-clients.md)

Deep handbook / Postman: `IDV/docs/` and `IDV/idv-server/postman/` in source — not copied here.

{{% hint style="info" %}}
The **service bearer token stays on the company backend**. Capture apps use a short-lived **capture token**, not the company service secret.
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
| Tenant policy, sessions, reviews, API auth | `idv-server` |
| Holding service tokens, starting sessions for apps | **Your** backend (sample: `company-backend`) |
| Hybrid entitlement metering on customer host | `license_v2` inside `idv-server` |
| Issuing Hybrid licences | `license-admin` (Identixia) |

## Decision rule

Trust aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing or error signals never auto-accept (`idv-server/idv/decision/`).
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "quick-start.md",
        "Quick start",
        "Run IDV server, Identity Console, company backend/admin, and licence admin locally.",
        """
## Order that works locally

1. Document engine `:14102` + Face engine `:14103` (see [Engines](engines.md))
2. [IDV server](platform-server.md) `:14187`
3. [Identity Console](platform-console.md) `:14188` (optional in prod — built into `/admin`)
4. [Company backend](company-backend.md) `:14195` + [Company Admin](company-admin.md) `:14189`
5. [License Admin](license-admin.md) `:14190` when testing Hybrid issue
6. An [applicant demo](components-clients.md)

## Storage defaults

| Project | Default SQLite |
| --- | --- |
| `idv-server` | `idv-server/database/idv.sqlite` (or `IDV_SQLITE_PATH`) |
| `company-backend` | `company-backend/database/company.sqlite` |
| `license-admin` | `license-admin/database/` |

PostgreSQL / media / Valkey / RabbitMQ: `python setup_database.py` from `IDV/`. See [Environment & storage](environment.md).

## Minimal commands

```bash
# Platform
cd IDV/idv-server && python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
# → http://127.0.0.1:14187/v1  and  /admin/

# Identity Console (develop)
cd IDV/idv-server-ui && npm install && npm run dev
# → http://127.0.0.1:14188/

# Company server + admin UI
cd IDV/company-backend && pip install -r requirements.txt
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
# → http://127.0.0.1:14195/  (built admin at /admin/)

cd IDV/company-admin && npm install && npm run dev
# → http://127.0.0.1:14189/

# Licence issuer (localhost only)
cd IDV/license-admin && pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
# → http://127.0.0.1:14190/
```
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "engines.md",
        "Document & Face engines",
        "How IDV calls Identixia Document and Face HTTP APIs.",
        """
## Default HTTP engines

When `IDV_ENGINES=http`, the platform calls:

| Role | Default URL | Example paths |
| --- | --- | --- |
| Document Reader | `http://127.0.0.1:14102` | `/api/documentProcess`, `/api/documentRecognition`, `/api/documentLiveness` |
| Face Recognition + liveness | `http://127.0.0.1:14103` | `/api/face/compare`, `/api/face/boxes`, `/api/face/template`, `/api/face/score`, `/api/face/liveness` |

Child pages: [Document engine](engines-document.md) · [Face engine](engines-face.md).

Same APIs as [ID Document SDK](../id-document-sdk/) and [Face SDK](../face-sdk/).

## Example — session create (platform API)

Usually the **company backend** calls this with the service bearer (not the capture app):

```http
POST /v1/sessions
Authorization: Bearer demo
X-Tenant-Id: ten_demo
Content-Type: application/json

{ "workflow_id": "onboarding_standard", "environment": "test" }
```

Then the company mints / returns a capture token; the applicant posts submissions with `X-IDV-Step-ID`.

## Matching note

Face 1:1 / 1:N uses the **Face SDK matcher**. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.

## Full API tables

`IDV/docs/API.md` and `IDV/idv-server/postman/` in the source tree.
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
| `idv-server/` | Platform API + workers (`:14187`) | [Platform server](platform-server.md) |
| `idv-server-ui/` | Identity Console (`:14188` / `/admin`) | [Identity Console](platform-console.md) |
| `company-backend/` | Sample **company server** (`:14195`) | [Company backend](company-backend.md) |
| `company-admin/` | Company operator UI (`:14189`) | [Company Admin](company-admin.md) |
| `license-admin/` | Hybrid issuer + brand (`:14190`) | [License Admin](license-admin.md) |
| `client/` | Applicant SDKs + demos | [Applicant clients](components-clients.md) |
| `packages/` | Shared UI / decision / licence libs | [Shared packages](shared-packages.md) |
| `license_v2/` | Shared Hybrid protocol | [Hybrid protocol](license-protocol.md) |
| `docs/` | Offline handbook + API notes | [Reference](reference.md) |
| `services/` | Superseded stubs — use `idv-server` | — |

## Brand

One pack only: `IDV/license-admin/brand/` → `/brand/*` and docs `.gitbook/assets/`.

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

IDV uses Hybrid licensing via `license-admin` and `license_v2`. The issuer UI listens on `:14190` (localhost). Company systems use `company-backend` (sample `:14195`) to hold the service token and start sessions — see [Company integration](idv/company.md).

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
| Brand | Logo and favicons live in docs `.gitbook/assets/`; IDV consoles use `IDV/license-admin/brand/`. |

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
        "Recommended path before wiring company systems and capture apps.",
        """
## Path

1. [Architecture](architecture.md) — company vs platform vs engines
2. [Environment & storage](environment.md) — `.env`, SQLite, PostgreSQL
3. Start [engines](engines.md), then [Quick start](quick-start.md)
4. Platform: [IDV server](platform-server.md) + [Identity Console](platform-console.md)
5. Company: [Company backend](company-backend.md) + [Company Admin](company-admin.md) + [Webhooks](company-webhooks.md)
6. Capture: [Applicant clients](components-clients.md)

Handbook: `IDV/docs/` (not duplicated here).
""",
    )
    hub(
        "idv/environment.md",
        "Environment & storage",
        "IDV .env keys, ports, and database defaults.",
        """
## Folder overrides (`.env`)

Copy `IDV/.env.example` → `IDV/.env`.

| Env key | Default |
| --- | --- |
| `IDV_SERVER_DIR` | `idv-server` |
| `IDV_SERVER_UI_DIST` | `idv-server-ui/dist` |
| `IDV_PORTAL_DIR` | `idv-server-ui/portal` |
| `IDV_BRAND_DIR` | `license-admin/brand` |
| `COMPANY_ADMIN_DIST` | `company-admin/dist` |
| `COMPANY_ADMIN_DIR` | `company-admin` |
| `LICENSE_ADMIN_DIR` | `license-admin` |
| `IDV_PORT` / `IDV_BASE_URL` | `14187` / `http://127.0.0.1:14187` |

## Durable storage

| Project | Default |
| --- | --- |
| `idv-server` | SQLite under `database/` (tenant-separated rows) |
| `company-backend` | `company-backend/database/company.sqlite` |
| `license-admin` | `license-admin/database/` (issuer ledger) |

Production: `python IDV/setup_database.py` for PostgreSQL / media / Valkey / RabbitMQ. Memory stores are for tests only (`IDV_FORCE_MEMORY` / `COMPANY_FORCE_MEMORY`).
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

Company systems integrate **through** this platform — see [Company integration](company.md).
""",
    )
    hub(
        "idv/platform-server.md",
        "IDV server",
        "idv-server: platform API, workers, storage, and /admin mount.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/idv-server/` |
| API | `http://127.0.0.1:14187/v1` |
| Admin (production build) | `http://127.0.0.1:14187/admin/` |
| Postman | `IDV/idv-server/postman/` |

```bash
cd IDV/idv-server
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
```

`IDV_OPEN_API=1` enables the local demo bearer. Workers and decision code live under `idv-server/idv/`.
""",
    )
    hub(
        "idv/platform-console.md",
        "Identity Console",
        "idv-server-ui — tenant operators: sessions, reviews, webhooks, workflows.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/idv-server-ui/` |
| Develop | `http://127.0.0.1:14188/` (proxies API to `:14187`) |
| Production | `npm run build` → served from `idv-server` at `/admin/` |

```bash
cd IDV/idv-server-ui
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
| Company server | `company-backend/` | 14195 |
| Company Admin UI | `company-admin/` | 14189 (dev) · built into `:14195/admin` |

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
        "Sample company-backend: holds the service bearer and starts IDV sessions.",
        """
## Role

`IDV/company-backend/` is the **sample company server**. It:

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
cd IDV/company-backend
pip install -r requirements.txt
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
```

Storage: `company-backend/database/company.sqlite` by default.

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
        "company-admin React UI for operators on the sample company backend.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/company-admin/` |
| Develop | `http://127.0.0.1:14189/` |
| Production | `npm run build` → `company-backend` serves `/admin/` |

```bash
cd IDV/company-admin
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
        "Company webhooks",
        "Connect Identity Console webhooks to the company-backend receiver.",
        """
## Wire-up (local)

1. Start **IDV server** and **company-backend** (`:14195`).
2. In **Company Admin → Settings**, copy the webhook URL:  
   `http://127.0.0.1:14195/demo/webhooks/idv`
3. In **Identity Console → Webhooks**, add that URL; select e.g. `session.created`, `session.completed`.
4. Copy the one-time `whsec_…` secret into Company Admin Settings and save.
5. Send a test event or finish a verification — Company Admin **Webhooks** lists deliveries.

## Signature

The receiver checks:

```text
X-IDV-Signature: sha256=<HMAC-SHA256 of the raw body>
```

Leave the secret blank only for an unsigned local trial.
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
| Shared protocol | [Hybrid protocol (`license_v2`)](license-protocol.md) |

The issuer never sees ID images or biometrics. Brand files for consoles live under `license-admin/brand/`.
""",
    )
    hub(
        "idv/license-admin.md",
        "License Admin",
        "Identixia Hybrid issuer (license-admin) on localhost :14190.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/license-admin/` |
| UI | `http://127.0.0.1:14190/` (**localhost only**) |
| Brand | `license-admin/brand/` → `/brand/*` |

```bash
cd IDV/license-admin
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
        "license_v2 shared protocol used by idv-server and license-admin.",
        """
## Overview

IDV uses a **Hybrid** licence model: day-to-day entitlement metering runs on the customer host; Identixia issues and renews licence files.

| Path | Role |
| --- | --- |
| `IDV/license_v2/` | Canonical protocol sources and tests |
| Vendored copies | Inside `idv-server/` and `license-admin/` for self-contained runs |
| `IDV/packages/license-core` | Helper package for consoles and shared libraries |

## Operating model

| Step | Where it happens |
| --- | --- |
| Issue / renew `license.txt` | [License Admin](license-admin.md) (Identixia) |
| Enforce usage on the host | `license_v2` inside `idv-server` |
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

Applicant SDKs are **not** here — they live under `IDV/client/packages/`.
""",
    )
    hub(
        "idv/reference.md",
        "Reference",
        "Where to find IDV API tables, Postman, and the offline handbook.",
        """
| Resource | Location in source |
| --- | --- |
| Endpoint / persistence notes | `IDV/docs/API.md` |
| Offline handbook (chapters) | `IDV/docs/handbook/` · `IDV/docs/index.html` |
| Postman (public / private / company) | `IDV/idv-server/postman/` |
| Architecture notes | `IDV/docs/architecture.md` |

This GitBook section stays a **navigator + quick start**. The handbook is generated from `IDV/docs/` and is not duplicated page-for-page here.
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
        "IDV client SDKs and demo apps under IDV/client/.",
        """
Capture SDKs and demos. The **service token stays on the company backend**; apps use capture tokens.

## Packages (`IDV/client/packages/`)

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
python IDV/client/tools/refresh_client.py
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
cd IDV/client/app/web
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
cd IDV/client/packages/idv-android
./gradlew publishToMavenLocal
cd ../../app/android
./gradlew :app:assembleDebug
```

Use a capture token from the company backend. Package sources: `IDV/client/packages/idv-android`.

Parent: [Applicant clients](components-clients.md).
""",
    )
    hub(
        "idv/client-ios.md",
        "iOS demo",
        "Run the IDV iOS applicant demo.",
        """
## Run

Open `IDV/client/app/ios/IdvClient.xcodeproj` and run the **IdvClient** scheme on a physical device when testing camera capture.

Session client package: `IDV/client/packages/idv-ios`.

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
| Flutter | `IDV/client/app/flutter` |
| React Native | `IDV/client/app/react_native` |

React Native capture helpers align with `packages/idv-web`. See `IDV/client/README.md` for bootstrap details.

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
        "    * [Quick start](idv/quick-start.md)",
        "    * [Environment & storage](idv/environment.md)",
        "  * [Architecture](idv/architecture.md)",
        "  * [Engines](idv/engines.md)",
        "    * [Document engine](idv/engines-document.md)",
        "    * [Face engine](idv/engines-face.md)",
        "  * [Platform](idv/platform.md)",
        "    * [IDV server](idv/platform-server.md)",
        "    * [Identity Console](idv/platform-console.md)",
        "  * [Company integration](idv/company.md)",
        "    * [Company backend (server)](idv/company-backend.md)",
        "    * [Company Admin UI](idv/company-admin.md)",
        "    * [Webhooks](idv/company-webhooks.md)",
        "  * [Licensing](idv/licensing.md)",
        "    * [License Admin](idv/license-admin.md)",
        "    * [Hybrid licence protocol](idv/license-protocol.md)",
        "  * [Applicant clients](idv/components-clients.md)",
        "    * [Web demo](idv/client-web.md)",
        "    * [Android demo](idv/client-android.md)",
        "    * [iOS demo](idv/client-ios.md)",
        "    * [Flutter & React Native](idv/client-other.md)",
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
