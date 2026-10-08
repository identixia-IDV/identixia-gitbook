---
description: >-
  Identixia documentation for Face SDK, ID Document SDK, SDK Server, and IDV.
icon: house
---

# Welcome to Identixia

<p align="center"><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/brand/logo.png" alt="Identixia" width="280"></p>

{% hint style="success" %}
Face recognition, face liveness, and ID document capture run on **your** device or server. Identixia does not receive the images.
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
      <td><strong>Face</strong> — recognition and passive liveness.</td>
      <td><a href="face-sdk/README.md">Face SDK</a></td>
    </tr>
    <tr>
      <td><strong>ID documents</strong> — OCR, MRZ, barcode, and document liveness.</td>
      <td><a href="id-document-sdk/README.md">ID Document SDK</a></td>
    </tr>
    <tr>
      <td><strong>IDV</strong> — self-hosted KYC sessions on your own stack.</td>
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

Use the sample app, then embed the SDK.

<a href="https://docs.identixia.com/developers" class="button primary" data-icon="code">Developers</a>
{% endcolumn %}
{% column %}
### First run

Pick the repository that matches the license, then activate.

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
Send the application id, bundle id, or machine code, then call activate before init.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Native engines and `*.xdb` databases ship on GitHub Releases. From a product clone, run `python scripts/get_runtime.py`. They are not committed to git.
{% endhint %}

<a href="https://identixia.com" class="button secondary" data-icon="globe">Website</a>
<a href="https://github.com/identixia-IDV" class="button secondary" data-icon="github">GitHub</a>
<a href="https://docs.identixia.com/guides/request-a-license-and-support" class="button primary" data-icon="key">Request a license</a>

{% include "./.gitbook/includes/footer.md" %}
