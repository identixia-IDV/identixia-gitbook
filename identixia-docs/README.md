---
description: >-
  What Identixia face and ID document products do, what you need to run a sample, and what the sample returns.
---

# Identixia Identity Verification SDK Documentation

![Identixia](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/brand/logo.png)

{% hint style="success" %}
Build identity verification with face recognition, passive liveness detection, and ID document capture. Processing runs on **your** device or server; images are not sent to Identixia.
{% endhint %}

## Products

<table data-view="cards">
  <thead>
    <tr>
      <th>Product</th>
      <th data-card-target data-type="content-ref" data-hidden>Open</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Face</strong> — face recognition, matching, and passive liveness detection.</td>
      <td><a href="face-sdk/README.md">Face SDK</a></td>
    </tr>
    <tr>
      <td><strong>ID documents</strong> — passport and ID card OCR, MRZ reading, barcode extraction, and document liveness.</td>
      <td><a href="id-document-sdk/README.md">ID Document SDK</a></td>
    </tr>
    <tr>
      <td><strong>SDK Server</strong> — the same HTTP API on Windows and Docker.</td>
      <td><a href="sdk-server/README.md">SDK Server</a></td>
    </tr>
  </tbody>
</table>

## Start here

{% stepper %}
{% step %}
### See what the product does
Open Face or ID documents above. Each page lists what the product is for, what you need, and what a sample returns.
{% endstep %}
{% step %}
### Run the sample
Follow [Run the sample](https://docs.identixia.com/guides/run-the-sample). Android and iOS are separate setups. From the product clone, run `python scripts/get_runtime.py`.
{% endstep %}
{% step %}
### Request a license
Send the Android application ID, iOS bundle identifier, or server machine code on [Request a license](https://docs.identixia.com/guides/request-a-license-and-support). Activate that key before initializing the SDK.
{% endstep %}
{% step %}
### Contact
License requests and technical support: [Contact](https://docs.identixia.com/guides/contact-us).
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Native engines and `*.xdb` databases ship on GitHub Releases. From a product clone, run `python scripts/get_runtime.py`. They are not committed to git.
{% endhint %}
