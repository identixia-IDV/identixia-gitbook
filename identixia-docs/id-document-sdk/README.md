---
description: >-
  On-premises ID Document Recognition and Document Liveness SDKs.
---

# Introduction

On-premises ID Document Recognition and Document Liveness (authenticity) SDKs.

Read passports, national IDs, and driver licenses on **your** device or server: OCR / MRZ / barcode fields, cropped images, and optional anti-spoof authenticity checks.

We provide SDKs for **Android**, **iOS**, **Flutter**, **React Native**, **Ionic**, **Windows**, and **Linux / Docker**.

| Function | What you get | License flag |
| --- | --- | --- |
| **Recognition** | Locate, OCR, MRZ, barcode, cropped images | `recognition` |
| **Liveness / authenticity** | Screen / printout / substitution checks | `authenticity` |

Full-product repositories run both when licensed. A **liveness-only** Linux / Docker API is available when you need authenticity without the full OCR surface.

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png" alt="Document demo status" width="480"><figcaption>Desktop demo — status</figcaption></figure>

## Next

* [Reference](reference.md) — platform quick starts and sample repositories
* [Result Format](result-json.md) · [Security check fields](security-fields.md)
* [SDK Server](../sdk-server/) — HTTP API (Windows & Docker)
* Function notes: [Recognition](recognition.md) · [Liveness](liveness.md)

{% hint style="info" %}
Document images and OCR fields stay on **your** device or server. Parse [Result Format](result-json.md) — do not scrape the Result UI.
{% endhint %}
