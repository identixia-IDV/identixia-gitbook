---
description: >-
  How to read document authenticity / liveness checks inside Result JSON tests[].
---

# Security check fields

## Where authenticity lives

Document authenticity (document liveness) is **not** a separate top-level `security` object in the customer process JSON. It appears as rows in `tests[]` where:

```text
group == "authenticity"   // also accepted: kind, or legacy "security" / "liveness"
```

Parent shape: [Result JSON](result-json.md).

## When rows appear

| Situation | Meaning |
| --- | --- |
| No authenticity rows | Feature **not licensed**, **not requested**, or engine omitted them — **not a pass** |
| Rows with `outcome: "fail"` | Treat as authenticity reject per your risk policy |
| Rows with `outcome: "hold"` | Not evaluated / skipped — do not treat as pass |
| Recognition-only license | Use OCR/MRZ (`readings` + validity/capture tests) only |

## Row fields

| Field | Meaning |
| --- | --- |
| `name` | Check id (e.g. `foilCheck`; legacy `hologramIntegrity` maps to the same idea) |
| `group` | Must resolve to `authenticity` |
| `outcome` | `pass` · `fail` · `hold` |
| `page` | `0` = front, `1` = back |
| `score` | Optional float (demo UI may show six decimals) |
| `note` / `reason` | Optional human-readable detail |

### Example authenticity row

```json
{
  "name": "foilCheck",
  "group": "authenticity",
  "page": 0,
  "outcome": "pass",
  "score": 0.88
}
```

### Example summary logic (same idea as the desktop demo)

```text
authenticity_rows = tests where group == "authenticity"
if none → "not evaluated"
else count pass / fail / hold → apply your policy (any fail ⇒ reject is common)
```

## License rule

| License | What you get |
| --- | --- |
| `authenticity` present | Authenticity `tests` populate when the route requests them |
| Missing | Empty authenticity set — never invent a pass |

Server routes: `POST /api/documentLiveness` (authenticity only) or `POST /api/documentProcess` (OCR + authenticity when licensed).
