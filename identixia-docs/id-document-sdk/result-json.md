---
description: >-
  Shared document process JSON for mobile recognize and server document APIs.
---

# Result JSON

## Purpose

Mobile `recognize` and server `POST /api/documentProcess` (plus recognition / liveness routes) return the **same idea**: one JSON object your app parses.

## Top-level fields

| Field | Meaning |
| --- | --- |
| `errorCode` / process `metadata.status` | Engine / process status |
| Document type / country | Identity class and issuing country |
| `ocr` / field readings | Visual-zone fields |
| `mrz` | Machine-readable zone |
| `barcode` | Barcode / QR fields |
| `images` | Crops (portrait, document, …) |
| `tests` / `verification` | Field and document checks |
| `security` | Authenticity / document liveness (license-gated) |
| `session` | Session metadata when provided |

### Example (trimmed)

```json
{
  "identity": { "documentType": "Passport", "country": "UTO" },
  "readings": [{ "field": "surname", "value": "DOE", "source": "mrz" }],
  "tests": [{ "name": "mrzChecksum", "result": "passed" }],
  "images": [{ "role": "portrait", "data": "…" }],
  "session": { "scenario": "FullProcess" }
}
```

Exact nesting can vary slightly by platform kit — prefer the sample `ResultParser` when present. Values `0` / `1` / `2` in verification rows usually mean pass / fail / not checked.

## Related

* [Security check fields](security-fields.md)
* [Document recognition](recognition.md) · [Document liveness](liveness.md)
