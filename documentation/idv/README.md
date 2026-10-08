---
description: >-
  Build web and mobile identity verification with Identixia IDV. Connect document OCR, face matching, capture apps, verification sessions, and reviews.
icon: building
---

# Self-Hosted Identity Verification and KYC Platform

**IDV** is Identixia's self-hosted identity verification platform for web and mobile Know Your Customer (KYC) workflows. It uses [SDK Server](../sdk-server/) (Face + Document HTTP engines) as the biometric backend.

The IDV platform connects your company backend and applicant capture apps to the Face and Document SDK services. It manages the verification workflow while those SDKs perform biometric and document processing.

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

1. [Project structure](https://docs.identixia.com/guides/idv/project-structure)
2. [Project setup](https://docs.identixia.com/guides/idv/environment) — `.env`, tokens, storage
3. [Initial setup process](https://docs.identixia.com/guides/idv/initial-setup)
4. [Understanding session states](session-states.md)
5. [iOS & Android](https://docs.identixia.com/developers/idv/components-clients) (and web demos)
6. [Creating a session (API)](https://docs.identixia.com/developers/idv/api)
7. [Webhook integration](https://docs.identixia.com/developers/idv/company-webhooks)
8. [Quick start](https://docs.identixia.com/guides/idv/quick-start) · [Walkthrough](https://docs.identixia.com/guides/idv/walkthrough)
9. [Production](https://docs.identixia.com/guides/idv/production) · [Reference](reference.md)

{% hint style="info" %}
Identity Console
{% endhint %}

{% hint style="danger" %}
**Safety:** Keep the company **service bearer** on the company backend only. Capture apps receive a short-lived **capture token**. Never commit secrets. `IDV_OPEN_API=1` / bearer `demo` is for **localhost demos only**.
{% endhint %}

{% include "../.gitbook/includes/footer.md" %}
