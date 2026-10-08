---
description: >-
  How to request an Identixia license for Face SDK, ID Document SDK, and IDV.
---

# Request a License & Support

{% hint style="warning" %}
Demo keys work only with the demo application id. A production key must match the id or machine code you send.
{% endhint %}

## Mobile SDK (Face / Document)

{% stepper %}
{% step %}
### Build with your id
Use your applicationId or bundle id, not the demo id.
{% endstep %}
{% step %}
### Send the id
Contact Identixia with that id and the product: Face recognition, Face liveness, Document recognition, or Document authenticity.
{% endstep %}
{% step %}
### Activate
Call activate, then init, as shown on the platform page.
{% endstep %}
{% endstepper %}

## Server SDK (Windows / Linux / Docker)

{% stepper %}
{% step %}
### Start the API
Start the container or Windows service once.
{% endstep %}
{% step %}
### Copy the machine code
Call `GET /api/machinecode` and copy `data.machinecode`. Docker and bare-metal codes differ.
{% endstep %}
{% step %}
### Activate
Call `POST /api/activate`, or set `LICENSE=` in `.env` and restart. Confirm with `GET /api/licenseStatus`.
{% endstep %}
{% endstepper %}

## IDV

IDV uses Hybrid licensing via `license` and `license/license_v2`. The issuer UI listens on `:14190` (localhost). Company systems use `company/backend` (sample `:14195`) to hold the service token and start sessions — see [Company integration](idv/company.md).

## Support

{% include "./.gitbook/includes/contact.md" %}
