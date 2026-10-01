---
description: >-
  Identixia documentation for Face SDK, ID Document SDK, and the IDV platform.
---

# Welcome to Identixia

<p align="center"><img src=".gitbook/assets/brand-logo.png" alt="Identixia" width="280"></p>

## Introduction

Identixia documentation covers **three products**. All biometric processing runs on **your** device or server.

| Product | Source in monorepo | What you get |
| --- | --- | --- |
| [**Face SDK**](face-sdk/) | `repositories/Face*` | Face recognition and passive face liveness |
| [**ID Document SDK**](id-document-sdk/) | `repositories/ID-Document*` | Document OCR/MRZ and document authenticity |
| [**IDV**](idv/) | `IDV/` | Verification platform that orchestrates the two SDKs |

## How to use these docs

The sidebar is multi-level: product → function → product line → channel → platform.

1. Open the **product** (Face SDK, ID Document SDK, or IDV).
2. Open **Recognition** or **Liveness** (for IDV: Getting started, Engines, or Components).
3. Choose **full product**, **recognition-only**, or **liveness-only**, then **Mobile** or **Server**.
4. Open your **platform** page → Quick start → Ready → API reference.
5. For IDV, start the Document and Face engines, then the IDV server and a client demo.

{% hint style="info" %}
Native engine binaries ship on GitHub Releases (`/releases/latest/download/…`). They are not committed to git. Demo UIs are optional — call the SDK or HTTP API directly in production.
{% endhint %}

## Products

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>Face SDK</strong></td><td>Detect, templates, 1:1 / 1:N, and passive liveness when licensed. Mobile and server repositories under <code>repositories/</code>.</td><td><a href=".gitbook/assets/face-android-home.png">face-android-home.png</a></td><td></td><td><a href="face-sdk/">face-sdk</a></td></tr>
<tr><td><strong>ID Document SDK</strong></td><td>Passport and ID OCR, MRZ, barcode, and document authenticity when licensed.</td><td><a href=".gitbook/assets/document-desktop-status.png">document-desktop-status.png</a></td><td></td><td><a href="id-document-sdk/">id-document-sdk</a></td></tr>
<tr><td><strong>IDV platform</strong></td><td>Sessions, capture clients, Identity Console, company sample, and Hybrid licensing — uses Face and Document engines over HTTP.</td><td><a href=".gitbook/assets/brand-mark.png">brand-mark.png</a></td><td></td><td><a href="idv/">idv</a></td></tr>
</tbody></table>

## Shared conventions

| Topic | Summary |
| --- | --- |
| Control vs process (HTTP) | `/api/health`, `/api/machinecode`, `/api/activate`, `/api/licenseStatus` return `{success,code,message,request_id,data}`. Process routes return engine JSON. |
| Threading (mobile) | Activate, init, detect, and recognize on a **background** thread. |
| License flags | Face: `recognition` / `liveness`. Document: `recognition` / `authenticity`. A missing flag means the feature is not evaluated. |
| Brand | Logo and favicons live in docs `.gitbook/assets/`; IDV consoles use `IDV/license/admin/brand/`. |

## Links

* [Request a license & support](request-a-license-and-support.md)
* [Contact](contact-us.md)
* [identixia.com](https://identixia.com)
* GitHub: [identixia-IDV](https://github.com/identixia-IDV)
