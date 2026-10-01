---
description: >-
  Create a verification session, mint a capture token, and hand launchUrl to the applicant.
---

# Creating a session (API)

## Step 1 — Get a service credential

| Environment | Credential |
| --- | --- |
| Local demo (`IDV_OPEN_API=1`) | Bearer `demo`, tenant `ten_demo` |
| Production | Real service token issued for your tenant — stored **only** on the company backend |

Never put the service bearer in a mobile/web applicant app.

## Step 2 — Recommended: company shortcut

Your merchant backend (sample `:14195`) creates the session and mint token together:

```bash
curl -s -X POST http://127.0.0.1:14195/demo/start-verification \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"onboarding_standard"}'
```

Response includes `sessionId`, `captureToken`, `launchUrl`, and `next_step`. Give **`launchUrl` / `captureToken`** to the applicant.

| Method | Path | Role |
| --- | --- | --- |
| `POST` | `/demo/start-verification` | Session + capture token |
| `GET` | `/demo/sessions/{id}` | Status refresh |
| `POST` | `/demo/sessions/{id}/cancel` | Cancel (service side) |
| `GET` | `/demo/workflows` | List workflows |

## Step 3 — Platform API (same result, two calls)

Use these from the **company backend** only:

```http
POST /v1/sessions
Authorization: Bearer <service>
X-Tenant-Id: <tenant>
Idempotency-Key: <unique>
Content-Type: application/json

{ "workflow_id": "onboarding_standard" }
```

```http
POST /v1/sessions/{session_id}/capture-token
Authorization: Bearer <service>
X-Tenant-Id: <tenant>
```

### Submit a capture step (applicant)

```http
POST /v1/sessions/{session_id}/submissions
Authorization: Bearer <captureToken>
Idempotency-Key: <unique>
X-IDV-Step-ID: <next_step.id>
X-IDV-Attempt: 1
Content-Type: application/json

{ "images": ["BASE64_JPEG"] }
```

Use the exact `next_step.id` from the session (e.g. `step_document_capture`, `step_face_capture`).

## Auth summary

| Caller | Credential |
| --- | --- |
| Company backend | Service bearer · `X-Tenant-Id` |
| Capture app | Capture token as Bearer |

Mutating calls often require `Idempotency-Key`.

## Other useful routes

| Method | Path | Role |
| --- | --- | --- |
| `GET` | `/v1/sessions` · `/v1/sessions/{id}` | List / poll session |
| `POST` | `/v1/sessions/{id}/cancel` | Cancel (service only) |
| `GET` | `/v1/identities` · `/v1/identities/{id}` | Finished record + `trust_state` |
| `POST` | `/v1/identities/{id}/transitions` | `accept` / `reject` / `reset_to_review` |
| `GET` | `/v1/workflows` | Includes `onboarding_standard` |

## Webhooks

Register in Identity Console. Events today: `session.created`, `session.completed`. See [Webhook integration](company-webhooks.md).

## Postman

| Collection | Path |
| --- | --- |
| Public | `IDV/idv-server/postman/IDV-Public.postman_collection.json` |
| Company sample | `IDV/idv-server/postman/Company-Backend-Sample.postman_collection.json` |
| Local env | `IDV/idv-server/postman/IDV-Local.postman_environment.json` |

Full persistence notes: `IDV/docs/API.md` in source. Session meanings: [Session states](session-states.md).
