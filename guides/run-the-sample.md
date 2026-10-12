---
description: >-
  Set up Identixia SDK sample apps for Android, iOS, Flutter, React Native, and Ionic, then download the runtime and activate your license.
icon: play
---

# Run the Identixia SDK Sample Apps

{% hint style="info" %}
Clone the repository for your chosen product and follow the tab for your development framework. Complete Android and iOS setup separately; iOS requires a Mac. Use `python3` on macOS.
{% endhint %}

```bash
python scripts/get_runtime.py
```

{% tabs %}
{% tab title="Android" %}
Requirements from the sample: Android Studio, JDK **17**, minSdk **24**, ABIs `arm64-v8a` and `armeabi-v7a`. Use a physical **arm64** phone for the camera.

```bash
python scripts/get_runtime.py
```

Open the Android project in Android Studio and run it. The sample prints the application id to send with a license request. Wait until status shows **Ready**.
{% endtab %}

{% tab title="iOS" %}
Requirements from the sample: a Mac, Xcode, and a physical iPhone. Deployment target is iOS **13+**. Open the `.xcworkspace`, select your team, and run. The sample prints the bundle id to send with a license request. Wait until status shows **Ready**.
{% endtab %}

{% tab title="Flutter" %}
From the repository root:

```bash
dart run tool/bootstrap.dart
flutter run -d android
```

iOS, from a Mac, on a physical device (Flutter 3.44 or newer):

```bash
cd example/ios && pod install && cd ..
flutter run -d ios
```
{% endtab %}

{% tab title="React Native" %}
{% hint style="warning" %}
These samples are Yarn workspaces. They do not run in Expo Go.
{% endhint %}

```bash
yarn
cd example && yarn android
```

iOS, from a Mac:

```bash
cd example/ios && pod install && cd ..
yarn ios --device
```
{% endtab %}

{% tab title="Ionic Capacitor" %}
Install and build the plugin before the example app. The example depends on the plugin in the parent folder.

```bash
npm install && npm run build
cd example && npm install && npm run sync
npm run android
```

`npm run android` and `npm run ios` open the native IDE. Press Run there. For iOS, run `npm run ios` on a Mac after `npm run sync`.
{% endtab %}

{% tab title="Ionic Cordova" %}
```bash
npm run setup:android
npm run android
```

iOS, from a Mac:

```bash
npm run setup:ios
npm run ios
```
{% endtab %}
{% tab title="Windows / Docker" %}
Same steps for a Windows service and a Docker build of the same product. They share one port.

1. Clone the Windows or Docker repository.
2. On a host install, run `python scripts/get_runtime.py`. A Docker Hub image already contains the runtime.
3. Copy `.env.example` to `.env`, install the Python dependencies, then start with `python run_server.py` (`python3` on macOS or Linux) or Docker Compose.
4. Read `GET /api/machinecode`, request a license, then `POST /api/activate`.
5. Call the process route for that product. Ports are on [SDK Server](https://docs.identixia.com/sdk-server).
{% endtab %}
{% endtabs %}

{% hint style="success" %}
Wait for the sample to show **Ready**, then select one of its supported features, such as image capture, face enrollment, or document recognition.
{% endhint %}

{% include "./.gitbook/includes/footer.md" %}
