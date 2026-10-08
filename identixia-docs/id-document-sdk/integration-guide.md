---
description: >-
  Set up the Identixia ID document recognition and OCR SDK, download native libraries and models, activate a license, and call the APIs.
---

# ID Document Recognition and OCR SDK Integration Guide

This is the **full ID Document SDK integration path**. Open the platform page for your stack after you finish these steps.

## 1. Choose a product

| Goal | Product line | Example repos |
| --- | --- | --- |
| OCR + optional authenticity | ID Document Recognition & Liveness Detection | Android / iOS / Flutter / RN / Ionic / Windows / Docker |
| OCR only | ID Document Recognition | Thin siblings + server ports |
| Authenticity / PAD only | ID Document Liveness Detection | Android / iOS / Windows / Docker |

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
