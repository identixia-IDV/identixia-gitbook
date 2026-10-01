---
description: >-
  idv-server: platform API, workers, storage, and /admin mount.
---

# IDV server

| Item | Detail |
| --- | --- |
| Folder | `IDV/idv-server/` |
| API | `http://127.0.0.1:14187/v1` |
| Admin (production build) | `http://127.0.0.1:14187/admin/` |
| Postman | `IDV/idv-server/postman/` |

```bash
cd IDV/idv-server
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
set IDV_OPEN_API=1
python app.py
```

`IDV_OPEN_API=1` enables the local demo bearer. Workers and decision code live under `idv-server/idv/`.
