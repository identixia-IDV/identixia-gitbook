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

## What you get

| Capability | Description |
| --- | --- |
| Locate and crop | Find the ID document in a camera frame or still image |
| OCR | Printed fields such as the name, document number, and dates |
| MRZ | Machine-readable zone, including check digits |
| Barcode / QR | Extracted when the document has one |
| Front and back | Both sides when the workflow requires them |
| Document authenticity | Screen, printout, and substitution checks when the license includes `authenticity` |
| Result JSON | `identity`, `readings`, `tests`, `images`, and `session`. Parse this object. Do not scrape the Result screen |

Authenticity is rows in `tests` with `group: "authenticity"`. An empty set is not a pass. See [Result format](result-json.md) and [Security checks](security-fields.md).

## What you need

| Requirement | Detail |
| --- | --- |
| License | `recognition` for OCR, MRZ, and barcode. Add `authenticity` for the security checks |
| Runtime | From the product repository, run `python scripts/get_runtime.py` |
| Database | `document.xdb`. On Android it is embedded in the AAR. On Windows and Linux it sits at the top of `lib/cpu/` |
| Capture | A physical device for camera demos. Align the document in the guide and capture the back when the document has one |

If `document.xdb` is missing, activate can succeed and OCR still fails at runtime.

## Samples

These repositories include recognition and document liveness. Server port **14102**. Gradio, when the image ships it, uses **14202**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](android.md) | [`ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) |
| iOS | [iOS](ios.md) | [`ID-Document-Recognition-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS) |
| Flutter | [Flutter](flutter.md) | [`ID-Document-Recognition-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Flutter) |
| React Native | [React Native](react-native.md) | [`ID-Document-Recognition-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](ionic-capacitor.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](ionic-cordova.md) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](windows.md) | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](linux-docker.md) | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) |

Other licenses use different repositories. [Choose a product](https://docs.identixia.com/guides/choose-a-product) lists them.

## Try it

1. Clone one repository above.
2. Run `python scripts/get_runtime.py`.
3. Follow [Run the sample](https://docs.identixia.com/guides/run-the-sample) until the sample shows **Ready**.
4. On Windows or Docker, call `POST /api/document/process` on port **14102**. See [SDK Server](../sdk-server/README.md).

![Document demo status](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-status.png)

## Next

* [Recognition](recognition.md) — OCR, MRZ, barcode, and crops
* [Liveness](liveness.md) — screen, printout, and substitution checks
* [Result format](result-json.md) · [Security checks](security-fields.md)

{% hint style="info" %}
Document images and OCR fields stay on **your** device or server. Parse [Result Format](result-json.md) — do not scrape the Result UI.
{% endhint %}
