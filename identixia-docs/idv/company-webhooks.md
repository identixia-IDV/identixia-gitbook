---
description: >-
  Subscribe to session events, verify HMAC signatures, and handle deliveries safely.
---

# Webhook integration

## Subscribe to events

1. Expose an HTTPS endpoint on **your** company server (sample: `POST /demo/webhooks/idv` on `:14195`).
2. In **Identity Console → Webhooks**, register that URL.
3. Select events: `session.created`, `session.completed` (only these are emitted today).
4. Store the one-time `whsec_…` secret in Company Admin **Settings** (or your secret manager).

Local sample URL: `http://127.0.0.1:14195/demo/webhooks/idv`.

## Handle webhooks

Your endpoint receives `POST` JSON:

```json
{
  "eventId": "evt_...",
  "eventType": "session.completed",
  "occurredAt": "2026-09-24T12:00:00+00:00",
  "payload": {
    "sessionId": "ses_...",
    "decision": "review"
  }
}
```

Headers include `X-IDV-Event` and `X-IDV-Signature`.

## Security verification

```text
X-IDV-Signature: sha256=<HMAC-SHA256 of the raw body>
```

Compute HMAC-SHA256 over the **raw** request body with `whsec_…` and compare in constant time. Leave the secret blank only for an unsigned **local** trial.

{{% hint style="danger" %}}
In production always verify the signature, reject bad signatures, and make handlers idempotent. Poll `GET /v1/sessions/{id}` if a delivery is missing.
{{% endhint %}}

## Test the integration

Use Identity Console → Webhooks → **Send test**, or finish a verification. Company Admin **Webhooks** (or `GET /demo/webhooks/events`) lists deliveries.

## Event types (supported)

| Event | When |
| --- | --- |
| `session.created` | New verification session started |
| `session.completed` | Verification finished (see `payload.decision` / identity trust) |

Related: [Initial setup process](initial-setup.md) · [Creating a session (API)](api.md) · [Session states](session-states.md).
