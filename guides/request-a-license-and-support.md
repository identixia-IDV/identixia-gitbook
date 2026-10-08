---
description: >-
  Request a license for Face SDK, ID Document SDK, or IDV. Learn which app identifier or machine code to provide and how to activate.
icon: envelope
---

# Request an Identixia SDK License and Technical Support

{% hint style="warning" %}
The bundled demo key is tied to the sample application's identifier. For your own app or server, request a license issued for its application ID, bundle identifier, or machine code.
{% endhint %}

## Mobile SDK (Face / Document)

{% stepper %}
{% step %}
### Build with your id
For your own app, configure its Android application ID or iOS bundle identifier before requesting a license. Keep the original identifier when evaluating the sample with its bundled demo key.
{% endstep %}
{% step %}
### Send the id
Send Identixia your application identifier, target platform, and required features: face recognition, face liveness, document OCR, or document liveness. The license must match the app and features you intend to use.
{% endstep %}
{% step %}
### Activate
Replace the demo key with the key issued for your app. Follow the platform sample to activate the license before initializing the SDK, then check the license status before using its features.
{% endstep %}
{% endstepper %}

## Server SDK (Windows / Linux / Docker)

{% stepper %}
{% step %}
### Start the API
Start the Docker container or Windows API service so you can request the machine code used for licensing.
{% endstep %}
{% step %}
### Copy the machine code
Call `GET /api/machinecode` in the environment where the SDK will run and copy `data.machinecode` from the JSON response. Send this code to Identixia with the product you need; a container may report a different code from its host.
{% endstep %}
{% step %}
### Activate
Submit your issued key to `POST /api/activate`, or set the `LICENSE` value in the server's `.env` file and restart. Check `GET /api/licenseStatus` to confirm activation and the features enabled by your license.
{% endstep %}
{% endstepper %}

## IDV

IDV uses Hybrid licensing via `license` and `license/license_v2`. The issuer UI listens on `:14190` (localhost). Company systems use `company/backend` (sample `:14195`) to hold the service token and start sessions — see [Company integration](https://docs.identixia.com/idv/company).

## Support

{% include "./.gitbook/includes/contact.md" %}

{% include "./.gitbook/includes/footer.md" %}
