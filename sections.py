"""Publish identixia-docs as three GitBook site sections.

GitBook sections are site navigation (gitbook-docs.yaml), not SUMMARY groups.
Each section is one space. The live space key ``space-1`` stays on Documentation.

The default section is served from the site root, so Documentation pages keep
https://docs.identixia.com/<page>. Developers and Guides use their section path.
The default space inside a section is opened without its own path.
"""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

import content_lib as C

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "identixia-docs"
DOCS = "https://docs.identixia.com"
REPO = ROOT.parent

DEVELOPERS = {
    "face-sdk/integration-guide.md",
    "face-sdk/reference.md",
    "face-sdk/android.md",
    "face-sdk/ios.md",
    "face-sdk/flutter.md",
    "face-sdk/react-native.md",
    "face-sdk/ionic-capacitor.md",
    "face-sdk/ionic-cordova.md",
    "face-sdk/windows.md",
    "face-sdk/linux-docker.md",
    "face-sdk/recognition-windows.md",
    "face-sdk/recognition-linux-docker.md",
    "face-sdk/recognition-android.md",
    "face-sdk/recognition-ios.md",
    "face-sdk/recognition-flutter.md",
    "face-sdk/recognition-react-native.md",
    "face-sdk/recognition-ionic-capacitor.md",
    "face-sdk/recognition-ionic-cordova.md",
    "face-sdk/liveness-android.md",
    "face-sdk/liveness-ios.md",
    "face-sdk/liveness-flutter.md",
    "face-sdk/liveness-react-native.md",
    "face-sdk/liveness-ionic-capacitor.md",
    "face-sdk/liveness-ionic-cordova.md",
    "face-sdk/liveness-windows.md",
    "face-sdk/liveness-linux-docker.md",
    "id-document-sdk/integration-guide.md",
    "id-document-sdk/reference.md",
    "id-document-sdk/android.md",
    "id-document-sdk/ios.md",
    "id-document-sdk/flutter.md",
    "id-document-sdk/react-native.md",
    "id-document-sdk/ionic-capacitor.md",
    "id-document-sdk/ionic-cordova.md",
    "id-document-sdk/windows.md",
    "id-document-sdk/linux-docker.md",
    "id-document-sdk/recognition-android.md",
    "id-document-sdk/recognition-ios.md",
    "id-document-sdk/recognition-flutter.md",
    "id-document-sdk/recognition-react-native.md",
    "id-document-sdk/recognition-ionic-capacitor.md",
    "id-document-sdk/recognition-ionic-cordova.md",
    "id-document-sdk/recognition-windows.md",
    "id-document-sdk/recognition-linux-docker.md",
    "id-document-sdk/liveness-android.md",
    "id-document-sdk/liveness-ios.md",
    "id-document-sdk/liveness-flutter.md",
    "id-document-sdk/liveness-react-native.md",
    "id-document-sdk/liveness-ionic-capacitor.md",
    "id-document-sdk/liveness-ionic-cordova.md",
    "id-document-sdk/liveness-windows.md",
    "id-document-sdk/liveness-linux-docker.md",
    "sdk-server/face-recognition.md",
    "sdk-server/face-liveness.md",
    "sdk-server/document-recognition.md",
    "sdk-server/document-liveness.md",
    "idv/api.md",
    "idv/company-webhooks.md",
    "idv/components-clients.md",
    "idv/client-android.md",
    "idv/client-ios.md",
    "idv/client-web.md",
    "idv/client-other.md",
    "idv/engines.md",
    "idv/engines-face.md",
    "idv/engines-document.md",
    "idv/license-protocol.md",
    "idv/license-admin.md",
    "idv/shared-packages.md",
}

GUIDES = {
    "idv/getting-started.md",
    "idv/quick-start.md",
    "idv/walkthrough.md",
    "idv/environment.md",
    "idv/initial-setup.md",
    "idv/project-structure.md",
    "idv/production.md",
    "idv/licensing.md",
    "request-a-license-and-support.md",
    "contact-us.md",
    "choose-a-product.md",
    "run-the-sample.md",
}

# Font Awesome names GitBook accepts in page frontmatter.
ICONS = {
    "README.md": "house",
    "recognition.md": "magnifying-glass",
    "liveness.md": "shield-halved",
    "full-product.md": "cubes",
    "full-mobile.md": "mobile-screen",
    "full-server.md": "server",
    "recognition-only.md": "crosshairs",
    "liveness-only.md": "eye",
    "liveness-only-mobile.md": "mobile-screen",
    "liveness-only-server.md": "server",
    "result-json.md": "brackets-curly",
    "security-fields.md": "lock",
    "integration-guide.md": "code",
    "reference.md": "book",
    "android.md": "mobile-screen",
    "ios.md": "mobile-screen",
    "flutter.md": "code",
    "react-native.md": "code",
    "ionic-capacitor.md": "bolt",
    "ionic-cordova.md": "bolt",
    "windows.md": "display",
    "linux-docker.md": "cube",
    "recognition-windows.md": "display",
    "recognition-linux-docker.md": "cube",
    "liveness-android.md": "shield",
    "liveness-ios.md": "shield",
    "liveness-windows.md": "shield",
    "liveness-linux-docker.md": "shield",
    "architecture.md": "diagram-project",
    "session-states.md": "list-ol",
    "components.md": "puzzle-piece",
    "platform.md": "building",
    "platform-console.md": "table-columns",
    "platform-server.md": "server",
    "company.md": "building",
    "company-admin.md": "user-gear",
    "company-backend.md": "gears",
    "api.md": "plug",
    "company-webhooks.md": "bell",
    "components-clients.md": "mobile-screen",
    "client-android.md": "mobile-screen",
    "client-ios.md": "mobile-screen",
    "client-web.md": "globe",
    "client-other.md": "puzzle-piece",
    "engines.md": "microchip",
    "engines-face.md": "user",
    "engines-document.md": "id-card",
    "license-protocol.md": "key",
    "license-admin.md": "key",
    "shared-packages.md": "boxes-stacked",
    "getting-started.md": "flag",
    "quick-start.md": "rocket",
    "walkthrough.md": "route",
    "environment.md": "sliders",
    "initial-setup.md": "wrench",
    "project-structure.md": "folder-tree",
    "production.md": "industry",
    "licensing.md": "key",
    "request-a-license-and-support.md": "envelope",
    "contact-us.md": "comments",
    "choose-a-product.md": "compass",
    "run-the-sample.md": "play",
    "face-recognition.md": "magnifying-glass",
    "face-liveness.md": "shield-halved",
    "document-recognition.md": "id-card",
    "document-liveness.md": "shield-halved",
}

SUMMARY_ICON = {
    "README.md": "🏠",
    "recognition.md": "🔍",
    "liveness.md": "🛡️",
    "full-product.md": "📦",
    "full-mobile.md": "📱",
    "full-server.md": "🖥️",
    "recognition-only.md": "🎯",
    "liveness-only.md": "👁️",
    "liveness-only-mobile.md": "📱",
    "liveness-only-server.md": "🖥️",
    "result-json.md": "📋",
    "security-fields.md": "🔐",
    "integration-guide.md": "💻",
    "reference.md": "📚",
    "android.md": "🤖",
    "ios.md": "🍎",
    "flutter.md": "💙",
    "react-native.md": "⚛️",
    "ionic-capacitor.md": "⚡",
    "ionic-cordova.md": "🔌",
    "windows.md": "🪟",
    "linux-docker.md": "🐳",
    "recognition-windows.md": "🪟",
    "recognition-linux-docker.md": "🐳",
    "liveness-android.md": "🤖",
    "liveness-ios.md": "🍎",
    "liveness-windows.md": "🪟",
    "liveness-linux-docker.md": "🐳",
    "architecture.md": "🏗️",
    "session-states.md": "🔁",
    "components.md": "🧩",
    "platform.md": "🏢",
    "platform-console.md": "🎛️",
    "platform-server.md": "🖥️",
    "company.md": "🏛️",
    "company-admin.md": "👤",
    "company-backend.md": "⚙️",
    "api.md": "🔌",
    "company-webhooks.md": "🔔",
    "components-clients.md": "📱",
    "client-android.md": "🤖",
    "client-ios.md": "🍎",
    "client-web.md": "🌐",
    "client-other.md": "🧩",
    "engines.md": "🧠",
    "engines-face.md": "👤",
    "engines-document.md": "🪪",
    "license-protocol.md": "🔑",
    "license-admin.md": "🔑",
    "shared-packages.md": "📦",
    "getting-started.md": "🚩",
    "quick-start.md": "🚀",
    "walkthrough.md": "🧭",
    "environment.md": "🎚️",
    "initial-setup.md": "🛠️",
    "project-structure.md": "📁",
    "production.md": "🏭",
    "licensing.md": "🔑",
    "request-a-license-and-support.md": "✉️",
    "contact-us.md": "💬",
    "choose-a-product.md": "🧭",
    "run-the-sample.md": "▶️",
    "face-recognition.md": "🔍",
    "face-liveness.md": "🛡️",
    "document-recognition.md": "🪪",
    "document-liveness.md": "🛡️",
}

LINK_RE = re.compile(r"(\]\(|url=\"|include \")([^\"\)\s]+)(\"|\)|)")
ASSET_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf"}


def section_of(rel: str) -> str:
    if rel in GUIDES or Path(rel).name in {"choose-a-product.md", "run-the-sample.md"}:
        return "guides"
    if rel in DEVELOPERS:
        return "developers"
    return "documentation"


def public_url(rel: str) -> str:
    """Public URL. Default section omits its slug; default space omits its path."""
    section = section_of(rel)
    stem = rel[:-3] if rel.endswith(".md") else rel
    if stem.endswith("/README"):
        stem = stem[: -len("/README")]
    prefix = "" if section == "documentation" else f"/{section}"
    if not stem or stem == "README":
        return f"{DOCS}{prefix}" if prefix else DOCS
    return f"{DOCS}{prefix}/{stem}"


def _url_variants(rel: str) -> list[str]:
    stem = rel[:-3] if rel.endswith(".md") else rel
    variants = [f"{DOCS}/{stem}"]
    if stem.endswith("/README"):
        folder = stem[: -len("/README")]
        variants.append(f"{DOCS}/{folder}")
        variants.append(f"{DOCS}/{folder}/")
    return variants


def moved_replacements() -> list[tuple[re.Pattern[str], str]]:
    pairs: list[tuple[str, str]] = []
    for rel in DEVELOPERS | GUIDES:
        target = public_url(rel)
        for old in _url_variants(rel):
            if old.rstrip("/") == target.rstrip("/"):
                continue
            pairs.append((old, target))
    pairs.sort(key=lambda item: len(item[0]), reverse=True)
    compiled: list[tuple[re.Pattern[str], str]] = []
    for old, target in pairs:
        compiled.append((re.compile(re.escape(old) + r"(?![A-Za-z0-9_-])"), target))
    return compiled


def rewrite_absolute(text: str, compiled: list[tuple[re.Pattern[str], str]]) -> str:
    for pattern, target in compiled:
        text = pattern.sub(lambda _m, dest=target: dest, text)
    return text


def ensure_icon(text: str, icon: str) -> str:
    if text.startswith("---\n") or text.startswith("---\r\n"):
        end = text.find("\n---", 3)
        if end != -1:
            front = text[:end]
            if re.search(r"(?m)^icon:", front):
                front = re.sub(r"(?m)^icon:.*$", f"icon: {icon}", front, count=1)
            else:
                front = front + f"\nicon: {icon}"
            return front + text[end:]
    return f"---\nicon: {icon}\n---\n\n{text}"


def _is_asset(link: str) -> bool:
    path = link.split("#", 1)[0].split("?", 1)[0]
    if ".gitbook/" in path.replace("\\", "/"):
        return True
    return Path(path).suffix.lower() in ASSET_EXT


def _target_rel(from_rel: str, link: str) -> str | None:
    raw = link.split("#", 1)[0].split("?", 1)[0].strip()
    if not raw or raw.startswith(("#", "http://", "https://", "mailto:")):
        return None
    if _is_asset(raw):
        return None
    path = raw
    if path.endswith("/"):
        path += "README.md"
    base = (SRC / from_rel).parent
    target = (base / path).resolve()
    try:
        rel = target.relative_to(SRC.resolve()).as_posix()
    except ValueError:
        return None
    if not rel.endswith(".md"):
        readme = SRC / rel / "README.md"
        if readme.is_file():
            return f"{rel}/README.md"
        return None
    if not (SRC / rel).is_file() and rel not in GUIDES:
        return None
    return rel


def rewrite_relative(text: str, from_rel: str) -> str:
    here = section_of(from_rel)

    def repl(match: re.Match[str]) -> str:
        prefix, link, suffix = match.group(1), match.group(2), match.group(3)
        anchor = ""
        if "#" in link:
            link, anchor = link.split("#", 1)
            anchor = "#" + anchor
        target = _target_rel(from_rel, link)
        if target is None or section_of(target) == here:
            return match.group(0)
        return f"{prefix}{public_url(target)}{anchor}{suffix}"

    return LINK_RE.sub(repl, text)


PATH_EMOJI = {
    "face-sdk/README.md": "👤",
    "id-document-sdk/README.md": "🪪",
    "idv/README.md": "🏢",
    "sdk-server/README.md": "🌐",
    "developers/README.md": "💻",
}

PATH_ICON = {
    "face-sdk/README.md": "user",
    "id-document-sdk/README.md": "id-card",
    "idv/README.md": "building",
    "sdk-server/README.md": "server",
}


def item(rel: str, label: str, indent: int = 0) -> str:
    pad = "  " * indent
    return f"{pad}* [{label}]({rel})"


# Developer sidebar. Each platform page is one of three SDKs.
_FACE_KINDS = (
    ("Face recognition and liveness", ""),
    ("Face recognition", "recognition-"),
    ("Face liveness detection", "liveness-"),
)
_DOC_KINDS = (
    ("ID document recognition and liveness", ""),
    ("ID document recognition and OCR", "recognition-"),
    ("ID document liveness detection", "liveness-"),
)
_PLATFORMS = (
    ("android", "Android"),
    ("ios", "iOS"),
    ("flutter", "Flutter"),
    ("react-native", "React Native"),
    ("ionic-capacitor", "Ionic Capacitor"),
    ("ionic-cordova", "Ionic Cordova"),
    ("windows", "Windows"),
    ("linux-docker", "Linux and Docker"),
)


def _platform_leaf(prefix: str, leaf: str) -> str:
    if prefix:
        return f"{prefix}{leaf}.md"
    return f"{leaf}.md"


def developer_product_nav(section: str, kinds: tuple[tuple[str, str], ...], titles: dict[str, str]) -> list[str]:
    """Mobile, then server. Native and cross-platform under mobile. Three SDKs under each platform."""
    lines: list[str] = []

    def add(rel: str, label: str, indent: int) -> None:
        lines.append(item(f"{section}/{rel}", label, indent))

    add("mobile-sdks.md", titles["mobile"], 0)
    add("native-mobile.md", titles["native"], 1)
    for leaf, name in _PLATFORMS[:2]:
        add(f"{leaf}-sdks.md", titles["platform"].format(name=name), 2)
        for label, prefix in kinds:
            add(_platform_leaf(prefix, leaf), label, 3)
    add("cross-platform.md", titles["cross"], 1)
    for leaf, name in _PLATFORMS[2:6]:
        add(f"{leaf}-sdks.md", titles["platform"].format(name=name), 2)
        for label, prefix in kinds:
            add(_platform_leaf(prefix, leaf), label, 3)
    add("server-apis.md", titles["server"], 0)
    for leaf, name in _PLATFORMS[6:]:
        add(f"{leaf}-sdks.md", titles["api"].format(name=name), 1)
        for label, prefix in kinds:
            add(_platform_leaf(prefix, leaf), label, 2)
    return lines


_FACE_TITLES = {
    "mobile": "Mobile face recognition SDKs",
    "native": "Android and iOS face SDKs",
    "cross": "Flutter, React Native, and Ionic face SDKs",
    "server": "Windows and Linux face recognition APIs",
    "platform": "{name} face recognition SDK",
    "api": "{name} face recognition API",
}
_DOC_TITLES = {
    "mobile": "Mobile ID document SDKs",
    "native": "Android and iOS ID document SDKs",
    "cross": "Flutter, React Native, and Ionic ID document SDKs",
    "server": "Windows and Linux ID document APIs",
    "platform": "{name} ID document SDK",
    "api": "{name} ID document API",
}


# IDV pages stay in the repo. They are omitted from the sidebar until the project is ready.
IDV_IN_NAV = False


def write_summaries() -> None:
    documentation = "\n".join(
        [
            "# Table of contents",
            "",
            item("README.md", "Welcome"),
            "",
            "## Face",
            "",
            item("face-sdk/README.md", "Introduction"),
            item("face-sdk/recognition.md", "Recognition"),
            item("face-sdk/liveness.md", "Liveness"),
            "",
            "## ID Document",
            "",
            item("id-document-sdk/README.md", "Introduction"),
            item("id-document-sdk/recognition.md", "Recognition"),
            item("id-document-sdk/liveness.md", "Liveness"),
            item("id-document-sdk/result-json.md", "Result format"),
            item("id-document-sdk/security-fields.md", "Security checks"),
            "",
            *(
                [
                    "## IDV",
                    "",
                    item("idv/README.md", "Overview"),
                    item("idv/architecture.md", "Architecture", 1),
                    item("idv/session-states.md", "Session states", 1),
                    item("idv/components.md", "Components"),
                    item("idv/reference.md", "Reference"),
                    item("idv/platform.md", "Platform"),
                    item("idv/platform-server.md", "IDV server", 1),
                    item("idv/platform-console.md", "Identity Console", 1),
                    item("idv/company.md", "Company"),
                    item("idv/company-backend.md", "Company backend", 1),
                    item("idv/company-admin.md", "Company Admin", 1),
                    "",
                ]
                if IDV_IN_NAV
                else []
            ),
            "## API",
            "",
            item("sdk-server/README.md", "SDK Server"),
            "",
        ]
    )
    developers = "\n".join(
        [
            "# Table of contents",
            "",
            "* [Start here](README.md)",
            "",
            "## Face recognition and liveness detection",
            "",
            item("face-sdk/integration-guide.md", "Face recognition SDK integration guide"),
            item("face-sdk/reference.md", "Face recognition SDK platform index"),
            *developer_product_nav("face-sdk", _FACE_KINDS, _FACE_TITLES),
            "",
            "## ID document recognition and liveness detection",
            "",
            item("id-document-sdk/integration-guide.md", "ID document SDK integration guide"),
            item("id-document-sdk/reference.md", "ID document SDK platform index"),
            *developer_product_nav("id-document-sdk", _DOC_KINDS, _DOC_TITLES),
            "",
            *(
                [
                    "## IDV",
                    "",
                    item("idv/api.md", "Session API"),
                    item("idv/company-webhooks.md", "Webhooks"),
                    item("idv/components-clients.md", "Clients"),
                    item("idv/client-android.md", "Android", 1),
                    item("idv/client-ios.md", "iOS", 1),
                    item("idv/client-web.md", "Web", 1),
                    item("idv/client-other.md", "Other", 1),
                    item("idv/engines.md", "Engines"),
                    item("idv/engines-face.md", "Face", 1),
                    item("idv/engines-document.md", "Documents", 1),
                    item("idv/shared-packages.md", "Shared packages"),
                    item("idv/license-protocol.md", "License protocol"),
                    item("idv/license-admin.md", "License admin"),
                    "",
                ]
                if IDV_IN_NAV
                else []
            ),
            "## API",
            "",
            item("sdk-server/face-recognition.md", "Face recognition"),
            item("sdk-server/face-liveness.md", "Face liveness"),
            item("sdk-server/document-recognition.md", "Document recognition"),
            item("sdk-server/document-liveness.md", "Document liveness"),
            "",
        ]
    )
    guides = "\n".join(
        [
            "# Table of contents",
            "",
            "* [Guides](README.md)",
            "",
            "## Choose and run",
            "",
            item("choose-a-product.md", "Choose a product"),
            item("run-the-sample.md", "Run the sample"),
            "",
            *(
                [
                    "## IDV first run",
                    "",
                    item("idv/getting-started.md", "Getting started"),
                    item("idv/quick-start.md", "Quick start"),
                    item("idv/walkthrough.md", "Walkthrough"),
                    "",
                    "## IDV project",
                    "",
                    item("idv/project-structure.md", "Project structure"),
                    item("idv/environment.md", "Environment"),
                    item("idv/initial-setup.md", "Initial setup"),
                    item("idv/production.md", "Production"),
                    "",
                ]
                if IDV_IN_NAV
                else []
            ),
            "## License and support",
            "",
            *(
                [item("idv/licensing.md", "Licensing")]
                if IDV_IN_NAV
                else []
            ),
            item("request-a-license-and-support.md", "Request a license"),
            item("contact-us.md", "Contact"),
            "",
        ]
    )
    (ROOT / "documentation" / "SUMMARY.md").write_text(documentation + "\n", encoding="utf-8", newline="\n")
    (ROOT / "developers" / "SUMMARY.md").write_text(developers + "\n", encoding="utf-8", newline="\n")
    (ROOT / "guides" / "SUMMARY.md").write_text(guides + "\n", encoding="utf-8", newline="\n")


def write_gitbook_yaml(directory: Path) -> None:
    (directory / ".gitbook.yaml").write_text(
        "root: .\n\nstructure:\n  readme: README.md\n  summary: SUMMARY.md\n",
        encoding="utf-8",
        newline="\n",
    )


def write_site_yaml() -> None:
    text = """$schema: https://api.gitbook.com/gitbook-docs.yaml
site:
  title: Identixia Docs
  structure:
    - type: section
      key: section-documentation
      title: Documentation
      path: documentation
      icon: book-open
      default: true
      description: What the products do, what you need, and what the sample returns.
      children:
        - type: space
          key: space-1
          title: Documentation
          path: content
          default: true
          content:
            directory: ./documentation
    - type: section
      key: section-developers
      title: Developers
      path: developers
      icon: code
      description: How to add the SDK to your app and call the kit.
      children:
        - type: space
          key: space-developers
          title: Developers
          path: content
          default: true
          content:
            directory: ./developers
    - type: section
      key: section-guides
      title: Guides
      path: guides
      icon: compass
      description: Choose a product, run the sample, request a license, and contact support.
      children:
        - type: space
          key: space-guides
          title: Guides
          path: content
          default: true
          content:
            directory: ./guides
"""
    (ROOT / "gitbook-docs.yaml").write_text(text, encoding="utf-8", newline="\n")


WELCOME_HINT = """{% hint style="info" %}
This site has three sections. **Documentation** is what the product does and what a sample returns. [Developers](https://docs.identixia.com/developers) is how to put the kit in your app. [Guides](https://docs.identixia.com/guides) is how to choose a product, run a sample, and request a license.
{% endhint %}

"""


def _landing(title: str, description: str, icon: str, body: str) -> str:
    return (
        "---\n"
        f"description: {description}\n"
        f"icon: {icon}\n"
        "---\n\n"
        f"# {title}\n\n"
        f"{body.strip()}\n"
    )


def footer_include(rel: str) -> str:
    depth = rel.count("/")
    path = ("../" * depth) + ".gitbook/includes/footer.md"
    if depth == 0:
        path = "./" + path
    return f'\n\n{{% include "{path}" %}}\n'


def append_footer(text: str, rel: str) -> str:
    if "includes/footer.md" in text:
        return text
    return text.rstrip() + footer_include(rel)


_REPO_PLATFORM = {
    "android": "Android",
    "ios": "iOS",
    "flutter": "Flutter",
    "react-native": "React-Native",
    "ionic-capacitor": "Ionic-Capacitor",
    "ionic-cordova": "Ionic-Cordova",
    "windows": "Windows",
    "linux-docker": "Docker",
}


def _catalog_page(title: str, description: str, icon: str, body: str) -> str:
    return (
        "---\n"
        "description: >-\n"
        f"  {description}\n"
        f"icon: {icon}\n"
        "---\n\n"
        f"# {title}\n\n"
        f"{body.strip()}\n"
    )


def _kit_rows(kinds: tuple[tuple[str, str], ...], repos: tuple[tuple[str, str], ...], leaf: str) -> str:
    suffix = _REPO_PLATFORM[leaf]
    rows = []
    for (label, prefix), (repo_prefix, repo_kind) in zip(kinds, repos):
        if repo_kind != prefix:
            raise SystemExit(f"catalog mismatch {label}")
        guide = _platform_leaf(prefix, leaf)
        repo = f"{repo_prefix}{suffix}"
        rows.append(
            f"| {label} | [`{repo}`](https://github.com/identixia-IDV/{repo}) | [{label}]({guide}) |"
        )
    return "\n".join(
        [
            "| SDK | Repository | Integration guide |",
            "| --- | --- | --- |",
            *rows,
        ]
    )


def write_developer_groups() -> None:
    """Parent pages for the Developers sidebar. GitBook only nests links under a real page."""
    face_repos = (
        ("FaceRecognition-LivenessDetection-", ""),
        ("FaceRecognition-", "recognition-"),
        ("FaceLivenessDetection-", "liveness-"),
    )
    doc_repos = (
        ("ID-Document-Recognition-Liveness-Detection-", ""),
        ("ID-Document-Recognition-", "recognition-"),
        ("ID-Document-Liveness-Detection-", "liveness-"),
    )
    products = (
        (
            "face-sdk",
            _FACE_KINDS,
            face_repos,
            _FACE_TITLES,
            "face recognition and face liveness detection",
            "Face recognition compares enrolled templates. Face liveness detection checks a color face image for presentation attacks and deepfakes. The combined product includes both when the license does.",
        ),
        (
            "id-document-sdk",
            _DOC_KINDS,
            doc_repos,
            _DOC_TITLES,
            "ID document recognition and document liveness detection",
            "Document recognition reads printed fields, the machine-readable zone, and supported barcodes. Document liveness detection checks whether the capture looks like a physical document. The combined product includes both when the license does.",
        ),
    )
    groups = (
        ("mobile-sdks.md", "mobile", "mobile-screen", _PLATFORMS[:6], "native-mobile.md", "cross-platform.md"),
        ("native-mobile.md", "native", "mobile-screen", _PLATFORMS[:2], None, None),
        ("cross-platform.md", "cross", "code", _PLATFORMS[2:6], None, None),
        ("server-apis.md", "server", "server", _PLATFORMS[6:], None, None),
    )
    root = ROOT / "developers"
    for section, kinds, repos, titles, product, about in products:
        for leaf, name in _PLATFORMS:
            title_key = "api" if leaf in {"windows", "linux-docker"} else "platform"
            title = titles[title_key].format(name=name)
            surface = "API" if title_key == "api" else "SDK"
            description = f"Integrate Identixia {product} with the {name} {surface}. Choose the combined kit, the recognition kit, or the liveness kit."
            body = "\n".join(
                [
                    about,
                    "",
                    "Choose the repository that matches the license you have.",
                    "",
                    _kit_rows(kinds, repos, leaf),
                ]
            )
            path = root / section / f"{leaf}-sdks.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(_catalog_page(title, description, "mobile-screen" if title_key == "platform" else "server", body), encoding="utf-8", newline="\n")
        for filename, key, icon, platforms, left, right in groups:
            title = titles[key]
            names = [name for _, name in platforms]
            if len(names) == 1:
                listed = names[0]
            elif len(names) == 2:
                listed = f"{names[0]} and {names[1]}"
            else:
                listed = ", ".join(names[:-1]) + f", and {names[-1]}"
            noun = "APIs" if key == "server" else "SDKs"
            if key == "server":
                listed = "Windows, Linux, and Docker"
            description = f"Identixia {product} {noun} for {listed}."
            parts = [about, ""]
            if left and right:
                parts.append(f"- [{titles['native']}]({left})")
                parts.append(f"- [{titles['cross']}]({right})")
                parts.append("")
            for leaf, name in platforms:
                child = titles["api" if leaf in {"windows", "linux-docker"} else "platform"].format(name=name)
                parts.append(f"## {child}")
                parts.append("")
                parts.append(_kit_rows(kinds, repos, leaf))
                parts.append("")
            path = root / section / filename
            path.write_text(_catalog_page(title, description, icon, "\n".join(parts)), encoding="utf-8", newline="\n")


def write_extra_pages() -> None:
    (ROOT / "developers" / "README.md").write_text(
        _landing(
            "Developers",
            "Integrate Identixia on mobile, desktop, and your own server.",
            "code",
            """
Add the SDK to your own application in this order.

{% stepper %}
{% step %}
### Open the integration guide
Start with [Face](face-sdk/integration-guide.md) or [ID documents](id-document-sdk/integration-guide.md). The guide names the repository for the license you have.
{% endstep %}
{% step %}
### Download the runtime
Clone that repository and run `python scripts/get_runtime.py`. Native libraries and database packs are on GitHub Releases. They are not in git.
{% endstep %}
{% step %}
### Activate, then call the kit
Activate the license before initialization. Mobile calls run on a background thread. Server calls use the HTTP routes on the platform page.
{% endstep %}
{% endstepper %}

<table data-view="cards">
  <thead>
    <tr>
      <th>Start from the product you licensed</th>
      <th data-card-target data-type="content-ref" data-hidden>Open</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Face</strong> recognition and liveness SDK integration for mobile apps and servers.</td>
      <td><a href="face-sdk/integration-guide.md">Face integration guide</a></td>
    </tr>
    <tr>
      <td><strong>ID document</strong> capture, text recognition, MRZ reading, and barcode extraction.</td>
      <td><a href="id-document-sdk/integration-guide.md">Document integration guide</a></td>
    </tr>
    <tr>
      <td><strong>HTTP API</strong> on Windows or Docker.</td>
      <td><a href="sdk-server/face-recognition.md">Face recognition API</a></td>
    </tr>
  </tbody>
</table>

{% columns %}
{% column %}
What the product returns is in [Documentation](https://docs.identixia.com).
{% endcolumn %}
{% column %}
Choosing a repository, running a sample, and requesting a license are in [Guides](https://docs.identixia.com/guides).
{% endcolumn %}
{% endcolumns %}

<a href="https://docs.identixia.com/guides/run-the-sample" class="button primary" data-icon="play">Run the sample</a>
<a href="https://github.com/identixia-IDV" class="button secondary" data-icon="github">Repositories</a>
""",
        ),
        encoding="utf-8",
        newline="\n",
    )
    (ROOT / "guides" / "README.md").write_text(
        _landing(
            "Guides",
            "Choose a product, run the sample, and activate a license.",
            "compass",
            """
{% hint style="info" %}
Use this section to understand the products, run a sample, and request a license. API calls stay in [Developers](https://docs.identixia.com/developers).
{% endhint %}

{% stepper %}
{% step %}
### Choose a product
Open [Choose a product](choose-a-product.md) and match the repository to the license flags you need.
{% endstep %}
{% step %}
### Run the sample
Follow [Run the sample](run-the-sample.md). Android and iOS are separate setups.
{% endstep %}
{% step %}
### Request a license
Send the machine code or application id from the sample on [Request a license](request-a-license-and-support.md).
{% endstep %}
{% step %}
### Contact
License requests and technical support are on [Contact](contact-us.md).
{% endstep %}
{% endstepper %}

<table data-view="cards">
  <thead>
    <tr>
      <th>Guide</th>
      <th data-card-target data-type="content-ref" data-hidden>Open</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Match the repository to the license.</td>
      <td><a href="choose-a-product.md">Choose a product</a></td>
    </tr>
    <tr>
      <td>Android and iOS commands for each sample.</td>
      <td><a href="run-the-sample.md">Run the sample</a></td>
    </tr>
    <tr>
      <td>Send an application id or machine code.</td>
      <td><a href="request-a-license-and-support.md">Request a license</a></td>
    </tr>
    <tr>
      <td>Email, phone, and Telegram.</td>
      <td><a href="contact-us.md">Contact</a></td>
    </tr>
  </tbody>
</table>
""",
        ),
        encoding="utf-8",
        newline="\n",
    )
    (ROOT / "guides" / "choose-a-product.md").write_text(
        _landing(
            "Choose a product",
            "Match the repository to the functions your license includes.",
            "compass",
            """
Use the license flags on the product introduction, then clone the repository in that row.

## Face

Recognition and liveness. License flags `recognition` and `liveness`. Server port **14103**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/face-sdk/android) | [`FaceRecognition-LivenessDetection-Android`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/face-sdk/ios) | [`FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/face-sdk/flutter) | [`FaceRecognition-LivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/face-sdk/react-native) | [`FaceRecognition-LivenessDetection-React-Native`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/face-sdk/ionic-capacitor) | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/face-sdk/ionic-cordova) | [`FaceRecognition-LivenessDetection-Ionic-Cordova`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/face-sdk/windows) | [`FaceRecognition-LivenessDetection-Windows`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/linux-docker) | [`FaceRecognition-LivenessDetection-Docker`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) |

Recognition without a liveness score. License flag `recognition`. These builds do not return a liveness score. Server port **14104**. Do not call `/api/face/liveness`.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/face-sdk/recognition-android) | [`FaceRecognition-Android`](https://github.com/identixia-IDV/FaceRecognition-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/face-sdk/recognition-ios) | [`FaceRecognition-iOS`](https://github.com/identixia-IDV/FaceRecognition-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/face-sdk/recognition-flutter) | [`FaceRecognition-Flutter`](https://github.com/identixia-IDV/FaceRecognition-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/face-sdk/recognition-react-native) | [`FaceRecognition-React-Native`](https://github.com/identixia-IDV/FaceRecognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/face-sdk/recognition-ionic-capacitor) | [`FaceRecognition-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceRecognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/face-sdk/recognition-ionic-cordova) | [`FaceRecognition-Ionic-Cordova`](https://github.com/identixia-IDV/FaceRecognition-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/face-sdk/recognition-windows) | [`FaceRecognition-Windows`](https://github.com/identixia-IDV/FaceRecognition-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/recognition-linux-docker) | [`FaceRecognition-Docker`](https://github.com/identixia-IDV/FaceRecognition-Docker) |

Presentation-attack and deepfake scores. License flag `liveness`. These builds do not enroll a gallery and do not run 1:N search. Server port **14105**. Routes: `POST /api/face/liveness` and `POST /api/face/deepfake`. Report REAL only when both checks pass.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/face-sdk/liveness-android) | [`FaceLivenessDetection-Android`](https://github.com/identixia-IDV/FaceLivenessDetection-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/face-sdk/liveness-ios) | [`FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/face-sdk/liveness-flutter) | [`FaceLivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceLivenessDetection-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/face-sdk/liveness-react-native) | [`FaceLivenessDetection-React-Native`](https://github.com/identixia-IDV/FaceLivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/face-sdk/liveness-ionic-capacitor) | [`FaceLivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/face-sdk/liveness-ionic-cordova) | [`FaceLivenessDetection-Ionic-Cordova`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/face-sdk/liveness-windows) | [`FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/liveness-linux-docker) | [`FaceLivenessDetection-Docker`](https://github.com/identixia-IDV/FaceLivenessDetection-Docker) |

## ID document

Recognition and authenticity. License flags `recognition` and `authenticity`. Server port **14102**. `POST /api/document/process` returns OCR and authenticity when that flag is on. `POST /api/document/recognition` returns OCR, MRZ, and barcode. `POST /api/document/liveness` returns authenticity.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/id-document-sdk/android) | [`ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/id-document-sdk/ios) | [`ID-Document-Recognition-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/id-document-sdk/flutter) | [`ID-Document-Recognition-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/id-document-sdk/react-native) | [`ID-Document-Recognition-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/id-document-sdk/ionic-capacitor) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/id-document-sdk/ionic-cordova) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/id-document-sdk/windows) | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/linux-docker) | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) |

OCR, MRZ, and barcode without document liveness. License flag `recognition`. Server port **14106**. This build does not serve `/api/document/liveness`.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/id-document-sdk/recognition-android) | [`ID-Document-Recognition-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/id-document-sdk/recognition-ios) | [`ID-Document-Recognition-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/id-document-sdk/recognition-flutter) | [`ID-Document-Recognition-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/id-document-sdk/recognition-react-native) | [`ID-Document-Recognition-React-Native`](https://github.com/identixia-IDV/ID-Document-Recognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/id-document-sdk/recognition-ionic-capacitor) | [`ID-Document-Recognition-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/id-document-sdk/recognition-ionic-cordova) | [`ID-Document-Recognition-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Recognition-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/id-document-sdk/recognition-windows) | [`ID-Document-Recognition-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/recognition-linux-docker) | [`ID-Document-Recognition-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Docker) |

Screen, printout, and substitution checks. License flag `authenticity`. No MRZ, barcode, or visual fields. Server port **14107**. `POST /api/document/liveness` takes `images` entries `{image, page_idx}`. This server does not expose `/api/document/process`.

| Platform | Where to start | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/id-document-sdk/liveness-android) | [`ID-Document-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/id-document-sdk/liveness-ios) | [`ID-Document-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/id-document-sdk/liveness-flutter) | [`ID-Document-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/id-document-sdk/liveness-react-native) | [`ID-Document-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/id-document-sdk/liveness-ionic-capacitor) | [`ID-Document-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/id-document-sdk/liveness-ionic-cordova) | [`ID-Document-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/id-document-sdk/liveness-windows) | [`ID-Document-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/liveness-linux-docker) | [`ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) |

## After you pick a repository

1. [Run the sample](run-the-sample.md) until it shows **Ready**.
2. [Request a license](request-a-license-and-support.md) for the sample application id or for your own application id or machine code.
3. [Contact](contact-us.md) if you need a key or help with a platform.

<a href="https://docs.identixia.com/developers" class="button primary" data-icon="code">Open Developers</a>
""",
        ),
        encoding="utf-8",
        newline="\n",
    )
    (ROOT / "guides" / "run-the-sample.md").write_text(
        _landing(
            "Run the sample",
            "Android and iOS commands for the Identixia sample apps.",
            "play",
            """
{% hint style="info" %}
Clone the product repository, then open the tab for your stack. Android and iOS are separate setups. On macOS use `python3`.
{% endhint %}

```bash
python scripts/get_runtime.py
```

{% tabs %}
{% tab title="Android" %}
Requirements from the sample: Android Studio, JDK **17**, minSdk **24**, ABIs `arm64-v8a` and `armeabi-v7a`. Use a physical **arm64** phone for the camera.

```bash
python scripts/get_runtime.py
```

Open the Android project in Android Studio and run it. The sample prints the application id to send with a license request. Wait until status shows **Ready**.
{% endtab %}

{% tab title="iOS" %}
Requirements from the sample: a Mac, Xcode, and a physical iPhone. Deployment target is iOS **13+**. Open the `.xcworkspace`, select your team, and run. The sample prints the bundle id to send with a license request. Wait until status shows **Ready**.
{% endtab %}

{% tab title="Flutter" %}
From the repository root:

```bash
dart run tool/bootstrap.dart
flutter run -d android
```

iOS, from a Mac, on a physical device (Flutter 3.44 or newer):

```bash
cd example/ios && pod install && cd ..
flutter run -d ios
```
{% endtab %}

{% tab title="React Native" %}
{% hint style="warning" %}
These samples are Yarn workspaces. They do not run in Expo Go.
{% endhint %}

```bash
yarn
cd example && yarn android
```

iOS, from a Mac:

```bash
cd example/ios && pod install && cd ..
yarn ios --device
```
{% endtab %}

{% tab title="Ionic Capacitor" %}
Install and build the plugin before the example app. The example depends on the plugin in the parent folder.

```bash
npm install && npm run build
cd example && npm install && npm run sync
npm run android
```

`npm run android` and `npm run ios` open the native IDE. Press Run there. For iOS, run `npm run ios` on a Mac after `npm run sync`.
{% endtab %}

{% tab title="Ionic Cordova" %}
```bash
npm run setup:android
npm run android
```

iOS, from a Mac:

```bash
npm run setup:ios
npm run ios
```
{% endtab %}
{% tab title="Windows / Docker" %}
Same steps for a Windows service and a Docker build of the same product. They share one port.

1. Clone the Windows or Docker repository.
2. On a host install, run `python scripts/get_runtime.py`. A Docker Hub image already contains the runtime.
3. Copy `.env.example` to `.env`, install the Python dependencies, then start with `python run_server.py` (`python3` on macOS or Linux) or Docker Compose.
4. Read `GET /api/machinecode`, request a license, then `POST /api/activate`.
5. Call the process route for that product. Ports are on [SDK Server](https://docs.identixia.com/sdk-server).
{% endtab %}
{% endtabs %}

{% hint style="success" %}
Wait until the sample shows **Ready**, then open the capture, enroll, or recognize action that the product includes.
{% endhint %}
""",
        ),
        encoding="utf-8",
        newline="\n",
    )
    write_developer_groups()


def _copy_space(name: str, compiled: list[tuple[re.Pattern[str], str]]) -> int:
    dest_root = ROOT / name
    count = 0
    for path in SRC.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(SRC).as_posix()
        if rel == "SUMMARY.md" or rel.startswith(".gitbook.yaml"):
            continue
        if rel.endswith(".md") and not rel.startswith(".gitbook/"):
            if section_of(rel) != name:
                continue
        elif rel.startswith(".gitbook/includes/"):
            pass
        else:
            continue
        target = dest_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if rel.endswith(".md") and not rel.startswith(".gitbook/"):
            text = path.read_text(encoding="utf-8")
            text = C.rewrite_asset_srcs(text)
            text = rewrite_relative(text, rel)
            text = rewrite_absolute(text, compiled)
            icon = PATH_ICON.get(rel) or ICONS.get(path.name, "file")
            if rel == "README.md" and name == "documentation":
                icon = "house"
                if 'data-view="cards"' not in text and WELCOME_HINT.strip() not in text:
                    if text.startswith("---"):
                        end = text.find("\n---", 3)
                        if end != -1:
                            insert_at = end + 4
                            if text[insert_at : insert_at + 1] == "\n":
                                insert_at += 1
                            text = text[:insert_at] + "\n" + WELCOME_HINT + text[insert_at:]
                    else:
                        text = WELCOME_HINT + text
            text = ensure_icon(text, icon)
            target.write_text(text, encoding="utf-8", newline="\n")
            count += 1
        else:
            shutil.copy2(path, target)
    return count


def rewrite_repo_links(compiled: list[tuple[re.Pattern[str], str]]) -> int:
    changed = 0
    roots = [
        REPO / "repositories",
        REPO / "catalog",
        REPO / "IDV",
        REPO / "scripts",
        REPO / "templates",
        REPO / "scaffolds",
        REPO / "hugging_face",
        REPO / "clients",
        REPO / "platform",
        REPO / ".github",
        REPO / "README.md",
    ]
    skip_dirs = {
        "node_modules",
        "dist",
        "build",
        ".git",
        "Pods",
        ".gradle",
        "android",
        "ios",
        "example",
        "Identixia",
    }
    skip = {SRC.resolve(), (ROOT / "documentation").resolve(), (ROOT / "developers").resolve(), (ROOT / "guides").resolve()}

    def walk(root: Path):
        if root.is_file():
            yield root
            return
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [name for name in dirnames if name not in skip_dirs]
            for name in filenames:
                yield Path(dirpath) / name

    for root in roots:
        files = list(walk(root)) if root.exists() else []
        for path in files:
            if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".py", ".yaml", ".yml"}:
                continue
            if any(parent in skip for parent in path.resolve().parents) or path.resolve() in skip:
                continue
            original = path.read_text(encoding="utf-8")
            updated = rewrite_absolute(original, compiled)
            if updated != original:
                path.write_text(updated, encoding="utf-8", newline="\n")
                changed += 1
    return changed


def rewrite_source_assets() -> None:
    for page in SRC.rglob("*.md"):
        original = page.read_text(encoding="utf-8")
        updated = C.rewrite_asset_srcs(original)
        if updated != original:
            page.write_text(updated, encoding="utf-8", newline="\n")


def write_footer_include(directory: Path) -> None:
    dest = directory / ".gitbook" / "includes" / "footer.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(C.FOOTER_MD, encoding="utf-8", newline="\n")


def stamp_footers() -> None:
    for name in ("documentation", "developers", "guides"):
        root = ROOT / name
        for page in root.rglob("*.md"):
            rel = page.relative_to(root).as_posix()
            if rel.startswith(".gitbook/") or rel == "SUMMARY.md":
                continue
            text = page.read_text(encoding="utf-8")
            updated = append_footer(text, rel)
            if updated != text:
                page.write_text(updated, encoding="utf-8", newline="\n")


def publish() -> None:
    if not (SRC / "SUMMARY.md").is_file():
        raise SystemExit(f"missing {SRC}/SUMMARY.md — run generate.py first")
    rewrite_source_assets()
    write_footer_include(SRC)
    assets = SRC / ".gitbook" / "assets"
    if assets.is_dir():
        shutil.rmtree(assets)
    for name in ("documentation", "developers", "guides"):
        dest = ROOT / name
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
    compiled = moved_replacements()
    counts = {name: _copy_space(name, compiled) for name in ("documentation", "developers", "guides")}
    write_extra_pages()
    for name in ("documentation", "developers", "guides"):
        write_gitbook_yaml(ROOT / name)
    write_summaries()
    stamp_footers()
    from editorial import refresh_copy

    for name in ("documentation", "developers", "guides"):
        refresh_copy(ROOT / name)
    write_site_yaml()
    linked = rewrite_repo_links(compiled)
    print(
        "sections: "
        + ", ".join(f"{name}={count}" for name, count in counts.items())
        + f", repo_links={linked}"
    )


if __name__ == "__main__":
    publish()
