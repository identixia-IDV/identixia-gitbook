---
description: >-
  idv-server-ui — tenant operators: sessions, reviews, webhooks, workflows.
---

# Identity Console

| Item | Detail |
| --- | --- |
| Folder | `IDV/idv-server-ui/` |
| Develop | `http://127.0.0.1:14188/` (proxies API to `:14187`) |
| Production | `npm run build` → served from `idv-server` at `/admin/` |

```bash
cd IDV/idv-server-ui
npm install && npm run dev
```

Use this console to register company webhook URLs, inspect identities/sessions, and run manual review.
