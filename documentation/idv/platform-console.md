---
description: >-
  IDV_console — tenant operators: sessions, reviews, webhooks, workflows.
icon: table-columns
---

# Identity Console

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
