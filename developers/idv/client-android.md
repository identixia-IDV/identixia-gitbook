---
description: >-
  Build and run the Android IDV sample app for applicant document and selfie capture in an identity verification session.
icon: mobile
---

# Android Identity Verification Sample App

## Build

```bash
cd IDV/demo_clients/packages/idv-android
./gradlew publishToMavenLocal
cd ../../app/android
./gradlew :app:assembleDebug
```

Use a capture token from the company backend. Package sources: `IDV/demo_clients/packages/idv-android`.

Parent: [Applicant clients](components-clients.md).

{% include "../.gitbook/includes/footer.md" %}
