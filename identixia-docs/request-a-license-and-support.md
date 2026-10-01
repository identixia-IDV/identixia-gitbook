---
description: >-
  How to request an Identixia license for Face SDK, ID Document SDK, and IDV.
---

# Request a License & Support

## Mobile SDK (Face / Document)

1. Build with **your** applicationId or bundle id (not the demo id).
2. Contact us with that id and the product (Face recognition, Face liveness, Document recognition, or Document authenticity).
3. Activate and initialize as shown on the platform page.

Demo keys work only for demo application ids.

## Server SDK (Windows / Linux / Docker)

1. Start the API once.
2. Call `GET /api/machinecode` and copy `data.machinecode`.
3. Send that code to Identixia. Docker and bare-metal machine codes differ — license the environment you ship.
4. Call `POST /api/activate`, or place `license.txt` and restart.
5. Confirm with `GET /api/licenseStatus`.

## IDV

IDV uses Hybrid licensing via `license-admin` and `license_v2`. The issuer UI listens on `:14190` (localhost). Company systems use `company-backend` (sample `:14195`) to hold the service token and start sessions — see [Company integration](idv/company.md).

## Support

{% include "./.gitbook/includes/contact.md" %}
