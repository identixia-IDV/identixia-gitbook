#!/usr/bin/env python3
"""Rebuild Identixia GitBook docs (FaceOnLive-style sidebar + content).

Sources:
  - repositories/* product READMEs + repositories/APPs/github_about.json (Face + Document)
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

ABOUT_PATH = ROOT / "repositories" / "APPs" / "github_about.json"
NAMES_PATH = ROOT / "repositories" / "APPs" / "repository_names.json"
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
    """Catalog path inside identixia-docs. Section prefixes are public URLs only."""
    if not url.startswith(DOCS_BASE):
        return None
    rel = url[len(DOCS_BASE) :].lstrip("/")
    for prefix in ("developers/", "guides/", "documentation/"):
        if rel.startswith(prefix):
            rel = rel[len(prefix) :]
            break
    return rel or None


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
            "raw.githubusercontent.com/identixia-IDV/identixia-assets",
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
    """Drop copied binaries. Pages link to identixia-assets on GitHub."""
    here = Path(__file__).resolve().parent
    for folder in (
        OUT / ".gitbook" / "assets",
        here / "documentation" / ".gitbook" / "assets",
        here / "developers" / ".gitbook" / "assets",
        here / "guides" / ".gitbook" / "assets",
    ):
        if folder.is_dir():
            shutil.rmtree(folder)
            print(f"removed local assets {folder.relative_to(here)}")


def out_path_for(rel: str) -> Path:
    if "/" not in rel:
        return OUT / rel / "README.md"
    section, leaf = rel.split("/", 1)
    return OUT / section / f"{leaf}.md"


APP_DOC_PREFIXES = (
    ("ID-Document-Recognition-Liveness-Detection-", "id-document-sdk", ""),
    ("ID-Document-Liveness-Detection-", "id-document-sdk", "liveness-"),
    ("ID-Document-Recognition-", "id-document-sdk", "recognition-"),
    ("FaceRecognition-LivenessDetection-", "face-sdk", ""),
    ("FaceLivenessDetection-", "face-sdk", "liveness-"),
    ("FaceRecognition-", "face-sdk", "recognition-"),
)
APP_SUFFIX_PLATFORM = {
    "Android": "Android",
    "iOS": "iOS",
    "Flutter": "Flutter",
    "React-Native": "ReactNative",
    "Ionic-Capacitor": "Ionic",
    "Ionic-Cordova": "Ionic-Cordova",
    "Windows": "Windows",
    "Docker": "Linux",
}
APP_SUFFIX_LEAF = {
    "Android": "android",
    "iOS": "ios",
    "Flutter": "flutter",
    "React-Native": "react-native",
    "Ionic-Capacitor": "ionic-capacitor",
    "Ionic-Cordova": "ionic-cordova",
    "Windows": "windows",
    "Docker": "linux-docker",
}


def app_doc_rel(name: str) -> tuple[str, str] | None:
    """Return (docs rel, platform label) for an app repository folder."""
    for prefix, section, leaf_prefix in APP_DOC_PREFIXES:
        if name.startswith(prefix):
            suffix = name[len(prefix) :]
            leaf = APP_SUFFIX_LEAF.get(suffix)
            plat = APP_SUFFIX_PLATFORM.get(suffix)
            if not leaf or not plat:
                return None
            return f"{section}/{leaf_prefix}{leaf}", plat
    return None


def write_missing_app_pages(owner: str) -> int:
    """Write a developer page for every app folder that does not have one yet."""
    apps = REPOS_DIR / "APPs"
    written = 0
    for path in sorted(apps.iterdir()):
        if not path.is_dir() or path.name.startswith("_") or path.name.startswith("."):
            continue
        mapped = app_doc_rel(path.name)
        if mapped is None:
            continue
        rel, plat = mapped
        if out_path_for(rel).is_file():
            continue
        item = {
            "name": path.name,
            "description": path.name.replace("-", " "),
            "homepage": f"{DOCS_BASE}/developers/{rel}",
        }
        build_product_page(owner, item, rel, {path.name: {"platform": plat}})
        print(f"PAGE {path.name} -> {rel}")
        written += 1
    return written


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
    readme_path = (REPOS_DIR / "APPs" / name) / "README.md"
    readme_body = ""
    if readme_path.is_file():
        raw = rewrite_links(readme_path.read_text(encoding="utf-8", errors="replace"), owner)
        readme_body = strip_readme_noise(raw)
    body = C.build_page_body(ctx, readme_body)
    out = out_path_for(rel)
    write_page(out, title, desc, body)
    return out


def write_integration_guides() -> None:
    """Top-level integration guides for Face and Document products."""
    write_page(
        OUT / "face-sdk" / "integration-guide.md",
        "Face SDK — Integration guide",
        "How to start a Face project, download runtime, place databases, and call every API.",
        """
This is the **full Face SDK integration path**. Open the platform page for your stack after you finish these steps.

## 1. Choose a product

| Goal | Product line | Example repos |
| --- | --- | --- |
| Recognition and liveness | Face Recognition & Liveness Detection | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14103**. |
| Recognition | Face Recognition | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14104**. These builds do not return a liveness score. |
| Liveness | Face Liveness Detection | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14105**. These builds do not enroll a gallery or run 1:N search. |

## 2. Clone and download the runtime

```bash
git clone https://github.com/identixia-IDV/<PRODUCT>.git
cd <PRODUCT>
python scripts/get_runtime.py
```

Pin a tag when you need a fixed build:

```bash
python scripts/get_runtime.py --tag 1.0.0
```

| Channel | Where files land |
| --- | --- |
| Android | `libfacesdk/*.aar` + `libfacesdk/databases/*.xdb` |
| iOS | Frameworks at repo root / `Frameworks/` + `databases/*.xdb` |
| Flutter / RN / Ionic | Sample Android + iOS paths (see that platform page) |
| Windows / Linux | `lib/cpu/` (binaries **and** every `recognition*.xdb`) |

{% hint style="warning" %}
Never ship the engine without database packs. Missing `*.xdb` files cause empty OCR / liveness / match results even when activate returns success.
{% endhint %}

## 3. Run the sample

* **Mobile:** Android Studio / Xcode / `flutter run` / `yarn android` / Ionic — wait for **Ready**.
* **Server:** `pip install -r requirements.txt` → `python run_server.py` / `python3 run_server.py` → `GET /api/health`.

## 4. Activate

* **Mobile:** demo key is bound to the sample application / bundle id. Your app needs a new key.
* **Server:** `GET /api/machinecode` → contact Identixia → `POST /api/activate` or set `LICENSE=` in `.env`.

## 5. Call the APIs

| Surface | Where to look |
| --- | --- |
| Mobile methods | Platform pages under [Reference](reference.md) (lifecycle, detect, match, liveness, gallery, VideoWorker) |
| HTTP endpoints | [SDK Server — Face Recognition](../sdk-server/face-recognition.md) and [Face Liveness](../sdk-server/face-liveness.md) |

## 6. Resources

* Releases: each product’s GitHub **Releases** page
* Postman: monorepo `postman/Identixia-API.postman_collection.json`
* Docs site: [docs.identixia.com](https://docs.identixia.com)
* License: [Request a license](../request-a-license-and-support.md)

Next: open your platform page (for example [Android](android.md) or [Windows](windows.md)).
""".strip()
        + "\n",
    )
    write_page(
        OUT / "id-document-sdk" / "integration-guide.md",
        "ID Document SDK — Integration guide",
        "How to start a Document project, download runtime, place document.xdb, and call every API.",
        """
This is the **full ID Document SDK integration path**. Open the platform page for your stack after you finish these steps.

## 1. Choose a product

| Goal | Product line | Example repos |
| --- | --- | --- |
| Recognition and authenticity | ID Document Recognition & Liveness Detection | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14102**. |
| Recognition | ID Document Recognition | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14106**. This build does not serve `/api/document/liveness`. |
| Authenticity | ID Document Liveness Detection | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14107**. It does not read MRZ, barcodes, or visual fields, and it does not expose `/api/document/process`. |

## 2. Clone and download the runtime

```bash
git clone https://github.com/identixia-IDV/<PRODUCT>.git
cd <PRODUCT>
python scripts/get_runtime.py
```

| Channel | Where files land |
| --- | --- |
| Android | `libdocsdk/documentreadersdk.aar` (`document.xdb` embedded) |
| iOS | `docsdk.xcframework` / `docsdk.framework` (`document.xdb` in the bundle) |
| Flutter / RN / Ionic | Sample Android + iOS paths (see that platform page) |
| Windows / Linux | `lib/cpu/` with `document.xdb` at the top level |

## 3. Run the sample

* **Mobile:** open Camera / Gallery after status shows **Ready**. Result is one scroll (identity, fields, checks, images).
* **Server:** start the HTTP API, then call `/api/document/process` or `/api/document/liveness`.

## 4. Activate

Same pattern as Face: mobile demo id vs your application id; server machine code → license → activate.

## 5. Call the APIs

| Surface | Where to look |
| --- | --- |
| Mobile methods | Platform pages (`setActivation`, `init`, `recognize`, `documentProcess`, locate / liveness) |
| HTTP endpoints | [SDK Server — Document Recognition](../sdk-server/document-recognition.md) · [Document Liveness](../sdk-server/document-liveness.md) |
| Result JSON | [Result Format](result-json.md) · [Security check fields](security-fields.md) |

## 6. Resources

* Releases: product GitHub **Releases**
* Postman: monorepo `postman/Identixia-API.postman_collection.json`
* License: [Request a license](../request-a-license-and-support.md)

Next: open your platform page (for example [Android](android.md) or [Windows](windows.md)).
""".strip()
        + "\n",
    )


def write_face_hub() -> None:
    """Introduction page for Face Recognition & Liveness Detection (FaceOnLive-style)."""
    body = f"""
On-premises Face Recognition and Face Liveness Detection (anti-spoofing) SDKs.

The algorithm runs in real time on phones and servers. It supports accurate **1:1** and **1:N** matching, **passive face liveness**, and face attributes (age, gender, mask/sunglasses, landmarks).

Use it for identity verification and attendance. Processing stays on **your** device or server.

We provide SDKs for **Android**, **iOS**, **Flutter**, **React Native**, **Ionic**, **Windows**, and **Linux / Docker**.

| Function | What you get | License flag |
| --- | --- | --- |
| **Recognition** | Detect, attributes, quality, templates, 1:1, 1:N | `recognition` |
| **Liveness** | Passive presentation-attack score | `liveness` |

## What you get

| Capability | Description |
| --- | --- |
| Face detection | Bounding box, landmarks, and pose |
| Attributes | Age, gender, and related traits when enabled |
| Quality | ICAO-style image and face quality scores |
| Templates | Numerical representations of faces that you store in **your** database |
| 1:1 match | Compare two images or two templates |
| 1:N identify | Save templates in a gallery, then search for the closest match |
| Passive liveness + deepfake | Presentation-attack and deepfake checks when the license includes `liveness`. Report REAL only when both pass |

A missing liveness score means the check was not evaluated. It does not mean the face passed.

## What you need

| Requirement | Detail |
| --- | --- |
| License | `recognition` for detect, template, and match. Add `liveness` for the presentation-attack and deepfake scores |
| Runtime | From the product repository, run `python scripts/get_runtime.py` |
| Databases | `recognition.xdb`, `recognition-common.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb`. When liveness is licensed, also `recognition-liveness.xdb` and `recognition-deepfake.xdb` |
| Gallery | You keep the enrolled templates. The SDK does not upload faces |

If a database pack is missing, activate can succeed and recognition or liveness still fails at runtime.

## Samples

These repositories include recognition and liveness. Server port **14103**. Gradio, when the image ships it, uses **14203**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`FaceRecognition-LivenessDetection-Android`]({GH}/FaceRecognition-LivenessDetection-Android) |
| iOS | [iOS](ios.md) | [`FaceRecognition-LivenessDetection-iOS`]({GH}/FaceRecognition-LivenessDetection-iOS) |
| Flutter | [Flutter](flutter.md) | [`FaceRecognition-LivenessDetection-Flutter`]({GH}/FaceRecognition-LivenessDetection-Flutter) |
| React Native | [React Native](react-native.md) | [`FaceRecognition-LivenessDetection-React-Native`]({GH}/FaceRecognition-LivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`]({GH}/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`FaceRecognition-LivenessDetection-Ionic-Cordova`]({GH}/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`FaceRecognition-LivenessDetection-Windows`]({GH}/FaceRecognition-LivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`FaceRecognition-LivenessDetection-Docker`]({GH}/FaceRecognition-LivenessDetection-Docker) |

Other licenses use different repositories. [Choose a product](https://docs.identixia.com/guides/choose-a-product) lists them.

## Try it

1. Clone one repository above.
2. Run `python scripts/get_runtime.py`.
3. Follow [Run the sample](https://docs.identixia.com/guides/run-the-sample) until the sample shows **Ready**.
4. On Windows or Docker, call the HTTP API on port **14103**. See [SDK Server](../sdk-server/README.md).

<figure><img src="../.gitbook/assets/face-android-home.png" alt="Face SDK Android home" width="160"><figcaption>Android demo home</figcaption></figure>

## Next

* [Recognition](recognition.md) — detect, template, 1:1, and 1:N
* [Liveness](liveness.md) — presentation-attack and deepfake scores

{{% hint style="info" %}}
Biometric images and templates stay on **your** device or server. Identixia does not host them.
{{% endhint %}}
""".strip()
    write_page(
        OUT / "face-sdk" / "README.md",
        "Introduction",
        "On-premises Face Recognition and Face Liveness Detection SDKs.",
        body + "\n",
    )
    write_page(
        OUT / "face-sdk" / "reference.md",
        "Reference",
        "Documentation for Face Recognition and Face Liveness Detection SDKs by platform.",
        f"""
Documentation for Face Recognition and Face Liveness Detection SDKs.

We provide SDKs for all platforms. Sample projects are on GitHub: [{GH.replace('https://github.com/', '')}]({GH}).

## Quick start

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`FaceRecognition-LivenessDetection-Android`]({GH}/FaceRecognition-LivenessDetection-Android) |
| iOS | [iOS](ios.md) | [`FaceRecognition-LivenessDetection-iOS`]({GH}/FaceRecognition-LivenessDetection-iOS) |
| Flutter | [Flutter](flutter.md) | [`FaceRecognition-LivenessDetection-Flutter`]({GH}/FaceRecognition-LivenessDetection-Flutter) |
| React Native | [React Native](react-native.md) | [`FaceRecognition-LivenessDetection-React-Native`]({GH}/FaceRecognition-LivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`]({GH}/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`FaceRecognition-LivenessDetection-Ionic-Cordova`]({GH}/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`FaceRecognition-LivenessDetection-Windows`]({GH}/FaceRecognition-LivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`FaceRecognition-LivenessDetection-Docker`]({GH}/FaceRecognition-LivenessDetection-Docker) |

## Face Recognition

These builds do not return a liveness score. Server port **14104**.

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Face Recognition (Android)](recognition-android.md) | [`FaceRecognition-Android`]({GH}/FaceRecognition-Android) |
| iOS | [Face Recognition (iOS)](recognition-ios.md) | [`FaceRecognition-iOS`]({GH}/FaceRecognition-iOS) |
| Flutter | [Face Recognition (Flutter)](recognition-flutter.md) | [`FaceRecognition-Flutter`]({GH}/FaceRecognition-Flutter) |
| React Native | [Face Recognition (React Native)](recognition-react-native.md) | [`FaceRecognition-React-Native`]({GH}/FaceRecognition-React-Native) |
| Ionic Capacitor | [Face Recognition (Ionic Capacitor)](recognition-ionic-capacitor.md) | [`FaceRecognition-Ionic-Capacitor`]({GH}/FaceRecognition-Ionic-Capacitor) |
| Ionic Cordova | [Face Recognition (Ionic Cordova)](recognition-ionic-cordova.md) | [`FaceRecognition-Ionic-Cordova`]({GH}/FaceRecognition-Ionic-Cordova) |
| Windows | [Face Recognition (Windows)](recognition-windows.md) | [`FaceRecognition-Windows`]({GH}/FaceRecognition-Windows) |
| Linux / Docker | [Face Recognition (Linux / Docker)](recognition-linux-docker.md) | [`FaceRecognition-Docker`]({GH}/FaceRecognition-Docker) |

## Face Liveness Detection

These builds score presentation attacks. They do not enroll a gallery or run 1:N search. Server port **14105**.

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Face Liveness (Android)](liveness-android.md) | [`FaceLivenessDetection-Android`]({GH}/FaceLivenessDetection-Android) |
| iOS | [Face Liveness (iOS)](liveness-ios.md) | [`FaceLivenessDetection-iOS`]({GH}/FaceLivenessDetection-iOS) |
| Flutter | [Flutter](liveness-flutter.md) | [`FaceLivenessDetection-Flutter`]({GH}/FaceLivenessDetection-Flutter) |
| React Native | [React Native](liveness-react-native.md) | [`FaceLivenessDetection-React-Native`]({GH}/FaceLivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](liveness-ionic-capacitor.md) | [`FaceLivenessDetection-Ionic-Capacitor`]({GH}/FaceLivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](liveness-ionic-cordova.md) | [`FaceLivenessDetection-Ionic-Cordova`]({GH}/FaceLivenessDetection-Ionic-Cordova) |
| Windows | [Face Liveness (Windows)](liveness-windows.md) | [`FaceLivenessDetection-Windows`]({GH}/FaceLivenessDetection-Windows) |
| Linux / Docker | [Face Liveness (Linux / Docker)](liveness-linux-docker.md) | [`FaceLivenessDetection-Docker`]({GH}/FaceLivenessDetection-Docker) |

HTTP APIs: [SDK Server](../sdk-server/).
""".strip()
        + "\n",
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

Recognition and liveness together. Server port **14103**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`FaceRecognition-LivenessDetection-Android`]({GH}/FaceRecognition-LivenessDetection-Android) |
| iOS | [iOS](ios.md) | [`FaceRecognition-LivenessDetection-iOS`]({GH}/FaceRecognition-LivenessDetection-iOS) |
| Flutter | [Flutter](flutter.md) | [`FaceRecognition-LivenessDetection-Flutter`]({GH}/FaceRecognition-LivenessDetection-Flutter) |
| React Native | [React Native](react-native.md) | [`FaceRecognition-LivenessDetection-React-Native`]({GH}/FaceRecognition-LivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`]({GH}/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`FaceRecognition-LivenessDetection-Ionic-Cordova`]({GH}/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`FaceRecognition-LivenessDetection-Windows`]({GH}/FaceRecognition-LivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`FaceRecognition-LivenessDetection-Docker`]({GH}/FaceRecognition-LivenessDetection-Docker) |

Recognition without a liveness score. Server port **14104**. Do not call `/api/face/liveness` on this build.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](recognition-android.md) | [`FaceRecognition-Android`]({GH}/FaceRecognition-Android) |
| iOS | [iOS](recognition-ios.md) | [`FaceRecognition-iOS`]({GH}/FaceRecognition-iOS) |
| Flutter | [Flutter](recognition-flutter.md) | [`FaceRecognition-Flutter`]({GH}/FaceRecognition-Flutter) |
| React Native | [React Native](recognition-react-native.md) | [`FaceRecognition-React-Native`]({GH}/FaceRecognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](recognition-ionic-capacitor.md) | [`FaceRecognition-Ionic-Capacitor`]({GH}/FaceRecognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](recognition-ionic-cordova.md) | [`FaceRecognition-Ionic-Cordova`]({GH}/FaceRecognition-Ionic-Cordova) |
| Windows | [Windows](recognition-windows.md) | [`FaceRecognition-Windows`]({GH}/FaceRecognition-Windows) |
| Linux / Docker | [Linux / Docker](recognition-linux-docker.md) | [`FaceRecognition-Docker`]({GH}/FaceRecognition-Docker) |

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

Presentation-attack and deepfake checks. Report REAL only when both pass. These builds do not enroll a gallery and do not run 1:N search. Server port **14105**. The routes are `POST /api/face/liveness` and `POST /api/face/deepfake`.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](liveness-android.md) | [`FaceLivenessDetection-Android`]({GH}/FaceLivenessDetection-Android) |
| iOS | [iOS](liveness-ios.md) | [`FaceLivenessDetection-iOS`]({GH}/FaceLivenessDetection-iOS) |
| Flutter | [Flutter](liveness-flutter.md) | [`FaceLivenessDetection-Flutter`]({GH}/FaceLivenessDetection-Flutter) |
| React Native | [React Native](liveness-react-native.md) | [`FaceLivenessDetection-React-Native`]({GH}/FaceLivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](liveness-ionic-capacitor.md) | [`FaceLivenessDetection-Ionic-Capacitor`]({GH}/FaceLivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](liveness-ionic-cordova.md) | [`FaceLivenessDetection-Ionic-Cordova`]({GH}/FaceLivenessDetection-Ionic-Cordova) |
| Windows | [Windows](liveness-windows.md) | [`FaceLivenessDetection-Windows`]({GH}/FaceLivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](liveness-linux-docker.md) | [`FaceLivenessDetection-Docker`]({GH}/FaceLivenessDetection-Docker) |

Recognition and liveness in one sample use the repositories on [Face SDK](README.md). That server listens on port **14103** and uses the same `/api/face/liveness` path.

Hub pack: [`Face-Liveness-Detection-SDK`]({GH}/Face-Liveness-Detection-SDK)

## Server example

Default Face API port is **14103** (confirm in the product README).

```bash
# Full / recognition+liveness Docker stack
curl -s -X POST http://127.0.0.1:14103/api/face/liveness \\
  -H "Content-Type: application/json" \\
  -d '{{"image":"BASE64_JPEG"}}'
```

Liveness-only Docker uses the same `/api/face/liveness` path on port **14105** — see [Linux / Docker (liveness only)](liveness-linux-docker.md).

## Mobile tip

Run activate → init → liveness on a **background** thread. Keep the camera preview on the UI thread. If VideoWorker / tracking is used, start it when the camera screen appears and stop it when the screen closes.

<figure><img src="../.gitbook/assets/liveness-mobile.png" alt="Mobile liveness" width="200"><figcaption>Mobile liveness result</figcaption></figure>
""".strip()
        + "\n",
    )


def write_document_hub() -> None:
    """Introduction page for ID Document Recognition & Liveness Detection (FaceOnLive-style)."""
    body = f"""
On-premises ID Document Recognition and Document Liveness (authenticity) SDKs.

Read passports, national IDs, and driver licenses on **your** device or server: OCR / MRZ / barcode fields, cropped images, and optional anti-spoof authenticity checks.

We provide SDKs for **Android**, **iOS**, **Flutter**, **React Native**, **Ionic**, **Windows**, and **Linux / Docker**.

| Function | What you get | License flag |
| --- | --- | --- |
| **Recognition** | Locate, OCR, MRZ, barcode, cropped images | `recognition` |
| **Liveness / authenticity** | Screen / printout / substitution checks | `authenticity` |

## What you get

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Printed fields such as the name, document number, and dates |
| MRZ | Machine-readable zone, including check digits |
| Barcode / QR | Extracted when the document has one |
| Front and back | Both sides when the workflow requires them |
| Document authenticity | Screen, printout, and substitution checks when the license includes `authenticity` |
| Result JSON | `identity`, `readings`, `tests`, `images`, and `session`. Parse this object. Do not scrape the Result screen |

Authenticity is rows in `tests` with `group: "authenticity"`. An empty set is not a pass. See [Result format](result-json.md) and [Security checks](security-fields.md).

## What you need

| Requirement | Detail |
| --- | --- |
| License | `recognition` for OCR, MRZ, and barcode. Add `authenticity` for the security checks |
| Runtime | From the product repository, run `python scripts/get_runtime.py` |
| Database | `document.xdb`. On Android it is embedded in the AAR. On Windows and Linux it sits at the top of `lib/cpu/` |
| Capture | A physical device for camera demos. Align the document in the guide and capture the back when the document has one |

If `document.xdb` is missing, activate can succeed and OCR still fails at runtime.

## Samples

These repositories include recognition and document liveness. Server port **14102**. Gradio, when the image ships it, uses **14202**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`ID-Document-Recognition-Liveness-Detection-Android`]({GH}/ID-Document-Recognition-Liveness-Detection-Android) |
| iOS | [iOS](ios.md) | [`ID-Document-Recognition-Liveness-Detection-iOS`]({GH}/ID-Document-Recognition-Liveness-Detection-iOS) |
| Flutter | [Flutter](flutter.md) | [`ID-Document-Recognition-Liveness-Detection-Flutter`]({GH}/ID-Document-Recognition-Liveness-Detection-Flutter) |
| React Native | [React Native](react-native.md) | [`ID-Document-Recognition-Liveness-Detection-React-Native`]({GH}/ID-Document-Recognition-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`ID-Document-Recognition-Liveness-Detection-Windows`]({GH}/ID-Document-Recognition-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`ID-Document-Recognition-Liveness-Detection-Docker`]({GH}/ID-Document-Recognition-Liveness-Detection-Docker) |

Other licenses use different repositories. [Choose a product](https://docs.identixia.com/guides/choose-a-product) lists them.

## Try it

1. Clone one repository above.
2. Run `python scripts/get_runtime.py`.
3. Follow [Run the sample](https://docs.identixia.com/guides/run-the-sample) until the sample shows **Ready**.
4. On Windows or Docker, call `POST /api/document/process` on port **14102**. See [SDK Server](../sdk-server/README.md).

<figure><img src="../.gitbook/assets/document-desktop-status.png" alt="Document demo status" width="480"><figcaption>Desktop demo — status</figcaption></figure>

## Next

* [Recognition](recognition.md) — OCR, MRZ, barcode, and crops
* [Liveness](liveness.md) — screen, printout, and substitution checks
* [Supported ID documents and countries](supported-documents.md)
* [Result format](result-json.md) · [Security checks](security-fields.md)

{{% hint style="info" %}}
Document images and OCR fields stay on **your** device or server. Parse [Result Format](result-json.md) — do not scrape the Result UI.
{{% endhint %}}
""".strip()
    write_page(
        OUT / "id-document-sdk" / "README.md",
        "Introduction",
        "On-premises ID Document Recognition and Document Liveness SDKs.",
        body + "\n",
    )


def write_supported_documents() -> None:
    """ID document series page. Data is the customer catalog, not address documents."""
    import json

    data_path = Path(__file__).resolve().parent / "data" / "supported-id-documents.json"
    if not data_path.is_file():
        print(f"SKIP supported documents: missing {data_path.name}")
        return
    data = json.loads(data_path.read_text(encoding="utf-8"))
    listed = data["listed"]
    total = data["catalog_total"]
    countries_total = data["countries_total"]
    family_rows = "\n".join(
        f"| {item['name']} | {item['count']} |" for item in data["families"]
    )
    letters = []
    blocks = ["## Document families", "", "| Document family | Templates |", "| --- | ---: |", family_rows, ""]
    current = None
    for country in data["countries"]:
        name = country["name"]
        letter = name[0].upper()
        if letter != current:
            current = letter
            letters.append(letter)
            blocks.append(f"## {letter}")
            blocks.append("")
        blocks.append(f"**{name}**")
        blocks.append("")
        for doc in country["documents"]:
            blocks.append(f"- {doc}")
        blocks.append("")
    jump = " ".join(f"[{letter}](#{letter.lower()})" for letter in letters)
    body = "\n".join(
        [
            f"The ID document recognition catalog contains **{total:,}** templates for **{countries_total}** issuing countries and authorities. This page lists **{listed:,}** templates from the most common document families. Proof of address is not included.",
            "",
            "Each line is one template: the document series, and the back side or an extra page when the catalog stores that side separately.",
            "",
            jump,
            "",
            *blocks,
        ]
    )
    write_page(
        OUT / "id-document-sdk" / "supported-documents.md",
        "Supported ID documents and countries",
        f"Identity document templates for {countries_total} issuing countries. {listed:,} templates from the most common document families in the ID document recognition catalog.",
        body,
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

Issuing countries and document series are listed in [Supported ID documents and countries](supported-documents.md).

## Capture tips

* Prefer a **physical** device for camera demos.
* Align the document inside the guide; capture front (and back when required).
* On mobile, call locate → capture → `recognize` on a **background** thread.

## Server routes

The full product listens on **14102**. Recognition only listens on **14106** and does not serve `/api/document/liveness`.

| Route | Role | Which build |
| --- | --- | --- |
| `POST /api/document/process` | OCR, MRZ, barcode, and authenticity when that license flag is on | Full product and recognition only |
| `POST /api/document/recognition` | OCR / MRZ / barcode only | Full product and recognition only |
| `POST /api/document/liveness` | Authenticity only | Full product and liveness only (port **14107**) |

```bash
curl -s -X POST http://127.0.0.1:14106/api/document/recognition \\
  -H "Content-Type: application/json" \\
  -d '{{"images":[{{"image":"BASE64_FRONT","page_idx":0}},{{"image":"BASE64_BACK","page_idx":1}}]}}'
```

Response shape: [Result JSON](result-json.md).

## Repositories

Recognition and document liveness together. Server port **14102**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`ID-Document-Recognition-Liveness-Detection-Android`]({GH}/ID-Document-Recognition-Liveness-Detection-Android) |
| iOS | [iOS](ios.md) | [`ID-Document-Recognition-Liveness-Detection-iOS`]({GH}/ID-Document-Recognition-Liveness-Detection-iOS) |
| Flutter | [Flutter](flutter.md) | [`ID-Document-Recognition-Liveness-Detection-Flutter`]({GH}/ID-Document-Recognition-Liveness-Detection-Flutter) |
| React Native | [React Native](react-native.md) | [`ID-Document-Recognition-Liveness-Detection-React-Native`]({GH}/ID-Document-Recognition-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`ID-Document-Recognition-Liveness-Detection-Windows`]({GH}/ID-Document-Recognition-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`ID-Document-Recognition-Liveness-Detection-Docker`]({GH}/ID-Document-Recognition-Liveness-Detection-Docker) |

Recognition without document liveness. Server port **14106**. This build does not serve `/api/document/liveness`.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](recognition-android.md) | [`ID-Document-Recognition-Android`]({GH}/ID-Document-Recognition-Android) |
| iOS | [iOS](recognition-ios.md) | [`ID-Document-Recognition-iOS`]({GH}/ID-Document-Recognition-iOS) |
| Flutter | [Flutter](recognition-flutter.md) | [`ID-Document-Recognition-Flutter`]({GH}/ID-Document-Recognition-Flutter) |
| React Native | [React Native](recognition-react-native.md) | [`ID-Document-Recognition-React-Native`]({GH}/ID-Document-Recognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](recognition-ionic-capacitor.md) | [`ID-Document-Recognition-Ionic-Capacitor`]({GH}/ID-Document-Recognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](recognition-ionic-cordova.md) | [`ID-Document-Recognition-Ionic-Cordova`]({GH}/ID-Document-Recognition-Ionic-Cordova) |
| Windows | [Windows](recognition-windows.md) | [`ID-Document-Recognition-Windows`]({GH}/ID-Document-Recognition-Windows) |
| Linux / Docker | [Linux / Docker](recognition-linux-docker.md) | [`ID-Document-Recognition-Docker`]({GH}/ID-Document-Recognition-Docker) |

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

Authenticity only. The sample does not read MRZ, barcodes, or visual fields. Server port **14107**. `POST /api/document/liveness` takes `images` entries `{{image, page_idx}}`. This server does not expose `/api/document/process`.

| Platform | Port | Where to start | Repository |
| --- | ---: | --- | --- |
| Android | — | Repository README | [`ID-Document-Liveness-Detection-Android`]({GH}/ID-Document-Liveness-Detection-Android) |
| iOS | — | Repository README | [`ID-Document-Liveness-Detection-iOS`]({GH}/ID-Document-Liveness-Detection-iOS) |
| Flutter | — | Repository README | [`ID-Document-Liveness-Detection-Flutter`]({GH}/ID-Document-Liveness-Detection-Flutter) |
| React Native | — | Repository README | [`ID-Document-Liveness-Detection-React-Native`]({GH}/ID-Document-Liveness-Detection-React-Native) |
| Ionic Capacitor | — | Repository README | [`ID-Document-Liveness-Detection-Ionic-Capacitor`]({GH}/ID-Document-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | — | Repository README | [`ID-Document-Liveness-Detection-Ionic-Cordova`]({GH}/ID-Document-Liveness-Detection-Ionic-Cordova) |
| Windows | 14107 | Repository README | [`ID-Document-Liveness-Detection-Windows`]({GH}/ID-Document-Liveness-Detection-Windows) |
| Linux / Docker | 14107 | [Linux / Docker](liveness-linux-docker.md) | [`ID-Document-Liveness-Detection-Docker`]({GH}/ID-Document-Liveness-Detection-Docker) |

Recognition and authenticity in one sample use the repositories on [ID Document SDK](README.md). That server listens on port **14102**.

### Example — authenticity-only (full server)

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/liveness \\
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

Mobile `recognize` and server `POST /api/document/process` (also recognition / liveness routes) return one **customer process JSON**. Parse this object in your app — do not scrape the demo Result UI.

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

Server routes: `POST /api/document/liveness` (authenticity only) or `POST /api/document/process` (OCR + authenticity when licensed).
""".strip()
        + "\n",
    )


def write_idv_pages() -> None:
    write_page(
        OUT / "idv" / "README.md",
        "IDV: Self-Host KYC Platform",
        "IDV is Identixia's self-host web & mobile KYC platform. It uses SDK Server as the biometric backend.",
        f"""
**IDV** is Identixia's open web & mobile KYC platform. It uses [SDK Server](../sdk-server/) (Face + Document HTTP engines) as the biometric backend.

It does not replace those SDKs — it orchestrates them between your company systems and applicant capture apps.

## Project components

| Component | Role | Folder · port |
| --- | --- | --- |
| **Platform (Admin)** | Tenant API, reviews, Identity Console | `IDV_server/` · `:14187` · UI `:14188` / `/admin` |
| **Company (Merchant)** | Holds service credentials; starts sessions | `company/backend/` · `:14195` · Admin `:14189` |
| **Applicant (User)** | Web / mobile capture apps | `client/` · e.g. web `:5175` |
| **Engines** | Document + Face HTTP APIs | Document `:14102` · Face `:14103` |

```text
Applicant app ──► Company backend :14195 ──► IDV server :14187 ──► Face / Document engines
                      │                         │
               Company Admin :14189      Identity Console /admin
```

## Guide (in order)

1. [Project structure](project-structure.md)
2. [Project setup](environment.md) — `.env`, tokens, storage
3. [Initial setup process](initial-setup.md)
4. [Understanding session states](session-states.md)
5. [iOS & Android](components-clients.md) (and web demos)
6. [Creating a session (API)](api.md)
7. [Webhook integration](company-webhooks.md)
8. [Quick start](quick-start.md) · [Walkthrough](walkthrough.md)
9. [Production](production.md) · [Reference](reference.md)

<figure><img src="../.gitbook/assets/idv-audit-console.png" alt="Identity Console" width="520"><figcaption>Identity Console</figcaption></figure>

{{% hint style="danger" %}}
**Safety:** Keep the company **service bearer** on the company backend only. Capture apps receive a short-lived **capture token**. Never commit secrets. `IDV_OPEN_API=1` / bearer `demo` is for **localhost demos only**.
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
| Tenant policy, sessions, reviews, API auth | `IDV_server` |
| Holding service tokens, starting sessions for apps | **Your** backend (sample: `company/backend`) |
| Hybrid entitlement metering on customer host | `license/license_v2` (issuer) / server copy in `IDV_server` |
| Issuing Hybrid licences | `license` (Identixia) |

## Decision rule

Trust aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing or error signals never auto-accept (`IDV_server/idv/decision/`).
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
3. Run `python IDV/IDV_server (then company)` **or** start services manually below
4. [Initial setup process](initial-setup.md) — console, company settings, webhook
5. [End-to-end walkthrough](walkthrough.md)

## Helper (recommended)

```bash
# Engines must already be healthy on :14102 and :14103
python IDV/IDV_server (then company)
```

Preflight checks engine health, starts IDV server + company backend, and prints URLs. It does **not** start License Admin and does **not** mean the stack is production-ready when `IDV_OPEN_API=1`.

## Storage defaults

| Project | Default SQLite |
| --- | --- |
| `IDV_server` | `IDV_server/database/idv.sqlite` (or `IDV_SQLITE_PATH`) |
| `company/backend` | `company/backend/database/company.sqlite` |
| `license` | `license/database/` |

PostgreSQL / media / Valkey / RabbitMQ: `python IDV/Install_db/setup_database.py` from `IDV/Install_db/`. See [Project setup](environment.md).

## Manual commands

```bash
# Platform (localhost demo auth only)
cd IDV/IDV_server && python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
# → http://127.0.0.1:14187/v1  and  /admin/

# Identity Console (develop)
cd IDV/IDV_console && npm install && npm run dev
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
cd IDV/license && pip install -r requirements.txt
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
| Document Reader | `http://127.0.0.1:14102` | `/api/document/process`, `/api/document/recognition`, `/api/document/liveness` |
| Face Recognition + liveness | `http://127.0.0.1:14103` | `/api/face/compare`, `/api/face/boxes`, `/api/face/template`, `/api/face/score`, `/api/face/liveness` |

Child pages: [Document engine](engines-document.md) · [Face engine](engines-face.md).

Same process APIs as [ID Document SDK](../id-document-sdk/) and [Face SDK](../face-sdk/). Document responses follow [Result JSON](../id-document-sdk/result-json.md).

## Numbered setup

1. Run the Document server (Windows or Docker) on **14102** — see [ID Document SDK → Server](../id-document-sdk/full-server.md).
2. Run the Face server on **14103** — see [Face SDK → Server](../face-sdk/full-server.md).
3. Activate each engine with **its** machine code (`GET /api/machinecode` → send to Identixia → set `LICENSE=` in `.env` or `POST /api/activate`). Docker and bare metal codes differ.
4. Confirm health:

```bash
curl -s http://127.0.0.1:14102/api/health
curl -s http://127.0.0.1:14103/api/health
```

5. Set `IDV_ENGINES=http`, `DOCUMENT_API_URL`, and `FACE_API_URL` in `IDV_server/.env` (see [Project setup](environment.md)).
6. Continue with [Initial setup process](initial-setup.md) or `python IDV/IDV_server (then company)`.

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
| `IDV_server/` | Platform API + workers (`:14187`) | [Platform server](platform-server.md) |
| `IDV_console/` | Identity Console (`:14188` / `/admin`) | [Identity Console](platform-console.md) |
| `company/backend/` | Sample **company server** (`:14195`) | [Company backend](company-backend.md) |
| `company/admin/` | Company operator UI (`:14189`) | [Company Admin](company-admin.md) |
| `license/` | Hybrid issuer + brand (`:14190`) | [License Admin](license-admin.md) |
| `app/` | Applicant SDKs + demos | [Applicant clients](components-clients.md) |
| `packages/` | Shared UI / decision / licence libs | [Shared packages](shared-packages.md) |
| `license/license_v2/` | Shared Hybrid protocol | [Hybrid protocol](license-protocol.md) |
| `docs/` | Offline handbook + API notes | [Reference](reference.md) |

## Brand

Brand files live in [`identixia-assets`](https://github.com/identixia-IDV/identixia-assets) under `brand/`.

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
{% hint style="warning" %}
Demo keys work only with the demo application id. A production key must match the id or machine code you send.
{% endhint %}

## Mobile SDK (Face / Document)

{% stepper %}
{% step %}
### Build with your id
Use your applicationId or bundle id, not the demo id.
{% endstep %}
{% step %}
### Send the id
Contact Identixia with that id and the product: Face recognition, Face liveness, Document recognition, or Document authenticity.
{% endstep %}
{% step %}
### Activate
Call activate, then init, as shown on the platform page.
{% endstep %}
{% endstepper %}

## Server SDK (Windows / Linux / Docker)

{% stepper %}
{% step %}
### Start the API
Start the container or Windows service once.
{% endstep %}
{% step %}
### Copy the machine code
Call `GET /api/machinecode` and copy `data.machinecode`. Docker and bare-metal codes differ.
{% endstep %}
{% step %}
### Activate
Call `POST /api/activate`, or set `LICENSE=` in `.env` and restart. Confirm with `GET /api/licenseStatus`.
{% endstep %}
{% endstepper %}

## IDV

IDV uses Hybrid licensing via `license` and `license/license_v2`. The issuer UI listens on `:14190` (localhost). Company systems use `company/backend` (sample `:14195`) to hold the service token and start sessions — see [Company integration](idv/company.md).

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
{% hint style="info" %}
License requests and technical support are available 24/7.
{% endhint %}

{% include "./.gitbook/includes/contact.md" %}
""".strip()
        + "\n",
    )
    (OUT / ".gitbook" / "includes").mkdir(parents=True, exist_ok=True)
    (OUT / ".gitbook" / "includes" / "contact.md").write_text(
        """<a href="mailto:contact@identixia.com" class="button primary" data-icon="envelope">contact@identixia.com</a>
<a href="https://wa.me/17018854218" class="button secondary" data-icon="comment">+1 (701) 885-4218</a>
<a href="https://t.me/identixia" class="button secondary" data-icon="paper-plane">@identixia</a>
""",
        encoding="utf-8",
        newline="\n",
    )
    (OUT / ".gitbook" / "includes" / "footer.md").write_text(
        C.FOOTER_MD,
        encoding="utf-8",
        newline="\n",
    )


def write_welcome() -> None:
    """Welcome page modeled on https://docs.faceonlive.com/ (company + product links)."""
    body = f"""
<p align="center"><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/brand/logo.png" alt="Identixia" width="280"></p>

{{% hint style="success" %}}
Face recognition, face liveness, and ID document capture run on **your** device or server. Identixia does not receive the images.
{{% endhint %}}

## Products

<table data-view="cards">
  <thead>
    <tr>
      <th>Product</th>
      <th data-card-target data-type="content-ref" data-hidden>Open</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Face</strong> — recognition and passive liveness.</td>
      <td><a href="face-sdk/README.md">Face SDK</a></td>
    </tr>
    <tr>
      <td><strong>ID documents</strong> — OCR, MRZ, barcode, and document liveness.</td>
      <td><a href="id-document-sdk/README.md">ID Document SDK</a></td>
    </tr>
    <tr>
      <td><strong>SDK Server</strong> — the same HTTP API on Windows and Docker.</td>
      <td><a href="sdk-server/README.md">SDK Server</a></td>
    </tr>
  </tbody>
</table>

## Start here

{{% stepper %}}
{{% step %}}
### See what the product does
Open Face or ID documents above. Each page lists what the product is for, what you need, and what a sample returns.
{{% endstep %}}
{{% step %}}
### Run the sample
Follow [Run the sample](https://docs.identixia.com/guides/run-the-sample). Android and iOS are separate setups. From the product clone, run `python scripts/get_runtime.py`.
{{% endstep %}}
{{% step %}}
### Request a license
Send the Android application ID, iOS bundle identifier, or server machine code on [Request a license](https://docs.identixia.com/guides/request-a-license-and-support). Activate that key before initializing the SDK.
{{% endstep %}}
{{% step %}}
### Contact
License requests and technical support: [Contact](https://docs.identixia.com/guides/contact-us).
{{% endstep %}}
{{% endstepper %}}

{{% hint style="warning" %}}
Native engines and `*.xdb` databases ship on GitHub Releases. From a product clone, run `python scripts/get_runtime.py`. They are not committed to git.
{{% endhint %}}
""".strip()
    write_page(
        OUT / "README.md",
        "Welcome to Identixia",
        "Identixia documentation for Face SDK, ID Document SDK, SDK Server, and IDV.",
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

Use these repositories when the license is **recognition only**. They detect faces, build templates, and run 1:1 and 1:N search. They do not return a liveness score. Phone, Windows, and Linux / Docker samples are listed on [Face recognition](recognition.md).

| Platform | Port | Docs | Repository |
| --- | ---: | --- | --- |
| Windows | 14104 | [Windows](recognition-windows.md) | [`FaceRecognition-Windows`]({GH}/FaceRecognition-Windows) |
| Linux / Docker | 14104 | [Linux / Docker](recognition-linux-docker.md) | [`FaceRecognition-Docker`]({GH}/FaceRecognition-Docker) |

Call `POST /api/face/analyze`, `/api/face/template`, `/api/face/compare` (`image1`, `image2`), `/api/face/enroll`, and `/api/face/search`. Do not call `/api/face/liveness` on this build.

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
        "Phone and cross-platform face liveness samples, without enroll or 1:N.",
        f"""
## Platforms

These builds score presentation attacks and deepfake checks. They do not enroll a gallery or run 1:N search.

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](liveness-android.md) | [`FaceLivenessDetection-Android`]({GH}/FaceLivenessDetection-Android) |
| iOS | [iOS](liveness-ios.md) | [`FaceLivenessDetection-iOS`]({GH}/FaceLivenessDetection-iOS) |
| Flutter | [Flutter](liveness-flutter.md) | [`FaceLivenessDetection-Flutter`]({GH}/FaceLivenessDetection-Flutter) |
| React Native | [React Native](liveness-react-native.md) | [`FaceLivenessDetection-React-Native`]({GH}/FaceLivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](liveness-ionic-capacitor.md) | [`FaceLivenessDetection-Ionic-Capacitor`]({GH}/FaceLivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](liveness-ionic-cordova.md) | [`FaceLivenessDetection-Ionic-Cordova`]({GH}/FaceLivenessDetection-Ionic-Cordova) |

## Integration path

1. Clone the sample and place the liveness runtime from GitHub Releases (`python scripts/get_runtime.py`).
2. Run until status shows **Ready**, then open the camera flow.
3. Activate with a license that includes `liveness`.
4. Treat a missing score as not evaluated, not as a pass.

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
| Windows | [Windows](liveness-windows.md) | [`FaceLivenessDetection-Windows`]({GH}/FaceLivenessDetection-Windows) | 14105 |
| Linux / Docker | [Linux / Docker](liveness-linux-docker.md) | [`FaceLivenessDetection-Docker`]({GH}/FaceLivenessDetection-Docker) | 14105 |

Process paths: `POST /api/face/liveness` and `POST /api/face/deepfake`. Control routes use the standard `{{success, code, message, request_id, data}}` envelope.

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
| `POST /api/document/process` | Full process (recognition + authenticity when licensed) |
| `POST /api/document/recognition` | OCR / MRZ / barcode only |
| `POST /api/document/liveness` | Authenticity only |

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

Use this line when the license is document authenticity only. The sample checks presentation attacks. It does not read MRZ, barcodes, or visual fields. Pair it with [Document recognition](recognition.md) when you also need the printed data.

| Platform | Port | Where to start | Repository |
| --- | ---: | --- | --- |
| Android | — | Repository README | [`ID-Document-Liveness-Detection-Android`]({GH}/ID-Document-Liveness-Detection-Android) |
| iOS | — | Repository README | [`ID-Document-Liveness-Detection-iOS`]({GH}/ID-Document-Liveness-Detection-iOS) |
| Flutter | — | Repository README | [`ID-Document-Liveness-Detection-Flutter`]({GH}/ID-Document-Liveness-Detection-Flutter) |
| React Native | — | Repository README | [`ID-Document-Liveness-Detection-React-Native`]({GH}/ID-Document-Liveness-Detection-React-Native) |
| Ionic Capacitor | — | Repository README | [`ID-Document-Liveness-Detection-Ionic-Capacitor`]({GH}/ID-Document-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | — | Repository README | [`ID-Document-Liveness-Detection-Ionic-Cordova`]({GH}/ID-Document-Liveness-Detection-Ionic-Cordova) |
| Windows | 14107 | Repository README | [`ID-Document-Liveness-Detection-Windows`]({GH}/ID-Document-Liveness-Detection-Windows) |
| Linux / Docker | 14107 | [Docker guide](liveness-linux-docker.md) | [`ID-Document-Liveness-Detection-Docker`]({GH}/ID-Document-Liveness-Detection-Docker) |

The HTTP call is `POST /api/document/liveness` with `images` entries `{{image, page_idx}}`. A liveness-only server does not expose `/api/document/process`.

Concept guide: [Document liveness](liveness.md). For OCR and authenticity in one build, use the [full product](full-product.md).
""",
    )
    hub(
        "id-document-sdk/reference.md",
        "Reference",
        "Documentation for ID Document Recognition and Document Liveness SDKs by platform.",
        f"""
Documentation for ID Document Recognition and Document Liveness SDKs.

We provide SDKs for all platforms. Sample projects are on GitHub: [{GH.replace("https://github.com/", "")}]({GH}).

## Quick start

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`ID-Document-Recognition-Liveness-Detection-Android`]({GH}/ID-Document-Recognition-Liveness-Detection-Android) |
| iOS | [iOS](ios.md) | [`ID-Document-Recognition-Liveness-Detection-iOS`]({GH}/ID-Document-Recognition-Liveness-Detection-iOS) |
| Flutter | [Flutter](flutter.md) | [`ID-Document-Recognition-Liveness-Detection-Flutter`]({GH}/ID-Document-Recognition-Liveness-Detection-Flutter) |
| React Native | [React Native](react-native.md) | [`ID-Document-Recognition-Liveness-Detection-React-Native`]({GH}/ID-Document-Recognition-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`]({GH}/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`ID-Document-Recognition-Liveness-Detection-Windows`]({GH}/ID-Document-Recognition-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`ID-Document-Recognition-Liveness-Detection-Docker`]({GH}/ID-Document-Recognition-Liveness-Detection-Docker) |

## ID Document Recognition

Linux / Docker and the phone and Windows samples. Server port **14106**. This build does not serve `/api/document/liveness`.

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](recognition-android.md) | [`ID-Document-Recognition-Android`]({GH}/ID-Document-Recognition-Android) |
| iOS | [iOS](recognition-ios.md) | [`ID-Document-Recognition-iOS`]({GH}/ID-Document-Recognition-iOS) |
| Flutter | [Flutter](recognition-flutter.md) | [`ID-Document-Recognition-Flutter`]({GH}/ID-Document-Recognition-Flutter) |
| React Native | [React Native](recognition-react-native.md) | [`ID-Document-Recognition-React-Native`]({GH}/ID-Document-Recognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](recognition-ionic-capacitor.md) | [`ID-Document-Recognition-Ionic-Capacitor`]({GH}/ID-Document-Recognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](recognition-ionic-cordova.md) | [`ID-Document-Recognition-Ionic-Cordova`]({GH}/ID-Document-Recognition-Ionic-Cordova) |
| Windows | [Windows](recognition-windows.md) | [`ID-Document-Recognition-Windows`]({GH}/ID-Document-Recognition-Windows) |
| Linux / Docker | [Linux / Docker](recognition-linux-docker.md) | [`ID-Document-Recognition-Docker`]({GH}/ID-Document-Recognition-Docker) |

## ID Document Liveness Detection

These samples check presentation attacks. They do not read MRZ, barcodes, or visual fields. Server port **14107**.

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](liveness-android.md) | [`ID-Document-Liveness-Detection-Android`]({GH}/ID-Document-Liveness-Detection-Android) |
| iOS | [iOS](liveness-ios.md) | [`ID-Document-Liveness-Detection-iOS`]({GH}/ID-Document-Liveness-Detection-iOS) |
| Flutter | [Flutter](liveness-flutter.md) | [`ID-Document-Liveness-Detection-Flutter`]({GH}/ID-Document-Liveness-Detection-Flutter) |
| React Native | [React Native](liveness-react-native.md) | [`ID-Document-Liveness-Detection-React-Native`]({GH}/ID-Document-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](liveness-ionic-capacitor.md) | [`ID-Document-Liveness-Detection-Ionic-Capacitor`]({GH}/ID-Document-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](liveness-ionic-cordova.md) | [`ID-Document-Liveness-Detection-Ionic-Cordova`]({GH}/ID-Document-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](liveness-windows.md) | [`ID-Document-Liveness-Detection-Windows`]({GH}/ID-Document-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](liveness-linux-docker.md) | [`ID-Document-Liveness-Detection-Docker`]({GH}/ID-Document-Liveness-Detection-Docker) |

## Formats

| Topic | Page |
| --- | --- |
| Process JSON | [Result Format](result-json.md) |
| Authenticity fields | [Security check fields](security-fields.md) |

HTTP APIs: [SDK Server](../sdk-server/).
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
5. [Quick start](quick-start.md) · helper `python IDV/IDV_server (then company)`
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
| **Admin (platform)** | Tenant API, workers, Identity Console | `IDV_server/`, `IDV_console/` | 14187 · 14188 |
| **Company (merchant)** | Your backend sample + operator UI | `company/backend/`, `company/admin/` | 14195 · 14189 |
| **Applicant (user)** | Capture SDKs and demo apps | `app/` | e.g. 5175 |
| **Engines** | Document + Face recognition / liveness | Face / Document SDK repos | 14102 · 14103 |

## Supporting folders

| Path | Role |
| --- | --- |
| `license/` | Hybrid licence **issuer** (Identixia ops) — `:14190`, private only |
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
cd IDV/IDV_server && set IDV_OPEN_API=1 && python app.py
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

Use a [client demo](components-clients.md) or Postman (`IDV/IDV_server/postman/IDV-Public.postman_collection.json`).

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
| Public | `IDV/IDV_server/postman/IDV-Public.postman_collection.json` |
| Company sample | `IDV/IDV_server/postman/Company-Backend-Sample.postman_collection.json` |
| Local env | `IDV/IDV_server/postman/IDV-Local.postman_environment.json` |

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
| Database | Prefer PostgreSQL via `python IDV/Install_db/setup_database.py` (or `--yes` for a guided default). SQLite is fine for local demos only. |
| Memory store | `IDV_FORCE_MEMORY` / `COMPANY_FORCE_MEMORY` are for tests — not production. |
| Webhooks | Require `whsec_…` HMAC verification; idempotent handlers; poll session API if a delivery is missed. |
| Brand | Serve `/brand/*` from `license/brand/` (or the configured `IDV_BRAND_DIR`). |

## Reverse proxy (sketch)

```text
Internet clients
      │
      ▼
 HTTPS terminator  ──►  IDV_server :14187  (/v1, /admin)
      │
      └──►  company/backend :14195  (merchant APIs + /admin)
                 │
                 ├──► IDV_server (service bearer)
                 └──► (optional) capture CDN / static hosting

Internal only:
  document-engine :14102
  face-engine     :14103
  license   :14190   ← Identixia / ops, not public
```

## Database

```bash
cd IDV
python IDV/Install_db/setup_database.py --check   # inspect current config
python IDV/Install_db/setup_database.py --yes     # non-interactive recommended local/prod bootstrap
```

Writes `IDV_server/.env` and creates schema. Production authority is **PostgreSQL**; media / Valkey / RabbitMQ options appear in the same wizard when you need them.

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

Edit `IDV_server/.env`. Restart servers after changes.

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
| `IDV_SERVER_DIR` | `IDV_server` |
| `IDV_SERVER_UI_DIST` | `IDV_console/dist` |
| `IDV_BRAND_DIR` | `license/brand` |
| `COMPANY_ADMIN_DIST` | `company/admin/dist` |
| `COMPANY_ADMIN_DIR` | `company/admin` |
| `LICENSE_ADMIN_DIR` | `license` |

## 4. Storage

| Project | Default |
| --- | --- |
| `IDV_server` | SQLite under `database/` (tenant-separated rows) |
| `company/backend` | `company/backend/database/company.sqlite` |
| `license` | `license/database/` (issuer ledger) |

Production: `python IDV/Install_db/setup_database.py` (or `--yes`) for PostgreSQL / media / Valkey / RabbitMQ. Memory stores are for tests only (`IDV_FORCE_MEMORY` / `COMPANY_FORCE_MEMORY`).

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
3. Platform + company running — `python IDV/IDV_server (then company)` or [Quick start](quick-start.md)

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
        "IDV_server: platform API, workers, storage, and /admin mount.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/IDV_server/` |
| API | `http://127.0.0.1:14187/v1` |
| Admin (production build) | `http://127.0.0.1:14187/admin/` |
| Postman | `IDV/IDV_server/postman/` |
| OpenAPI notes | `IDV/docs/API.md` |

```bash
cd IDV/IDV_server
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
```

`IDV_OPEN_API=1` enables the local demo bearer (`demo` / `ten_demo`). Disable it outside local demos — see [Production](production.md).

Integrator routes: [Creating a session (API)](api.md). Decision code: `IDV_server/idv/decision/`.
""",
    )
    hub(
        "idv/platform-console.md",
        "Identity Console",
        "IDV_console — tenant operators: sessions, reviews, webhooks, workflows.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/IDV_console/` |
| Develop | `http://127.0.0.1:14188/` (proxies API to `:14187`) |
| Production | `npm run build` → served from `IDV_server` at `/admin/` |

```bash
cd IDV/IDV_console
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

The issuer never sees ID images or biometrics. Brand files for consoles live under `license/brand/`.
""",
    )
    hub(
        "idv/license-admin.md",
        "License Admin",
        "Identixia Hybrid issuer (license) on localhost :14190.",
        """
| Item | Detail |
| --- | --- |
| Folder | `IDV/license/` |
| UI | `http://127.0.0.1:14190/` (**localhost only**) |
| Brand | `license/brand/` → `/brand/*` |

```bash
cd IDV/license
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
        "license_v2 shared protocol used by IDV_server and license.",
        """
## Overview

IDV uses a **Hybrid** licence model: day-to-day entitlement metering runs on the customer host; Identixia issues and renews licence files.

| Path | Role |
| --- | --- |
| `IDV/license/license_v2/` | Canonical protocol sources and tests |
| Vendored copies | Inside `IDV_server/` and `license/` for self-contained runs |
| `IDV/packages/license-core` | Helper package for consoles and shared libraries |

## Operating model

| Step | Where it happens |
| --- | --- |
| Issue / renew `license.txt` | [License Admin](license-admin.md) (Identixia) |
| Enforce usage on the host | `license/license_v2` (issuer) / server copy in `IDV_server` |
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

Applicant SDKs are **not** here — they live under `IDV/demo_clients/packages/`.
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
| Postman (public / private / company) | `IDV/IDV_server/postman/` |
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
| Modes | `/api/face/compare` · `/boxes` · `/template` · `/score` · `/liveness` |

IDV uses the Face SDK matcher for 1:1 and related steps. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.

## Related docs

* [Face SDK → Server](../face-sdk/full-server.md)
* Parent: [Engines](engines.md)
""",
    )
    hub(
        "idv/components-clients.md",
        "Applicant clients",
        "IDV client SDKs and demo apps under IDV/demo_clients/.",
        """
Capture SDKs and demos. The **service token stays on the company backend**; apps use capture tokens.

## Packages (`IDV/demo_clients/packages/`)

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
python IDV/demo_clients/tools/refresh_client.py
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
cd IDV/demo_clients/demos/web
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
cd IDV/demo_clients/packages/idv-android
./gradlew publishToMavenLocal
cd ../../app/android
./gradlew :app:assembleDebug
```

Use a capture token from the company backend. Package sources: `IDV/demo_clients/packages/idv-android`.

Parent: [Applicant clients](components-clients.md).
""",
    )
    hub(
        "idv/client-ios.md",
        "iOS demo",
        "Run the IDV iOS applicant demo.",
        """
## Run

Open `IDV/demo_clients/demos/ios/IdvClient.xcodeproj` and run the **IdvClient** scheme on a physical device when testing camera capture.

Session client package: `IDV/demo_clients/packages/idv-ios`.

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
| Flutter | `IDV/demo_clients/demos/flutter` |
| React Native | `IDV/demo_clients/demos/react_native` |

React Native capture helpers align with `packages/idv-web`. See `IDV/demo_clients/README.md` for bootstrap details.

Parent: [Applicant clients](components-clients.md).
""",
    )


def write_sdk_server() -> None:
    """HTTP SDK Server section — full integration guides for Windows/Docker APIs."""
    write_page(
        OUT / "sdk-server" / "README.md",
        "SDK Server",
        "On-premise Windows and Docker HTTP APIs: ports, response shapes, and which repository to run.",
        """
SDK Server is the on-premise HTTP API. A Windows build and a Docker build of the **same product** share one port and the same `/api` routes. Phone SDKs are not this API.

Use this page to pick the port. Request bodies and platform setup are in [Developers](https://docs.identixia.com/developers).

## Products and ports

| Product | Default port | Gradio demo | Docs |
| --- | --- | --- | --- |
| Document recognition + liveness | **14102** | **14202** | [Document Recognition](document-recognition.md) |
| Face recognition + liveness | **14103** | **14203** | [Face Recognition](face-recognition.md) |
| Face recognition only | **14104** | **14204** | [Face Recognition](face-recognition.md) |
| Face liveness only | **14105** | **14205** | [Face Liveness](face-liveness.md) |
| Document recognition only | **14106** | **14206** | [Document Recognition](document-recognition.md) |
| Document liveness only | **14107** | **14207** | [Document Liveness](document-liveness.md) |

## Start any server (same pattern)

1. Clone the product repository (Windows or Docker).
2. Download runtime libraries and databases:

```bash
python scripts/get_runtime.py
```

3. Copy `.env.example` → `.env`, install Python deps, start (`python run_server.py` / `python3 run_server.py` or Docker Compose).
4. Read the machine code, request a license, activate.
5. Call process routes with base64 images (JSON or multipart).

```bash
curl -s http://127.0.0.1:14103/api/machinecode
curl -s -X POST http://127.0.0.1:14103/api/activate \\
  -H "Content-Type: application/json" \\
  -d '{"license":"YOUR_KEY"}'
curl -s http://127.0.0.1:14103/api/health
curl -s http://127.0.0.1:14103/api/licenseStatus
```

## Response shapes

| Route type | Shape |
| --- | --- |
| Control (`/api/health`, `/api/activate`, `/api/machinecode`, `/api/licenseStatus`, `/api/backend`) | `{success, code, message, request_id, data}` |
| Process (`/api/face/*`, `/api/document/*`) | Engine / process JSON (not the control envelope) |

## Runtime placement

| Platform | Path after `get_runtime.py` |
| --- | --- |
| Windows / Linux host | `lib/cpu/` — binaries **and** every required `*.xdb` |
| Docker Hub image | Runtime is already inside the image |

Never ship binaries without database packs. Face recognition needs the full `recognition*.xdb` set; document products need `document.xdb`.

## Postman

Import once (every path, no duplicates):

* Monorepo: `postman/Identixia-API.postman_collection.json`
* Environment: `postman/Identixia-Local.postman_environment.json`
* Set `baseUrl` to the product under test (`http://127.0.0.1:14102` … `14107`)

## Platform deep-dives

* Face: [Windows](../face-sdk/windows.md) · [Linux / Docker](../face-sdk/linux-docker.md)
* Document: [Windows](../id-document-sdk/windows.md) · [Linux / Docker](../id-document-sdk/linux-docker.md)

## Next

* [Face Recognition](face-recognition.md)
* [Face Liveness](face-liveness.md)
* [Document Recognition](document-recognition.md)
* [Document Liveness](document-liveness.md)
""".strip()
        + "\n",
    )
    write_page(
        OUT / "sdk-server" / "face-recognition.md",
        "Face Recognition",
        "Full HTTP integration guide for face recognition (+ optional liveness).",
        """
Start Face Recognition (+ Liveness) Windows/Docker on port **14103** (recognition-only uses **14104**).

## Start the project

```bash
git clone https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows.git
cd FaceRecognition-LivenessDetection-Windows
python scripts/get_runtime.py
cp -n .env.example .env
pip install -r requirements.txt
python run_server.py
```

Linux / Docker: see [Linux / Docker](../face-sdk/linux-docker.md). Place files under `lib/cpu/` including every `recognition*.xdb` pack.

## Activate

```bash
curl -s http://127.0.0.1:14103/api/machinecode
curl -s -X POST http://127.0.0.1:14103/api/activate \\
  -H "Content-Type: application/json" \\
  -d '{"license":"YOUR_KEY"}'
curl -s http://127.0.0.1:14103/api/licenseStatus
```

## All endpoints

### Control

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Process up |
| `GET` | `/api/backend` | Backend / SDK info |
| `GET` | `/api/machinecode` | Machine fingerprint |
| `GET` | `/api/licenseStatus` | `recognition`, `liveness` flags |
| `POST` | `/api/activate` | Activate license |

### Face process

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
| `POST` | `/api/face/liveness` | `image` | PAD + deepfake (when licensed) |
| `POST` | `/api/face/deepfake` | `image` | Deepfake-only |
| `POST` | `/api/face/enroll` | `image`, `name` | Gallery enroll |
| `POST` | `/api/face/search` | `image`, `threshold` | 1:N search |
| `GET` | `/api/face/gallery` | — | List gallery |
| `DELETE` | `/api/face/gallery/{id}` | — | Remove entry |
| `POST` | `/api/face/track/start` | config | Start track session |
| `POST` | `/api/face/track/frame` | `image` | Push frame |
| `GET` | `/api/face/track/events` | — | Poll events |
| `POST` | `/api/face/track/stop` | — | Stop session |

## cURL — analyze

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/analyze \\
  -H "Content-Type: application/json" \\
  -d '{"image":"BASE64_JPEG","cropImage":false}'
```

## cURL — compare (1:1)

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/compare \\
  -H "Content-Type: application/json" \\
  -d '{"image1":"BASE64_A","image2":"BASE64_B"}'
```

## cURL — liveness (when licensed)

```bash
curl -s -X POST http://127.0.0.1:14103/api/face/liveness \\
  -H "Content-Type: application/json" \\
  -d '{"image":"BASE64_JPEG"}'
```

Authenticity is **REAL** only when PAD and deepfake both pass.

## Python

```python
import base64, json, urllib.request
from pathlib import Path

image = base64.b64encode(Path("photo.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:14103/api/face/analyze",
    data=json.dumps({"image": image, "cropImage": False}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

## JavaScript

```javascript
const image = /* base64 string */;
const res = await fetch("http://127.0.0.1:14103/api/face/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image, cropImage: false }),
});
console.log(await res.json());
```

## Resources

* [Windows product guide](../face-sdk/windows.md)
* [Linux / Docker product guide](../face-sdk/linux-docker.md)
* [Postman](README.md#postman)
* [Request a license](../request-a-license-and-support.md)
""".strip()
        + "\n",
    )
    write_page(
        OUT / "sdk-server" / "face-liveness.md",
        "Face Liveness",
        "Full HTTP integration guide for passive face liveness (+ deepfake).",
        """
Start Face Liveness Windows/Docker on port **14105** (the full Face product also exposes liveness on **14103**).

## Start the project

```bash
git clone https://github.com/identixia-IDV/FaceLivenessDetection-Windows.git
cd FaceLivenessDetection-Windows
python scripts/get_runtime.py
cp -n .env.example .env
pip install -r requirements.txt
python run_server.py
```

Place under `lib/cpu/`: engine binaries plus `recognition-common.xdb`, `recognition-liveness.xdb`, and `recognition-deepfake.xdb`. Matcher packs (`recognition.xdb`, attr, quality) are **not** included in the liveness-only product.

## Activate

```bash
curl -s http://127.0.0.1:14105/api/machinecode
curl -s -X POST http://127.0.0.1:14105/api/activate \\
  -H "Content-Type: application/json" \\
  -d '{"license":"YOUR_KEY"}'
curl -s http://127.0.0.1:14105/api/licenseStatus
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | Liveness entitlement |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/face/liveness` | PAD + deepfake (combined authenticity) |
| `POST` | `/api/face/deepfake` | Deepfake-only score |

Authenticity is **REAL** only when PAD and deepfake both pass.

## cURL

```bash
curl -s -X POST http://127.0.0.1:14105/api/face/liveness \\
  -H "Content-Type: application/json" \\
  -d '{"image":"BASE64_JPEG"}'
```

## Python

```python
import base64, json, urllib.request
from pathlib import Path

image = base64.b64encode(Path("photo.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:14105/api/face/liveness",
    data=json.dumps({"image": image}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

## JavaScript

```javascript
const image = /* base64 string */;
const res = await fetch("http://127.0.0.1:14105/api/face/liveness", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image }),
});
console.log(await res.json());
```

## Resources

* [Face Liveness (Windows)](../face-sdk/liveness-windows.md)
* [Face Liveness (Linux / Docker)](../face-sdk/liveness-linux-docker.md)
* [Postman](README.md#postman)
""".strip()
        + "\n",
    )
    write_page(
        OUT / "sdk-server" / "document-recognition.md",
        "Document Recognition",
        "Full HTTP integration guide for ID document recognition (+ optional authenticity).",
        """
Start Document full product on port **14102** (recognition-only uses **14106**).

## Start the project

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows.git
cd ID-Document-Recognition-Liveness-Detection-Windows
python scripts/get_runtime.py
cp -n .env.example .env
pip install -r requirements.txt
python run_server.py
```

Place under `lib/cpu/`: `DocumentReaderSDK.dll` (or Linux `.so` files) **and** `document.xdb`.

## Activate

```bash
curl -s http://127.0.0.1:14102/api/machinecode
curl -s -X POST http://127.0.0.1:14102/api/activate \\
  -H "Content-Type: application/json" \\
  -d '{"license":"YOUR_KEY"}'
curl -s http://127.0.0.1:14102/api/licenseStatus
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/backend` | Backend info |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | `recognition`, `authenticity` flags |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/document/process` | Full process (OCR + optional authenticity) |
| `POST` | `/api/document/recognition` | Recognition only |
| `POST` | `/api/document/liveness` | Authenticity / PAD only |
| `POST` | `/api/document/general` | General helper |

Prefer `images: [{ "image": "<b64>" }, …]` when the binding expects an array (see Postman). Some samples also accept `image` / `image2`.

## cURL — process

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/process \\
  -H "Content-Type: application/json" \\
  -d '{"images":[{"image":"BASE64_FRONT"},{"image":"BASE64_BACK"}]}'
```

## Python

```python
import base64, json, urllib.request
from pathlib import Path

front = base64.b64encode(Path("front.jpg").read_bytes()).decode()
back = base64.b64encode(Path("back.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:14102/api/document/process",
    data=json.dumps({"images": [{"image": front}, {"image": back}]}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

## Resources

* [Result Format](../id-document-sdk/result-json.md)
* [Security check fields](../id-document-sdk/security-fields.md)
* [Windows](../id-document-sdk/windows.md) · [Linux / Docker](../id-document-sdk/linux-docker.md)
* [Postman](README.md#postman)
""".strip()
        + "\n",
    )
    write_page(
        OUT / "sdk-server" / "document-liveness.md",
        "Document Liveness",
        "Full HTTP integration guide for document authenticity / PAD.",
        """
Start Document Liveness Windows/Docker on port **14107** (the full Document product also exposes authenticity on **14102**).

## Start the project

```bash
git clone https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows.git
cd ID-Document-Liveness-Detection-Windows
python scripts/get_runtime.py
cp -n .env.example .env
pip install -r requirements.txt
python run_server.py
```

Place under `lib/cpu/`: engine binaries and liveness-only `document.xdb` (packed from `db_liveness.dat`). OCR recognition databases are **not** included.

## Activate

```bash
curl -s http://127.0.0.1:14107/api/machinecode
curl -s -X POST http://127.0.0.1:14107/api/activate \\
  -H "Content-Type: application/json" \\
  -d '{"license":"YOUR_KEY"}'
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health |
| `GET` | `/api/machinecode` | Machine code |
| `GET` | `/api/licenseStatus` | Entitlement |
| `POST` | `/api/activate` | Activate |
| `POST` | `/api/document/liveness` | Authenticity / PAD for front (+ back) images |

This product is **PAD / authenticity**, not OCR. Pair with Document Recognition when you need fields.

## cURL

```bash
curl -s -X POST http://127.0.0.1:14107/api/document/liveness \\
  -H "Content-Type: application/json" \\
  -d '{"images":["BASE64_FRONT","BASE64_BACK"]}'
```

## Python

```python
import base64, json, urllib.request
from pathlib import Path

front = base64.b64encode(Path("front.jpg").read_bytes()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:14107/api/document/liveness",
    data=json.dumps({"images": [front]}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=180) as resp:
    print(resp.read().decode())
```

## JavaScript

```javascript
const image = /* front base64 */;
const res = await fetch("http://127.0.0.1:14107/api/document/liveness", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image }),
});
console.log(await res.json());
```

See [Security check fields](../id-document-sdk/security-fields.md).
""".strip()
        + "\n",
    )


def write_summary(_structure: dict[str, list[tuple[str, str]]] | None = None) -> None:
    """FaceOnLive-style shallow sidebar. Leaf platform files keep stable catalog URLs.

    Pattern (see https://docs.faceonlive.com/):
      Welcome → SDK Server → IDV (KYC) → Face SDK (Intro + Reference) → Document SDK (Intro + Reference)
    """
    lines = [
        "# Table of contents",
        "",
        "",
        "* [Welcome to Identixia](README.md)",
        "",
        "## Face",
        "",
        "* [Introduction](face-sdk/README.md)",
        "* [Recognition](face-sdk/recognition.md)",
        "* [Liveness](face-sdk/liveness.md)",
        "",
        "## ID Document",
        "",
        "* [Introduction](id-document-sdk/README.md)",
        "* [Recognition](id-document-sdk/recognition.md)",
        "* [Liveness](id-document-sdk/liveness.md)",
        "* [Result format](id-document-sdk/result-json.md)",
        "* [Security checks](id-document-sdk/security-fields.md)",
        "* [Supported ID documents and countries](id-document-sdk/supported-documents.md)",
        "",
        "## API",
        "",
        "* [SDK Server](sdk-server/README.md)",
        "",
        "## Developers",
        "",
        "* [Face integration guide](face-sdk/integration-guide.md)",
        "  * [Platform index](face-sdk/reference.md)",
        "  * [Android](face-sdk/android.md)",
        "  * [iOS](face-sdk/ios.md)",
        "  * [Flutter](face-sdk/flutter.md)",
        "  * [React Native](face-sdk/react-native.md)",
        "  * [Ionic Capacitor](face-sdk/ionic-capacitor.md)",
        "  * [Ionic Cordova](face-sdk/ionic-cordova.md)",
        "  * [Windows](face-sdk/windows.md)",
        "  * [Linux / Docker](face-sdk/linux-docker.md)",
        "  * [Face Recognition — Windows](face-sdk/recognition-windows.md)",
        "  * [Face Recognition — Linux / Docker](face-sdk/recognition-linux-docker.md)",
        "  * [Face Liveness — Android](face-sdk/liveness-android.md)",
        "  * [Face Liveness — iOS](face-sdk/liveness-ios.md)",
        "  * [Face Liveness — Windows](face-sdk/liveness-windows.md)",
        "  * [Face Liveness — Linux / Docker](face-sdk/liveness-linux-docker.md)",
        "* [ID Document integration guide](id-document-sdk/integration-guide.md)",
        "  * [Platform index](id-document-sdk/reference.md)",
        "  * [Android](id-document-sdk/android.md)",
        "  * [iOS](id-document-sdk/ios.md)",
        "  * [Flutter](id-document-sdk/flutter.md)",
        "  * [React Native](id-document-sdk/react-native.md)",
        "  * [Ionic Capacitor](id-document-sdk/ionic-capacitor.md)",
        "  * [Ionic Cordova](id-document-sdk/ionic-cordova.md)",
        "  * [Windows](id-document-sdk/windows.md)",
        "  * [Linux / Docker](id-document-sdk/linux-docker.md)",
        "  * [ID Document Recognition — Linux / Docker](id-document-sdk/recognition-linux-docker.md)",
        "  * [ID Document Liveness — Linux / Docker](id-document-sdk/liveness-linux-docker.md)",
        "* [Face recognition API](sdk-server/face-recognition.md)",
        "* [Face liveness API](sdk-server/face-liveness.md)",
        "* [Document recognition API](sdk-server/document-recognition.md)",
        "* [Document liveness API](sdk-server/document-liveness.md)",
        "",
        "## Guides",
        "",
        "* [Request a license](request-a-license-and-support.md)",
        "* [Contact](contact-us.md)",
        "",
    ]
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_gitbook_yaml() -> None:
    """Space icon uses Identixia favicon (single brand pack)."""
    (OUT / ".gitbook.yaml").write_text(
        "root: .\n\n"
        "# Images are loaded from identixia-IDV/identixia-assets. Do not commit binaries here.\n"
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
    write_supported_documents()
    write_integration_guides()
    write_sdk_server()
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

    written = write_missing_app_pages(owner)
    print(f"missing app pages written: {written}")

    write_welcome()
    write_summary(structure)
    for page in OUT.rglob("*.md"):
        original = page.read_text(encoding="utf-8")
        updated = C.rewrite_asset_srcs(original)
        if updated != original:
            page.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Wrote docs under {OUT}")
    from editorial import refresh_copy

    refresh_copy(OUT)
    from sections import publish

    publish()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
