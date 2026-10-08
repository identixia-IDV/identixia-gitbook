---
description: >-
  Identixia Hybrid issuer (license) on localhost :14190.
icon: key
---

# License Admin

| Item | Detail |
| --- | --- |
| Folder | `IDV/license/` |
| UI | `http://127.0.0.1:14190/` (**localhost only**) |
| Brand | `license/brand/` → `/brand/*` |

```bash
cd IDV/license
pip install -r requirements.txt
set LICENSE_ADMIN_PASSWORD=a-long-first-password
python app.py
```

First sign-in enrols an authenticator for the seeded `admin` operator.

### Operator exchange

| Action | Customer sends | You return |
| --- | --- | --- |
| First issue | `license_request.txt` | `license.txt` |
| Same host again | — | Used count kept (no restore) |

`POST /api/v2/online/report` may be exposed via reverse proxy for customer sync; do **not** expose the operator UI off-box.

{% include "../.gitbook/includes/footer.md" %}
