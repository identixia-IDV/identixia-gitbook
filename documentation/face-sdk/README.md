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

## What you need

A license that includes `recognition`. Add `liveness` when you need a presentation-attack score. From the product repository, run `python scripts/get_runtime.py` so the native libraries and `*.xdb` databases are on disk. You keep the gallery database.

## Try it

* [Run the sample](https://docs.identixia.com/guides/run-the-sample)
* [Choose a product](https://docs.identixia.com/guides/choose-a-product)
* [SDK Server](../sdk-server/README.md) — Windows and Docker HTTP API

![Face SDK Android home](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/face-recognition/android/home.png)

## Next

* [Recognition](recognition.md) · [Liveness](liveness.md)

{% hint style="info" %}
Biometric images and templates stay on **your** device or server. Identixia does not host them.
{% endhint %}

{% include "../.gitbook/includes/footer.md" %}
