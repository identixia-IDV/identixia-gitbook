---
description: >-
  Official Identixia documentation for on-premise Face Recognition, Liveness, and ID Document SDKs.
---

# Welcome to Identixia

### Introduction

Official documentation for **Identixia** on-premise biometric SDKs:

* **Face Recognition** — enroll, 1:N identify, templates, quality, 1:1 match; optional passive liveness
* **Liveness Detection** — passive face presentation-attack detection
* **ID Document Recognition** — OCR, MRZ, barcode; optional document liveness
* **ID Document Liveness** — document anti-spoofing API (separate from OCR)

Processing stays on your device or server. Biometric data is **not** sent to Identixia cloud.

### How to use these docs

1. Open the product that matches your license.
2. Open the **platform** page (Android, iOS, Flutter, React Native, Ionic, Windows, Linux/Docker).
3. Follow setup in the product README / this page to place the runtime and run the demo.
4. For server SDKs, copy the machine code, then [request a license](request-a-license-and-support.md).
5. Call activate → init (or HTTP activate), then the process APIs. Store templates and document JSON in **your** database.

Native binaries are **not** in git. Use GitHub Releases (`/releases/latest/download/…`) or the paths listed on each platform page.

{% hint style="info" %}
The demo is a full sample app. Production integrations copy the runtime and call the SDK/API — you do not need the demo screens.
{% endhint %}

### Products

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>Face Recognition SDK</strong></td><td>On-premise face recognition for phones and servers. Enroll, 1:N identify, templates, quality, and 1:1 match. Passive liveness when the license includes it.</td><td><a href=".gitbook/assets/Lucid_Origin_A_futuristic_face_recognition_interface_for_Facep_1.jpg">Lucid_Origin_A_futuristic_face_recognition_interface_for_Facep_1.jpg</a></td><td></td><td><a href="face-recognition-sdk/">face-recognition-sdk</a></td></tr><tr><td><strong>Liveness Detection SDK</strong></td><td>Passive face presentation-attack detection on device or on your server. Scores a camera frame or still image when the license allows it.</td><td><a href=".gitbook/assets/Lucid_Origin_Splitscreen_concept_showing_real_face_vs_spoof_at_0.jpg">Lucid_Origin_Splitscreen_concept_showing_real_face_vs_spoof_at_0.jpg</a></td><td></td><td><a href="liveness-detection-sdk/">liveness-detection-sdk</a></td></tr><tr><td><strong>ID Document Recognition SDK</strong></td><td>Passport, national ID, and driver license OCR, MRZ, and barcode extraction. Document liveness runs when the license includes it.</td><td><a href=".gitbook/assets/Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg">Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg</a></td><td></td><td><a href="id-document-recognition-sdk/">id-document-recognition-sdk</a></td></tr><tr><td><strong>ID Document Liveness SDK</strong></td><td>On-premise ID document liveness API for Linux and Docker. Separate from OCR. Document anti-spoofing when the license includes it.</td><td><a href=".gitbook/assets/Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg">Lucid_Origin_A_modern_UI_showing_an_ID_card_being_scanned_boun_0.jpg</a></td><td></td><td><a href="id-document-liveness-sdk/">id-document-liveness-sdk</a></td></tr>
</tbody></table>

### Links

* [Request a license & support](request-a-license-and-support.md)
* [Contact](contact-us.md)
* Website: [identixia.com](https://identixia.com)
* GitHub org: [identixia-IDV](https://github.com/identixia-IDV)
