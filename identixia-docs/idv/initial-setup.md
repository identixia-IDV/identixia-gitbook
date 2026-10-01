---
description: >-
  First Identity Console access, company settings, and webhook secret — after engines and .env.
---

# Initial setup process

## Before you start

1. Engines healthy — [Prerequisites: engines](engines.md)
2. `.env` configured — [Project setup](environment.md)
3. Platform + company running — `python IDV/scripts/start_local.py` or [Quick start](quick-start.md)

## 1. Open Identity Console

| Mode | URL |
| --- | --- |
| Production build (served by server) | http://127.0.0.1:14187/admin/ |
| Develop UI | http://127.0.0.1:14188/ |

Confirm the console can reach the API (meta / sessions list loads). With `IDV_OPEN_API=1`, local demo auth uses bearer `demo` and tenant `ten_demo`.

## 2. Company Admin settings

1. Open Company Admin: http://127.0.0.1:14189/ (or `:14195/admin/` when built-in).
2. Confirm **Overview** shows IDV reachable.
3. Note the webhook receiver URL:  
   `http://127.0.0.1:14195/demo/webhooks/idv`

## 3. Register webhook + store secret

1. Identity Console → **Webhooks** → add the company URL.
2. Select `session.created` and `session.completed`.
3. Copy the one-time `whsec_…` secret.
4. Paste it into Company Admin → **Settings** and save.

Details: [Webhook integration](company-webhooks.md).

{{% hint style="danger" %}}
Treat `whsec_…` like a password. Do not put it in applicant apps or public repos.
{{% endhint %}}

## 4. Service credential reminder

| Credential | Where it lives |
| --- | --- |
| `IDV_SERVICE_TOKEN` | Company backend only |
| Capture token / `launchUrl` | Returned to the applicant app for one session |

## 5. First verification

Use Company Admin → **Start verification** (workflow `onboarding_standard`) or:

```bash
curl -s -X POST http://127.0.0.1:14195/demo/start-verification \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"onboarding_standard"}'
```

Share `launchUrl` or `captureToken` with the applicant — not the service bearer.

Next: [Session states](session-states.md) · [Creating a session (API)](api.md) · [Walkthrough](walkthrough.md).
