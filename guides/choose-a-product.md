---
description: >-
  Match an Identixia repository to the face or ID document license you need, then run the sample.
icon: compass
---

# Choose a product

Use the license flags on the product introduction, then clone the repository in that row.

## Face

| You need | License flags | Repositories | Server port |
| --- | --- | --- | ---: |
| Detect, attributes, quality, templates, 1:1, 1:N, and a passive liveness score | `recognition` and `liveness` | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Names start with `FaceRecognition-LivenessDetection-`. | 14103 |
| Detect, templates, 1:1, and 1:N. No liveness score. | `recognition` | Windows [`FaceRecognition-Windows`](https://github.com/identixia-IDV/FaceRecognition-Windows) and Linux / Docker [`FaceRecognition-Docker`](https://github.com/identixia-IDV/FaceRecognition-Docker). There is no phone SDK for this license. | 14104 |
| A presentation-attack score. No enroll and no 1:N search. | `liveness` | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Names start with `FaceLivenessDetection-`. | 14105 |

Phone and desktop pages for recognition plus liveness are in [Developers](https://docs.identixia.com/developers/face-sdk/integration-guide). Face liveness phone samples that have no separate developer page are the Flutter, React Native, Ionic Capacitor, and Ionic Cordova repositories above. Their setup is the repository README.

Windows and Docker face recognition calls are `POST /api/face/analyze`, `/api/face/template`, `/api/face/compare`, `/api/face/enroll`, and `/api/face/search`. Do not call `/api/face/liveness` on the recognition build. The liveness build uses `POST /api/face/liveness` and `POST /api/face/deepfake`.

## ID document

| You need | License flags | Repositories | Server port |
| --- | --- | --- | ---: |
| Locate, OCR, MRZ, barcode, cropped images, and authenticity checks | `recognition` and `authenticity` | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Names start with `ID-Document-Recognition-Liveness-Detection-`. | 14102 |
| OCR, MRZ, and barcode. No document liveness route. | `recognition` | Linux / Docker [`ID-Document-Recognition-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Docker). | 14106 |
| Screen, printout, and substitution checks. No MRZ, barcode, or visual fields. | `authenticity` | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Names start with `ID-Document-Liveness-Detection-`. | 14107 |

The recognition build does not serve `/api/document/liveness`. The authenticity build does not expose `/api/document/process`. On the combined server, `POST /api/document/process` returns OCR and authenticity when that license flag is on, `POST /api/document/recognition` returns OCR / MRZ / barcode, and `POST /api/document/liveness` returns authenticity.

## After you pick a repository

1. [Run the sample](run-the-sample.md) until it shows **Ready**.
2. [Request a license](request-a-license-and-support.md) for the sample application id or for your own application id or machine code.
3. [Contact](contact-us.md) if you need a key or help with a platform.

<a href="https://docs.identixia.com/developers" class="button primary" data-icon="code">Open Developers</a>

{% include "./.gitbook/includes/footer.md" %}
