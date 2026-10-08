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
Open the Android project in Android Studio and run it on a device or emulator. The sample prints the application id to send with a license request.
{% endtab %}

{% tab title="iOS" %}
Open the `.xcworkspace` on a Mac, select your team, and run on a physical device. The sample prints the bundle id to send with a license request.
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
{% endtabs %}

{% hint style="success" %}
Wait for the sample to show **Ready**, then select one of its supported features, such as image capture, face enrollment, or document recognition.
{% endhint %}

{% include "./.gitbook/includes/footer.md" %}
