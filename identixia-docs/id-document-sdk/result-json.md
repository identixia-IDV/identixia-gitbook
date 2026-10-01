---
description: >-
  Customer process JSON for mobile recognize and server document APIs.
---

# Result JSON

## Purpose

Mobile `recognize` and server `POST /api/documentProcess` (also recognition / liveness routes) return one **customer process JSON**. Parse this object in your app — do not scrape the demo Result UI.

Allowed top-level keys:

| Key | Role |
| --- | --- |
| `identity` | Document class, country, overall score |
| `readings` | OCR / MRZ / barcode field rows |
| `tests` | Validity, capture, and authenticity checks |
| `images` | Crops (face, document pages, …) as base64 |
| `session` | Job id, status code, detail, timestamp |

There is **no** separate top-level `security` object. Authenticity lives in `tests` rows with `group: "authenticity"`.

## Field shapes

### `identity`

| Field | Example | Meaning |
| --- | --- | --- |
| `class` / `type` | `"Passport"` | Document class |
| `country` | `"UTO"` | Issuing country |
| `score` | `0.91` | Overall document confidence when present |

### `readings[]`

| Field | Example | Meaning |
| --- | --- | --- |
| `name` | `"familyName"`, `"firstNames"`, `"docNumber"` | Canonical field id |
| `value` | `"DOE"` | Extracted text |
| `origin` / `source` | `"visual"`, `"zone"`, `"code"`, `"chip"` | Visual OCR, MRZ zone, barcode, RFID |
| `score` | `0.97` | Optional confidence |

Kits may still emit legacy names (`surname`, `mrz`, …). Prefer the sample `ResultParser` / `ix_payload` helpers when present.

### `tests[]`

| Field | Example | Meaning |
| --- | --- | --- |
| `name` | `"expiry"`, `"focus"`, `"foilCheck"` | Check id |
| `group` / `kind` | `"validity"`, `"capture"`, `"authenticity"` | Category |
| `outcome` / `result` | `"pass"`, `"fail"`, `"hold"` | Decision (`hold` ≈ skip / not evaluated) |
| `page` | `0` / `1` | Front / back when applicable |
| `score` | `0.88` | Optional numeric score |
| `note` / `reason` | `"expired"` | Optional explanation |

Overall UI grouping uses **most-severe-wins** within each kind: `fail` > `hold` > `pass`.

### `images[]`

| Field | Meaning |
| --- | --- |
| `name` / `id` | Crop role (`face`, document page, …) |
| `page` | Page index when multi-page |
| `data` / `image` | Base64 payload |

### `session`

| Field | Meaning |
| --- | --- |
| `jobId` | Transaction / job id |
| `code` | `0` = ready / success; non-zero = failure |
| `detail` | Short status (`ready`, `failed`, …) |
| `at` | ISO timestamp |

## Example (contract fixture)

```json
{
  "identity": { "class": "Passport", "country": "UTO", "score": 0.91 },
  "readings": [
    { "name": "familyName", "value": "DOE", "origin": "visual", "score": 0.97 },
    { "name": "firstNames", "value": "JOHN", "origin": "visual", "score": 0.96 },
    { "name": "docNumber", "value": "123456789", "origin": "zone", "score": 0.99 }
  ],
  "tests": [
    { "name": "expiry", "group": "validity", "outcome": "pass" },
    { "name": "focus", "group": "capture", "outcome": "pass", "score": 0.9 },
    { "name": "foilCheck", "group": "authenticity", "page": 0, "outcome": "pass", "score": 0.88 }
  ],
  "images": [
    { "name": "face", "page": 0, "data": "<base64>" }
  ],
  "session": {
    "jobId": "identixia_0123456789abcdef0123456789abcdef",
    "code": 0,
    "detail": "ready",
    "at": "2026-09-14T00:55:12Z"
  }
}
```

## Related

* [Security check fields](security-fields.md) — authenticity rows in detail
* [Document recognition](recognition.md) · [Document liveness](liveness.md)
