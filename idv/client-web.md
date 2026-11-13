---
description: >-
  Run the web IDV sample and connect browser-based applicant capture to your company backend and verification sessions.
---

# Web Identity Verification Sample App

## Run locally

```bash
cd IDV/demo_clients/demos/web
npm install && npm run dev
# http://127.0.0.1:5175/
```

## Integration rule

Start verification through the [company backend](company-backend.md) (or your own server). Do not embed the company service bearer in the browser.

Parent: [Applicant clients](components-clients.md).
