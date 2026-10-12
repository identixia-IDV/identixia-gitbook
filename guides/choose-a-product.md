---
description: >-
  Match an Identixia repository to the face or ID document license you need, then run the sample.
icon: compass
---

# Choose a product

Use the license flags on the product introduction, then clone the repository in that row.

## Face

Recognition and liveness. License flags `recognition` and `liveness`. Server port **14103**.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/face-sdk/android) | [`FaceRecognition-LivenessDetection-Android`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/face-sdk/ios) | [`FaceRecognition-LivenessDetection-iOS`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/face-sdk/flutter) | [`FaceRecognition-LivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/face-sdk/react-native) | [`FaceRecognition-LivenessDetection-React-Native`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/face-sdk/ionic-capacitor) | [`FaceRecognition-LivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/face-sdk/ionic-cordova) | [`FaceRecognition-LivenessDetection-Ionic-Cordova`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/face-sdk/windows) | [`FaceRecognition-LivenessDetection-Windows`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/linux-docker) | [`FaceRecognition-LivenessDetection-Docker`](https://github.com/identixia-IDV/FaceRecognition-LivenessDetection-Docker) |

Recognition without a liveness score. License flag `recognition`. These builds do not return a liveness score. Server port **14104**. Do not call `/api/face/liveness`.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/face-sdk/recognition-android) | [`FaceRecognition-Android`](https://github.com/identixia-IDV/FaceRecognition-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/face-sdk/recognition-ios) | [`FaceRecognition-iOS`](https://github.com/identixia-IDV/FaceRecognition-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/face-sdk/recognition-flutter) | [`FaceRecognition-Flutter`](https://github.com/identixia-IDV/FaceRecognition-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/face-sdk/recognition-react-native) | [`FaceRecognition-React-Native`](https://github.com/identixia-IDV/FaceRecognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/face-sdk/recognition-ionic-capacitor) | [`FaceRecognition-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceRecognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/face-sdk/recognition-ionic-cordova) | [`FaceRecognition-Ionic-Cordova`](https://github.com/identixia-IDV/FaceRecognition-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/face-sdk/recognition-windows) | [`FaceRecognition-Windows`](https://github.com/identixia-IDV/FaceRecognition-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/recognition-linux-docker) | [`FaceRecognition-Docker`](https://github.com/identixia-IDV/FaceRecognition-Docker) |

Presentation-attack and deepfake scores. License flag `liveness`. These builds do not enroll a gallery and do not run 1:N search. Server port **14105**. Routes: `POST /api/face/liveness` and `POST /api/face/deepfake`. Report REAL only when both checks pass.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/face-sdk/liveness-android) | [`FaceLivenessDetection-Android`](https://github.com/identixia-IDV/FaceLivenessDetection-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/face-sdk/liveness-ios) | [`FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/face-sdk/liveness-flutter) | [`FaceLivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceLivenessDetection-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/face-sdk/liveness-react-native) | [`FaceLivenessDetection-React-Native`](https://github.com/identixia-IDV/FaceLivenessDetection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/face-sdk/liveness-ionic-capacitor) | [`FaceLivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/face-sdk/liveness-ionic-cordova) | [`FaceLivenessDetection-Ionic-Cordova`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/face-sdk/liveness-windows) | [`FaceLivenessDetection-Windows`](https://github.com/identixia-IDV/FaceLivenessDetection-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/liveness-linux-docker) | [`FaceLivenessDetection-Docker`](https://github.com/identixia-IDV/FaceLivenessDetection-Docker) |

## ID document

Recognition and authenticity. License flags `recognition` and `authenticity`. Server port **14102**. `POST /api/document/process` returns OCR and authenticity when that flag is on. `POST /api/document/recognition` returns OCR, MRZ, and barcode. `POST /api/document/liveness` returns authenticity.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/id-document-sdk/android) | [`ID-Document-Recognition-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/id-document-sdk/ios) | [`ID-Document-Recognition-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/id-document-sdk/flutter) | [`ID-Document-Recognition-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/id-document-sdk/react-native) | [`ID-Document-Recognition-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/id-document-sdk/ionic-capacitor) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/id-document-sdk/ionic-cordova) | [`ID-Document-Recognition-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/id-document-sdk/windows) | [`ID-Document-Recognition-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/linux-docker) | [`ID-Document-Recognition-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Docker) |

OCR, MRZ, and barcode without document liveness. License flag `recognition`. Server port **14106**. This build does not serve `/api/document/liveness`.

| Platform | Guide | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/id-document-sdk/recognition-android) | [`ID-Document-Recognition-Android`](https://github.com/identixia-IDV/ID-Document-Recognition-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/id-document-sdk/recognition-ios) | [`ID-Document-Recognition-iOS`](https://github.com/identixia-IDV/ID-Document-Recognition-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/id-document-sdk/recognition-flutter) | [`ID-Document-Recognition-Flutter`](https://github.com/identixia-IDV/ID-Document-Recognition-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/id-document-sdk/recognition-react-native) | [`ID-Document-Recognition-React-Native`](https://github.com/identixia-IDV/ID-Document-Recognition-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/id-document-sdk/recognition-ionic-capacitor) | [`ID-Document-Recognition-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Recognition-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/id-document-sdk/recognition-ionic-cordova) | [`ID-Document-Recognition-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Recognition-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/id-document-sdk/recognition-windows) | [`ID-Document-Recognition-Windows`](https://github.com/identixia-IDV/ID-Document-Recognition-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/recognition-linux-docker) | [`ID-Document-Recognition-Docker`](https://github.com/identixia-IDV/ID-Document-Recognition-Docker) |

Screen, printout, and substitution checks. License flag `authenticity`. No MRZ, barcode, or visual fields. Server port **14107**. `POST /api/document/liveness` takes `images` entries `{image, page_idx}`. This server does not expose `/api/document/process`.

| Platform | Where to start | Repository |
| --- | --- | --- |
| Android | [Android](https://docs.identixia.com/developers/id-document-sdk/liveness-android) | [`ID-Document-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android) |
| iOS | [iOS](https://docs.identixia.com/developers/id-document-sdk/liveness-ios) | [`ID-Document-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-iOS) |
| Flutter | [Flutter](https://docs.identixia.com/developers/id-document-sdk/liveness-flutter) | [`ID-Document-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Flutter) |
| React Native | [React Native](https://docs.identixia.com/developers/id-document-sdk/liveness-react-native) | [`ID-Document-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-React-Native) |
| Ionic Capacitor | [Ionic Capacitor](https://docs.identixia.com/developers/id-document-sdk/liveness-ionic-capacitor) | [`ID-Document-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | [Ionic Cordova](https://docs.identixia.com/developers/id-document-sdk/liveness-ionic-cordova) | [`ID-Document-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Cordova) |
| Windows | [Windows](https://docs.identixia.com/developers/id-document-sdk/liveness-windows) | [`ID-Document-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows) |
| Linux / Docker | [Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/liveness-linux-docker) | [`ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) |

## After you pick a repository

1. [Run the sample](run-the-sample.md) until it shows **Ready**.
2. [Request a license](request-a-license-and-support.md) for the sample application id or for your own application id or machine code.
3. [Contact](contact-us.md) if you need a key or help with a platform.

<a href="https://docs.identixia.com/developers" class="button primary" data-icon="code">Open Developers</a>

{% include "./.gitbook/includes/footer.md" %}
