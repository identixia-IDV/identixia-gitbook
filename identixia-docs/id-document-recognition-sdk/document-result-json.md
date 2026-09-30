---
description: >-
  Shared document recognition / process JSON shape across mobile and server SDKs.
---

# Document result JSON

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
