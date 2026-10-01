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

## What this SDK is

The **Face SDK** runs on the phone or on your server. It covers two licensed functions:

| Function | What it does | License flag |
| --- | --- | --- |
| **Recognition** | Detect faces, attributes, quality, templates, 1:1 match, 1:N identify | `recognition` |
| **Liveness** | Passive presentation-attack score (real person vs photo/screen) | `liveness` |

Pick a **repository that matches your license**. A recognition-only build will not invent liveness scores.

## Choose a product line

| You need | Use |
| --- | --- |
| Recognition **and** liveness in one app / API | Full platforms below (Android → Docker) |
| Recognition only | [Windows](recognition-windows.md) · [Linux / Docker](recognition-linux-docker.md) |
| Liveness only | [Android](liveness-android.md) · [iOS](liveness-ios.md) · [Windows](liveness-windows.md) · [Linux / Docker](liveness-linux-docker.md) |

Read the function guides first if you are new:

* [Face recognition](recognition.md) — APIs, gallery, match
* [Face liveness](liveness.md) — when scores appear, how to gate UX

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

## How to integrate

1. Open the platform page for your stack.
2. Clone the sample → place engine binaries from GitHub Releases → run until **Ready**.
3. Activate with **your** application id / machine code (demo keys only work for demo ids).
4. Call recognition and liveness APIs on a **background** thread (mobile) or via HTTP (server).

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
## In plain words

Face **recognition** turns a camera image into something you can store and compare:

1. **Find** the face (box, landmarks, pose).
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
## In plain words

Face **liveness** answers: “Is this a live person, or a photo / screen / replay?”

It is **passive** — the user looks at the camera; there is no smile/blink challenge in the core API.

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

## What this SDK is

The **ID Document SDK** reads passports, national IDs, and driver licenses **on-premise**. Two licensed functions:

| Function | What it does | License flag |
| --- | --- | --- |
| **Recognition** | Locate, OCR, MRZ, barcode, cropped images | `recognition` |
| **Liveness / authenticity** | Anti-spoof checks (screen, printout, substitution) | `authenticity` |

Full product repositories run **both** when the license allows. There is also a **liveness-only** Linux / Docker API if you only need authenticity.

## Start here

1. [Document recognition](recognition.md) — fields, MRZ, images
2. [Document liveness](liveness.md) — security checks vs OCR
3. [Result JSON](result-json.md) — one shape for mobile and server
4. [Security check fields](security-fields.md) — how to read authenticity

## Full product (recognition + liveness)

| Platform | Repository | Docs |
| --- | --- | --- |
| Android | [`ID-Document-Recognition-Liveness-Detection-Android`]({GH}/ID-Document-Recognition-Liveness-Detection-Android) | [Android](android.md) |
| iOS | [`ID-Document-Recognition-Liveness-Detection-iOS`]({GH}/ID-Document-Recognition-Liveness-Detection-iOS) | [iOS](ios.md) |
| Flutter | [`ID-Document-Recognition-Liveness-Detection-Flutter`]({GH}/ID-Document-Recognition-Liveness-Detection-Flutter) | [Flutter](flutter.md) |
| React Native | [`ID-Document-Recognition-Liveness-Detection-React-Native`]({GH}/ID-Document-Recognition-Liveness-Detection-React-Native) | [React Native](react-native.md) |
| Ionic Capacitor | [`…-Ionic-Capacitor`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) | [Ionic Capacitor](ionic-capacitor.md) |
| Ionic Cordova | [`…-Ionic-Cordova`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) | [Ionic Cordova](ionic-cordova.md) |
| Windows | [`…-Windows`]({GH}/ID-Document-Recognition-Liveness-Detection-Windows) | [Windows](windows.md) |
| Linux / Docker | [`…-Docker`]({GH}/ID-Document-Recognition-Liveness-Detection-Docker) | [Linux / Docker](linux-docker.md) |

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
## In plain words

Document **recognition** finds the card in the frame and extracts:

* Visual-zone fields (name, document number, dates, …)
* **MRZ** (machine-readable zone)
* Barcode / QR when present
* Cropped images (portrait, document, signature, …)

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
## In plain words

Document **liveness** (authenticity) checks whether the ID is likely a real document versus:

* A screen replay
* A printout / paper copy
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
        "Identixia IDV: customer-run verification server, consoles, licensing, and applicant clients.",
        f"""
<p align="center"><img src="../.gitbook/assets/brand-logo.png" alt="Identixia" width="220"></p>
<p align="center"><img src="../.gitbook/assets/favicon.png" alt="Identixia mark" width="48"></p>

## What IDV is

**IDV** is the Identixia identity-verification **platform** (folder `IDV/` in the monorepo). It is not a replacement for the Face or Document SDKs — it **orchestrates** them.

| Piece | Role |
| --- | --- |
| `idv-server` | Platform API + workers (`:14187`) |
| `idv-server-ui` | Identity Console (dev `:14188`, production `/admin`) |
| `company-backend` + `company-admin` | Sample merchant backend + UI |
| `license-admin` | Hybrid licence issuer (`:14190`) |
| `client/` | Applicant SDKs and demo apps |
| `license_v2` / `packages/` | Shared protocol and libraries |

Brand logo and favicons for the consoles live in `IDV/license-admin/brand/` and are served at `/brand/*`.

## Read next

1. [Architecture](architecture.md) — who owns what
2. [Quick start](quick-start.md) — run locally
3. [Document & Face engines](engines.md) — HTTP wiring to the SDKs
4. [Components & clients](components.md) — packages and demos

Deep offline handbook (chapters, Postman, schema): see `IDV/docs/` in the source tree — not duplicated here.

{{% hint style="info" %}}
With `IDV_ENGINES=http`, IDV calls your local Document and Face HTTP APIs. Start those SDK servers first (or point env URLs at your deployment).
{{% endhint %}}
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "architecture.md",
        "Architecture",
        "IDV runtime flow, authority boundaries, and decision policy.",
        """
## Runtime flow

```text
Company backend                Capture app (web / mobile)
       │                                │
       │  POST /v1/sessions             │
       │  mint capture token            │
       ├───────────────────────────────►│
       │                                │ submissions (+ step headers)
       │                                ▼
       │                         IDV Server :14187
       │                    normalize → engines → decision
       │                                │
       ▼                                ▼
 Identity Console /admin          reviews · identities · webhooks
```

1. Business backend creates a session with service credentials.
2. Backend mints a **session-scoped capture token**.
3. Capture client submits protected SDK bundles to `/submissions`.
4. Server normalizes signals, evaluates trust factors, opens review when needed.
5. Outbound events use a transactional outbox; inbound vendor callbacks use a durable inbox.

## Authority

| Concern | Owner |
| --- | --- |
| Document OCR / face match / liveness scores | Document SDK + Face SDK (or adapters) |
| Tenant policy, review leases, API auth | IDV server |
| Hybrid entitlement metering | `license_v2` inside `idv-server` |
| Licence issuance | `license-admin` |

## Decision rule

Trust aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing or error signals never auto-accept. Implementation lives under `idv-server/idv/decision/`.
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "quick-start.md",
        "Quick start",
        "Run IDV server, console, company sample, and licence admin locally.",
        """
## Storage defaults

Local durable storage defaults to **SQLite** under each project’s `database/` folder.

| Project | Default |
| --- | --- |
| `idv-server` | `idv-server/database/idv.sqlite` (or `IDV_SQLITE_PATH`) |
| `company-backend` | `company-backend/database/company.sqlite` |
| `license-admin` | `license-admin/database/` |

For PostgreSQL / media / Valkey / RabbitMQ: `python setup_database.py` from `IDV/`.

## 1. IDV server

```bash
cd IDV/idv-server
python -m venv .venv && .venv/Scripts/activate   # or source .venv/bin/activate
pip install -r requirements.txt
set IDV_OPEN_API=1                               # Windows; export on Unix
python app.py
```

* API: `http://127.0.0.1:14187/v1`
* Admin: `http://127.0.0.1:14187/admin/`

## 2. Identity Console (develop)

```bash
cd IDV/idv-server-ui
npm install && npm run dev
```

Open `http://127.0.0.1:14188/` (proxies API to `:14187`). Production build is served from the server at `/admin/`.

## 3. Company sample

```bash
cd IDV/company-backend && pip install -r requirements.txt && python app.py
# UI: cd IDV/company-admin && npm install && npm run dev  → :14189
```

## 4. Licence admin

```bash
cd IDV/license-admin
pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
```

Open `http://127.0.0.1:14190` (localhost only). Favicon and logo: `license-admin/brand/`.

## 5. Applicant demos

See [Components & clients](components.md) and `IDV/client/README.md`.
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

These are the same APIs documented under [ID Document SDK](../id-document-sdk/) and [Face SDK](../face-sdk/).

## Example — create session then capture (sketch)

```http
POST /v1/sessions
Authorization: Bearer demo
X-Tenant-Id: ten_demo
Content-Type: application/json

{ "workflow_id": "onboarding_standard", "environment": "test" }
```

The response includes session id and next step. Your backend mints a capture token; the applicant app posts submissions with `X-IDV-Step-ID` and `Authorization: Bearer <capture-token>`.

IDV then calls Document/Face engines, stores results, and applies trust decision policy.

## Matching note

Face 1:1 / 1:N uses the **Face SDK matcher**. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.

## Full API tables

Postman collections and endpoint-level persistence notes live in `IDV/docs/API.md` and `IDV/idv-server/postman/` (source tree).
""".strip()
        + "\n",
    )
    write_page(
        OUT / "idv" / "components.md",
        "Components & clients",
        "IDV folders, applicant SDKs, and demo apps — without duplicating the handbook.",
        f"""
## Top-level layout (`IDV/`)

| Path | Role | Port (dev) |
| --- | --- | --- |
| `idv-server/` | Platform API + workers | 14187 |
| `idv-server-ui/` | Identity Console | 14188 |
| `company-backend/` | Sample company API | 14195 |
| `company-admin/` | Company operator UI | 14189 |
| `license-admin/` | Identixia Hybrid issuer + **brand** | 14190 |
| `client/` | Applicant SDKs and demos | (per app) |
| `packages/` | Shared server/console libraries | — |
| `license_v2/` | Shared licence protocol | — |
| `docs/` | Offline handbook + API reference | — |

## Applicant clients (`IDV/client/`)

| Path | Role |
| --- | --- |
| `packages/idv-web` | Embeddable web verification UI |
| `packages/idv-react` | React wrapper |
| `packages/idv-android` | Android SDK (CameraX capture) |
| `packages/idv-ios` | Swift package `IdvSdk` |
| `app/web` · `app/android` · `app/ios` · `app/flutter` · `app/react_native` | Demo hosts |

Web demo:

```bash
cd IDV/client/app/web
npm install && npm run dev
# http://127.0.0.1:5175/
```

Refresh engines/catalog into demos (from monorepo root):

```bash
python IDV/client/tools/refresh_client.py
```

## Brand assets

Use **one** brand pack — do not copy logos into every app:

* Source: `IDV/license-admin/brand/` (`logo.png`, `favicon.ico`, `favicon.png`, `apple-touch-icon.png`)
* Runtime: served as `/brand/*` from licence admin / configured brand dir
* Docs site: same files under `.gitbook/assets/` (`brand-logo.png`, `favicon.png`, …)

GitHub: monorepo [`identixia-IDV`]({GH}) — IDV sources ship with your distribution; Face/Document demos are separate public product repos under the same org.
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

1. Build with **your** applicationId / bundle id (not the demo id).
2. Contact us with the id and product (Face recognition / Face liveness / Document recognition / Document authenticity).
3. Activate → init as shown on the platform page.

Demo keys work only for demo application ids.

## Server SDK (Windows / Linux / Docker)

1. Start the API once.
2. `GET /api/machinecode` → copy `data.machinecode`.
3. Send that code to Identixia. **Docker and bare metal differ.**
4. `POST /api/activate` or place `license.txt` and restart.
5. Confirm with `GET /api/licenseStatus`.

## IDV

IDV uses Hybrid licensing via `license-admin` / `license_v2`. Use the issuer UI on `:14190` (localhost) and the entitlement flow described in `IDV/docs/`.

## Support

{% include "./.gitbook/includes/contact.md" %}
""".strip()
        + "\n",
    )
    write_page(
        OUT / "contact-us.md",
        "Contact",
        "Contact Identixia for licenses and support.",
        """
## Availability

We are available 24/7.

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

Identixia documentation is organized into **three products**:

| Product | Source in monorepo | What you get |
| --- | --- | --- |
| [**Face SDK**](face-sdk/) | `repositories/Face*` | Face recognition and passive face liveness |
| [**ID Document SDK**](id-document-sdk/) | `repositories/ID-Document*` | Document OCR/MRZ and document authenticity |
| [**IDV**](idv/) | `IDV/` | Verification platform that calls the two SDKs |

Biometric data stays on **your** device or server.

## How to use these docs

The left sidebar is **multi-level** (product → function → product line → channel → platform).

1. Open the **product** (Face, Document, or IDV).
2. Open **Recognition** or **Liveness** (or IDV → Getting started / Engines / Components).
3. Pick **full product**, **recognition-only**, or **liveness-only**, then **Mobile** or **Server**.
4. Open your **platform** page → Quick start → Ready → API reference.
5. For IDV, start Document + Face engines, then the IDV server and a client demo.

{% hint style="info" %}
Native engine binaries ship on GitHub Releases (`/releases/latest/download/…`). They are not committed to git. Demo UIs are optional — call the SDK/API directly in production.
{% endhint %}

## Products

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>Face SDK</strong></td><td>Detect, templates, 1:1 / 1:N, and passive liveness when licensed. Mobile and server repositories under <code>repositories/</code>.</td><td><a href=".gitbook/assets/face-android-home.png">face-android-home.png</a></td><td></td><td><a href="face-sdk/">face-sdk</a></td></tr>
<tr><td><strong>ID Document SDK</strong></td><td>Passport and ID OCR, MRZ, barcode, and document authenticity when licensed.</td><td><a href=".gitbook/assets/document-desktop-status.png">document-desktop-status.png</a></td><td></td><td><a href="id-document-sdk/">id-document-sdk</a></td></tr>
<tr><td><strong>IDV platform</strong></td><td>Sessions, capture clients, Identity Console, company sample, and Hybrid licensing — uses Face + Document engines over HTTP.</td><td><a href=".gitbook/assets/brand-mark.png">brand-mark.png</a></td><td></td><td><a href="idv/">idv</a></td></tr>
</tbody></table>

## Shared ideas

| Topic | Summary |
| --- | --- |
| Control vs process (HTTP) | `/api/health`, `/api/machinecode`, `/api/activate`, `/api/licenseStatus` → `{success,code,message,request_id,data}`. Process routes return engine JSON. |
| Threading (mobile) | Activate, init, detect, recognize on a **background** thread. |
| License flags | Face: `recognition` / `liveness`. Document: `recognition` / `authenticity`. Missing flag ⇒ feature not run. |
| Brand | Logo and favicons: docs `.gitbook/assets/`; IDV consoles `IDV/license-admin/brand/`. |

## Links

* [Request a license & support](request-a-license-and-support.md)
* [Contact](contact-us.md)
* [identixia.com](https://identixia.com)
* GitHub: [identixia-IDV](https://github.com/identixia-IDV)
""".strip()
    write_page(
        OUT / "README.md",
        "Welcome to Identixia",
        "Identixia docs: Face SDK, ID Document SDK, and IDV platform — clear setup and API guidance.",
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

Choose **full product** when one app or one API must do both:

* face recognition (detect, template, 1:1, 1:N)
* passive face liveness (when the license includes `liveness`)

## Where to go next

| Channel | Page |
| --- | --- |
| Phones & cross-platform | [Mobile](full-mobile.md) |
| Windows & Docker | [Server](full-server.md) |

Function guides: [Recognition](recognition.md) · [Liveness](liveness.md)
""",
    )
    hub(
        "face-sdk/full-mobile.md",
        "Mobile & cross-platform",
        "Full Face SDK samples for Android, iOS, Flutter, React Native, and Ionic.",
        """
## Platforms

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | `FaceRecognition-LivenessDetection-Android` |
| iOS | [iOS](ios.md) | `FaceRecognition-LivenessDetection-iOS` |
| Flutter | [Flutter](flutter.md) | `FaceRecognition-LivenessDetection-Flutter` |
| React Native | [React Native](react-native.md) | `FaceRecognition-LivenessDetection-React-Native` |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | `…-Ionic-Capacitor` |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | `…-Ionic-Cordova` |

Open the platform page → Quick start → Ready → API reference.
""",
    )
    hub(
        "face-sdk/full-server.md",
        "Server (Windows & Docker)",
        "Full Face SDK HTTP APIs for Windows and Linux/Docker.",
        """
## Platforms

| Platform | Docs | Default port |
| --- | --- | --- |
| Windows | [Windows](windows.md) | 14103 |
| Linux / Docker | [Linux / Docker](linux-docker.md) | 14103 |

Control routes use `{success,code,message,request_id,data}`. Process routes return engine JSON.
""",
    )
    hub(
        "face-sdk/recognition-only.md",
        "Recognition-only products",
        "Face recognition without liveness packs — Windows and Linux/Docker.",
        """
## When to use

Use these when your license is **recognition only** (no `liveness` flag / no liveness packs).

| Platform | Docs |
| --- | --- |
| Windows | [Windows (recognition only)](recognition-windows.md) |
| Linux / Docker | [Linux / Docker (recognition only)](recognition-linux-docker.md) |

For recognition **with** liveness in one build, use the [full product](full-product.md) instead.
""",
    )
    hub(
        "face-sdk/liveness-only.md",
        "Liveness-only products",
        "Standalone face liveness SDKs without the full recognition gallery stack.",
        """
## When to use

Score a face for presentation-attack detection without shipping the full enroll / 1:N stack.

### Mobile

| Platform | Docs |
| --- | --- |
| Android | [Android](liveness-android.md) |
| iOS | [iOS](liveness-ios.md) |

### Server

| Platform | Docs |
| --- | --- |
| Windows | [Windows](liveness-windows.md) |
| Linux / Docker | [Linux / Docker](liveness-linux-docker.md) |

Concept guide: [Face liveness](liveness.md).
""",
    )
    hub(
        "face-sdk/liveness-only-mobile.md",
        "Liveness-only — mobile",
        "Android and iOS standalone face liveness samples.",
        """
| Platform | Docs |
| --- | --- |
| Android | [Android](liveness-android.md) |
| iOS | [iOS](liveness-ios.md) |
""",
    )
    hub(
        "face-sdk/liveness-only-server.md",
        "Liveness-only — server",
        "Windows and Linux/Docker standalone face liveness APIs.",
        """
| Platform | Docs |
| --- | --- |
| Windows | [Windows](liveness-windows.md) |
| Linux / Docker | [Linux / Docker](liveness-linux-docker.md) |
""",
    )

    # —— ID Document SDK ——
    hub(
        "id-document-sdk/full-product.md",
        "Full product (recognition + liveness)",
        "Document repositories that ship OCR/MRZ and authenticity together.",
        """
## When to use

One sample / API for document **recognition** and document **authenticity** (when licensed).

| Channel | Page |
| --- | --- |
| Phones & cross-platform | [Mobile](full-mobile.md) |
| Windows & Docker | [Server](full-server.md) |

Guides: [Recognition](recognition.md) · [Liveness](liveness.md) · [Result JSON](result-json.md)
""",
    )
    hub(
        "id-document-sdk/full-mobile.md",
        "Mobile & cross-platform",
        "Full Document SDK samples for Android, iOS, Flutter, React Native, and Ionic.",
        """
| Platform | Docs |
| --- | --- |
| Android | [Android](android.md) |
| iOS | [iOS](ios.md) |
| Flutter | [Flutter](flutter.md) |
| React Native | [React Native](react-native.md) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) |
""",
    )
    hub(
        "id-document-sdk/full-server.md",
        "Server (Windows & Docker)",
        "Full Document SDK HTTP APIs for Windows and Linux/Docker.",
        """
| Platform | Docs | Default port |
| --- | --- | --- |
| Windows | [Windows](windows.md) | 14102 |
| Linux / Docker | [Linux / Docker](linux-docker.md) | 14102 |

Routes: `/api/documentProcess`, `/api/documentRecognition`, `/api/documentLiveness`.
""",
    )
    hub(
        "id-document-sdk/liveness-only.md",
        "Liveness-only products",
        "Document authenticity API without the full OCR product surface.",
        """
## When to use

You only need document anti-spoofing (authenticity), not a full OCR UI.

| Platform | Docs |
| --- | --- |
| Linux / Docker | [Document liveness Docker](liveness-linux-docker.md) |

Concept guide: [Document liveness](liveness.md).
""",
    )
    hub(
        "id-document-sdk/reference.md",
        "Reference",
        "Shared Document SDK result shapes and security fields.",
        """
| Topic | Page |
| --- | --- |
| Process / recognize JSON | [Result JSON](result-json.md) |
| Authenticity fields | [Security check fields](security-fields.md) |

Parse JSON in your app — do not scrape the demo Result screen.
""",
    )

    # —— IDV ——
    hub(
        "idv/getting-started.md",
        "Getting started",
        "How to approach Identixia IDV before running services.",
        """
## Path

1. Skim [Architecture](architecture.md) (who owns what).
2. Start Document + Face HTTP engines ([Engines](engines.md)).
3. Follow [Quick start](quick-start.md) for `idv-server` and the console.
4. Wire an applicant client from [Components](components.md).

Deep handbook chapters stay in the source tree under `IDV/docs/` (not duplicated here).
""",
    )
    hub(
        "idv/engines-document.md",
        "Document engine",
        "How IDV calls the ID Document SDK HTTP API.",
        """
## Default

| Setting | Value |
| --- | --- |
| Base URL | `http://127.0.0.1:14102` |
| Modes | `documentProcess` · `documentRecognition` · `documentLiveness` |

Docs for that server: [ID Document SDK → Server](../id-document-sdk/full-server.md).

Parent: [Document & Face engines](engines.md).
""",
    )
    hub(
        "idv/engines-face.md",
        "Face engine",
        "How IDV calls the Face SDK HTTP API.",
        """
## Default

| Setting | Value |
| --- | --- |
| Base URL | `http://127.0.0.1:14103` |
| Modes | compare · boxes · template · score · liveness |

Docs for that server: [Face SDK → Server](../face-sdk/full-server.md).

Parent: [Document & Face engines](engines.md).
""",
    )
    hub(
        "idv/components-server.md",
        "Platform server",
        "idv-server API, workers, and admin mount.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/idv-server/` |
| API | `http://127.0.0.1:14187/v1` |
| Admin UI (prod) | `http://127.0.0.1:14187/admin/` |

See [Quick start](quick-start.md) for venv + `IDV_OPEN_API=1`.
""",
    )
    hub(
        "idv/components-consoles.md",
        "Consoles & admin UIs",
        "Identity Console, company admin, and licence admin.",
        """
| UI | Folder | Dev port |
| --- | --- | --- |
| Identity Console | `idv-server-ui/` | 14188 |
| Company Admin | `company-admin/` | 14189 |
| Licence Admin | `license-admin/` | 14190 |

Brand (logo / favicon): `license-admin/brand/` → `/brand/*`.
""",
    )
    hub(
        "idv/components-clients.md",
        "Applicant clients",
        "IDV client SDKs and demo apps under IDV/client/.",
        """
## Packages

| Package | Role |
| --- | --- |
| `packages/idv-web` | Embeddable web capture UI |
| `packages/idv-react` | React wrapper |
| `packages/idv-android` | Android SDK |
| `packages/idv-ios` | Swift package |

## Demo hosts

| App | Path |
| --- | --- |
| Web | [Web demo](client-web.md) |
| Android | [Android demo](client-android.md) |
| iOS | [iOS demo](client-ios.md) |
| Flutter / React Native | [Other demos](client-other.md) |

Refresh engines into demos: `python IDV/client/tools/refresh_client.py`.
""",
    )
    hub(
        "idv/client-web.md",
        "Web demo",
        "Run the IDV web applicant demo.",
        """
```bash
cd IDV/client/app/web
npm install && npm run dev
# http://127.0.0.1:5175/
```

Package: `IDV/client/packages/idv-web`.
""",
    )
    hub(
        "idv/client-android.md",
        "Android demo",
        "Build the IDV Android applicant demo.",
        """
```bash
cd IDV/client/packages/idv-android
./gradlew publishToMavenLocal
cd ../../app/android
./gradlew :app:assembleDebug
```
""",
    )
    hub(
        "idv/client-ios.md",
        "iOS demo",
        "Run the IDV iOS applicant demo.",
        """
Open `IDV/client/app/ios/IdvClient.xcodeproj` and run the **IdvClient** scheme.

Session client: `IDV/client/packages/idv-ios`.
""",
    )
    hub(
        "idv/client-other.md",
        "Flutter & React Native demos",
        "Other IDV applicant demo hosts.",
        """
| App | Path |
| --- | --- |
| Flutter | `IDV/client/app/flutter` |
| React Native | `IDV/client/app/react_native` |

Capture helpers for RN come from `packages/idv-web`. See `IDV/client/README.md`.
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
        "  * [Architecture](idv/architecture.md)",
        "  * [Engines](idv/engines.md)",
        "    * [Document engine](idv/engines-document.md)",
        "    * [Face engine](idv/engines-face.md)",
        "  * [Components](idv/components.md)",
        "    * [Platform server](idv/components-server.md)",
        "    * [Consoles & admin UIs](idv/components-consoles.md)",
        "    * [Applicant clients](idv/components-clients.md)",
        "      * [Web demo](idv/client-web.md)",
        "      * [Android demo](idv/client-android.md)",
        "      * [iOS demo](idv/client-ios.md)",
        "      * [Flutter & React Native](idv/client-other.md)",
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
