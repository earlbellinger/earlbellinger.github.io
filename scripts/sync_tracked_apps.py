#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
APPS_ROOT = REPO_ROOT / "apps"
APPS_MANIFEST = REPO_ROOT / "_data" / "apps.json"
SYNC_STATE = REPO_ROOT / "_data" / "app-sync-state.json"
DEFAULT_EXCLUDES = {".git", "node_modules", ".sass-cache", ".DS_Store"}
BINARY_SUFFIXES = {
    ".br",
    ".doc",
    ".docx",
    ".eot",
    ".gif",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".npy",
    ".pdf",
    ".png",
    ".ttf",
    ".webp",
    ".woff",
    ".woff2",
    ".zip",
}

OZWIZARD_LOADER_PATTERN = re.compile(
    r"<script>\s*"
    r"\(function \(\) \{\s*"
    r"var script = document\.createElement\(\"script\"\);"
    r".*?"
    r"document\.head\.appendChild\(script\);\s*"
    r"\}\);\s*"
    r"\}\(\)\);\s*"
    r"</script>",
    re.DOTALL,
)

OZWIZARD_STATIC_LOADER = """<script>
    (function () {
      var script = document.createElement("script");
      script.src = "./assets/wizard_of_oz-file.js";
      window.addEventListener("DOMContentLoaded", function () {
        document.head.appendChild(script);
      });
    }());
  </script>"""


class SyncError(RuntimeError):
    pass


def log(message: str) -> None:
    print(message, flush=True)


def run(command: list[str], cwd: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    resolved = resolve_command(command)
    log(f"+ {' '.join(command)}  (cwd={cwd})")
    try:
        return subprocess.run(resolved, cwd=str(cwd), check=check, text=True)
    except FileNotFoundError as error:
        raise SyncError(f"Command not found: {command[0]}") from error


def capture(command: list[str], cwd: Path, *, check: bool = True) -> str:
    resolved = resolve_command(command)
    result = subprocess.run(
        resolved,
        cwd=str(cwd),
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def resolve_command(command: list[str]) -> list[str]:
    if not command:
        raise SyncError("Empty command")
    executable = shutil.which(command[0])
    if executable:
        return [executable, *command[1:]]
    return command


def load_manifest() -> list[dict]:
    with APPS_MANIFEST.open("r", encoding="utf-8") as handle:
        apps = json.load(handle)
    if not isinstance(apps, list):
        raise SyncError(f"{APPS_MANIFEST} must contain a JSON array")
    slugs = [app.get("slug") for app in apps]
    if len(slugs) != len(set(slugs)):
        raise SyncError("App manifest contains duplicate slugs")
    for app in apps:
        validate_app(app)
    return apps


def validate_app(app: dict) -> None:
    required = ["slug", "name", "description", "href", "repo", "branch", "sync"]
    missing = [key for key in required if key not in app]
    if missing:
        raise SyncError(f"App manifest entry is missing required keys: {missing}")
    slug = app["slug"]
    if not re.fullmatch(r"[A-Za-z0-9_-]+", slug):
        raise SyncError(f"Unsafe app slug: {slug}")
    sync = app["sync"]
    if "artifact_path" not in sync and "paths" not in sync:
        raise SyncError(f"{slug} needs sync.artifact_path or sync.paths")
    if "commands" in sync:
        for command in sync["commands"]:
            if not isinstance(command, list) or not all(isinstance(part, str) for part in command):
                raise SyncError(f"{slug} command must be a list of strings: {command}")


def select_apps(apps: list[dict], requested: str) -> list[dict]:
    if requested == "all":
        return sorted(apps, key=lambda app: app.get("order", 0))
    matches = [app for app in apps if app["slug"] == requested]
    if not matches:
        available = ", ".join(sorted(app["slug"] for app in apps))
        raise SyncError(f"Unknown app '{requested}'. Available apps: {available}")
    return matches


def validate_dispatch(apps: list[dict], args: argparse.Namespace) -> None:
    if args.app == "all":
        if args.source_repo or args.source_branch or args.source_sha:
            raise SyncError("source repo/branch/sha dispatch metadata can only be used with one app")
        return

    app = apps[0]
    if args.source_repo and args.source_repo.lower() != app["repo"].lower():
        raise SyncError(f"Dispatch repo {args.source_repo} does not match manifest repo {app['repo']}")
    if args.source_branch and args.source_branch != app["branch"]:
        raise SyncError(f"Dispatch branch {args.source_branch} does not match manifest branch {app['branch']}")


def safe_manifest_path(value: str) -> Path:
    if not value or value.startswith(("/", "\\")):
        raise SyncError(f"Unsafe manifest path: {value!r}")
    path = Path(value)
    if any(part in ("", ".", "..") for part in path.parts):
        raise SyncError(f"Unsafe manifest path: {value!r}")
    return path


def ensure_inside(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    resolved.relative_to(root.resolve())
    return resolved


def clone_app(app: dict, workspace: Path, expected_sha: str | None) -> tuple[Path, str]:
    clone_dir = workspace / "source" / app["slug"]
    clone_dir.parent.mkdir(parents=True, exist_ok=True)
    clone_url = f"https://github.com/{app['repo']}.git"
    run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--single-branch",
            "--branch",
            app["branch"],
            clone_url,
            str(clone_dir),
        ],
        REPO_ROOT,
    )
    if expected_sha:
        run(["git", "fetch", "origin", expected_sha, "--depth", "1"], clone_dir)
        run(["git", "checkout", "--detach", expected_sha], clone_dir)
    source_sha = capture(["git", "rev-parse", "HEAD"], clone_dir)
    return clone_dir, source_sha


def run_build_commands(app: dict, clone_dir: Path) -> None:
    sync = app["sync"]
    workdir = clone_dir / safe_manifest_path(sync.get("workdir", "."))
    if not workdir.exists():
        raise SyncError(f"{app['slug']} workdir does not exist: {workdir}")
    for command in sync.get("commands", []):
        run(command, workdir)


def copy_app_output(app: dict, clone_dir: Path, output_dir: Path) -> None:
    sync = app["sync"]
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    if "paths" in sync:
        for item in sync["paths"]:
            copy_manifest_item(clone_dir / safe_manifest_path(item), output_dir / safe_manifest_path(item))
    else:
        artifact = clone_dir / safe_manifest_path(sync["artifact_path"])
        if not artifact.is_dir():
            raise SyncError(f"{app['slug']} artifact directory does not exist: {artifact}")
        copy_directory_contents(artifact, output_dir, excludes=set(sync.get("exclude", [])))

    for move in sync.get("moves", []):
        move_output_path(output_dir, move["from"], move["to"])

    normalize_text_files(output_dir)
    for postprocess in sync.get("postprocess", []):
        run_postprocess(postprocess, output_dir)
    normalize_text_files(output_dir)


def copy_manifest_item(source: Path, target: Path) -> None:
    if not source.exists():
        raise SyncError(f"Manifest source path does not exist: {source}")
    if source.is_dir():
        shutil.copytree(source, target, ignore=ignore_names(set()))
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def copy_directory_contents(source: Path, target: Path, *, excludes: set[str]) -> None:
    for child in source.iterdir():
        if child.name in DEFAULT_EXCLUDES or child.name in excludes:
            continue
        destination = target / child.name
        if child.is_dir():
            shutil.copytree(child, destination, ignore=ignore_names(excludes))
        else:
            shutil.copy2(child, destination)


def ignore_names(extra_excludes: set[str]):
    excludes = DEFAULT_EXCLUDES | extra_excludes

    def ignore(_directory: str, names: list[str]) -> list[str]:
        return [name for name in names if name in excludes]

    return ignore


def move_output_path(output_dir: Path, source_value: str, target_value: str) -> None:
    source = output_dir / safe_manifest_path(source_value)
    target = output_dir / safe_manifest_path(target_value)
    if not source.exists():
        raise SyncError(f"Move source does not exist: {source}")
    if target.exists():
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))


def run_postprocess(name: str, output_dir: Path) -> None:
    if name == "ozwizard_static_loader":
        index_path = output_dir / "index.html"
        text = index_path.read_text(encoding="utf-8")
        new_text, count = OZWIZARD_LOADER_PATTERN.subn(OZWIZARD_STATIC_LOADER, text, count=1)
        if count != 1:
            raise SyncError("Could not rewrite OZwizard loader in index.html")
        index_path.write_text(new_text, encoding="utf-8", newline="\n")
        return
    raise SyncError(f"Unknown postprocess step: {name}")


def normalize_text_files(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in BINARY_SUFFIXES:
            continue
        data = path.read_bytes()
        if b"\x00" in data:
            continue
        normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if normalized != data:
            path.write_bytes(normalized)


def tree_fingerprint(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    result: dict[str, str] = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if any(part in DEFAULT_EXCLUDES for part in path.relative_to(root).parts):
            continue
        rel = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        result[rel] = digest
    return result


def replace_destination(slug: str, output_dir: Path) -> Path:
    destination = ensure_inside(APPS_ROOT / slug, APPS_ROOT)
    if destination.exists():
        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(output_dir, destination)
    return destination


def load_state() -> dict:
    if not SYNC_STATE.exists():
        return {}
    with SYNC_STATE.open("r", encoding="utf-8") as handle:
        state = json.load(handle)
    return state if isinstance(state, dict) else {}


def write_state(state: dict) -> None:
    SYNC_STATE.parent.mkdir(parents=True, exist_ok=True)
    with SYNC_STATE.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")


def update_state(state: dict, app: dict, source_sha: str) -> None:
    state[app["slug"]] = {
        "repo": app["repo"],
        "branch": app["branch"],
        "source_sha": source_sha,
        "synced_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }


def stage_and_commit(changed: list[dict]) -> bool:
    if not changed:
        log("No app output changes detected; nothing to commit.")
        return False

    paths = [f"apps/{item['slug']}" for item in changed] + ["_data/app-sync-state.json"]
    run(["git", "add", "-A", "--", *paths], REPO_ROOT)
    diff_result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(REPO_ROOT))
    if diff_result.returncode == 0:
        log("No staged changes after sync; nothing to commit.")
        return False

    if len(changed) == 1:
        item = changed[0]
        subject = f"Sync {item['slug']} app"
    else:
        subject = "Sync tracked apps"
    body = "\n".join(
        f"- {item['slug']}: {item['repo']}@{item['source_sha'][:12]}" for item in changed
    )
    run(["git", "commit", "-m", subject, "-m", body], REPO_ROOT)
    return True


def sync_one_app(app: dict, workspace: Path, dry_run: bool, expected_sha: str | None) -> dict:
    log(f"== Syncing {app['slug']} from {app['repo']} ({app['branch']}) ==")
    clone_dir, source_sha = clone_app(app, workspace, expected_sha)
    run_build_commands(app, clone_dir)
    output_dir = workspace / "output" / app["slug"]
    copy_app_output(app, clone_dir, output_dir)

    destination = APPS_ROOT / app["slug"]
    changed = tree_fingerprint(output_dir) != tree_fingerprint(destination)
    if dry_run:
        status = "would change" if changed else "no changes"
        log(f"[dry-run] {app['slug']}: {status}")
    elif changed:
        replace_destination(app["slug"], output_dir)
        log(f"{app['slug']}: replaced apps/{app['slug']}")
    else:
        log(f"{app['slug']}: no output changes")

    return {
        "slug": app["slug"],
        "repo": app["repo"],
        "branch": app["branch"],
        "source_sha": source_sha,
        "changed": changed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync source-backed apps into the website repo.")
    parser.add_argument("--app", default="all", help="App slug to sync, or 'all'.")
    parser.add_argument("--dry-run", action="store_true", help="Build and compare without changing files.")
    parser.add_argument("--commit", action="store_true", help="Commit changed app output and sync state.")
    parser.add_argument("--source-repo", default="", help="Expected source repo from repository_dispatch.")
    parser.add_argument("--source-branch", default="", help="Expected source branch from repository_dispatch.")
    parser.add_argument("--source-sha", default="", help="Exact source commit SHA to sync.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    apps = select_apps(load_manifest(), args.app)
    validate_dispatch(apps, args)

    with tempfile.TemporaryDirectory(prefix="tracked-app-sync-") as tmp:
        workspace = Path(tmp)
        results = [
            sync_one_app(
                app,
                workspace,
                dry_run=args.dry_run,
                expected_sha=args.source_sha or None,
            )
            for app in apps
        ]

    changed = [result for result in results if result["changed"]]
    if args.dry_run:
        return 0

    if changed:
        state = load_state()
        for item in changed:
            app = next(app for app in apps if app["slug"] == item["slug"])
            update_state(state, app, item["source_sha"])
        write_state(state)

    if args.commit:
        stage_and_commit(changed)
    elif changed:
        log("Changes are present in the working tree; rerun with --commit to commit them.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        log(f"Command failed with exit code {error.returncode}: {' '.join(error.cmd)}")
        raise SystemExit(error.returncode)
    except SyncError as error:
        log(f"error: {error}")
        raise SystemExit(1)
