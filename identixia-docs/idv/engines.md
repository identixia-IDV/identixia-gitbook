---
description: >-
  How IDV calls Identixia Document and Face HTTP APIs.
---

# Document & Face engines

## Default HTTP engines

When `IDV_ENGINES=http`, the platform calls:

| Role | Default URL | Example paths |
| --- | --- | --- |
| Document Reader | `http://127.0.0.1:14102` | `/api/documentProcess`, `/api/documentRecognition`, `/api/documentLiveness` |
| Face Recognition + liveness | `http://127.0.0.1:14103` | `/api/face/compare`, `/api/face/boxes`, `/api/face/template`, `/api/face/score`, `/api/face/liveness` |

These are the same APIs documented under [ID Document SDK](../id-document-sdk/) and [Face SDK](../face-sdk/).

## Example — create session then capture (sketch)

```http
POST /v1/sessions
Authorization: Bearer demo
X-Tenant-Id: ten_demo
Content-Type: application/json

{ "workflow_id": "onboarding_standard", "environment": "test" }
```

The response includes session id and next step. Your backend mints a capture token; the applicant app posts submissions with `X-IDV-Step-ID` and `Authorization: Bearer <capture-token>`.

IDV then calls Document/Face engines, stores results, and applies trust decision policy.

## Matching note

Face 1:1 / 1:N uses the **Face SDK matcher**. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.

## Full API tables

Postman collections and endpoint-level persistence notes live in `IDV/docs/API.md` and `IDV/idv-server/postman/` (source tree).
