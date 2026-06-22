#!/usr/bin/env python3
"""Quantum Lens workspace resolver + system-context seeder.

The plugin install dir (${CLAUDE_PLUGIN_ROOT}) is shared and read-only. All per-repo,
writable state (analyses, solutions, index, system-context) lives in a WORKSPACE resolved
per host repo. This module is the single source of truth for that resolution so commands
never hand-roll paths (which caused the original bare-relative output bug).

Resolution order (first match wins):
  1. $QUANTUM_LENS_HOME                      (explicit override)
  2. <cwd>/.quantum-lens                     (created on first write)

CLI:
  python ql_workspace.py --plugin-root "${CLAUDE_PLUGIN_ROOT}"
      -> resolves + ensures the tree, seeds system-context templates if absent,
         prints a JSON blob with resolved paths and the list of seeded files.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SYSTEM_CONTEXT_FILES = ("SYSTEM-MAP.md", "architecture.md", "project-goals.md")


def resolve_workspace(cwd: str | None = None) -> Path:
    env = os.environ.get("QUANTUM_LENS_HOME")
    if env:
        return Path(env).expanduser().resolve()
    base = Path(cwd) if cwd else Path.cwd()
    return (base / ".quantum-lens").resolve()


def ensure_tree(ws: Path) -> None:
    (ws / "outputs" / "analyses").mkdir(parents=True, exist_ok=True)
    (ws / "outputs" / "solutions").mkdir(parents=True, exist_ok=True)
    (ws / "system-context").mkdir(parents=True, exist_ok=True)
    index = ws / "outputs" / "index.json"
    if not index.exists():
        index.write_text(json.dumps({"version": 1, "records": []}, indent=2), encoding="utf-8")


def seed_system_context(ws: Path, plugin_root: str | None) -> list[str]:
    """Copy the 3 system-context templates from the plugin into the workspace if absent.

    Returns the list of filenames that were freshly seeded. If a template is missing in the
    plugin, seed a minimal stub so the read target always exists.
    """
    seeded: list[str] = []
    dest_dir = ws / "system-context"
    dest_dir.mkdir(parents=True, exist_ok=True)
    src_dir = Path(plugin_root) / "system-context" if plugin_root else None
    for name in SYSTEM_CONTEXT_FILES:
        dest = dest_dir / name
        if dest.exists():
            continue
        src = (src_dir / name) if src_dir else None
        if src and src.exists():
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            title = name.replace(".md", "").replace("-", " ").title()
            dest.write_text(f"# {title}\n\n_(template — fill this in)_\n", encoding="utf-8")
        seeded.append(name)
    return seeded


def system_context_status(ws: Path, plugin_root: str | None = None) -> dict:
    """Report each system-context file's state: missing | stub | template | filled.

    `template` = present but byte-identical to the plugin's seed template (not yet customized).
    `filled` = present and diverged from the template (user edited it). This distinction matters:
    the Solution Engine only does system-aware comparison when at least one file is `filled`.
    """
    status = {}
    src_dir = Path(plugin_root) / "system-context" if plugin_root else None
    for name in SYSTEM_CONTEXT_FILES:
        p = ws / "system-context" / name
        if not p.exists():
            status[name] = "missing"
            continue
        body = p.read_text(encoding="utf-8")
        if "_(template — fill this in)_" in body:
            status[name] = "stub"
            continue
        src = (src_dir / name) if src_dir else None
        if src and src.exists() and body == src.read_text(encoding="utf-8"):
            status[name] = "template"
        else:
            status[name] = "filled"
    return status


def prepare(plugin_root: str | None, cwd: str | None = None) -> dict:
    ws = resolve_workspace(cwd)
    ensure_tree(ws)
    seeded = seed_system_context(ws, plugin_root)
    return {
        "workspace": str(ws),
        "outputs_dir": str(ws / "outputs"),
        "analyses_dir": str(ws / "outputs" / "analyses"),
        "solutions_dir": str(ws / "outputs" / "solutions"),
        "index_path": str(ws / "outputs" / "index.json"),
        "system_context_dir": str(ws / "system-context"),
        "seeded": seeded,
        "system_context_status": system_context_status(ws, plugin_root),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Resolve + prepare the Quantum Lens workspace.")
    ap.add_argument("--plugin-root", default=os.environ.get("CLAUDE_PLUGIN_ROOT"),
                    help="Plugin install root (for seeding system-context templates).")
    ap.add_argument("--cwd", default=None, help="Override host cwd (testing).")
    args = ap.parse_args(argv)
    print(json.dumps(prepare(args.plugin_root, args.cwd), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
