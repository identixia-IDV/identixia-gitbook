---
description: >-
  Read passports and ID cards with Identixia document OCR, MRZ, and barcode SDKs. Add licensed document liveness checks on mobile or self-hosted servers.
---

# ID Document OCR and Liveness Detection SDKs

Build document capture and identity data extraction with Identixia ID document recognition, optical character recognition (OCR), and document liveness SDKs.

Read passports, national ID cards, and driver licenses on **your** device or server. Extract printed text, read the machine-readable zone (MRZ), decode supported barcodes, and obtain cropped document images. Add document anti-spoofing checks when enabled by your license.

We provide SDKs for **Android**, **iOS**, **Flutter**, **React Native**, **Ionic**, **Windows**, and **Linux / Docker**.

| Function | What you get | License flag |
| --- | --- | --- |
| **Recognition** | Locate, OCR, MRZ, barcode, cropped images | `recognition` |
| **Liveness / authenticity** | Screen / printout / substitution checks | `authenticity` |

Combined SDK repositories support both recognition and document liveness when licensed. Choose the **liveness-only** Linux / Docker API when you need document authenticity checks without text extraction.

![Document demo status](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png)

## Next

* [Reference](reference.md) — platform quick starts and sample repositories
* [Result Format](result-json.md) · [Security check fields](security-fields.md)
* [SDK Server](../sdk-server/) — HTTP API (Windows & Docker)
* Function notes: [Recognition](recognition.md) · [Liveness](liveness.md)

{% hint style="info" %}
Document images and OCR fields stay on **your** device or server. Parse [Result Format](result-json.md) — do not scrape the Result UI.
{% endhint %}
