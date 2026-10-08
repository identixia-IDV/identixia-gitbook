---
description: >-
  Learn how Identixia ID document recognition and OCR works, which APIs to use, and which sample repositories match your platform.
---

# ID Document Recognition and OCR SDK Features and Integration

## Overview

Document **recognition** finds the card in the frame and extracts:

* Read printed document fields such as the name, document number, and dates using optical character recognition
* **MRZ** (machine-readable zone)
* Barcode / QR when present
* Cropped images (portrait, document, signature, and related crops)

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
curl -s -X POST http://127.0.0.1:14106/api/document/recognition \
  -H "Content-Type: application/json" \
  -d '{"images":[{"image":"BASE64_FRONT","page_idx":0},{"image":"BASE64_BACK","page_idx":1}]}'
```

Response shape: [Result JSON](result-json.md).

## Repositories

Full mobile + server samples are listed on the [ID Document SDK](README.md) hub.  
Packaging hub: [`ID-Document-Recognition-Liveness-Detection-SDK`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK)
