---
description: >-
  License-gated document authenticity / liveness fields in the document result JSON.
---

# Document security check fields

When the license includes document liveness / authenticity, the result JSON may populate `security` (and related `verification.security`) with engine checks against screen replays, printouts, and substitution.

Treat missing or empty security blocks as **not licensed / not run**, not as a pass.

Mobile and server SDKs share the same field names where possible. Prefer the structured `security` object over scraping demo UI labels.

See [Document result JSON](document-result-json.md) for the parent object.
