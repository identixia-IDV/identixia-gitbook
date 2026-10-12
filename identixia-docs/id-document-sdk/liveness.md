---
description: >-
  Understand Identixia ID document liveness detection, presentation attack checks, license requirements, and how to interpret results.
---

# ID Document Liveness Detection and Anti-Spoofing

## Overview

Document **liveness**, also called document presentation attack detection (PAD), checks for signs that an ID image comes from a spoofed presentation, such as:

* A screen replay
* A printout or paper copy
* Portrait or document substitution (when the engine supports it)

Document liveness checks evaluate authenticity; optical character recognition (OCR) extracts text. Run liveness checks separately or alongside document recognition, depending on the SDK and license you choose.

## License rule

| License | What you get |
| --- | --- |
| `authenticity` present | `security` / related checks populate in result JSON |
| Missing | Security results are empty or omitted; an unavailable check does **not** mean the document passed |

See [Security check fields](security-fields.md).

## Where it ships

Authenticity only. The sample does not read MRZ, barcodes, or visual fields. Server port **14107**. `POST /api/document/liveness` takes `images` entries `{image, page_idx}`. This server does not expose `/api/document/process`.

| Platform | Port | Where to start | Repository |
| --- | ---: | --- | --- |
| Android | — | Repository README | [`ID-Document-Liveness-Detection-Android`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Android) |
| iOS | — | Repository README | [`ID-Document-Liveness-Detection-iOS`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-iOS) |
| Flutter | — | Repository README | [`ID-Document-Liveness-Detection-Flutter`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Flutter) |
| React Native | — | Repository README | [`ID-Document-Liveness-Detection-React-Native`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-React-Native) |
| Ionic Capacitor | — | Repository README | [`ID-Document-Liveness-Detection-Ionic-Capacitor`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Capacitor) |
| Ionic Cordova | — | Repository README | [`ID-Document-Liveness-Detection-Ionic-Cordova`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Ionic-Cordova) |
| Windows | 14107 | Repository README | [`ID-Document-Liveness-Detection-Windows`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Windows) |
| Linux / Docker | 14107 | [Linux / Docker](liveness-linux-docker.md) | [`ID-Document-Liveness-Detection-Docker`](https://github.com/identixia-IDV/ID-Document-Liveness-Detection-Docker) |

Recognition and authenticity in one sample use the repositories on [ID Document SDK](README.md). That server listens on port **14102**.

### Example — authenticity-only (full server)

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/liveness \
  -H "Content-Type: application/json" \
  -d '{"images":["BASE64_FRONT"]}'
```

![Liveness checks UI](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png)
