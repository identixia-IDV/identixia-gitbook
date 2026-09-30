---
description: >-
  On-device ID document recognition SDK for iOS. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.
---

# ID Document Recognition iOS SDK

On-device ID document recognition SDK for iOS. Passport, national ID, and driver license OCR, MRZ, and barcode capture. Document liveness runs when the license includes it.

### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS" %}

[`identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS)

### From the product README

## <img src="https://cdn.simpleicons.org/apple/000000" width="32" height="32" alt="" /> Identixia ID Document Recognition and Liveness Detection — iOS

**On-device ID document recognition** for iPhone: passports, national IDs, and driver licenses with passport MRZ OCR, ID card barcode, live capture, and optional document liveness / authenticity. Designed for KYC and eKYC — **all recognition runs on device**; Identixia never receives your document images.

<p><img src="https://img.shields.io/badge/On-device-0F766E?style=flat-square" alt="On-device" /> <img src="https://img.shields.io/badge/Passport%20MRZ%20OCR-0F766E?style=flat-square" alt="Passport%20MRZ%20OCR" /> <img src="https://img.shields.io/badge/ID%20barcode-0F766E?style=flat-square" alt="ID%20barcode" /> <img src="https://img.shields.io/badge/Document%20liveness-0F766E?style=flat-square" alt="Document%20liveness" /> <img src="https://img.shields.io/badge/KYC%20%2F%20eKYC-5A6573?style=flat-square" alt="KYC%20%2F%20eKYC" /></p>

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Read this once before cloning. Mobile demos ship a **bundled license** for the sample application / bundle id. Production apps need a new key from Identixia. [Initial commands](#-initial-commands) lists clone → place runtime → run → activate options.

| Topic | Basic information |
| --- | --- |
| **Product** | On-device **ID document recognition SDK** for iOS (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · passport MRZ · barcode / QR · optional document liveness |
| **Runtime zip** | `docsdk.framework` from Google Drive zip `PENDING` |
| **Demo id / license** | `com.identixia.documentreader.app` — bundled demo license until **12 Aug 2027** |
| **Activate** | Sample app: keep the demo id and bundled key. Your app: new applicationId / bundle id → [contact](#-contact) → call the SDK activate API (see docs). |
| **Tools** | **Xcode 15+** · physical **iPhone** |
| **UI** | Wide Camera Home · Gallery / About · one-scroll Result |
| **Privacy** | All processing on device — no Identixia cloud for document data |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

Clone the sample, place the runtime, and run it.

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Clone and place the runtime

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS.git
cd ID-Document-Recognition-Liveness-Detection-iOS
```

Download the runtime zip (`PENDING`) and place:

```text
docsdk.framework
```

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Run the demo

Open `DocumentReader.xcodeproj` in **Xcode 15+** → set Signing Team → Run on a physical iPhone.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> Activate / license

Please [contact us](#-contact) to get a license for your own app. The sample already includes a demo license for its application id.

### <img src="https://img.shields.io/badge/-4-0F766E?style=for-the-badge" alt="" /> First capture

Wait until Home status = **Ready**, then use Camera / Gallery (or the face mode tiles). Confirm Result / About shows a licensed state before integrating into your own app.

---

## <img src="https://api.iconify.design/lucide/list-checks.svg?color=%230F766E" width="24" height="24" alt="" /> What you get

| Capability | What it does |
| --- | --- |
| <img src="https://api.iconify.design/lucide/id-card.svg?color=%230F766E" width="16" height="16" alt="" /> Passport / ID / DL | On-device ID document recognition for passports, national IDs, and driver licenses |
| <img src="https://api.iconify.design/lucide/scan-text.svg?color=%230F766E" width="16" height="16" alt="" /> Passport MRZ OCR | Machine-readable zone OCR for ICAO travel documents |
| <img src="https://api.iconify.design/lucide/scan-barcode.svg?color=%230F766E" width="16" height="16" alt="" /> ID card barcode | PDF417 / barcode extraction on supported cards |
| <img src="https://api.iconify.design/lucide/camera.svg?color=%230F766E" width="16" height="16" alt="" /> Live capture | Camera locate + Capture; gallery front / optional back |
| <img src="https://api.iconify.design/lucide/shield.svg?color=%230F766E" width="16" height="16" alt="" /> Document liveness | Optional authenticity / PAD (screen, print, photo-swap) when licensed |
| <img src="https://api.iconify.design/lucide/scroll-text.svg?color=%230F766E" width="16" height="16" alt="" /> Result UI | One scroll: identity → fields → checks → images → Raw JSON |
| <img src="https://api.iconify.design/lucide/house.svg?color=%230F766E" width="16" height="16" alt="" /> Home UI | Wide Camera tile + Gallery / About |

---

## <img src="https://api.iconify.design/lucide/pc-case.svg?color=%230F766E" width="24" height="24" alt="" /> Requirements

| | |
| --- | --- |
| Device | Physical **iPhone** (camera demos) |
| Tools | **Xcode 15+**, CocoaPods not required for the framework demo |
| Demo bundle id | `com.identixia.documentreader.app` |

---

## <img src="https://api.iconify.design/lucide/package.svg?color=%230F766E" width="24" height="24" alt="" /> Runtime zip

> **Google Drive (single zip):** `PENDING`

Unzip `docsdk.framework` next to `DocumentReader.xcodeproj` at the repo root:

```text
docsdk.framework
DocumentReader.xcodeproj
```

---

## <img src="https://api.iconify.design/lucide/rocket.svg?color=%230F766E" width="24" height="24" alt="" /> Run

```text
1. git clone https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS.git
2. Place docsdk.framework at the repo root (from the runtime zip)
3. Open DocumentReader.xcodeproj in Xcode 15+
4. Set your Signing Team; keep bundle id com.identixia.documentreader.app for the demo license
5. Run on a physical iPhone → Home Ready → Camera / Gallery
```

---

## <img src="https://api.iconify.design/lucide/key-round.svg?color=%230F766E" width="24" height="24" alt="" /> License

| | |
| --- | --- |
| Demo bundle id | `com.identixia.documentreader.app` |
| Bundled demo license | Until **12 Aug 2027** for that id |
| Capabilities | Recognition and/or document liveness per key |

The code below shows how to use the license:

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/blob/be88a3a057808ed15a4a1e74f5828a33df7d2dcd/DocumentReader/ViewController.swift#L14-L15](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/blob/be88a3a057808ed15a4a1e74f5828a33df7d2dcd/DocumentReader/ViewController.swift#L14-L15)

[https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/blob/be88a3a057808ed15a4a1e74f5828a33df7d2dcd/DocumentReader/ViewController.swift#L147-L149](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS/blob/be88a3a057808ed15a4a1e74f5828a33df7d2dcd/DocumentReader/ViewController.swift#L147-L149)

Please [contact us](#-contact) to get a license for **your own app**.

---

## <img src="https://api.iconify.design/lucide/puzzle.svg?color=%230F766E" width="24" height="24" alt="" /> Use in your app

Embed `docsdk.framework`, activate with your license string, init, then recognize. See [docs](https://doc.identixia.com). Do not ship the demo bundle id with a production key mismatch.

Typical KYC path: Home Ready → Camera (or Gallery front/back) → one-scroll Result → Raw JSON for your backend mapping.

---

## <img src="https://api.iconify.design/lucide/images.svg?color=%230F766E" width="24" height="24" alt="" /> Screenshots

<p align="center">
<img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-result.png" width="720" alt="ID document recognition Gradio demo — front and back capture, fields, and cropped images" />
</p>

---

## <img src="https://api.iconify.design/lucide/layers.svg?color=%230F766E" width="24" height="24" alt="" /> Platforms

| | Platform | Repo |
| --- | --- | --- |
| <img src="https://cdn.simpleicons.org/android/3DDC84" width="18" height="18" alt="" /> | Android | [ID-Document-Recognition-Liveness-Detection-Android](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) |
| <img src="https://cdn.simpleicons.org/apple/000000" width="18" height="18" alt="" /> | iOS | [ID-Document-Recognition-Liveness-Detection-iOS](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS) |
| <img src="https://cdn.simpleicons.org/flutter/02569B" width="18" height="18" alt="" /> | Flutter | [ID-Document-Recognition-Liveness-Detection-Flutter](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Flutter) |
| <img src="https://cdn.simpleicons.org/react/61DAFB" width="18" height="18" alt="" /> | React Native | [ID-Document-Recognition-Liveness-Detection-React-Native](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-React-Native) |
| <img src="https://cdn.simpleicons.org/ionic/3880FF" width="18" height="18" alt="" /> | Ionic Capacitor | [ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| <img src="https://cdn.simpleicons.org/apachecordova/E8E8E8" width="18" height="18" alt="" /> | Ionic Cordova | [ID-Document-Recognition-Liveness-Detection-Ionic-Cordova](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| <img src="https://cdn.simpleicons.org/windows/0078D4" width="18" height="18" alt="" /> | Windows | [ID-Document-Recognition-Liveness-Detection-Windows](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) |
| <img src="https://cdn.simpleicons.org/docker/2496ED" width="18" height="18" alt="" /> | Linux / Docker | [ID-Document-Recognition-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) |

Document liveness only: [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

---

## <img src="https://api.iconify.design/lucide/mail.svg?color=%230F766E" width="24" height="24" alt="" /> Contact

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>


{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths documented in the product README. They are not committed to git.
{% endhint %}
