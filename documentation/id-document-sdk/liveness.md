---
description: >-
  Understand Identixia ID document liveness detection, presentation attack checks, license requirements, and how to interpret results.
icon: shield-halved
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

| Product | Docs |
| --- | --- |
| Full Document SDK (mobile + server) | Platform pages on [ID Document SDK](README.md) |
| Liveness-only Linux / Docker | [Document liveness Docker](https://docs.identixia.com/developers/id-document-sdk/liveness-linux-docker) |

### Example — authenticity-only (full server)

```bash
curl -s -X POST http://127.0.0.1:14102/api/document/liveness \
  -H "Content-Type: application/json" \
  -d '{"images":["BASE64_FRONT"]}'
```

![Liveness checks UI](https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png)

{% include "../.gitbook/includes/footer.md" %}
