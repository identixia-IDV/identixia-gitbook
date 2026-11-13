---
description: >-
  Connect the ID Document SDK HTTP API to IDV for document recognition, OCR, and licensed document authenticity checks.
---

# Document OCR Engine Integration with IDV

## Default configuration

| Setting | Value |
| --- | --- |
| Base URL | `http://127.0.0.1:14102` |
| Modes | `documentProcess` · `documentRecognition` · `documentLiveness` |

IDV selects recognition, authenticity, or full process based on workflow steps and licence flags. Parse engine responses as [Result JSON](../id-document-sdk/result-json.md).

## Related docs

* [ID Document SDK → Server](../id-document-sdk/full-server.md)
* Parent: [Engines](engines.md)
