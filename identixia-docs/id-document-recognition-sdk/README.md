---
description: >-
  ID document recognition SDK for Android, iOS, Windows, and Docker. OCR, MRZ, and barcode extraction for passports, national IDs, and driver licenses. Document liveness requires the matching license.
---

# ID Document Recognition SDK


## Overview

ID document recognition SDK for Android, iOS, Windows, and Docker. OCR, MRZ, and barcode extraction for passports, national IDs, and driver licenses. Document liveness requires the matching license.

Everything runs **on-premise** (on the phone or on your server). Identixia does **not** receive biometric images or templates.

| | |
| --- | --- |
| **Product repository** | `ID-Document-Recognition-Liveness-Detection-SDK` |
| **Platform** | Hub |
| **Docs site** | [doc.identixia.com](https://doc.identixia.com) |


### Repository

{% embed url="https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK" %}

Source: [`identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK)

## What you can do

See the platform pages linked below for capabilities.

## Prerequisites

See the product README for toolchain details.

## Start here

Open the platform page that matches your license and stack. Each page includes quick start, activation, full API reference, and troubleshooting.

## Product README (reference)

The following is adapted from the shipping repository README for screenshots, exact commands, and platform-specific notes.

## <img src="https://api.iconify.design/lucide/id-card.svg?color=%230F766E" width="32" height="32" alt="" /> Identixia ID Document Recognition and Liveness Detection SDK

**On-premise / on-device ID document recognition** for passports, national IDs, and driver licenses — passport MRZ OCR, ID card barcode, live capture, and optional document liveness / authenticity. Built for KYC and eKYC: **no** identity images or fields are sent to Identixia cloud.

Ship once across mobile, plugins, Windows, and Docker with the same product family and licensing model. Mobile demos use a wide Camera Home plus Gallery / About, and a one-scroll Result (identity → fields → checks → images → Raw JSON).

<p><img src="https://img.shields.io/badge/On-premise-0F766E?style=flat-square" alt="On-premise" /> <img src="https://img.shields.io/badge/On-device-0F766E?style=flat-square" alt="On-device" /> <img src="https://img.shields.io/badge/MRZ%20OCR-0F766E?style=flat-square" alt="MRZ%20OCR" /> <img src="https://img.shields.io/badge/Document%20liveness-0F766E?style=flat-square" alt="Document%20liveness" /> <img src="https://img.shields.io/badge/KYC%20%2F%20eKYC-5A6573?style=flat-square" alt="KYC%20%2F%20eKYC" /></p>

Docs: [docs.identixia.com](https://doc.identixia.com) · Docker: [`identixia/document-reader`](https://hub.docker.com/r/identixia/document-reader)

---

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> Basics

Start here. Mobile samples include a demo license. Server samples print a machine code; please contact us with that machine code to get a license.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise / on-device **ID document recognition SDK** hub (KYC / eKYC) |
| **Documents** | Passport, national ID, driver license — OCR · passport MRZ · barcode / QR · optional document liveness |
| **Runtime** | One Google Drive zip per platform — see each App README (`PENDING` until URL is published) |
| **Machine code (servers)** | `GET /api/machinecode` prints `data.machinecode`. Please contact us with that machine code to get a license. |
| **Activate (servers)** | Replace the key in the included `license.txt`, then send that file with `POST /api/activate`. |
| **Activate (mobile)** | Keep the demo id for the sample key, or request a production key for your own applicationId / bundle id. |
| **Tools** | Pick Android / iOS / Flutter / RN / Ionic / Windows / Docker — each App README has the exact run path |
| **Ports** | Recognition API **14102**. Document liveness API **14107**. |
| **Privacy** | On-device or in your VPC — no Identixia cloud for document data |

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Initial commands

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Run the server

```bash
docker pull identixia/document-reader:latest
docker run -d --name identixia-document-reader \
  --shm-size=2gb --privileged \
  -p 14102:14102 \
  -v /etc/machine-id:/etc/machine-id:ro \
  identixia/document-reader:latest
```

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Get a license

```bash
curl -s http://127.0.0.1:14102/api/machinecode
```

The response is JSON. Your machine code is `data.machinecode`.

Please [contact us](#-contact) with the machine code to get a license.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> Activate

This repository includes `license.txt`. Replace the key in that file with the license we send you, then run this command from the repository folder:

```bash
curl -s -X POST http://127.0.0.1:14102/api/activate -H "Content-Type: text/plain" --data-binary @license.txt
```

### <img src="https://img.shields.io/badge/-4-0F766E?style=for-the-badge" alt="" /> Process a document

Replace `BASE64_JPEG` with a base64-encoded JPEG of the document.

```bash
curl -s -X POST http://127.0.0.1:14102/api/documentProcess -H "Content-Type: application/json" -d "{"images":[{"image":"BASE64_JPEG"}]}"
```

---

## <img src="https://api.iconify.design/lucide/sparkles.svg?color=%230F766E" width="24" height="24" alt="" /> Why Identixia

| | | |
| --- | --- | --- |
| <img src="https://api.iconify.design/lucide/shield-check.svg?color=%230F766E" width="18" height="18" alt="" /> | **Privacy by design** | On-device or in your VPC — identity data never leaves your perimeter for Identixia SaaS. |
| <img src="https://api.iconify.design/lucide/globe.svg?color=%230F766E" width="18" height="18" alt="" /> | **KYC / eKYC ready** | Passport MRZ OCR, ID barcodes, and optional authenticity in one stack. |
| <img src="https://api.iconify.design/lucide/layers.svg?color=%230F766E" width="18" height="18" alt="" /> | **One product family** | Android → iOS → Flutter / RN / Ionic → Windows → Docker without changing vendors. |
| <img src="https://api.iconify.design/lucide/key-round.svg?color=%230F766E" width="18" height="18" alt="" /> | **Flexible license** | Recognition, document liveness, or both — match what you ship. |
| <img src="https://api.iconify.design/lucide/rocket.svg?color=%230F766E" width="18" height="18" alt="" /> | **Demo to production** | Sample apps and an HTTP API on port 14102. |

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

| Surface | Ports / notes |
| --- | --- |
| Windows / Linux HTTP API | **14102** |
| Document liveness Docker | [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) · API **14107** |

---

## <img src="https://api.iconify.design/lucide/map.svg?color=%230F766E" width="24" height="24" alt="" /> How to evaluate

1. Pick a **platform repo** from the table below (public GitHub name).
2. Download that platform’s **runtime zip** (Drive link is `PENDING` in each App README until published).
3. Follow the numbered **Run** section — clone URL, extract path, and exact scripts are listed there.
4. Mobile: wait for Home **Ready**, then Camera / Gallery. Server: hit `/api/health` on **14102**.

Demo mobile licenses (where bundled) target `com.identixia.documentreader` / `com.identixia.documentreader.app` until **12 Aug 2027**.

---

## <img src="https://api.iconify.design/lucide/package.svg?color=%230F766E" width="24" height="24" alt="" /> Runtime zips

Each platform App README names a **Google Drive single zip** (`PENDING` until links are published). Unzip so binaries sit at the documented path — not nested in an extra folder. One zip per runtime (Android AAR, iOS framework, Windows/Linux `lib/cpu`, etc.).

---

## <img src="https://api.iconify.design/lucide/layers.svg?color=%230F766E" width="24" height="24" alt="" /> Choose platform

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

Document authenticity API only: [ID-Document-Liveness-Detection-Docker](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker)

---

## <img src="https://api.iconify.design/lucide/boxes.svg?color=%230F766E" width="24" height="24" alt="" /> Also from Identixia

- [Face Recognition SDK](https://github.com/identixia-IDV/Face-Recognition-SDK) — on-device and on-premise face recognition, with passive liveness when the license includes it
- [Face Liveness Detection](https://github.com/identixia-IDV/Face-Liveness-Detection-SDK)

---


## Support

{% include "../.gitbook/includes/contact.md" %}

### Platforms in this section

* [ID Document Recognition Android SDK](id-document-recognition-android-sdk.md)
* [ID Document Recognition iOS SDK](id-document-recognition-ios-sdk.md)
* [ID Document Recognition Flutter SDK](id-document-recognition-flutter-sdk.md)
* [ID Document Recognition React Native SDK](id-document-recognition-react-native-sdk.md)
* [ID Document Recognition Ionic Capacitor SDK](id-document-recognition-ionic-capacitor-sdk.md)
* [ID Document Recognition Ionic Cordova SDK](id-document-recognition-ionic-cordova-sdk.md)
* [ID Document Recognition Windows SDK](id-document-recognition-windows-sdk.md)
* [ID Document Recognition Linux / Docker SDK](id-document-recognition-linux-sdk.md)
* [Document result JSON](document-result-json.md)
* [Document security check fields](document-security-check-fields.md)
