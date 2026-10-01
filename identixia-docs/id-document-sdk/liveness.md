---
description: >-
  Document authenticity / anti-spoofing — separate from OCR, license-gated.
---

# Document liveness

## In plain words

Document **liveness** (authenticity) checks whether the ID is likely a real document versus:

* A screen replay
* A printout / paper copy
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
| Liveness-only Linux / Docker | [Document liveness Docker](liveness-linux-docker.md) |

### Example — authenticity-only (full server)

```bash
curl -s -X POST http://127.0.0.1:14102/api/documentLiveness \
  -H "Content-Type: application/json" \
  -d '{"images":["BASE64_FRONT"]}'
```

<figure><img src="../.gitbook/assets/document-desktop-checks-liveness.png" alt="Liveness checks UI" width="480"><figcaption>Desktop demo — liveness checks</figcaption></figure>
