---
description: >-
  Hybrid licence issuer and protocol used by the IDV platform.
---

# Licensing

IDV uses **Hybrid** licensing: day-to-day metering on the customer host, issuance by Identixia.

| Piece | Docs |
| --- | --- |
| Issuer UI / APIs | [License Admin](license-admin.md) |
| Shared protocol | [Hybrid protocol (`license_v2`)](license-protocol.md) |
| Production exposure | Keep issuer on localhost — [Production](production.md) |

## Operator exchange

| Action | Customer sends | You return |
| --- | --- | --- |
| First issue | `license_request.txt` | `license.txt` |
| Same host again | — | Used count kept (no restore) |

The issuer never sees ID images or biometrics. Brand files for consoles live under `license-admin/brand/`.
