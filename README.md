# GitBook push (docs.identixia.com)

Source tree for the Identixia documentation site. Content is organized into **three products**:

| Pillar | Monorepo source | GitBook folder |
|--------|-----------------|----------------|
| **Face SDK** | `repositories/Face*` | `identixia-docs/face-sdk/` |
| **ID Document SDK** | `repositories/ID-Document*` | `identixia-docs/id-document-sdk/` |
| **IDV** | `IDV/` | `identixia-docs/idv/` |

Each SDK section explains **recognition** and **liveness**, then platform implementations. IDV explains the platform that calls Face and Document HTTP engines. The offline handbook under `IDV/docs/` is not duplicated page-for-page here.

The published site is three GitBook sections. `identixia-docs/` is the generator output. `publish()` in `sections.py` copies pages into `documentation/`, `developers/`, and `guides/`, each with its own `SUMMARY.md` and page icons. Documentation stays on the site root. Developer and guide pages use `/developers/` and `/guides/`.

## Regenerate

```bash
python gitbook-push/generate.py
```

Rewrites `identixia-docs/` markdown and removes obsolete section folders. Images point at `identixia-IDV/identixia-assets` on GitHub. Slugs match `repositories/APPs/github_about.json` homepages.

## Push to GitBook repo

Remote: `git@github.com:identixia-IDV/identixia-gitbook.git`

```bash
python gitbook-push/gitbook_push.py
python gitbook-push/gitbook_push.py --ssh
python gitbook-push/gitbook_push.py --force
python gitbook-push/gitbook_push.py --no-generate
```

## Layout

| Path | Role |
|------|------|
| `gitbook-docs.yaml` | Site sections: Documentation, Developers, Guides |
| `sections.py` | Split pages, icons, and cross-section links |
| `documentation/` | Product concepts (space key `space-1`) |
| `developers/` | Platform, HTTP, and IDV integration |
| `guides/` | Setup, samples, licensing |
| `generate.py` | Rebuild from catalog, READMEs, and IDV summaries |
| `content_lib.py` | Platform page builders (API, quick start, screenshots) |
| `identixia-docs/` | Generator markdown (split into the three section folders on publish) |
| `identixia-docs/SUMMARY.md` | Generator table of contents |

## Images

Pages use `https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/...`. When a file is not in that repository, the image tag stays and the alt text is what readers see. Do not commit screenshot binaries under `gitbook-push/`.

## Notes

* Platform pages are customer guides: overview, capabilities, prerequisites, quick start, license, API, troubleshooting, screenshots, next steps, and a repository README appendix.
* Engine binaries stay on GitHub Releases — not in git.
* After catalog or product README changes, run `generate.py` (or `gitbook-push/gitbook_push.py`).
