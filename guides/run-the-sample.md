---
description: Android and iOS commands for the Identixia sample apps.
icon: play
---

# Run the sample

{% hint style="info" %}
Clone the product repository, then open the tab for your stack. Android and iOS are separate setups. On macOS use `python3`.
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
Wait until the sample shows **Ready**, then open the capture, enroll, or recognize action that the product includes.
{% endhint %}

{% include "./.gitbook/includes/footer.md" %}
