---
description: >-
  license_v2 shared protocol used by idv-server and license-admin.
---

# Hybrid licence protocol

| Path | Role |
| --- | --- |
| `IDV/license_v2/` | Canonical protocol sources + tests |
| Vendored copies | Inside `idv-server/` and `license-admin/` for self-contained runs |
| `IDV/packages/license-core` | Helper package for consoles/libs |

Offline metering runs on the customer IDV host; usage receipts / status checks go to Identixia (USB or online sync). One commercial Hybrid product — operators do not pick STRICT/LENIENT tiers in the issuer UI.
