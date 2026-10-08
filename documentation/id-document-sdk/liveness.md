---
description: >-
  Document authenticity / anti-spoofing — separate from OCR, license-gated.
icon: shield-halved
---

# Document liveness

## Overview

Document **liveness** (authenticity) checks whether the ID is likely a physical document versus:

* A screen replay
* A printout or paper copy
* Portrait or document substitution (when the engine supports it)

It does **not** replace OCR. You can run authenticity alone or together with recognition.

## License rule

| License | What you get |
| --- | --- |
| `authenticity` present | `security` / related checks populate in result JSON |
| Missing | Empty or omitted security — **not** a pass |

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

<figure><img src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/screenshots/document-reader/desktop/demo-ui-checks-liveness.png" alt="Liveness checks UI" width="480"><figcaption>Desktop demo — liveness checks</figcaption></figure>

{% include "../.gitbook/includes/footer.md" %}
