# GitBook push (docs.identixia.com)

Source tree for the Identixia documentation site. Content is organized into **three products**:

| Pillar | Monorepo source | GitBook folder |
|--------|-----------------|----------------|
| **Face SDK** | `repositories/Face*` | `identixia-docs/face-sdk/` |
| **ID Document SDK** | `repositories/ID-Document*` | `identixia-docs/id-document-sdk/` |
| **IDV** | `IDV/` | `identixia-docs/idv/` |

Each SDK section explains **recognition** and **liveness**, then platform implementations. IDV explains the platform that calls Face and Document HTTP engines. The offline handbook under `IDV/docs/` is not duplicated page-for-page here.

The GitBook sidebar is **4–5 levels deep**: product → function → product line → channel → platform (see `identixia-docs/SUMMARY.md`). Catalog homepage URLs for platform leaves stay stable across regenerations.

## Regenerate

```bash
python gitbook-push/generate.py
```

Rewrites `identixia-docs/` markdown, syncs brand assets and screenshots into `.gitbook/assets/` (one file per asset), and removes obsolete section folders. Slugs match `catalog/github_about.json` homepages.

## Push to GitBook repo

Remote: `git@github.com:identixia-IDV/identixia-gitbook.git`

```bash
python catalog/gitbook_push.py
python catalog/gitbook_push.py --ssh
python catalog/gitbook_push.py --force
python catalog/gitbook_push.py --no-generate
```

## Layout

| Path | Role |
|------|------|
| `gitbook-docs.yaml` | GitBook space config |
| `generate.py` | Rebuild from catalog, READMEs, and IDV summaries |
| `content_lib.py` | Platform page builders (API, quick start, screenshots) |
| `identixia-docs/` | Markdown published to GitBook |
| `identixia-docs/SUMMARY.md` | Table of contents |
| `identixia-docs/.gitbook/assets/` | Logo, favicons, screenshots (copied once; not duplicated elsewhere) |

## Brand

| Asset | Source | Docs name |
|-------|--------|-----------|
| Logo | `repositories/identixia-assets/brand/logo.png` | `brand-logo.png` |
| Mark | `repositories/identixia-assets/brand/mark.png` | `brand-mark.png` |
| Favicons | `IDV/license-admin/brand/` | `favicon.ico`, `favicon.png`, `apple-touch-icon.png` |

IDV consoles serve the same brand pack from `license-admin/brand/` as `/brand/*`. Do not copy logos into every product repository.

## Notes

* Platform pages are customer guides: overview, capabilities, prerequisites, quick start, license, API, troubleshooting, curated screenshots, next steps, and a repository README appendix.
* Screenshots come only from `repositories/identixia-assets` (flattened once into `.gitbook/assets/`).
* Engine binaries stay on GitHub Releases — not in git.
* After catalog or product README changes, run `generate.py` (or `catalog/gitbook_push.py`).
