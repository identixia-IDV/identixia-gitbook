---
description: >-
  Set up the Identixia face recognition SDK, download native libraries and models, activate a license, and call the APIs.
---

# Face Recognition SDK Integration Guide

This is the **full Face SDK integration path**. Open the platform page for your stack after you finish these steps.

## 1. Choose a product

| Goal | Product line | Example repos |
| --- | --- | --- |
| Recognition and liveness | Face Recognition & Liveness Detection | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14103**. |
| Recognition | Face Recognition | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14104**. These builds do not return a liveness score. |
| Liveness | Face Liveness Detection | Android, iOS, Flutter, React Native, Ionic Capacitor, Ionic Cordova, Windows, Linux / Docker. Server port **14105**. These builds do not enroll a gallery or run 1:N search. |

## 2. Clone and download the runtime

```bash
git clone https://github.com/identixia-IDV/<PRODUCT>.git
cd <PRODUCT>
```

Download the `runtime` GitHub Release for that repository (or the paired Android / iOS `runtime` Release for Flutter, React Native, and Ionic) and extract it into the folder in the table. The engine and database packs are not in git.

| Channel | Where files land |
| --- | --- |
| Android (Face) | `libfacerecognitionsdk/`, `libfacelivenesssdk/`, or `libfacefullsdk/` (AAR + `databases/*.xdb`) |
| Android (Document) | `libdocumentrecognitionsdk/`, `libdocumentlivenesssdk/`, or `libdocumentfullsdk/` (the `.aar`) |
| iOS | Unzip at the repository root so frameworks and database packs land in the sample folders |
| Flutter / RN / Ionic | Sample Android + iOS paths (see that platform page) |
| Windows / Linux | `lib/cpu/` (binaries **and** every required `*.xdb`) |

{% hint style="warning" %}
Never ship the engine without database packs. Missing `*.xdb` files cause empty OCR / liveness / match results even when activate returns success.
{% endhint %}

## 3. Run the sample

* **Mobile:** Android Studio / Xcode / `flutter run` / `yarn android` / Ionic — wait for **Ready**.
* **Server:** `pip install -r requirements.txt` → `python run_server.py` / `python3 run_server.py` → `GET /api/health`.

## 4. Activate

* **Mobile:** demo key is bound to the sample application / bundle id. Your app needs a new key.
* **Server:** `GET /api/machinecode` → contact Identixia → `POST /api/activate` or set `LICENSE=` in `.env`.

## 5. Call the APIs

| Surface | Where to look |
| --- | --- |
| Mobile methods | Platform pages under [Reference](reference.md) (lifecycle, detect, match, liveness, gallery, VideoWorker) |
| HTTP endpoints | [SDK Server — Face Recognition](../sdk-server/face-recognition.md) and [Face Liveness](../sdk-server/face-liveness.md) |

## 6. Resources

* Releases: each product’s GitHub **Releases** page
* Postman: monorepo `postman/Identixia-API.postman_collection.json`
* Docs site: [docs.identixia.com](https://docs.identixia.com)
* License: [Request a license](../request-a-license-and-support.md)

Next: open your platform page (for example [Android](android.md) or [Windows](windows.md)).
