---
description: >-
  OCR, MRZ, barcode, and images from ID documents — APIs and repositories.
icon: magnifying-glass
---

# Document recognition

## Overview

Document **recognition** finds the card in the frame and extracts:

* Visual-zone fields (name, document number, dates, and related data)
* **MRZ** (machine-readable zone)
* Barcode / QR when present
* Cropped images (portrait, document, signature, and related crops)

## Capture tips

* Prefer a **physical** device for camera demos.
* Align the document inside the guide; capture front (and back when required).
* On mobile, call locate → capture → `recognize` on a **background** thread.

## Server routes (full Document Docker / Windows)

Default full-product API port is **14102** (confirm in the README).

| Route | Role |
| --- | --- |
| `POST /api/document/process` | Full process (recognition + authenticity when licensed) |
| `POST /api/document/recognition` | OCR / MRZ / barcode only |
| `POST /api/document/liveness` | Authenticity only |

### Example — recognition-only call

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/recognition \
  -H "Content-Type: application/json" \
  -d '{"images":["BASE64_FRONT","BASE64_BACK"]}'
```

Response shape: [Result JSON](result-json.md).

## Repositories

Full mobile + server samples are listed on the [ID Document SDK](README.md) hub.  
Packaging hub: [`ID-Document-Recognition-Liveness-Detection-SDK`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-SDK)

{% include "../.gitbook/includes/footer.md" %}
