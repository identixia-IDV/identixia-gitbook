---
description: >-
  Integrate the self-hosted Identixia face recognition and document OCR HTTP API on Windows or Docker. Follow setup, activation, and request examples.
icon: server
---

# Face Recognition and Document OCR HTTP API

SDK Server is the on-premise HTTP API. A Windows build and a Docker build of the **same product** share one port and the same `/api` routes. Phone SDKs are not this API.

Use this page to pick the port. Request bodies and platform setup are in [Developers](https://docs.identixia.com/developers).

## Products and ports

| Product | Default port | Gradio demo | Docs |
| --- | --- | --- | --- |
| Document recognition + liveness | **14102** | **14202** | [Document Recognition](https://docs.identixia.com/developers/sdk-server/document-recognition) |
| Face recognition + liveness | **14103** | **14203** | [Face Recognition](https://docs.identixia.com/developers/sdk-server/face-recognition) |
| Face recognition only | **14104** | **14204** | [Face Recognition](https://docs.identixia.com/developers/sdk-server/face-recognition) |
| Face liveness only | **14105** | **14205** | [Face Liveness](https://docs.identixia.com/developers/sdk-server/face-liveness) |
| Document recognition only | **14106** | **14206** | [Document Recognition](https://docs.identixia.com/developers/sdk-server/document-recognition) |
| Document liveness only | **14107** | **14207** | [Document Liveness](https://docs.identixia.com/developers/sdk-server/document-liveness) |

## Start any server (same pattern)

1. Clone the product repository (Windows or Docker).
2. Download the `runtime` GitHub Release and extract it into `lib/cpu/`.

3. Copy `.env.example` → `.env`, install Python deps, start (`python run_server.py` / `python3 run_server.py` or Docker Compose).
4. Read the machine code, request a license, activate.
5. Call process routes with base64 images (JSON or multipart).

```bash
curl -s http://127.0.0.1:14103/api/machinecode
curl -s -X POST http://127.0.0.1:14103/api/activate \
  -H "Content-Type: application/json" \
  -d '{"license":"YOUR_KEY"}'
curl -s http://127.0.0.1:14103/api/health
curl -s http://127.0.0.1:14103/api/licenseStatus
```

## Response shapes

| Route type | Shape |
| --- | --- |
| Control (`/api/health`, `/api/activate`, `/api/machinecode`, `/api/licenseStatus`, `/api/backend`) | `{success, code, message, request_id, data}` |
| Process (`/api/face/*`, `/api/document/*`) | Engine / process JSON (not the control envelope) |

## Runtime placement

| Platform | Where to unzip the Release |
| --- | --- |
| Windows / Linux host | `lib/cpu/` — binaries **and** every required `*.xdb` |
| Docker Hub image | Runtime is already inside the image |

Never ship binaries without database packs. Face recognition needs the full `recognition*.xdb` set; document products need `document.xdb`.

## Postman

Import once (every path, no duplicates):

* Monorepo: `postman/Identixia-API.postman_collection.json`
* Environment: `postman/Identixia-Local.postman_environment.json`
* Set `baseUrl` to the product under test (`http://127.0.0.1:14102` … `14107`)

## Platform deep-dives

* Face: [Windows](https://docs.identixia.com/developers/face-sdk/windows) · [Linux / Docker](https://docs.identixia.com/developers/face-sdk/linux-docker)
* Document: [Windows](https://docs.identixia.com/developers/id-document-sdk/windows) · [Linux / Docker](https://docs.identixia.com/developers/id-document-sdk/linux-docker)

## Next

* [Face Recognition](https://docs.identixia.com/developers/sdk-server/face-recognition)
* [Face Liveness](https://docs.identixia.com/developers/sdk-server/face-liveness)
* [Document Recognition](https://docs.identixia.com/developers/sdk-server/document-recognition)
* [Document Liveness](https://docs.identixia.com/developers/sdk-server/document-liveness)

{% include "../.gitbook/includes/footer.md" %}
