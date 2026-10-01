---
description: >-
  Sample company/backend: holds the service bearer and starts IDV sessions.
---

# Company backend (server)

## Role

`IDV/company/backend/` is the **sample company server**. It:

* Holds `IDV_SERVICE_TOKEN` / tenant id
* Starts verifications against IDV (`POST` session flows)
* Exposes demo APIs for capture apps (`POST /demo/start-verification`)
* Receives IDV webhooks (`POST /demo/webhooks/idv`)
* Serves the built Company Admin at `/admin/`

| Surface | URL |
| --- | --- |
| Health | `http://127.0.0.1:14195/health` |
| Start verification | `POST /demo/start-verification` |
| Webhook ingest | `POST /demo/webhooks/idv` |
| Admin UI (built) | `http://127.0.0.1:14195/admin/` |

## Run

```bash
cd IDV/company/backend
pip install -r requirements.txt
set IDV_BASE_URL=http://127.0.0.1:14187
set IDV_SERVICE_TOKEN=demo
set IDV_TENANT_ID=ten_demo
python app.py
```

Storage: `company/backend/database/company.sqlite` by default.

### Example — start via company backend (JS sketch)

```js
const start = await IdvApi.startViaCompanyBackend({
  companyBackendUrl: "http://127.0.0.1:14195",
});
// use start.captureToken / launch URL in the applicant app
```
