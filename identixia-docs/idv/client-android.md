---
description: >-
  Build the IDV Android applicant demo.
---

# Android demo

```bash
cd IDV/client/packages/idv-android
./gradlew publishToMavenLocal
cd ../../app/android
./gradlew :app:assembleDebug
```
