---
description: >-
  Read passports and ID cards with Identixia document OCR, MRZ, and barcode SDKs. Add licensed document liveness checks on mobile or self-hosted servers.
icon: id-card
---

# ID Document OCR and Liveness Detection SDKs

Build document capture and identity data extraction with Identixia ID document recognition, optical character recognition (OCR), and document liveness SDKs.

Read passports, national ID cards, and driver licenses on **your** device or server. Extract printed text, read the machine-readable zone (MRZ), decode supported barcodes, and obtain cropped document images. Add document anti-spoofing checks when enabled by your license.

We provide SDKs for **Android**, **iOS**, **Flutter**, **React Native**, **Ionic**, **Windows**, and **Linux / Docker**.

| Function | What you get | License flag |
| --- | --- | --- |
| **Recognition** | Locate, OCR, MRZ, barcode, cropped images | `recognition` |
| **Liveness / authenticity** | Screen / printout / substitution checks | `authenticity` |

## What you need

A license that includes `recognition` for OCR, MRZ, and barcode reading. Add `authenticity` when you need screen, printout, or substitution checks. From the product repository, run `python scripts/get_runtime.py`.

## Try it

* [Run the sample](https://docs.identixia.com/guides/run-the-sample)
* [Choose a product](https://docs.identixia.com/guides/choose-a-product)
* [Result format](result-json.md) · [Security checks](security-fields.md)

![Document demo status](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png)

## Next

* [Recognition](recognition.md) · [Liveness](liveness.md)
* [SDK Server](../sdk-server/README.md)

{% hint style="info" %}
Document images and OCR fields stay on **your** device or server. Parse [Result Format](result-json.md) — do not scrape the Result UI.
{% endhint %}

{% include "../.gitbook/includes/footer.md" %}
