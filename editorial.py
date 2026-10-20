"""Clear, search-oriented page copy without changing GitBook presentation.

Applied to generated pages and section landing pages so regeneration retains
the same wording. URLs, code examples, media, icons, and GitBook blocks stay intact.
"""
from __future__ import annotations

import re
from pathlib import Path


IDV = {
    "README": ("Self-Hosted Identity Verification and KYC Platform", "Build web and mobile identity verification with Identixia IDV. Connect document OCR, face matching, capture apps, verification sessions, and reviews."),
    "api": ("Identity Verification Session API", "Create IDV verification sessions, issue capture tokens, and open applicant capture flows through your company backend."),
    "architecture": ("Identity Verification Platform Architecture", "Understand how the IDV server, company backend, capture apps, biometric engines, and admin consoles work together."),
    "client-android": ("Android Identity Verification Sample App", "Build and run the Android IDV sample app for applicant document and selfie capture in an identity verification session."),
    "client-ios": ("iOS Identity Verification Sample App", "Run the iOS IDV sample app and connect applicant document and selfie capture to your identity verification backend."),
    "client-other": ("Flutter and React Native Identity Verification Samples", "Explore Flutter and React Native sample clients for connecting mobile applicant capture to Identixia IDV sessions."),
    "client-web": ("Web Identity Verification Sample App", "Run the web IDV sample and connect browser-based applicant capture to your company backend and verification sessions."),
    "company-admin": ("Company Admin Console for Identity Verification", "Use the sample Company Admin interface to manage your company integration with the Identixia identity verification platform."),
    "company-backend": ("Company Backend Integration for Identity Verification", "Connect your company backend to IDV, keep service credentials on the server, and create verification sessions for applicants."),
    "company-webhooks": ("Identity Verification Webhooks and Event Delivery", "Receive IDV session events, verify webhook signatures, and handle identity verification event deliveries in your backend."),
    "company": ("Company Integration with the IDV Platform", "Connect company systems to Identixia IDV using the sample backend and admin interface for identity verification sessions."),
    "components-clients": ("Identity Verification Client SDKs and Sample Apps", "Choose web, Android, iOS, Flutter, or React Native applicant clients for document and selfie capture with Identixia IDV."),
    "components": ("Identity Verification Platform Components", "Find the IDV server, company backend, applicant clients, admin consoles, and biometric engines in the project structure."),
    "engines-document": ("Document OCR Engine Integration with IDV", "Connect the ID Document SDK HTTP API to IDV for document recognition, OCR, and licensed document authenticity checks."),
    "engines-face": ("Face Recognition Engine Integration with IDV", "Connect the Face SDK HTTP API to IDV for face matching and licensed face liveness checks during identity verification."),
    "engines": ("Set Up Face and Document Engines for IDV", "Start and activate the Face and ID Document HTTP engines before connecting them to your self-hosted IDV platform."),
    "environment": ("IDV Environment and Backend Configuration", "Configure IDV environment variables, engine URLs, service tokens, and storage for your identity verification deployment."),
    "getting-started": ("Get Started with Self-Hosted Identity Verification", "Set up Identixia IDV step by step, from biometric engines and configuration to your first verification session and webhook."),
    "initial-setup": ("Initial IDV Console and Company Setup", "Set up Identity Console access, company settings, and webhook configuration after preparing your IDV engines and environment."),
    "license-admin": ("IDV License Administration", "Use the local Identixia license administration service to manage licenses for your IDV platform deployment."),
    "license-protocol": ("IDV Hybrid License Protocol", "Understand the shared license_v2 protocol used by the Identixia IDV server and license issuer."),
    "licensing": ("IDV Platform Licensing and Activation", "Understand the license issuer and Hybrid licensing components used by the self-hosted Identixia IDV platform."),
    "platform-console": ("Identity Console for Verification Operations", "Use Identity Console to manage IDV sessions, manual reviews, webhooks, and identity verification workflows."),
    "platform-server": ("IDV Identity Verification Server", "Explore the IDV platform API, background workers, storage, and admin interface for self-hosted identity verification."),
    "platform": ("Self-Hosted IDV Server and Identity Console", "Learn how the Identixia IDV server and Identity Console support identity verification sessions and operator reviews."),
    "production": ("Deploy the IDV Platform to Production", "Prepare an IDV deployment with authentication, TLS, database configuration, engine connectivity, and restricted service access."),
    "project-structure": ("IDV Project Structure and Service Roles", "Find the platform, company, applicant, and engine components in the Identixia IDV repository before setting up your deployment."),
    "quick-start": ("IDV Platform Quick Start", "Run the IDV server, Identity Console, company backend, and license administration service in a local development environment."),
    "reference": ("Identity Verification API and Integration Reference", "Find IDV API tables, Postman requests, and the offline handbook for implementing your identity verification integration."),
    "session-states": ("Identity Verification Session States and Results", "Understand IDV session status and identity trust states as applicants move through capture, processing, and review."),
    "shared-packages": ("Shared IDV Platform and Console Packages", "Locate the shared libraries used by the Identixia platform and company interfaces in IDV/packages."),
    "walkthrough": ("Complete an Identity Verification Session", "Follow one IDV verification from engine startup and applicant capture through webhook delivery and operator review."),
}

ROOT_PAGES = {
    "contact-us": ("Contact Identixia for SDK Licensing and Support", "Contact Identixia for face recognition, liveness detection, document OCR, and IDV licensing or technical integration support."),
    "request-a-license-and-support": ("Request an Identixia SDK License and Technical Support", "Request a license for Face SDK, ID Document SDK, or IDV. Learn which app identifier or machine code to provide and how to activate."),
    "choose-a-product": ("Choose a product", "Match an Identixia repository to the face or ID document license you need, then run the sample."),
    "run-the-sample": ("Run the Identixia SDK Sample Apps", "Set up Identixia SDK sample apps for Android, iOS, Flutter, React Native, and Ionic, then download the runtime and activate your license."),
}

PLATFORMS = {
    "android": "Android", "ios": "iOS", "flutter": "Flutter",
    "react-native": "React Native", "ionic-capacitor": "Ionic Capacitor",
    "ionic-cordova": "Ionic Cordova", "windows": "Windows",
    "linux-docker": "Linux and Docker",
}


def sentence_name(value: str) -> str:
    return value.lower().replace("id document", "ID document").replace("ocr", "OCR")


def platform_description(face: bool, mode: str, platform: str) -> str:
    """One sentence for the GitBook subtitle. The page body does not repeat it."""
    mobile = platform not in ("Windows", "Linux and Docker")
    where = "on the device" if mobile else "on your server"
    if face and mode == "liveness":
        return (
            f"Passive face liveness for {platform}. Presentation-attack and deepfake checks "
            f"run {where}. A face is REAL only when both pass."
        )
    if not face and mode == "liveness":
        return (
            f"ID document liveness for {platform}. Presentation-attack checks for passports and ID cards "
            f"run {where}, separate from OCR."
        )
    if face and mode == "recognition":
        return (
            f"Face recognition for {platform}. Detection, attributes, quality, templates, and 1:1 match "
            f"run {where}. This build does not include liveness."
        )
    if not face and mode == "recognition":
        return (
            f"ID document recognition for {platform}. Passport, national ID, and driver license OCR, MRZ, "
            f"and barcode reading run {where}. This build does not include document liveness."
        )
    if face:
        return (
            f"Face recognition and liveness for {platform}. Enrollment, templates, and 1:N search run {where}. "
            "Passive liveness runs when the license includes it."
        )
    return (
        f"ID document recognition and liveness for {platform}. Passport, national ID, and driver license "
        f"OCR, MRZ, and barcode reading run {where}. Document liveness runs when the license includes it."
    )


def page_metadata(rel: str, section: str) -> tuple[str, str] | None:
    path = Path(rel)
    leaf = path.stem
    family = path.parts[0] if len(path.parts) > 1 else ""
    if family == "idv":
        return IDV.get(leaf)
    if not family:
        if leaf != "README":
            return ROOT_PAGES.get(leaf)
        if section == "developers":
            return ("Identity Verification SDK and API Developer Guides", "Add the Identixia SDK to your app: download the runtime, activate a license, and call the kit on each platform.")
        if section == "guides":
            return ("Identity Verification SDK Setup and Licensing Guides", "Choose an Identixia product, run the sample, request a license, and contact support.")
        return ("Identixia Identity Verification SDK Documentation", "What Identixia face and ID document products do, what you need to run a sample, and what the sample returns.")
    if family == "sdk-server":
        product = {"README": "Face Recognition and Document OCR", "face-recognition": "Face Recognition", "face-liveness": "Face Liveness Detection", "document-recognition": "ID Document Recognition and OCR", "document-liveness": "ID Document Liveness Detection"}.get(leaf)
        if product:
            return (f"{product} HTTP API", f"Integrate the self-hosted Identixia {sentence_name(product)} HTTP API on Windows or Docker. Follow setup, activation, and request examples.")
    if family not in ("face-sdk", "id-document-sdk"):
        return None
    face = family == "face-sdk"
    product = "Face Recognition" if face else "ID Document Recognition and OCR"
    liveness = "Face Liveness Detection" if face else "ID Document Liveness Detection"
    mode = "combined"
    platform_leaf = leaf
    for prefix in ("recognition-", "liveness-"):
        if leaf.startswith(prefix):
            mode = prefix[:-1]
            platform_leaf = leaf[len(prefix):]
    if platform_leaf in PLATFORMS:
        platform = PLATFORMS[platform_leaf]
        name = liveness if mode == "liveness" else product
        if mode == "combined":
            name = "Face Recognition and Liveness Detection" if face else "ID Document OCR and Liveness Detection"
        title = f"{name} SDK for {platform}"
        return title, platform_description(face, mode, platform)
    if leaf == "README" and not face:
        return ("ID Document OCR and Liveness Detection SDKs", "Read passports and ID cards with Identixia document OCR, MRZ, and barcode SDKs. Add licensed document liveness checks on mobile or self-hosted servers.")
    metadata = {
        "README": (f"{product} and Liveness Detection SDKs", f"Explore Identixia {product.lower()} and liveness SDKs for mobile apps and self-hosted servers. Compare features and choose a platform."),
        "recognition": (f"{product} SDK Features and Integration", f"Learn how Identixia {product.lower()} works, which APIs to use, and which sample repositories match your platform."),
        "liveness": (f"{liveness} and Anti-Spoofing", f"Understand Identixia {liveness.lower()}, presentation attack checks, license requirements, and how to interpret results."),
        "full-product": (f"{product} with Liveness Detection", f"Choose Identixia SDKs that combine {product.lower()} with licensed liveness checks for mobile or server integration."),
        "full-mobile": (f"{product} SDKs for Mobile Apps", f"Compare Android, iOS, Flutter, React Native, and Ionic samples for Identixia {product.lower()} with licensed liveness checks."),
        "full-server": (f"{product} APIs for Windows and Docker", f"Deploy Identixia {product.lower()} with licensed liveness checks using self-hosted HTTP APIs on Windows or Linux and Docker."),
        "recognition-only": (f"{product} SDKs without Liveness", f"Choose a recognition-only Identixia SDK for {product.lower()}. Compare available repositories and integration options."),
        "liveness-only": (f"Standalone {liveness} SDKs", f"Choose a standalone Identixia {liveness.lower()} SDK for anti-spoofing checks, separate from recognition."),
        "liveness-only-mobile": (f"{liveness} SDKs for Android and iOS", f"Integrate standalone Identixia {liveness.lower()} on Android or iOS. Explore sample apps and license requirements."),
        "liveness-only-server": (f"{liveness} APIs for Windows and Docker", f"Run standalone Identixia {liveness.lower()} through a self-hosted HTTP API on Windows or Linux and Docker."),
        "integration-guide": (f"{product} SDK Integration Guide", f"Set up the Identixia {product.lower()} SDK, download native libraries and models, activate a license, and call the APIs."),
        "reference": (f"{product} SDK Platform Reference", f"Find platform guides and sample repositories for Identixia {product.lower()} and liveness detection SDKs."),
        "result-json": ("ID Document OCR Result JSON Reference", "Read document recognition results from mobile and server APIs, including identity fields, MRZ data, barcodes, images, and checks."),
        "security-fields": ("Document Liveness and Security Check Results", "Interpret document authenticity and liveness checks in result JSON. Understand missing checks and license-dependent security fields."),
    }
    result = metadata.get(leaf)
    if result:
        return result[0], result[1].replace("id document", "ID document").replace("ocr", "OCR")
    return None


REPLACEMENTS = {
    "On-premises ID Document Recognition and Document Liveness (authenticity) SDKs.": "Build document capture and identity data extraction with Identixia ID document recognition, optical character recognition (OCR), and document liveness SDKs.",
    "Read passports, national IDs, and driver licenses on **your** device or server: OCR / MRZ / barcode fields, cropped images, and optional anti-spoof authenticity checks.": "Read passports, national ID cards, and driver licenses on **your** device or server. Extract printed text, read the machine-readable zone (MRZ), decode supported barcodes, and obtain cropped document images. Add document anti-spoofing checks when enabled by your license.",
    "Full-product repositories run both when licensed. A **liveness-only** Linux / Docker API is available when you need authenticity without the full OCR surface.": "The license flags are `recognition` and `authenticity`. [Choose a product](https://docs.identixia.com/guides/choose-a-product) lists the repository for each one.",
    "<strong>Face</strong> — recognition and passive liveness.": "<strong>Face</strong> — face recognition, matching, and passive liveness detection.",
    "<strong>ID documents</strong> — OCR, MRZ, barcode, and document liveness.": "<strong>ID documents</strong> — passport and ID card OCR, MRZ reading, barcode extraction, and document liveness.",
    "<strong>IDV</strong> — self-hosted KYC sessions on your own stack.": "<strong>IDV</strong> — self-hosted identity verification and Know Your Customer (KYC) sessions.",
    "<strong>Face</strong> on a phone or desktop.": "<strong>Face</strong> recognition and liveness SDK integration for mobile apps and servers.",
    "<strong>ID document</strong> capture, MRZ, and barcode.": "<strong>ID document</strong> capture, text recognition, MRZ reading, and barcode extraction.",
    "On-premises Face Recognition and Face Liveness Detection (anti-spoofing) SDKs.": "Build biometric identity verification with Identixia face recognition and passive face liveness detection SDKs. Run face matching and anti-spoofing checks on your own devices or servers.",
    "The algorithm runs in real time on phones and servers. It supports accurate **1:1** and **1:N** matching, **passive face liveness**, and face attributes (age, gender, mask/sunglasses, landmarks).": "Compare two faces with **one-to-one (1:1) matching**, or search an enrolled gallery with **one-to-many (1:N) identification**. Depending on the selected SDK and license, you can also run **passive face liveness** checks and obtain face attributes and landmark coordinates.",
    "Use it for identity verification and attendance. Processing stays on **your** device or server.": "Use these SDKs in identity verification, attendance, and access-control workflows. Processing stays on **your** device or server.",
    "Face recognition, face liveness, and ID document capture run on **your** device or server. Identixia does not receive the images.": "Build identity verification with face recognition, passive liveness detection, and ID document capture. Processing runs on **your** device or server; images are not sent to Identixia.",
    "Use the sample app, then embed the SDK.": "Run the sample app for your platform, then integrate its capture and SDK calls into your application.",
    "Pick the repository that matches the license, then activate.": "Choose a sample that supports the features you need, download its runtime, and activate the matching SDK license.",
    "Send the application id, bundle id, or machine code, then call activate before init.": "Request a license using your Android application ID, iOS bundle identifier, or server machine code. Activate the returned key before initializing the SDK.",
    "Demo keys work only with the demo application id. A production key must match the id or machine code you send.": "The bundled demo key is tied to the sample application's identifier. For your own app or server, request a license issued for its application ID, bundle identifier, or machine code.",
    "Use your applicationId or bundle id, not the demo id.": "For your own app, configure its Android application ID or iOS bundle identifier before requesting a license. Keep the original identifier when evaluating the sample with its bundled demo key.",
    "Contact Identixia with that id and the product: Face recognition, Face liveness, Document recognition, or Document authenticity.": "Send Identixia your application identifier, target platform, and required features: face recognition, face liveness, document OCR, or document liveness. The license must match the app and features you intend to use.",
    "Call activate, then init, as shown on the platform page.": "Replace the demo key with the key issued for your app. Follow the platform sample to activate the license before initializing the SDK, then check the license status before using its features.",
    "Start the container or Windows service once.": "Start the Docker container or Windows API service so you can request the machine code used for licensing.",
    "Call `GET /api/machinecode` and copy `data.machinecode`. Docker and bare-metal codes differ.": "Call `GET /api/machinecode` in the environment where the SDK will run and copy `data.machinecode` from the JSON response. Send this code to Identixia with the product you need; a container may report a different code from its host.",
    "Call `POST /api/activate`, or set `LICENSE=` in `.env` and restart. Confirm with `GET /api/licenseStatus`.": "Submit your issued key to `POST /api/activate`, or set the `LICENSE` value in the server's `.env` file and restart. Check `GET /api/licenseStatus` to confirm activation and the features enabled by your license.",
    "Document **liveness** (authenticity) checks whether the ID is likely a physical document versus:": "Document **liveness**, also called document presentation attack detection (PAD), checks for signs that an ID image comes from a spoofed presentation, such as:",
    "It does **not** replace OCR. You can run authenticity alone or together with recognition.": "Document liveness checks evaluate authenticity; optical character recognition (OCR) extracts text. Run liveness checks separately or alongside document recognition, depending on the SDK and license you choose.",
    "Empty or omitted security — **not** a pass": "Security results are empty or omitted; an unavailable check does **not** mean the document passed",
    "Serialize native SDK calls on **one background thread**. The engine is not concurrent.": "Run native SDK calls sequentially on **one background thread**. The engine does not support simultaneous calls.",
    "Compact feature vectors stored in **your** database": "Numerical representations of faces that you can store in **your** database for comparison",
    "Enroll a gallery and search (mobile VideoWorker / server gallery)": "Save face templates in a gallery, then search for the closest match using the platform's gallery API",
    "PAD and deepfake together when the license includes `liveness`; REAL only if both pass": "Run presentation attack detection (PAD) and deepfake checks when the license includes `liveness`; report REAL only when both pass",
    "Score one RGB face for PAD and deepfake; REAL only when both engines say real": "Check a color face image for presentation attacks and deepfakes; report REAL only when both checks pass",
    "Visual-zone fields (name, document number, dates, and related data)": "Read printed document fields such as the name, document number, and dates using optical character recognition",
    "Machine-readable zone parse and checksum checks": "Read the machine-readable zone (MRZ) and validate its check digits",
    "Native engines and model databases are **not** stored in git. Every product ships `scripts/get_runtime.py`, which downloads the correct GitHub Release assets and places them where the sample expects.": "Download the `runtime` GitHub Release and extract it into the folder the sample expects. The engine and database packs are not stored in git.",
    "Download the native SDK libraries and model files before running the sample. Use `scripts/get_runtime.py` to retrieve the required GitHub Release assets and place them in the sample's expected folders.": "Download the `runtime` GitHub Release and extract it into the folder the sample expects. The engine and database packs are not stored in git.",
    "Unzip so files land in the documented path — **not** nested inside an extra folder.": "Extract the archive directly into the documented folder. Check that the library and model files are not inside an additional nested directory.",
    "Clone the product repository, then open the tab for your stack. Android and iOS are separate setups. On macOS use `python3`.": "Clone the repository for your chosen product and follow the tab for your development framework. Complete Android and iOS setup separately; iOS requires a Mac. Use `python3` on macOS.",
    "Wait until the sample shows **Ready**, then open the capture, enroll, or recognize action that the product includes.": "Wait for the sample to show **Ready**, then select one of its supported features, such as image capture, face enrollment, or document recognition.",
    "It does not replace those SDKs — it orchestrates them between your company systems and applicant capture apps.": "The IDV platform connects your company backend and applicant capture apps to the Face and Document SDK services. It manages the verification workflow while those SDKs perform biometric and document processing.",
    "**IDV** is Identixia's open web & mobile KYC platform.": "**IDV** is Identixia's self-hosted identity verification platform for web and mobile Know Your Customer (KYC) workflows.",
    " · helper `python IDV/IDV_server (then company)`": " — start the IDV services, then the company integration, using the commands in the guide",
}


def edit_page(text: str, rel: str, section: str) -> str:
    """Edit metadata and prose only; leave code and visual markup unchanged."""
    metadata = page_metadata(rel, section)
    if metadata:
        title, description = metadata
        text = re.sub(r"(?m)^# [^\n]+", lambda _: "# " + title, text, count=1)
        # Keep frontmatter fields, including icons, in their existing order.
        front = re.match(r"\A---\n[\s\S]*?\n---\n", text)
        if front:
            updated = re.sub(r"(?m)^description:.*(?:\n[ \t]+[^\n]*)*", lambda _: "description: >-\n  " + description, front.group())
            text = updated + text[front.end():]
    chunks = re.split(r"(```[^\n]*\n[\s\S]*?```|~~~[^\n]*\n[\s\S]*?~~~)", text)
    for i in range(0, len(chunks), 2):
        for old, new in REPLACEMENTS.items():
            chunks[i] = chunks[i].replace(old, new)
    return "".join(chunks)


def refresh_copy(root: Path) -> int:
    count = 0
    for page in root.rglob("*.md"):
        rel = page.relative_to(root).as_posix()
        if rel.startswith(".gitbook/") or page.name == "SUMMARY.md":
            continue
        original = page.read_text(encoding="utf-8")
        updated = edit_page(original, rel, root.name)
        if updated != original:
            page.write_text(updated, encoding="utf-8", newline="\n")
            count += 1
    return count
