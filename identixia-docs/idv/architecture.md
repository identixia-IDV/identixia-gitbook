---
description: >-
  IDV runtime flow, authority boundaries, and decision policy.
---

# Architecture

## Runtime flow

```text
Company backend                Capture app (web / mobile)
       │                                │
       │  POST /v1/sessions             │
       │  mint capture token            │
       ├───────────────────────────────►│
       │                                │ submissions (+ step headers)
       │                                ▼
       │                         IDV Server :14187
       │                    normalize → engines → decision
       │                                │
       ▼                                ▼
 Identity Console /admin          reviews · identities · webhooks
```

1. Business backend creates a session with service credentials.
2. Backend mints a **session-scoped capture token**.
3. Capture client submits protected SDK bundles to `/submissions`.
4. Server normalizes signals, evaluates trust factors, opens review when needed.
5. Outbound events use a transactional outbox; inbound vendor callbacks use a durable inbox.

## Authority

| Concern | Owner |
| --- | --- |
| Document OCR / face match / liveness scores | Document SDK + Face SDK (or adapters) |
| Tenant policy, review leases, API auth | IDV server |
| Hybrid entitlement metering | `license_v2` inside `idv-server` |
| Licence issuance | `license-admin` |

## Decision rule

Trust aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing or error signals never auto-accept. Implementation lives under `idv-server/idv/decision/`.
