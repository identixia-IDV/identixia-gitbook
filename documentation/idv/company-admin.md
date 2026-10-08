---
description: >-
  Use the sample Company Admin interface to manage your company integration with the Identixia identity verification platform.
icon: user-gear
---

# Company Admin Console for Identity Verification

| Item | Detail |
| --- | --- |
| Folder | `IDV/company/admin/` |
| Develop | `http://127.0.0.1:14189/` |
| Production | `npm run build` → `company/backend` serves `/admin/` |

```bash
cd IDV/company/admin
npm install && npm run dev
```

## Operator areas (sample)

| Area | What it does |
| --- | --- |
| Overview | IDV reachability, session/webhook counts |
| Start verification | Pick workflow, external ref, customer; copy capture token / URL |
| Sessions | Refresh status from IDV, cancel, inspect payload |
| Workflows | List published workflows from `/v1/workflows` |
| Webhooks | Recent deliveries + settings for webhook URL/secret |

Shared React helpers: `IDV/packages/admin-ui`.

{% include "../.gitbook/includes/footer.md" %}
