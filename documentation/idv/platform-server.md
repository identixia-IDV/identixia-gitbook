---
description: >-
  Explore the IDV platform API, background workers, storage, and admin interface for self-hosted identity verification.
icon: server
---

# IDV Identity Verification Server

| Item | Detail |
| --- | --- |
| Folder | `IDV/IDV_server/` |
| API | `http://127.0.0.1:14187/v1` |
| Admin (production build) | `http://127.0.0.1:14187/admin/` |
| Postman | `IDV/IDV_server/postman/` |
| OpenAPI notes | `IDV/docs/API.md` |

```bash
cd IDV/IDV_server
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
```

`IDV_OPEN_API=1` enables the local demo bearer (`demo` / `ten_demo`). Disable it outside local demos — see [Production](https://docs.identixia.com/guides/idv/production).

Integrator routes: [Creating a session (API)](https://docs.identixia.com/developers/idv/api). Decision code: `IDV_server/idv/decision/`.

{% include "../.gitbook/includes/footer.md" %}
