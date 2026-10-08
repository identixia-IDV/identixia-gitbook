#!/usr/bin/env python3
"""Push regenerated GitBook docs to identixia-IDV/identixia-gitbook.

Remote (canonical)::

  git@github.com:identixia-IDV/identixia-gitbook.git

Flow
----
1. Regenerate ``gitbook-push/identixia-docs`` from catalog + product READMEs
   (skip with ``--no-generate``).
2. Require GitHub username + token (prompted if omitted).
3. Sync ``gitbook-push/`` into a clone of the remote and push ``main``.

Examples
--------
  python gitbook-push/gitbook_push.py
  python gitbook-push/gitbook_push.py --force
  python gitbook-push/gitbook_push.py --no-generate --message "Docs sync"
  python gitbook-push/gitbook_push.py --ssh   # push over SSH (still needs user for commit)
  python repositories/APPs/github_manage.py gitbook --ssh
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABOUT_PATH = ROOT / "repositories" / "APPs" / "github_about.json"
GITBOOK_SRC = ROOT / "gitbook-push"
GENERATE_PY = GITBOOK_SRC / "generate.py"

DEFAULT_REMOTE_SSH = "git@github.com:identixia-IDV/identixia-gitbook.git"
DEFAULT_REMOTE_HTTPS = "https://github.com/identixia-IDV/identixia-gitbook.git"


def die(msg: str, code: int = 1) -> None:
    print("ERROR:", msg, file=sys.stderr)
    raise SystemExit(code)


def run(
    cmd: list[str],
    *,
    check: bool = True,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    capture: bool = False,
) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(
        cmd,
        check=check,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=capture,
        text=True,
    )


def load_about() -> dict:
    if not ABOUT_PATH.is_file():
        return {}
    return json.loads(ABOUT_PATH.read_text(encoding="utf-8"))


def require_credentials(args: argparse.Namespace) -> tuple[str, str]:
    user = (args.user or "").strip()
    token = (args.token or "").strip()
    if not user:
        user = input("GitHub username: ").strip()
    if not token and not args.ssh:
        token = getpass.getpass("GitHub token: ").strip()
    if not user:
        die("GitHub username is required")
    if not args.ssh and not token:
        die("GitHub token is required (or pass --ssh to push with SSH keys)")
    return user, token


def remote_url(about: dict, *, ssh: bool, user: str, token: str) -> str:
    if ssh:
        return (about.get("gitbook_remote") or DEFAULT_REMOTE_SSH).strip()
    # HTTPS with token for non-interactive auth
    https = (about.get("gitbook_remote_https") or DEFAULT_REMOTE_HTTPS).strip()
    if https.startswith("https://"):
        rest = https[len("https://") :]
        return f"https://{user}:{token}@{rest}"
    return https


def regenerate() -> None:
    if not GENERATE_PY.is_file():
        die(f"missing generator: {GENERATE_PY}")
    run([sys.executable, str(GENERATE_PY)], cwd=ROOT)


def wipe_worktree(dest: Path) -> None:
    for child in dest.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def copy_gitbook_tree(src: Path, dest: Path) -> None:
    """Copy gitbook-push contents (docs + config), skip local generator helpers if desired."""
    ignore = shutil.ignore_patterns(
        "__pycache__",
        "*.pyc",
        ".git",
        ".DS_Store",
    )
    for child in src.iterdir():
        if child.name == ".git":
            continue
        target = dest / child.name
        if child.is_dir():
            shutil.copytree(child, target, ignore=ignore, dirs_exist_ok=True)
        else:
            shutil.copy2(child, target)


def git_env(user: str, token: str, *, ssh: bool) -> dict[str, str]:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["IDENTIXIA_GIT_USER"] = user
    env["IDENTIXIA_GIT_EMAIL"] = f"{user}@users.noreply.github.com"
    if not ssh and token:
        raw = f"{user}:{token}".encode("utf-8")
        env["IDENTIXIA_GIT_BASIC"] = base64.b64encode(raw).decode("ascii")
        env["GH_TOKEN"] = token
        env["GITHUB_TOKEN"] = token
    return env


def git_cmd(env: dict[str, str], *args: str, cwd: Path | None = None, check: bool = True):
    user = env["IDENTIXIA_GIT_USER"]
    email = env["IDENTIXIA_GIT_EMAIL"]
    cmd = [
        "git",
        "-c",
        "credential.helper=",
        "-c",
        f"user.name={user}",
        "-c",
        f"user.email={email}",
    ]
    basic = env.get("IDENTIXIA_GIT_BASIC")
    if basic:
        cmd.extend(["-c", f"http.extraheader=Authorization: Basic {basic}"])
    cmd.extend(args)
    return run(cmd, cwd=cwd, env=env, check=check)


def push_gitbook(
    *,
    url: str,
    user: str,
    token: str,
    ssh: bool,
    message: str,
    force: bool,
    dry_run: bool,
) -> None:
    if not GITBOOK_SRC.is_dir():
        die(f"missing source tree: {GITBOOK_SRC}")
    if not (GITBOOK_SRC / "identixia-docs" / "SUMMARY.md").is_file():
        die("identixia-docs/SUMMARY.md missing — run generate first (or drop --no-generate)")

    if dry_run:
        print(f"DRY push {GITBOOK_SRC} -> {DEFAULT_REMOTE_SSH if ssh else DEFAULT_REMOTE_HTTPS}")
        return

    env = git_env(user, token, ssh=ssh)
    # Clone without embedding token in process list when using header auth:
    clone_url = DEFAULT_REMOTE_HTTPS if not ssh else url
    if ssh:
        clone_url = url

    with tempfile.TemporaryDirectory(prefix="ix-gitbook-push-") as tmp:
        dest = Path(tmp) / "identixia-gitbook"
        r = git_cmd(
            env,
            "clone",
            "--branch",
            "main",
            "--single-branch",
            clone_url,
            str(dest),
            check=False,
        )
        if r.returncode != 0:
            r2 = git_cmd(env, "clone", clone_url, str(dest), check=False)
            if r2.returncode != 0:
                die(
                    "clone failed — check SSH keys / token access to "
                    "identixia-IDV/identixia-gitbook"
                )
            git_cmd(env, "checkout", "-B", "main", cwd=dest, check=False)

        wipe_worktree(dest)
        copy_gitbook_tree(GITBOOK_SRC, dest)
        git_cmd(env, "add", "-A", cwd=dest)
        diff = run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=dest,
            check=False,
            env=env,
        )
        if diff.returncode == 0:
            print("SKIP: no changes to push")
            return
        git_cmd(env, "commit", "-m", message, cwd=dest)
        push_args = ["push", "origin", "HEAD:main"]
        if force:
            push_args.insert(1, "--force")
        git_cmd(env, *push_args, cwd=dest)
        print(f"OK: pushed to {DEFAULT_REMOTE_SSH}")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Regenerate and push GitBook docs to identixia-IDV/identixia-gitbook.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument(
        "--user",
        default="",
        help="GitHub username (prompted if omitted)",
    )
    ap.add_argument(
        "--token",
        default="",
        help="GitHub token for HTTPS push (prompted if omitted; not required with --ssh)",
    )
    ap.add_argument(
        "--ssh",
        action="store_true",
        help=f"Push via SSH ({DEFAULT_REMOTE_SSH}) using local SSH keys",
    )
    ap.add_argument(
        "--no-generate",
        action="store_true",
        help="Do not run gitbook-push/generate.py before push",
    )
    ap.add_argument(
        "--message",
        default="Sync Identixia GitBook docs from catalog workspace.",
        help="Commit message",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Force-push main",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without cloning or pushing",
    )
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    about = load_about()

    if not args.no_generate:
        print("== regenerate gitbook-push/identixia-docs", flush=True)
        if args.dry_run:
            print("DRY: python gitbook-push/generate.py")
        else:
            regenerate()

    user, token = require_credentials(args)
    url = remote_url(about, ssh=bool(args.ssh), user=user, token=token)
    print(
        f"== push gitbook -> {DEFAULT_REMOTE_SSH if args.ssh else DEFAULT_REMOTE_HTTPS}",
        flush=True,
    )
    push_gitbook(
        url=url,
        user=user,
        token=token,
        ssh=bool(args.ssh),
        message=args.message,
        force=bool(args.force),
        dry_run=bool(args.dry_run),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
