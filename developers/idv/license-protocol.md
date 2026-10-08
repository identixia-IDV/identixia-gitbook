---
description: >-
  Understand the shared license_v2 protocol used by the Identixia IDV server and license issuer.
icon: key
---

# IDV Hybrid License Protocol

## Overview

IDV uses a **Hybrid** licence model: day-to-day entitlement metering runs on the customer host; Identixia issues and renews licence files.

| Path | Role |
| --- | --- |
| `IDV/license/license_v2/` | Canonical protocol sources and tests |
| Vendored copies | Inside `IDV_server/` and `license/` for self-contained runs |
| `IDV/packages/license-core` | Helper package for consoles and shared libraries |

## Operating model

| Step | Where it happens |
| --- | --- |
| Issue / renew `license.txt` | [License Admin](license-admin.md) (Identixia) |
| Enforce usage on the host | `license/license_v2` (issuer) / server copy in `IDV_server` |
| Sync usage receipts | USB export or `POST /api/v2/online/report` (when exposed) |

There is one commercial Hybrid product. Operators do not choose STRICT/LENIENT tiers in the issuer UI. The issuer never receives ID images or biometrics.

Parent: [Licensing](https://docs.identixia.com/guides/idv/licensing).

{% include "../.gitbook/includes/footer.md" %}
