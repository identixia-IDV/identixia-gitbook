---
description: >-
  License-gated document authenticity / liveness fields in the document result JSON.
---

# Document security check fields

## When security fields appear

If the license includes document liveness / authenticity, the result JSON populates `security` (and related verification / tests rows) with engine checks against:

* Screen replay
* Printout / paper copy
* Portrait or document substitution (when supported)

## How to interpret

| Situation | Meaning |
| --- | --- |
| `security` missing / empty | Feature **not licensed** or **not requested** — not a pass |
| Checks present with fail | Treat as authenticity reject per your risk policy |
| Recognition-only license | Use OCR/MRZ/barcode only; do not invent security passes |

Mobile and server SDKs share field names where possible. Prefer structured `security` / `tests` arrays over UI labels.

Parent object: [Document result JSON](document-result-json.md).
