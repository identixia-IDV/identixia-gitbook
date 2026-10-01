---
description: >-
  Run one verification: engines, IDV server, company backend, capture, webhook, review.
---

# End-to-end walkthrough

## Goal

Complete one `onboarding_standard` verification locally and see a `session.completed` webhook plus an identity in Identity Console.

## 1. Start engines

| Service | URL |
| --- | --- |
| Document | `http://127.0.0.1:14102` — activate, then `GET /api/health` |
| Face | `http://127.0.0.1:14103` — activate, then `GET /api/health` |

## 2. Start platform + company

```bash
# IDV server
cd IDV/platform/server && set IDV_OPEN_API=1 && python app.py
# → http://127.0.0.1:14187/v1  and  /admin/

# Company backend
cd IDV/company/backend
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
# → http://127.0.0.1:14195/
```

Optional UIs: Identity Console `:14188` (or `/admin` on the server), Company Admin `:14189`.

## 3. Register a webhook

1. Company Admin → Settings → webhook URL  
   `http://127.0.0.1:14195/demo/webhooks/idv`
2. Identity Console → Webhooks → add that URL for `session.created` and `session.completed`
3. Copy the one-time `whsec_…` into Company Admin Settings

Details: [Company webhooks](company-webhooks.md).

## 4. Start verification (company API)

```bash
curl -s -X POST http://127.0.0.1:14195/demo/start-verification \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"onboarding_standard"}'
```

Response includes `sessionId`, `captureToken`, `launchUrl`, and `next_step`. Hand the **capture token** (or launch URL) to the applicant app — never the service bearer.

## 5. Capture steps

1. `GET /v1/sessions/{id}` with `Authorization: Bearer <captureToken>` → read `next_step.id`
2. `POST /v1/sessions/{id}/submissions` with headers:
   * `Authorization: Bearer <captureToken>`
   * `Idempotency-Key: <unique>`
   * `X-IDV-Step-ID: <next_step.id>`
   * `X-IDV-Attempt: 1`
   * Body: `{ "images": ["<base64>"] }` (or the shape the step expects)
3. Repeat until the session completes (typical: document then face)

Use a [client demo](components-clients.md) or Postman (`IDV/platform/server/postman/IDV-Public.postman_collection.json`).

## 6. Confirm outcome

| Check | Where |
| --- | --- |
| Webhook delivery | Company Admin → Webhooks · or `GET /demo/webhooks/events` |
| Session + identity | Identity Console · or `GET /v1/sessions/{id}` / `GET /v1/identities/{id}` |
| Trust decision | Identity `trust_state` / `trust_factors` · webhook `payload.decision` |

Decision aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing engine signals never auto-accept.

## 7. Optional review

If trust is `review`, claim the case in Identity Console (or `POST /v1/review-cases/{identity_id}/claim`) and transition with `accept` / `reject`.

API details: [Creating a session (API)](api.md). Production hardening: [Production](production.md).
