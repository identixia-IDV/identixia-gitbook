---
description: >-
  Connect Identity Console webhooks to the company-backend receiver.
---

# Company webhooks

## Wire-up (local)

1. Start **IDV server** and **company-backend** (`:14195`).
2. In **Company Admin → Settings**, copy the webhook URL:  
   `http://127.0.0.1:14195/demo/webhooks/idv`
3. In **Identity Console → Webhooks**, add that URL; select e.g. `session.created`, `session.completed`.
4. Copy the one-time `whsec_…` secret into Company Admin Settings and save.
5. Send a test event or finish a verification — Company Admin **Webhooks** lists deliveries.

## Signature

The receiver checks:

```text
X-IDV-Signature: sha256=<HMAC-SHA256 of the raw body>
```

Leave the secret blank only for an unsigned local trial.
