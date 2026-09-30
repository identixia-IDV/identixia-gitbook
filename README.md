# GitBook push (docs.identixia.com)

Source tree for the Identixia docs site. Pages are generated from
`catalog/github_about.json` homepage URLs and each product’s current
`repositories/<name>/README.md`.

## Regenerate

```bash
python gitbook-push/generate.py
```

This rewrites `identixia-docs/` (keeps `.gitbook/assets/`). Slugs match the
`homepage` fields in the catalog so GitHub About links stay stable.

## Push to GitBook repo

Remote: `git@github.com:identixia-IDV/identixia-gitbook.git`

```bash
# Regenerate + push (prompts for GitHub username + token; HTTPS)
python catalog/gitbook_push.py

# Push over SSH keys
python catalog/gitbook_push.py --ssh

# Force-push / skip regenerate
python catalog/gitbook_push.py --force
python catalog/gitbook_push.py --no-generate
```

## Layout

| Path | Role |
|------|------|
| `gitbook-docs.yaml` | GitBook space config |
| `generate.py` | Rebuild from catalog + product READMEs |
| `identixia-docs/` | Markdown published to GitBook |
| `identixia-docs/SUMMARY.md` | Table of contents |

## Notes

* Pages are **detailed customer guides**: overview, prerequisites, quick start, license,
  full API reference, troubleshooting, curated screenshots, plus the product README appendix.
* Screenshots live in `identixia-docs/.gitbook/assets/` (copied from `repositories/identixia-assets`).
  Re-copy from that pack if product UI screenshots change, then regenerate.
* Product docs live here — not under a separate `docs/` tree.
* Engine binaries stay on GitHub Releases (`/releases/latest/download/…`), not in git.
* Contact / license pages are generated with the same command.
* After changing catalog or product READMEs, run `generate.py` (or `catalog/gitbook_push.py`).
