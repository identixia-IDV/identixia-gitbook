---
description: >-
  On-premises Face Recognition and Face Liveness Detection SDKs.
---

# Introduction

On-premises Face Recognition and Face Liveness Detection (anti-spoofing) SDKs.

The algorithm runs in real time on phones and servers. It supports accurate **1:1** and **1:N** matching, **passive face liveness**, and face attributes (age, gender, mask/sunglasses, landmarks).

Use it for identity verification and attendance. Processing stays on **your** device or server.

We provide SDKs for **Android**, **iOS**, **Flutter**, **React Native**, **Ionic**, **Windows**, and **Linux / Docker**.

| Function | What you get | License flag |
| --- | --- | --- |
| **Recognition** | Detect, attributes, quality, templates, 1:1, 1:N | `recognition` |
| **Liveness** | Passive presentation-attack score | `liveness` |

Choose a repository that matches your license. A recognition-only build does not return liveness scores.

<figure><img src="../.gitbook/assets/face-android-home.png" alt="Face SDK Android home" width="160"><figcaption>Android demo home</figcaption></figure>

## Next

* [Reference](reference.md) — platform quick starts and sample repositories
* [SDK Server](../sdk-server/) — HTTP API (Windows & Docker)
* Function notes: [Recognition](recognition.md) · [Liveness](liveness.md)

{% hint style="info" %}
Biometric images and templates stay on **your** device or server. Identixia does not host them.
{% endhint %}
