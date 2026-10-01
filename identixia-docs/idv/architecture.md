---
description: >-
  IDV runtime flow across company backend, platform server, engines, and consoles.
---

# Architecture

## Runtime flow

```text
Company backend :14195              Capture app (web / mobile)
       │                                      │
       │  service bearer → POST /v1/sessions  │
       │  mint capture token / launch URL     │
       ├─────────────────────────────────────►│
       │                                      │ submissions (+ step headers)
       │                                      ▼
       │                               IDV Server :14187
       │                          engines → decision → store
       │                                      │
       │◄──────── webhooks (session.*) ───────┤
       ▼                                      ▼
 Company Admin :14189                 Identity Console /admin
```

1. **Company backend** holds the service credentials and starts a verification session on IDV.
2. It returns a **capture token** / launch URL to the applicant app (or operator UI).
3. The **capture client** submits step bundles to IDV (`/submissions`).
4. IDV calls **Document** and **Face** HTTP engines, evaluates trust, may open review.
5. IDV notifies the company via **webhooks**; operators use Identity Console and Company Admin.

## Authority

| Concern | Owner |
| --- | --- |
| Document OCR / face match / liveness scores | Document SDK + Face SDK |
| Tenant policy, sessions, reviews, API auth | `platform/server` |
| Holding service tokens, starting sessions for apps | **Your** backend (sample: `company/backend`) |
| Hybrid entitlement metering on customer host | `license/license_v2` inside `platform/server` |
| Issuing Hybrid licences | `license/admin` (Identixia) |

## Decision rule

Trust aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing or error signals never auto-accept (`platform/server/idv/decision/`).
