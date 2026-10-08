---
description: >-
  Integrate standalone Identixia face liveness detection on Android or iOS. Explore sample apps and license requirements.
---

# Face Liveness Detection SDKs for Android and iOS

## Platforms

These builds score presentation attacks and deepfake checks. They do not enroll a gallery or run 1:N search.

| Platform | Docs | Repository |
| --- | --- | --- |
| Android | [Android](liveness-android.md) | [`FaceLivenessDetection-Android`](https://github.com/identixia-IDV/FaceLivenessDetection-Android) |
| iOS | [iOS](liveness-ios.md) | [`FaceLivenessDetection-iOS`](https://github.com/identixia-IDV/FaceLivenessDetection-iOS) |
| Flutter | Repository README | [`FaceLivenessDetection-Flutter`](https://github.com/identixia-IDV/FaceLivenessDetection-Flutter) |
| React Native | Repository README | [`FaceLivenessDetection-React-Native`](https://github.com/identixia-IDV/FaceLivenessDetection-React-Native) |
| Ionic Capacitor | Repository README | [`FaceLivenessDetection-Ionic-Capacitor`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Capacitor) |
| Ionic Cordova | Repository README | [`FaceLivenessDetection-Ionic-Cordova`](https://github.com/identixia-IDV/FaceLivenessDetection-Ionic-Cordova) |

## Integration path

1. Clone the sample and place the liveness runtime from GitHub Releases (`python scripts/get_runtime.py`).
2. Run until status shows **Ready**, then open the camera flow.
3. Activate with a license that includes `liveness`.
4. Treat a missing score as not evaluated, not as a pass.

Parent: [Liveness-only products](liveness-only.md).
