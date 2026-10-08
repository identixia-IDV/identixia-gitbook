---
description: >-
  IDV is Identixia's self-host web & mobile KYC platform. It uses SDK Server as the biometric backend.
---

# IDV: Self-Host KYC Platform

**IDV** is Identixia's open web & mobile KYC platform. It uses [SDK Server](../sdk-server/) (Face + Document HTTP engines) as the biometric backend.

It does not replace those SDKs — it orchestrates them between your company systems and applicant capture apps.

## Project components

| Component | Role | Folder · port |
| --- | --- | --- |
| **Platform (Admin)** | Tenant API, reviews, Identity Console | `IDV_server/` · `:14187` · UI `:14188` / `/admin` |
| **Company (Merchant)** | Holds service credentials; starts sessions | `company/backend/` · `:14195` · Admin `:14189` |
| **Applicant (User)** | Web / mobile capture apps | `client/` · e.g. web `:5175` |
| **Engines** | Document + Face HTTP APIs | Document `:14102` · Face `:14103` |

```text
Applicant app ──► Company backend :14195 ──► IDV server :14187 ──► Face / Document engines
                      │                         │
               Company Admin :14189      Identity Console /admin
```

## Guide (in order)

1. [Project structure](project-structure.md)
2. [Project setup](environment.md) — `.env`, tokens, storage
3. [Initial setup process](initial-setup.md)
4. [Understanding session states](session-states.md)
5. [iOS & Android](components-clients.md) (and web demos)
6. [Creating a session (API)](api.md)
7. [Webhook integration](company-webhooks.md)
8. [Quick start](quick-start.md) · [Walkthrough](walkthrough.md)
9. [Production](production.md) · [Reference](reference.md)

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/idv/audit-console.png" alt="Identity Console" width="520"><figcaption>Identity Console</figcaption></figure>

{% hint style="danger" %}
**Safety:** Keep the company **service bearer** on the company backend only. Capture apps receive a short-lived **capture token**. Never commit secrets. `IDV_OPEN_API=1` / bearer `demo` is for **localhost demos only**.
{% endhint %}
