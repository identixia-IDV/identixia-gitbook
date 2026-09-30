---
description: >-
  Shared document recognition / process JSON shape across mobile and server SDKs.
---

# Document result JSON

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
