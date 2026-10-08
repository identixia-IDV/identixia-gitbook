---
description: >-
  Connect the ID Document SDK HTTP API to IDV for document recognition, OCR, and licensed document authenticity checks.
icon: id-card
---

# Document OCR Engine Integration with IDV

## Default configuration

| Setting | Value |
| --- | --- |
| Base URL | `http://127.0.0.1:14102` |
| Modes | `documentProcess` · `documentRecognition` · `documentLiveness` |

IDV selects recognition, authenticity, or full process based on workflow steps and licence flags. Parse engine responses as [Result JSON](https://docs.identixia.com/id-document-sdk/result-json).

## Related docs

* [ID Document SDK → Server](https://docs.identixia.com/id-document-sdk/full-server)
* Parent: [Engines](engines.md)

{% include "../.gitbook/includes/footer.md" %}
