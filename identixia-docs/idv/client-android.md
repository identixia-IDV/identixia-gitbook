---
description: >-
  Build the IDV Android applicant demo.
---

# Android demo

## Build

```bash
cd IDV/client/packages/idv-android
./gradlew publishToMavenLocal
cd ../../app/android
./gradlew :app:assembleDebug
```

Use a capture token from the company backend. Package sources: `IDV/client/packages/idv-android`.

Parent: [Applicant clients](components-clients.md).
