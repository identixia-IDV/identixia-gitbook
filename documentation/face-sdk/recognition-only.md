---
description: >-
  Choose a recognition-only Identixia SDK for face recognition. Compare available repositories and integration options.
icon: crosshairs
---

# Face Recognition SDKs without Liveness

## When to use

Use these repositories when the license is **recognition only**. They detect faces, build templates, and run 1:1 and 1:N search. They do not return a liveness score, and there is no recognition-only phone SDK. Phone apps that need recognition ship in the [full product](full-product.md).

| Platform | Port | Docs | Repository |
| --- | ---: | --- | --- |
| Windows | 14104 | [Windows](https://docs.identixia.com/developers/face-sdk/recognition-windows) | [`FaceRecognition-Windows`](https://github.com/identixia-IDV/FaceRecognition-Windows) |
| Linux / Docker | 14104 | [Linux / Docker](https://docs.identixia.com/developers/face-sdk/recognition-linux-docker) | [`FaceRecognition-Docker`](https://github.com/identixia-IDV/FaceRecognition-Docker) |

Call `POST /api/face/analyze`, `/api/face/template`, `/api/face/compare` (`image1`, `image2`), `/api/face/enroll`, and `/api/face/search`. Do not call `/api/face/liveness` on this build.

Concept guide: [Face recognition](recognition.md).

{% include "../.gitbook/includes/footer.md" %}
