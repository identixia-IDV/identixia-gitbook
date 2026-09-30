---
description: >-
  Detailed Identixia docs for Face Recognition, Liveness, and ID Document SDKs — setup, activation, and full API reference.
---

# Welcome to Identixia

## Introduction

Official **Identixia** documentation for on-premise biometric SDKs. Use these pages to integrate every customer-facing function: activation, capture, recognition, matching, liveness, and result handling.

* **Face Recognition** — detect, attributes, quality, templates, 1:1, 1:N; optional passive liveness
* **Liveness Detection** — passive face presentation-attack detection
* **ID Document Recognition** — OCR, MRZ, barcode; optional document liveness
* **ID Document Liveness** — document anti-spoofing API (separate from OCR)

Biometric data stays on **your** device or server.

## How to use these docs

1. Open your **product** section.
2. Open your **platform** page.
3. Follow **Quick start** → run the demo → confirm Ready.
4. Read **License and activation**, then **API reference** for every function you will call.
5. Use **Troubleshooting** when something fails.
6. Server integrators: copy machine code → [request a license](request-a-license-and-support.md) → `POST /api/activate`.

{% hint style="info" %}
Native engine binaries are distributed via GitHub Releases (`/releases/latest/download/…`) or the paths in each README. They are not committed to git. The demo UI is optional in production — call the SDK/API directly.
{% endhint %}

## Products

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>Face Recognition SDK</strong></td><td>On-premise face recognition for phones and servers. Enroll, 1:N identify, templates, quality, and 1:1 match. Passive liveness when the license includes it.</td><td><a href=".gitbook/assets/Lucid_Origin_A_futuristic_face_recognition_interface_for_Facep_1.jpg">Lucid_Origin_A_futuristic_face_recognition_interface_for_Facep_1.jpg</a></td><td></td><td><a href="face-recognition-sdk/">face-recognition-sdk</a></td></tr><tr><td><strong>Liveness Detection SDK</strong></td><td>Passive face presentation-attack detection on device or on your server. Scores a camera frame or still image when the license allows it.</td><td><a href=".gitbook/assets/Lucid_Origin_Splitscreen_concept_showing_real_face_vs_spoof_at_0.jpg">Lucid_Origin_Splitscreen_concept_showing_real_face_vs_spoof_at_0.jpg</a></td><td></td><td><a href="liveness-detection-sdk/">liveness-detection-sdk</a></td></tr><tr><td><strong>ID Document Recognition SDK</strong></td><td>Passport, national ID, and driver license OCR, MRZ, and barcode extraction. Document liveness runs when the license includes it.</td><td><a href=".gitbook/assets/Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg">Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg</a></td><td></td><td><a href="id-document-recognition-sdk/">id-document-recognition-sdk</a></td></tr><tr><td><strong>ID Document Liveness SDK</strong></td><td>On-premise ID document liveness API for Linux and Docker. Separate from OCR. Document anti-spoofing when the license includes it.</td><td><a href=".gitbook/assets/Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg">Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg</a></td><td></td><td><a href="id-document-liveness-sdk/">id-document-liveness-sdk</a></td></tr>
</tbody></table>

## Shared concepts

| Topic | Summary |
| --- | --- |
| Control vs process (HTTP) | `/api/health`, `/api/machinecode`, `/api/activate`, `/api/licenseStatus` use `{success,code,message,request_id,data}`. Process routes return engine JSON. |
| Threading (mobile) | Activate, init, detect, recognize on a **background** thread. |
| License flags | Face: `recognition` / `liveness`. Document: `recognition` / `authenticity`. Missing flag ⇒ feature not run. |
| Your storage | Persist templates and document fields in **your** database. |

## Links

* [Request a license & support](request-a-license-and-support.md)
* [Contact](contact-us.md)
* [identixia.com](https://identixia.com)
* GitHub: [identixia-IDV](https://github.com/identixia-IDV)
