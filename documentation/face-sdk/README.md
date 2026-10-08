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

Choose a repository that matches your license. A recognition-only build does not return liveness scores.

![Face SDK Android home](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/home.png)

## Next

* [Reference](https://docs.identixia.com/developers/face-sdk/reference) — platform quick starts and sample repositories
* [SDK Server](../sdk-server/) — HTTP API (Windows & Docker)
* Function notes: [Recognition](recognition.md) · [Liveness](liveness.md)

{% hint style="info" %}
Biometric images and templates stay on **your** device or server. Identixia does not host them.
{% endhint %}

{% include "../.gitbook/includes/footer.md" %}
