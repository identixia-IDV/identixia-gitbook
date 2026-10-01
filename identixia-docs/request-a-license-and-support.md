---
description: >-
  How to request an Identixia license for Face SDK, ID Document SDK, and IDV.
---

# Request a License & Support

## Mobile SDK (Face / Document)

1. Build with **your** applicationId / bundle id (not the demo id).
2. Contact us with the id and product (Face recognition / Face liveness / Document recognition / Document authenticity).
3. Activate → init as shown on the platform page.

Demo keys work only for demo application ids.

## Server SDK (Windows / Linux / Docker)

1. Start the API once.
2. `GET /api/machinecode` → copy `data.machinecode`.
3. Send that code to Identixia. **Docker and bare metal differ.**
4. `POST /api/activate` or place `license.txt` and restart.
5. Confirm with `GET /api/licenseStatus`.

## IDV

IDV uses Hybrid licensing via `license-admin` / `license_v2`. Issuer UI: `:14190` (localhost). Company systems use `company-backend` (sample `:14195`) to hold the service token and start sessions — see the [IDV → Company integration](idv/company.md) docs.

## Support

{% include "./.gitbook/includes/contact.md" %}
