---
description: >-
  Explore face recognition, liveness detection, ID document OCR, and self-hosted KYC. Find SDK setup guides, HTTP APIs, and licensing instructions.
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
      <td><strong>IDV</strong> — self-hosted identity verification and Know Your Customer (KYC) sessions.</td>
      <td><a href="idv/README.md">IDV platform</a></td>
    </tr>
    <tr>
      <td><strong>SDK Server</strong> — the same HTTP API on Windows and Docker.</td>
      <td><a href="sdk-server/README.md">SDK Server</a></td>
    </tr>
  </tbody>
</table>

{% columns %}
{% column %}
### On a phone or desktop

Run the sample app for your platform, then integrate its capture and SDK calls into your application.

<a href="https://docs.identixia.com/developers" class="button primary" data-icon="code">Developers</a>
{% endcolumn %}
{% column %}
### First run

Choose a sample that supports the features you need, download its runtime, and activate the matching SDK license.

<a href="https://docs.identixia.com/guides" class="button secondary" data-icon="compass">Guides</a>
{% endcolumn %}
{% endcolumns %}

## Start here

{% stepper %}
{% step %}
### Choose the product
Open Face, Documents, or IDV above. Recognition-only builds do not include liveness. Liveness-only builds do not enroll or search a gallery.
{% endstep %}
{% step %}
### Run the sample
Clone the repository and follow the platform page. Android and iOS are separate setups.
{% endstep %}
{% step %}
### Activate
Request a license using your Android application ID, iOS bundle identifier, or server machine code. Activate the returned key before initializing the SDK.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Native engines and `*.xdb` databases ship on GitHub Releases. From a product clone, run `python scripts/get_runtime.py`. They are not committed to git.
{% endhint %}

<a href="https://identixia.com" class="button secondary" data-icon="globe">Website</a>
<a href="https://github.com/identixia-IDV" class="button secondary" data-icon="github">GitHub</a>
<a href="https://docs.identixia.com/guides/request-a-license-and-support" class="button primary" data-icon="key">Request a license</a>
