---
description: >-
  Start and activate the Face and ID Document HTTP engines before connecting them to your self-hosted IDV platform.
icon: microchip
---

# Set Up Face and Document Engines for IDV

## Why this comes first

IDV calls Identixia **Document** and **Face** HTTP APIs for OCR, authenticity, match, and liveness. Start and activate those engines **before** the IDV server and company sample.

When `IDV_ENGINES=http`, the platform uses:

| Role | Default URL | Example paths |
| --- | --- | --- |
| Document Reader | `http://127.0.0.1:14102` | `/api/document/process`, `/api/document/recognition`, `/api/document/liveness` |
| Face Recognition + liveness | `http://127.0.0.1:14103` | `/api/face/compare`, `/api/face/boxes`, `/api/face/template`, `/api/face/score`, `/api/face/liveness` |

Child pages: [Document engine](engines-document.md) · [Face engine](engines-face.md).

Same process APIs as [ID Document SDK](https://docs.identixia.com/id-document-sdk) and [Face SDK](https://docs.identixia.com/face-sdk). Document responses follow [Result JSON](https://docs.identixia.com/id-document-sdk/result-json).

## Numbered setup

1. Run the Document server (Windows or Docker) on **14102** — see [ID Document SDK → Server](https://docs.identixia.com/id-document-sdk/full-server).
2. Run the Face server on **14103** — see [Face SDK → Server](https://docs.identixia.com/face-sdk/full-server).
3. Activate each engine with **its** machine code (`GET /api/machinecode` → send to Identixia → set `LICENSE=` in `.env` or `POST /api/activate`). Docker and bare metal codes differ.
4. Confirm health:

```bash
curl -s http://127.0.0.1:14102/api/health
curl -s http://127.0.0.1:14103/api/health
```

5. Set `IDV_ENGINES=http`, `DOCUMENT_API_URL`, and `FACE_API_URL` in `IDV_server/.env` (see [Project setup](https://docs.identixia.com/guides/idv/environment)).
6. Continue with [Initial setup process](https://docs.identixia.com/guides/idv/initial-setup) or `python IDV/IDV_server (then company)`.

## Session create (platform API)

Usually the **company backend** calls this with the service bearer (not the capture app):

```http
POST /v1/sessions
Authorization: Bearer demo
X-Tenant-Id: ten_demo
Idempotency-Key: <unique>
Content-Type: application/json

{ "workflow_id": "onboarding_standard" }
```

Then mint a capture token and hand it to the applicant app. Full flow: [Creating a session (API)](api.md) · [Walkthrough](https://docs.identixia.com/guides/idv/walkthrough).

## Matching note

Face 1:1 uses the **Face SDK matcher**. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.

{% include "../.gitbook/includes/footer.md" %}
