---
description: >-
  Connect the Face SDK HTTP API to IDV for face matching and licensed face liveness checks during identity verification.
---

# Face Recognition Engine Integration with IDV

## Default configuration

| Setting | Value |
| --- | --- |
| Base URL | `http://127.0.0.1:14103` |
| Modes | `/api/face/compare` · `/boxes` · `/template` · `/score` · `/liveness` |

IDV uses the Face SDK matcher for 1:1 and related steps. Optional vector indexes stay off until interoperability gates are set — ANN distance alone never decides trust.

## Related docs

* [Face SDK → Server](../face-sdk/full-server.md)
* Parent: [Engines](engines.md)
