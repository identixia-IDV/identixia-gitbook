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

Child pages: [Document engine](engines-document.md) · [Face engine](engines-face.md).

Same APIs as [ID Document SDK](../id-document-sdk/) and [Face SDK](../face-sdk/).

## Example — session create (platform API)

Usually the **company backend** calls this with the service bearer (not the capture app):

```http
POST /v1/sessions
Authorization: Bearer demo
X-Tenant-Id: ten_demo
Content-Type: application/json

{ "workflow_id": "onboarding_standard", "environment": "test" }
```

Then the company mints / returns a capture token; the applicant posts submissions with `X-IDV-Step-ID`.

## Matching note

Face 1:1 / 1:N uses the **Face SDK matcher**. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.

## Full API tables

`IDV/docs/API.md` and `IDV/idv-server/postman/` in the source tree.
