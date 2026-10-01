---
description: >-
  Session status and identity trust_state through an Identixia IDV verification.
---

# Session states

## Session status

Each verification **session** moves through:

| Status | Meaning |
| --- | --- |
| `created` | Session row exists; capture may not have started |
| `capturing` | Waiting for / receiving applicant step submissions |
| `processing` | Engines / pipeline evaluating the latest submission |
| `completed` | Finalized — identity created or linked; see trust state |
| `cancelled` | Stopped by the company (service bearer) |
| `expired` | Timed out before completion |
| `technical_error` | Unrecoverable platform / pipeline error |

## Identity trust state

When a session completes, the **identity** carries the decision:

| `trust_state` | Meaning |
| --- | --- |
| `incomplete` | Not finished evaluating |
| `review` | Needs human review in Identity Console |
| `accepted` | Auto-accepted or accepted after review |
| `rejected` | Auto-rejected or rejected after review |
| `anonymized` | Personal data erased |

Aggregation is **most-severe-wins** (`reject` > `review` > `accept`). Missing engine signals never auto-accept.

## Starting a verification (operator)

Like a “create session + share link” flow:

1. Company Admin → **Start verification** (or `POST /demo/start-verification`).
2. Copy **`launchUrl`** (or show a QR of that URL in your own UI) and/or **`captureToken`**.
3. Applicant opens the link / app; session stays `capturing` until steps finish.
4. On completion, webhook `session.completed` fires; Identity Console shows the identity.

Each capture token / launch URL is session-scoped. Start a **new** verification for each applicant attempt.

## Reviewer path

If `trust_state` is `review`:

1. Open Identity Console → review cases / identity detail.
2. Claim the case if required.
3. Transition with `accept` or `reject` ([Creating a session (API)](api.md) · identities section).

Next: [Creating a session (API)](api.md) · [Webhook integration](company-webhooks.md).
