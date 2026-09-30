#!/usr/bin/env python3
"""Rebuild detailed GitBook docs from catalog + product READMEs + API guides.

Keeps URL slugs from catalog/github_about.json homepages.

  python gitbook-push/generate.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_lib as C  # noqa: E402

ABOUT_PATH = ROOT / "catalog" / "github_about.json"
NAMES_PATH = ROOT / "catalog" / "repository_names.json"
REPOS_DIR = ROOT / "repositories"
OUT = Path(__file__).resolve().parent / "identixia-docs"
DOCS_BASE = "https://docs.identixia.com"

TITLES: dict[str, str] = {
    "face-recognition-sdk": "Face Recognition SDK",
    "face-recognition-android-sdk": "Face Recognition Android SDK",
    "face-recognition-ios-sdk": "Face Recognition iOS SDK",
    "face-recognition-android-sdk-1": "Face Recognition React Native SDK",
    "face-recognition-android-sdk-2": "Face Recognition Flutter SDK",
    "face-recognition-android-sdk-3": "Face Recognition Ionic Cordova SDK",
    "face-recognition-ionic-capacitor-sdk": "Face Recognition Ionic Capacitor SDK",
    "face-recognition-sdk-windows": "Face Recognition + Liveness Windows SDK",
    "face-recognition-sdk-linux": "Face Recognition + Liveness Linux / Docker SDK",
    "face-recognition-windows-sdk": "Face Recognition Windows SDK",
    "face-recognition-linux-sdk": "Face Recognition Linux / Docker SDK",
    "liveness-detection-sdk": "Liveness Detection SDK",
    "liveness-detection-android-sdk": "Liveness Detection Android SDK",
    "liveness-detection-ios-sdk": "Liveness Detection iOS SDK",
    "liveness-detection-windows-sdk": "Liveness Detection Windows SDK",
    "liveness-detection-linux-sdk": "Liveness Detection Linux / Docker SDK",
    "id-document-recognition-sdk": "ID Document Recognition SDK",
    "id-document-recognition-android-sdk": "ID Document Recognition Android SDK",
    "id-document-recognition-ios-sdk": "ID Document Recognition iOS SDK",
    "id-document-recognition-windows-sdk": "ID Document Recognition Windows SDK",
    "id-document-recognition-linux-sdk": "ID Document Recognition Linux / Docker SDK",
    "id-document-recognition-flutter-sdk": "ID Document Recognition Flutter SDK",
    "id-document-recognition-react-native-sdk": "ID Document Recognition React Native SDK",
    "id-document-recognition-ionic-capacitor-sdk": "ID Document Recognition Ionic Capacitor SDK",
    "id-document-recognition-ionic-cordova-sdk": "ID Document Recognition Ionic Cordova SDK",
    "id-document-liveness-sdk": "ID Document Liveness SDK",
}

SECTION_ORDER: dict[str, list[str]] = {
    "face-recognition-sdk": [
        "face-recognition-android-sdk",
        "face-recognition-ios-sdk",
        "face-recognition-android-sdk-2",
        "face-recognition-android-sdk-1",
        "face-recognition-ionic-capacitor-sdk",
        "face-recognition-android-sdk-3",
        "face-recognition-sdk-windows",
        "face-recognition-sdk-linux",
        "face-recognition-windows-sdk",
        "face-recognition-linux-sdk",
    ],
    "liveness-detection-sdk": [
        "liveness-detection-android-sdk",
        "liveness-detection-ios-sdk",
        "liveness-detection-windows-sdk",
        "liveness-detection-linux-sdk",
    ],
    "id-document-recognition-sdk": [
        "id-document-recognition-android-sdk",
        "id-document-recognition-ios-sdk",
        "id-document-recognition-flutter-sdk",
        "id-document-recognition-react-native-sdk",
        "id-document-recognition-ionic-capacitor-sdk",
        "id-document-recognition-ionic-cordova-sdk",
        "id-document-recognition-windows-sdk",
        "id-document-recognition-linux-sdk",
        "document-result-json",
        "document-security-check-fields",
    ],
    "id-document-liveness-sdk": [],
}

SECTION_META = {
    "face-recognition-sdk": {
        "blurb": (
            "On-premise face recognition for phones and servers. Enroll, 1:N identify, "
            "templates, quality, and 1:1 match. Passive liveness when the license includes it."
        ),
        "cover": ".gitbook/assets/face-android-home.png",
    },
    "liveness-detection-sdk": {
        "blurb": (
            "Passive face presentation-attack detection on device or on your server. "
            "Scores a camera frame or still image when the license allows it."
        ),
        "cover": ".gitbook/assets/liveness-mobile.png",
    },
    "id-document-recognition-sdk": {
        "blurb": (
            "Passport, national ID, and driver license OCR, MRZ, and barcode extraction. "
            "Document liveness runs when the license includes it."
        ),
        "cover": ".gitbook/assets/document-desktop-result.png",
    },
    "id-document-liveness-sdk": {
        "blurb": (
            "On-premise ID document liveness API for Linux and Docker. Separate from OCR. "
            "Document anti-spoofing when the license includes it."
        ),
        "cover": ".gitbook/assets/document-docker-result.png",
    },
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


def title_for(slug: str) -> str:
    base = slug.rsplit("/", 1)[-1]
    return TITLES.get(base) or TITLES.get(slug) or re.sub(r"[-_]+", " ", base).title()


def rewrite_links(text: str, owner: str) -> str:
    # Normalize legacy doc. host to docs.
    text = text.replace("https://doc.identixia.com", DOCS_BASE)
    text = text.replace("https://docs.identixia.com", DOCS_BASE)
    text = text.replace("https://github.com/identixiaAI/", f"https://github.com/{owner}/")
    return text


def _plain_heading(line: str) -> str:
    """Strip HTML/icon img tags from markdown headings for GitBook."""
    m = re.match(r"^(#{1,6})\s+(.*)$", line)
    if not m:
        return line
    level, rest = m.group(1), m.group(2)
    # Drop leading <img ... /> icons
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
        # Drop trailing Contact section — Support is added by the generator.
        if re.search(r"Contact\s*$", line) and (
            "mail.svg" in line or line.strip().startswith("##")
        ):
            break
        # Drop README Screenshots blocks — generator inserts curated local assets.
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
        # Drop remote badge / icon rows that often break in GitBook.
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
        # Normalize legacy assets org + prefer docs host already handled upstream.
        line = line.replace(
            "raw.githubusercontent.com/identixiaAI/identixia-assets",
            "raw.githubusercontent.com/identixia-IDV/identixia-assets",
        )
        if re.match(r"^#+\s+", line):
            line = _plain_heading(line)
        out.append(line)
    text = "\n".join(out).strip() + "\n"
    # Drop empty HTML wrappers left behind
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


def build_product_page(owner: str, item: dict, rel: str, by_name: dict[str, dict]) -> Path:
    name = item["name"]
    desc = item["description"]
    title = title_for(rel)
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

    if "/" not in rel:
        out = OUT / rel / "README.md"
    else:
        section, leaf = rel.split("/", 1)
        out = OUT / section / f"{leaf}.md"
    write_page(out, title, desc, body)
    return out


def write_section_index(section: str, children: list[tuple[str, str]]) -> None:
    path = OUT / section / "README.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if "### Platforms in this section" in text or not children:
        return
    lines = ["\n### Platforms in this section\n"]
    for label, link in children:
        lines.append(f"* [{label}]({link})")
    path.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_welcome(structure: dict[str, list[tuple[str, str]]]) -> None:
    cards = []
    for sec, meta in SECTION_META.items():
        cover = meta.get("cover", "")
        cover_cell = f'<a href="{cover}">{Path(cover).name}</a>' if cover else ""
        cards.append(
            f"<tr><td><strong>{title_for(sec)}</strong></td><td>{meta['blurb']}</td>"
            f"<td>{cover_cell}</td><td></td>"
            f'<td><a href="{sec}/">{sec}</a></td></tr>'
        )
    body = f"""
<p align="center"><img src=".gitbook/assets/brand-logo.png" alt="Identixia" width="280"></p>

## Introduction

Official **Identixia** documentation for on-premise biometric SDKs. Use these pages to integrate every customer-facing function: activation, capture, recognition, matching, liveness, and result handling.

* **Face Recognition** — detect, attributes, quality, templates, 1:1, 1:N; optional passive liveness
* **Liveness Detection** — passive face presentation-attack detection
* **ID Document Recognition** — OCR, MRZ, barcode; optional document liveness
* **ID Document Liveness** — document anti-spoofing API (separate from OCR)

Biometric data stays on **your** device or server.

## How to use these docs

1. Open your **product** section.
2. Open your **platform** page.
3. Follow **Quick start** → run the demo → confirm Ready.
4. Read **License and activation**, then **API reference** for every function you will call.
5. Use **Troubleshooting** when something fails.
6. Server integrators: copy machine code → [request a license](request-a-license-and-support.md) → `POST /api/activate`.

{{% hint style="info" %}}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths in each README. They are not committed to git. The demo UI is optional in production — call the SDK/API directly.
{{% endhint %}}

## Products

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
{''.join(cards)}
</tbody></table>

## Shared concepts

| Topic | Summary |
| --- | --- |
| Control vs process (HTTP) | `/api/health`, `/api/machinecode`, `/api/activate`, `/api/licenseStatus` use `{{success,code,message,request_id,data}}`. Process routes return engine JSON. |
| Threading (mobile) | Activate, init, detect, recognize on a **background** thread. |
| License flags | Face: `recognition` / `liveness`. Document: `recognition` / `authenticity`. Missing flag ⇒ feature not run. |
| Your storage | Persist templates and document fields in **your** database. |

## Links

* [Request a license & support](request-a-license-and-support.md)
* [Contact](contact-us.md)
* [identixia.com](https://identixia.com)
* GitHub: [identixia-IDV](https://github.com/identixia-IDV)
"""
    write_page(
        OUT / "README.md",
        "Welcome to Identixia",
        "Detailed Identixia docs for Face Recognition, Liveness, and ID Document SDKs — setup, activation, and full API reference.",
        body.strip() + "\n",
    )


def write_static_pages() -> None:
    write_page(
        OUT / "request-a-license-and-support.md",
        "Request a License & Support",
        "How to request an Identixia SDK license for mobile and server products.",
        """
## Need a license?

### Mobile SDK

1. Build your app with **your** applicationId / bundle id (not the demo id).
2. Contact us (email / WhatsApp / Telegram) with the id and product (Face / Liveness / Document).
3. Integrate the key with activate → init as shown on the platform page.

The sample apps ship a **demo key** for the sample id only. Do not reuse it in production.

### Server SDK (Windows / Linux / Docker)

1. Start the API once.
2. `GET /api/machinecode` and copy `data.machinecode`.
3. Send that code to Identixia. **Docker and bare metal have different codes.**
4. `POST /api/activate` with the license file, or place `license.txt` and restart.
5. Confirm with `GET /api/licenseStatus`.

## Support

We offer integration help and after-sale support for Identixia biometric solutions.

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

    write_page(
        OUT / "id-document-recognition-sdk" / "document-result-json.md",
        "Document result JSON",
        "Shared document recognition / process JSON shape across mobile and server SDKs.",
        """
## Purpose

`recognize` (mobile) and `POST /api/documentProcess` (Linux / Windows) return the **same idea**: one JSON object your app parses. Dedicated `documentRecognition` / `documentLiveness` routes use the same shape with recognition-only or authenticity-only fields populated.

Do **not** scrape the demo Result screen — parse this JSON.

## Top-level fields

| Field | Meaning |
| ----- | ------- |
| `errorCode` / process `metadata.status` | Engine / process status |
| `documentName` / identity class | Document type name |
| `countryName` | Issuing country |
| `score` | Locate / document confidence |
| `msg` / `metadata.message` | Optional message |
| `verification` / `tests` | Field and document checks |
| `imageQuality` | Capture quality checks |
| `ocr` / field readings | Visual-zone fields |
| `mrz` | Machine-readable zone |
| `barcode` | Barcode / QR fields |
| `images` | Crops (portrait, document, signature, …) |
| `security` | Authenticity / document liveness (license-gated) |

Mobile kits may normalize Android output toward an iOS-shaped contract — use the kit `ResultParser` when present.

## `verification` values

| Value | Meaning |
| ---: | --- |
| `0` | Pass |
| `1` | Fail |
| `2` | Not checked |

Image-quality check enums may use a different 0/1/2 mapping — see the kit parser comments.

## Related HTTP routes

| Route | Role |
| --- | --- |
| `POST /api/documentProcess` | Full process |
| `POST /api/documentRecognition` | OCR / MRZ / barcode |
| `POST /api/documentLiveness` | Authenticity only |

See also [Document security check fields](document-security-check-fields.md).
""".strip()
        + "\n",
    )
    write_page(
        OUT / "id-document-recognition-sdk" / "document-security-check-fields.md",
        "Document security check fields",
        "License-gated document authenticity / liveness fields in the document result JSON.",
        """
## When security fields appear

If the license includes document liveness / authenticity, the result JSON populates `security` (and related verification / tests rows) with engine checks against:

* Screen replay
* Printout / paper copy
* Portrait or document substitution (when supported)

## How to interpret

| Situation | Meaning |
| --- | --- |
| `security` missing / empty | Feature **not licensed** or **not requested** — not a pass |
| Checks present with fail | Treat as authenticity reject per your risk policy |
| Recognition-only license | Use OCR/MRZ/barcode only; do not invent security passes |

Mobile and server SDKs share field names where possible. Prefer structured `security` / `tests` arrays over UI labels.

Parent object: [Document result JSON](document-result-json.md).
""".strip()
        + "\n",
    )


def write_summary(structure: dict[str, list[tuple[str, str]]]) -> None:
    lines = [
        "# Table of contents",
        "",
        "",
        "* [Welcome to Identixia](README.md)",
    ]
    for section in (
        "face-recognition-sdk",
        "liveness-detection-sdk",
        "id-document-recognition-sdk",
        "id-document-liveness-sdk",
    ):
        lines.append(f"* [{title_for(section)}]({section}/README.md)")
        kids = structure.get(section, [])
        by_leaf = {Path(link).stem: (label, link) for label, link in kids}
        preferred = SECTION_ORDER.get(section, [])
        ordered: list[tuple[str, str]] = []
        seen: set[str] = set()
        for leaf in preferred:
            if leaf in by_leaf:
                ordered.append(by_leaf[leaf])
                seen.add(leaf)
        for leaf, pair in by_leaf.items():
            if leaf not in seen:
                ordered.append(pair)
        for label, link in ordered:
            lines.append(f"  * [{label}]({section}/{link})")
    lines.append("* [Request a License & Support](request-a-license-and-support.md)")
    lines.append("* [Contact](contact-us.md)")
    lines.append("")
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    about, by_name = load_catalog()
    owner = (about.get("publish_owner") or about.get("owner") or "identixia-IDV").strip()
    OUT.mkdir(parents=True, exist_ok=True)

    structure: dict[str, list[tuple[str, str]]] = {
        "face-recognition-sdk": [],
        "liveness-detection-sdk": [],
        "id-document-recognition-sdk": [],
        "id-document-liveness-sdk": [],
    }

    for item in about["repositories"]:
        name = item["name"]
        if name == "identixia-assets":
            continue
        rel = homepage_rel(item["homepage"])
        if not rel:
            print(f"SKIP non-docs homepage: {name}")
            continue
        path = build_product_page(owner, item, rel, by_name)
        print(f"OK {name} -> {path.relative_to(OUT.parent)} ({path.stat().st_size} bytes)")
        if "/" in rel:
            section, leaf = rel.split("/", 1)
            structure.setdefault(section, []).append((title_for(rel), f"{leaf}.md"))

    write_static_pages()
    structure["id-document-recognition-sdk"].extend(
        [
            ("Document result JSON", "document-result-json.md"),
            ("Document security check fields", "document-security-check-fields.md"),
        ]
    )

    for section, kids in structure.items():
        # Stable order for index links
        by_leaf = {Path(link).stem: (label, link) for label, link in kids}
        ordered = []
        seen = set()
        for leaf in SECTION_ORDER.get(section, []):
            if leaf in by_leaf:
                ordered.append(by_leaf[leaf])
                seen.add(leaf)
        for leaf, pair in by_leaf.items():
            if leaf not in seen:
                ordered.append(pair)
        write_section_index(section, ordered)

    write_welcome(structure)
    write_summary(structure)
    print(f"Wrote detailed docs under {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
