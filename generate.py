#!/usr/bin/env python3
"""Rebuild gitbook-push/identixia-docs from catalog + current product READMEs.

Keeps GitBook URL slugs from catalog/github_about.json homepages so GitHub
About links keep working.

  python gitbook-push/generate.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABOUT_PATH = ROOT / "catalog" / "github_about.json"
REPOS_DIR = ROOT / "repositories"
OUT = Path(__file__).resolve().parent / "identixia-docs"
DOCS_BASE = "https://doc.identixia.com"

# Display titles for known slugs (fallback: title-case filename).
TITLES: dict[str, str] = {
    "face-recognition-sdk": "Face Recognition SDK",
    "face-recognition-android-sdk": "Face Recognition Android SDK",
    "face-recognition-ios-sdk": "Face Recognition iOS SDK",
    "face-recognition-android-sdk-1": "Face Recognition React Native SDK",
    "face-recognition-android-sdk-2": "Face Recognition Flutter SDK",
    "face-recognition-android-sdk-3": "Face Recognition Ionic Cordova SDK",
    "face-recognition-ionic-capacitor-sdk": "Face Recognition Ionic Capacitor SDK",
    "face-recognition-sdk-windows": "Face Recognition + Liveness Windows SDK",
    "face-recognition-sdk-linux": "Face Recognition + Liveness Linux SDK",
    "face-recognition-windows-sdk": "Face Recognition Windows SDK",
    "face-recognition-linux-sdk": "Face Recognition Linux SDK",
    "liveness-detection-sdk": "Liveness Detection SDK",
    "liveness-detection-android-sdk": "Liveness Detection Android SDK",
    "liveness-detection-ios-sdk": "Liveness Detection iOS SDK",
    "liveness-detection-windows-sdk": "Liveness Detection Windows SDK",
    "liveness-detection-linux-sdk": "Liveness Detection Linux SDK",
    "id-document-recognition-sdk": "ID Document Recognition SDK",
    "id-document-recognition-android-sdk": "ID Document Recognition Android SDK",
    "id-document-recognition-ios-sdk": "ID Document Recognition iOS SDK",
    "id-document-recognition-windows-sdk": "ID Document Recognition Windows SDK",
    "id-document-recognition-linux-sdk": "ID Document Recognition Linux SDK",
    "id-document-recognition-flutter-sdk": "ID Document Recognition Flutter SDK",
    "id-document-recognition-react-native-sdk": "ID Document Recognition React Native SDK",
    "id-document-recognition-ionic-capacitor-sdk": "ID Document Recognition Ionic Capacitor SDK",
    "id-document-recognition-ionic-cordova-sdk": "ID Document Recognition Ionic Cordova SDK",
    "id-document-liveness-sdk": "ID Document Liveness SDK",
}

# Preferred child order under each section (slug basename).
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
        "cover": ".gitbook/assets/Lucid_Origin_A_futuristic_face_recognition_interface_for_Facep_1.jpg",
    },
    "liveness-detection-sdk": {
        "blurb": (
            "Passive face presentation-attack detection on device or on your server. "
            "Scores a camera frame or still image when the license allows it."
        ),
        "cover": ".gitbook/assets/Lucid_Origin_Splitscreen_concept_showing_real_face_vs_spoof_at_0.jpg",
    },
    "id-document-recognition-sdk": {
        "blurb": (
            "Passport, national ID, and driver license OCR, MRZ, and barcode extraction. "
            "Document liveness runs when the license includes it."
        ),
        "cover": ".gitbook/assets/Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg",
    },
    "id-document-liveness-sdk": {
        "blurb": (
            "On-premise ID document liveness API for Linux and Docker. Separate from OCR. "
            "Document anti-spoofing when the license includes it."
        ),
        "cover": ".gitbook/assets/Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg",
    },
}


def die(msg: str) -> None:
    raise SystemExit(f"ERROR: {msg}")


def load_about() -> dict:
    return json.loads(ABOUT_PATH.read_text(encoding="utf-8"))


def homepage_rel(url: str) -> str | None:
    if not url.startswith(DOCS_BASE):
        return None
    path = url[len(DOCS_BASE) :].lstrip("/")
    return path or None


def title_for(slug: str) -> str:
    base = slug.rsplit("/", 1)[-1]
    if base in TITLES:
        return TITLES[base]
    if slug in TITLES:
        return TITLES[slug]
    return re.sub(r"[-_]+", " ", base).title()


def rewrite_links(text: str, publish_owner: str) -> str:
    text = text.replace("https://docs.identixia.com", DOCS_BASE)
    text = text.replace("https://github.com/identixiaAI/", f"https://github.com/{publish_owner}/")
    # Prefer publish org for product clones already using either owner.
    return text


def strip_readme_noise(body: str) -> str:
    """Turn a product README into GitBook-friendly markdown."""
    # Drop leading centered brand/badge blocks (keep content after first heading).
    lines = body.splitlines()
    out: list[str] = []
    started = False
    for line in lines:
        if not started:
            if re.match(r"^#+\s+", line):
                started = True
                # Prefer a single H1 from our generator; demote README H1 → H2.
                if line.startswith("# "):
                    out.append("## " + line[2:])
                else:
                    out.append(line)
            continue
        # Drop orphan closing tags from removed <div align="center"> wrappers.
        if line.strip() in {"</div>", "<div align=\"center\">", "<div align='center'>"}:
            continue
        out.append(line)
    text = "\n".join(out).strip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def frontmatter(description: str) -> str:
    desc = description.replace("\n", " ").strip()
    if len(desc) > 280:
        desc = desc[:277] + "..."
    return (
        "---\n"
        f"description: >-\n"
        f"  {desc}\n"
        "---\n\n"
    )


def write_page(path: Path, title: str, description: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = frontmatter(description) + f"# {title}\n\n" + body.rstrip() + "\n"
    path.write_text(content, encoding="utf-8", newline="\n")


def github_block(owner: str, name: str) -> str:
    return (
        f"### Repository\n\n"
        f"{{% embed url=\"https://github.com/{owner}/{name}\" %}}\n\n"
        f"[`{owner}/{name}`](https://github.com/{owner}/{name})\n"
    )


def build_product_page(
    *,
    owner: str,
    item: dict,
    rel: str,
) -> tuple[Path, str]:
    """Return (out_path, summary_label)."""
    name = item["name"]
    desc = item["description"]
    title = title_for(rel)
    readme_path = REPOS_DIR / name / "README.md"
    parts: list[str] = []
    parts.append(desc)
    parts.append("")
    parts.append(github_block(owner, name))
    if readme_path.is_file():
        raw = readme_path.read_text(encoding="utf-8", errors="replace")
        raw = rewrite_links(raw, owner)
        body = strip_readme_noise(raw)
        parts.append("### From the product README\n")
        parts.append(body)
    else:
        parts.append(
            "{% hint style=\"warning\" %}\n"
            f"Local README missing for `{name}`.\n"
            "{% endhint %}\n"
        )
    parts.append(
        "\n{% hint style=\"info\" %}\n"
        "Native engine binaries are distributed via GitHub Releases "
        "(`/releases/latest/download/…`) or the paths documented in the product README. "
        "They are not committed to git.\n"
        "{% endhint %}\n"
    )

    # Section hub → README.md; leaf → <slug>.md
    if "/" not in rel:
        out = OUT / rel / "README.md"
        label = title
    else:
        section, leaf = rel.split("/", 1)
        out = OUT / section / f"{leaf}.md"
        label = title
    write_page(out, title, desc, "\n".join(parts))
    return out, label


def write_section_hub(section: str, children: list[tuple[str, str]], hub_item: dict | None, owner: str) -> None:
    meta = SECTION_META.get(section, {"blurb": "", "cover": ""})
    title = title_for(section)
    blurb = meta.get("blurb") or (hub_item["description"] if hub_item else title)
    lines = [blurb, ""]
    if hub_item:
        lines.append(github_block(owner, hub_item["name"]))
        readme = REPOS_DIR / hub_item["name"] / "README.md"
        if readme.is_file():
            raw = rewrite_links(readme.read_text(encoding="utf-8", errors="replace"), owner)
            lines.append("### Overview\n")
            lines.append(strip_readme_noise(raw))
    if children:
        lines.append("\n### Platforms\n")
        for label, link in children:
            lines.append(f"* [{label}]({link})")
        lines.append("")
    out = OUT / section / "README.md"
    # Hub product whose homepage IS the section root already wrote README — merge carefully.
    if out.exists() and hub_item and homepage_rel(hub_item["homepage"]) == section:
        # Product page already written as section README; append platform index if missing.
        existing = out.read_text(encoding="utf-8")
        if "### Platforms" not in existing and children:
            out.write_text(
                existing.rstrip()
                + "\n\n### Platforms\n\n"
                + "\n".join(f"* [{label}]({link})" for label, link in children)
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
        return
    write_page(out, title, blurb, "\n".join(lines))


def write_welcome(sections: list[str]) -> None:
    cards = []
    for sec in sections:
        meta = SECTION_META.get(sec, {})
        cover = meta.get("cover", "")
        title = title_for(sec)
        blurb = meta.get("blurb", "")
        cover_cell = f'<a href="{cover}">{Path(cover).name}</a>' if cover else ""
        cards.append(
            f"<tr><td><strong>{title}</strong></td><td>{blurb}</td>"
            f"<td>{cover_cell}</td><td></td>"
            f'<td><a href="{sec}/">{sec}</a></td></tr>'
        )
    body = f"""
### Introduction

Official documentation for **Identixia** on-premise biometric SDKs:

* **Face Recognition** — enroll, 1:N identify, templates, quality, 1:1 match; optional passive liveness
* **Liveness Detection** — passive face presentation-attack detection
* **ID Document Recognition** — OCR, MRZ, barcode; optional document liveness
* **ID Document Liveness** — document anti-spoofing API (separate from OCR)

Processing stays on your device or server. Biometric data is **not** sent to Identixia cloud.

### How to use these docs

1. Open the product that matches your license.
2. Open the **platform** page (Android, iOS, Flutter, React Native, Ionic, Windows, Linux/Docker).
3. Follow setup in the product README / this page to place the runtime and run the demo.
4. For server SDKs, copy the machine code, then [request a license](request-a-license-and-support.md).
5. Call activate → init (or HTTP activate), then the process APIs. Store templates and document JSON in **your** database.

Native binaries are **not** in git. Use GitHub Releases (`/releases/latest/download/…`) or the paths listed on each platform page.

{{% hint style="info" %}}
The demo is a full sample app. Production integrations copy the runtime and call the SDK/API — you do not need the demo screens.
{{% endhint %}}

### Products

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
{''.join(cards)}
</tbody></table>

### Links

* [Request a license & support](request-a-license-and-support.md)
* [Contact](contact-us.md)
* Website: [identixia.com](https://identixia.com)
* GitHub org: [identixia-IDV](https://github.com/identixia-IDV)
"""
    write_page(
        OUT / "README.md",
        "Welcome to Identixia",
        "Official Identixia documentation for on-premise Face Recognition, Liveness, and ID Document SDKs.",
        body.strip() + "\n",
    )


def write_static_pages() -> None:
    write_page(
        OUT / "request-a-license-and-support.md",
        "Request a License & Support",
        "How to request an Identixia SDK license for mobile and server products.",
        """
### Need a license?

* **Mobile SDK:** contact us via WhatsApp, Telegram, or email. Request a new license for your own application / bundle id (the sample ships a demo key for its id only).
* **Server SDK (Linux / Windows / Docker):** start the API once, copy the machine code from logs or `GET /api/machinecode`, and send that code. Docker and a native host have **different** machine codes. Use the code from the environment you will run in production.

Do not paste demo license keys into your production app.

### Need support?

We offer **free integration** help with Identixia biometric solutions, plus after-sale and maintenance support.

### Contact

{% include "./.gitbook/includes/contact.md" %}
""".strip()
        + "\n",
    )
    write_page(
        OUT / "contact-us.md",
        "Contact",
        "Contact Identixia for licenses and support.",
        """
### Availability

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
`recognize` (mobile) and `POST /api/documentProcess` (Linux / Windows) return the same idea: one JSON object. Dedicated `documentRecognition` / `documentLiveness` (and matching HTTP paths) use the same shape with recognition-only or authenticity-only fields populated.

Parse this object in your app. Do not copy the demo Result screen.

### Top-level fields

| Field | Meaning |
| ----- | ------- |
| `errorCode` | Optional engine error |
| `documentName` | Document type name |
| `countryName` | Issuing country |
| `score` | Document / locate confidence |
| `msg` | Optional message |
| `verification` | Field and document checks |
| `imageQuality` | Capture quality checks |
| `ocr` | Visual-zone fields |
| `mrz` | Machine-readable zone |
| `barcode` | Barcode / QR fields |
| `images` | Crops (portrait, document, signature, …) |
| `security` | Authenticity / document liveness (license-gated) |

### `verification` values

**0** Pass · **1** Fail · **2** Not checked

### Related HTTP routes

* `POST /api/documentProcess`
* `POST /api/documentRecognition`
* `POST /api/documentLiveness`

See also [Document security check fields](document-security-check-fields.md).
""".strip()
        + "\n",
    )
    write_page(
        OUT / "id-document-recognition-sdk" / "document-security-check-fields.md",
        "Document security check fields",
        "License-gated document authenticity / liveness fields in the document result JSON.",
        """
When the license includes document liveness / authenticity, the result JSON may populate `security` (and related `verification.security`) with engine checks against screen replays, printouts, and substitution.

Treat missing or empty security blocks as **not licensed / not run**, not as a pass.

Mobile and server SDKs share the same field names where possible. Prefer the structured `security` object over scraping demo UI labels.

See [Document result JSON](document-result-json.md) for the parent object.
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
    about = load_about()
    owner = (about.get("publish_owner") or about.get("owner") or "identixia-IDV").strip()
    OUT.mkdir(parents=True, exist_ok=True)

    # Map section → list of (label, filename.md)
    structure: dict[str, list[tuple[str, str]]] = {
        "face-recognition-sdk": [],
        "liveness-detection-sdk": [],
        "id-document-recognition-sdk": [],
        "id-document-liveness-sdk": [],
    }
    hubs: dict[str, dict] = {}

    for item in about["repositories"]:
        name = item["name"]
        if name == "identixia-assets":
            continue
        rel = homepage_rel(item["homepage"])
        if not rel:
            print(f"SKIP non-docs homepage: {name} -> {item['homepage']}")
            continue
        # Hub section pages (no slash)
        if "/" not in rel:
            hubs[rel] = item
            build_product_page(owner=owner, item=item, rel=rel)
            continue
        section, leaf = rel.split("/", 1)
        if section not in structure:
            structure[section] = []
        path, label = build_product_page(owner=owner, item=item, rel=rel)
        structure[section].append((label, f"{leaf}.md"))
        print(f"OK {name} -> {path.relative_to(OUT.parent)}")

    # Supplementary doc pages under document recognition
    write_static_pages()
    structure["id-document-recognition-sdk"].extend(
        [
            ("Document result JSON", "document-result-json.md"),
            ("Document security check fields", "document-security-check-fields.md"),
        ]
    )

    for section, kids in structure.items():
        write_section_hub(section, kids, hubs.get(section), owner)

    write_welcome(list(structure.keys()))
    write_summary(structure)

    # Ensure gitbook-docs.yaml exists
    yaml_path = Path(__file__).resolve().parent / "gitbook-docs.yaml"
    if not yaml_path.is_file():
        yaml_path.write_text(
            "$schema: https://api.gitbook.com/gitbook-docs.yaml\n"
            "site:\n"
            "  title: Identixia Docs\n"
            "  structure:\n"
            "    - type: space\n"
            "      key: space-1\n"
            "      title: Identixia Docs\n"
            "      path: identixia-docs\n"
            "      default: true\n"
            "      content:\n"
            "        directory: ./identixia-docs\n",
            encoding="utf-8",
            newline="\n",
        )

    print(f"Wrote pages under {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
