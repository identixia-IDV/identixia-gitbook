---
description: >-
  How to request an Identixia SDK license for mobile and server products.
---

# Request a License & Support

## Need a license?

### Mobile SDK

1. Build your app with **your** applicationId / bundle id (not the demo id).
2. Contact us (email / WhatsApp / Telegram) with the id and product (Face / Liveness / Document).
3. Integrate the key with activate → init as shown on the platform page.

The sample apps ship a **demo key** for the sample id only. Do not reuse it in production.

### Server SDK (Windows / Linux / Docker)

1. Start the API once.
2. `GET /api/machinecode` and copy `data.machinecode`.
3. Send that code to Identixia. **Docker and bare metal have different codes.**
4. `POST /api/activate` with the license file, or place `license.txt` and restart.
5. Confirm with `GET /api/licenseStatus`.

## Support

We offer integration help and after-sale support for Identixia biometric solutions.

{% include "./.gitbook/includes/contact.md" %}
