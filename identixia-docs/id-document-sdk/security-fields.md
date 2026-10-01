---
description: >-
  How to read document authenticity / liveness fields in result JSON.
---

# Security check fields

## When security fields appear

If the license includes document authenticity, the result includes `security` (and related `tests` rows) for anti-spoof checks.

| Situation | Meaning |
| --- | --- |
| `security` missing / empty | Feature **not licensed** or **not requested** — not a pass |
| Checks present with fail | Treat as authenticity reject per your risk policy |
| Recognition-only license | Use OCR/MRZ only; do not invent security passes |

Parent object: [Result JSON](result-json.md).
