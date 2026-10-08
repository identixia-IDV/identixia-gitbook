---
description: >-
  Use Identity Console to manage IDV sessions, manual reviews, webhooks, and identity verification workflows.
icon: table-columns
---

# Identity Console for Verification Operations

| Item | Detail |
| --- | --- |
| Folder | `IDV/IDV_console/` |
| Develop | `http://127.0.0.1:14188/` (proxies API to `:14187`) |
| Production | `npm run build` → served from `IDV_server` at `/admin/` |

```bash
cd IDV/IDV_console
npm install && npm run dev
```

Use this console to register company webhook URLs, inspect identities/sessions, and run manual review.

{% include "../.gitbook/includes/footer.md" %}
