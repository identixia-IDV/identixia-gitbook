---
description: >-
  Choose a recognition-only Identixia SDK for face recognition. Compare available repositories and integration options.
---

# Face Recognition SDKs without Liveness

## When to use

Use these repositories when the license is **recognition only**. They detect faces, build templates, and run 1:1 and 1:N search. They do not return a liveness score. Phone, Windows, and Linux / Docker samples are listed on [Face recognition](recognition.md).

| Platform | Port | Docs | Repository |
| --- | ---: | --- | --- |
| Windows | 14104 | [Windows](recognition-windows.md) | [`FaceRecognition-Windows`](https://github.com/identixia-IDV/FaceRecognition-Windows) |
| Linux / Docker | 14104 | [Linux / Docker](recognition-linux-docker.md) | [`FaceRecognition-Docker`](https://github.com/identixia-IDV/FaceRecognition-Docker) |

Call `POST /api/face/analyze`, `/api/face/template`, `/api/face/compare` (`image1`, `image2`), `/api/face/enroll`, and `/api/face/search`. Do not call `/api/face/liveness` on this build.

Concept guide: [Face recognition](recognition.md).
