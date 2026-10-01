---
description: >-
  Sample merchant company server and admin UI that talk to IDV.
---

# Company integration

Your **company** (bank, fintech, marketplace) owns applicant UX launch and service credentials.

The sample in this repo:

| Piece | Folder | Port |
| --- | --- | --- |
| Company server | `company-backend/` | 14195 |
| Company Admin UI | `company-admin/` | 14189 (dev) · built into `:14195/admin` |

| Page | Topic |
| --- | --- |
| [Company backend](company-backend.md) | Start sessions, health, webhook ingest |
| [Company Admin](company-admin.md) | Operator UI |
| [Webhooks](company-webhooks.md) | Wire Identity Console → company receiver |

{{% hint style="info" %}}
Keep `IDV_SERVICE_TOKEN` on the company server only. Capture apps must not embed it.
{{% endhint %}}
