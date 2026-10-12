---
description: >-
  Explore Identixia face recognition and liveness SDKs for mobile apps and self-hosted servers. Compare features and choose a platform.
icon: user
---

# Face Recognition and Liveness Detection SDKs

Build biometric identity verification with Identixia face recognition and passive face liveness detection SDKs. Run face matching and anti-spoofing checks on your own devices or servers.

Compare two faces with **one-to-one (1:1) matching**, or search an enrolled gallery with **one-to-many (1:N) identification**. Depending on the selected SDK and license, you can also run **passive face liveness** checks and obtain face attributes and landmark coordinates.

Use these SDKs in identity verification, attendance, and access-control workflows. Processing stays on **your** device or server.

We provide SDKs for **Android**, **iOS**, **Flutter**, **React Native**, **Ionic**, **Windows**, and **Linux / Docker**.

| Function | What you get | License flag |
| --- | --- | --- |
| **Recognition** | Detect, attributes, quality, templates, 1:1, 1:N | `recognition` |
| **Liveness** | Passive presentation-attack score | `liveness` |

## What you get

| Capability | Description |
| --- | --- |
| Face detection | Bounding box, landmarks, and pose |
| Attributes | Age, gender, and related traits when enabled |
| Quality | ICAO-style image and face quality scores |
| Templates | Numerical representations of faces that you store in **your** database |
| 1:1 match | Compare two images or two templates |
| 1:N identify | Save templates in a gallery, then search for the closest match |
| Passive liveness + deepfake | Presentation-attack and deepfake checks when the license includes `liveness`. Report REAL only when both pass |

A missing liveness score means the check was not evaluated. It does not mean the face passed.

## What you need

| Requirement | Detail |
| --- | --- |
| License | `recognition` for detect, template, and match. Add `liveness` for the presentation-attack and deepfake scores |
| Runtime | Download the runtime zip from GitHub Releases |
| Databases | `recognition.xdb`, `recognition-common.xdb`, `recognition-attr.xdb`, `recognition-quality.xdb`. When liveness is licensed, also `recognition-liveness.xdb` and `recognition-deepfake.xdb` |
| Gallery | You keep the enrolled templates. The SDK does not upload faces |

If a database pack is missing, activate can succeed and recognition or liveness still fails at runtime.

## Samples

These repositories include recognition and liveness. Server port **14103**. Gradio, when the image ships it, uses **14203**.

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

Other licenses use different repositories. [Choose a product](https://docs.identixia.com/guides/choose-a-product) lists them.

## Try it

1. Clone one repository above.
2. Download the runtime zip from GitHub Releases and unzip it into the sample folder.
3. Follow [Run the sample](https://docs.identixia.com/guides/run-the-sample) until the sample shows **Ready**.
4. On Windows or Docker, call the HTTP API on port **14103**. See [SDK Server](../sdk-server/README.md).

![Face SDK Android home](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/home.png)

## Next

* [Recognition](recognition.md) — detect, template, 1:1, and 1:N
* [Liveness](liveness.md) — presentation-attack and deepfake scores

{% hint style="info" %}
Biometric images and templates stay on **your** device or server. Identixia does not host them.
{% endhint %}

{% include "../.gitbook/includes/footer.md" %}
