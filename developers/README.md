---
description: >-
  Add the Identixia SDK to your app: download the runtime, activate a license, and call the kit on each platform.
icon: code
---

# Identity Verification SDK and API Developer Guides

Add the SDK to your own application in this order.

{% stepper %}
{% step %}
### Open the integration guide
Start with [Face](face-sdk/integration-guide.md) or [ID documents](id-document-sdk/integration-guide.md). The guide names the repository for the license you have.
{% endstep %}
{% step %}
### Download the runtime
Clone that repository, then download the runtime zip from its GitHub Releases page and unzip it into the sample folder. Native libraries and database packs are not in git.
{% endstep %}
{% step %}
### Activate, then call the kit
Activate the license before initialization. Mobile calls run on a background thread. Server calls use the HTTP routes on the platform page.
{% endstep %}
{% endstepper %}

<table data-view="cards">
  <thead>
    <tr>
      <th>Start from the product you licensed</th>
      <th data-card-target data-type="content-ref" data-hidden>Open</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Face</strong> recognition and liveness SDK integration for mobile apps and servers.</td>
      <td><a href="face-sdk/integration-guide.md">Face integration guide</a></td>
    </tr>
    <tr>
      <td><strong>ID document</strong> capture, text recognition, MRZ reading, and barcode extraction.</td>
      <td><a href="id-document-sdk/integration-guide.md">Document integration guide</a></td>
    </tr>
    <tr>
      <td><strong>HTTP API</strong> on Windows or Docker.</td>
      <td><a href="sdk-server/face-recognition.md">Face recognition API</a></td>
    </tr>
  </tbody>
</table>

{% columns %}
{% column %}
What the product returns is in [Documentation](https://docs.identixia.com).
{% endcolumn %}
{% column %}
Choosing a repository, running a sample, and requesting a license are in [Guides](https://docs.identixia.com/guides).
{% endcolumn %}
{% endcolumns %}

<a href="https://docs.identixia.com/guides/run-the-sample" class="button primary" data-icon="play">Run the sample</a>
<a href="https://github.com/identixia-IDV" class="button secondary" data-icon="github">Repositories</a>

{% include "./.gitbook/includes/footer.md" %}
