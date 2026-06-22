#!/usr/bin/env python3
"""Quantum Lens workspace resolver + seeder (system-context AND lens config).

The plugin install dir (${CLAUDE_PLUGIN_ROOT}) is shared and read-only. All per-repo, writable
state lives in a WORKSPACE resolved per host repo. This module is the single source of truth for
that resolution + seeding so commands never hand-roll paths (the original bare-relative bug) and
never write into the read-only plugin dir (the /lens-calibrate bug).

Writable state in the workspace:
  outputs/{analyses,solutions}/ + index.json   (handled with ql_persist.py)
  system-context/*.md                            (seeded from plugin templates)
  scenario.json                                  (lens-config OVERLAY over plugin defaults)
  agents/{custom-lens}-agent.md                  (custom lens bodies; built-ins stay in plugin)

Resolution order (first match wins):
  1. $QUANTUM_LENS_HOME      (explicit override)
  2. <cwd>/.quantum-lens     (created on first write)

Lens selection is resolved deterministically here (not in prompt prose): the default depth->lens
map below is the CANONICAL definition; the workspace scenario.json overlay applies deltas
(disabled_lenses, custom_lenses, depth_default).

CLI:
  python ql_workspace.py --plugin-root P                 # prepare (create + seed), print JSON
  python ql_workspace.py --plugin-root P --full          # also materialize built-in lens agents
  python ql_workspace.py --lenses --depth standard       # print resolved lens list (JSON)
  python ql_workspace.py --resolve-agent void-reader --plugin-root P   # print agent path (ws-first)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SYSTEM_CONTEXT_FILES = ("SYSTEM-MAP.md", "architecture.md", "project-goals.md")
CONFIG_NAME = "scenario.json"

# CANONICAL lens-selection defaults. The workspace overlay applies deltas on top of this.
DEFAULT_DEPTH_DEFAULT = "standard"
DEFAULT_DEPTH_MAP = {
    "quick": ["void-reader", "failure-romantic"],
    "standard": ["void-reader", "paradox-hunter", "boundary-dissolver", "failure-romantic"],
    "deep": ["void-reader", "paradox-hunter", "boundary-dissolver",
             "temporal-archaeologist", "scale-shifter", "failure-romantic"],
}


def default_config() -> dict:
    return {
        "depth_default": DEFAULT_DEPTH_DEFAULT,
        "depth_map": {k: list(v) for k, v in DEFAULT_DEPTH_MAP.items()},
        "disabled_lenses": [],
        "custom_lenses": [],
    }


# --------------------------------------------------------------------------- resolution
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
    (ws / "agents").mkdir(parents=True, exist_ok=True)
    index = ws / "outputs" / "index.json"
    if not index.exists():
        index.write_text(json.dumps({"version": 1, "records": []}, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------- seeding
def seed_system_context(ws: Path, plugin_root: str | None) -> list[str]:
    """Copy the 3 system-context templates from the plugin into the workspace if absent."""
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


def seed_config(ws: Path) -> bool:
    """Write the minimal lens-config overlay if absent. Returns True if freshly seeded."""
    cfg = ws / CONFIG_NAME
    if cfg.exists():
        return False
    cfg.write_text(json.dumps(default_config(), indent=2), encoding="utf-8")
    return True


def materialize_agents(ws: Path, plugin_root: str | None) -> list[str]:
    """--full: copy every built-in *-agent.md from the plugin into the workspace for local editing.

    Does not overwrite agents already present in the workspace (those are user-customized/custom).
    """
    copied: list[str] = []
    if not plugin_root:
        return copied
    src_dir = Path(plugin_root) / "agents"
    dest_dir = ws / "agents"
    dest_dir.mkdir(parents=True, exist_ok=True)
    if not src_dir.exists():
        return copied
    for src in sorted(src_dir.glob("*-agent.md")):
        dest = dest_dir / src.name
        if dest.exists():
            continue
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        copied.append(src.name)
    return copied


# --------------------------------------------------------------------------- config use
def load_config(ws: Path) -> dict:
    """Load the workspace overlay merged over defaults (tolerant of missing keys/file)."""
    cfg = default_config()
    p = ws / CONFIG_NAME
    if p.exists():
        try:
            user = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(user, dict):
                cfg.update({k: user[k] for k in user})
                # ensure depth_map keeps defaults for any unspecified depth
                if "depth_map" in user and isinstance(user["depth_map"], dict):
                    merged = {k: list(v) for k, v in DEFAULT_DEPTH_MAP.items()}
                    merged.update(user["depth_map"])
                    cfg["depth_map"] = merged
        except json.JSONDecodeError:
            pass
    return cfg


def resolve_lenses(ws: Path, depth: str) -> list[str]:
    """Effective lens list for a depth: depth_map[depth] - disabled + custom (matching depth)."""
    cfg = load_config(ws)
    base = list(cfg.get("depth_map", {}).get(depth, []))
    disabled = set(cfg.get("disabled_lenses", []))
    out = [l for l in base if l not in disabled]
    for c in cfg.get("custom_lenses", []):
        name = c.get("name")
        if name and depth in c.get("depth_modes", []) and name not in out:
            out.append(name)
    return out


def resolve_agent(ws: Path, plugin_root: str | None, lens: str) -> str:
    """Path to a lens agent definition: workspace-first, plugin-fallback."""
    fname = lens if lens.endswith("-agent.md") else f"{lens}-agent.md"
    ws_path = ws / "agents" / fname
    if ws_path.exists():
        return str(ws_path)
    if plugin_root:
        return str(Path(plugin_root) / "agents" / fname)
    return str(ws_path)


def config_status(ws: Path) -> dict:
    cfg = load_config(ws)
    return {
        "depth_default": cfg.get("depth_default"),
        "disabled_lenses": cfg.get("disabled_lenses", []),
        "custom_lenses": [c.get("name") for c in cfg.get("custom_lenses", [])],
        "config_exists": (ws / CONFIG_NAME).exists(),
    }


def system_context_status(ws: Path, plugin_root: str | None = None) -> dict:
    """Report each system-context file's state: missing | stub | template | filled."""
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


# --------------------------------------------------------------------------- prepare (the catch)
def prepare(plugin_root: str | None, cwd: str | None = None, full: bool = False) -> dict:
    ws = resolve_workspace(cwd)
    ensure_tree(ws)
    seeded = seed_system_context(ws, plugin_root)
    seeded_config = seed_config(ws)
    materialized = materialize_agents(ws, plugin_root) if full else []
    return {
        "workspace": str(ws),
        "outputs_dir": str(ws / "outputs"),
        "analyses_dir": str(ws / "outputs" / "analyses"),
        "solutions_dir": str(ws / "outputs" / "solutions"),
        "index_path": str(ws / "outputs" / "index.json"),
        "system_context_dir": str(ws / "system-context"),
        "config_path": str(ws / CONFIG_NAME),
        "agents_dir": str(ws / "agents"),
        "seeded": seeded,
        "seeded_config": seeded_config,
        "materialized_agents": materialized,
        "system_context_status": system_context_status(ws, plugin_root),
        "config_status": config_status(ws),
    }


# --------------------------------------------------------------------------- cli
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Resolve + prepare the Quantum Lens workspace.")
    ap.add_argument("--plugin-root", default=os.environ.get("CLAUDE_PLUGIN_ROOT"),
                    help="Plugin install root (for seeding templates + agent fallback).")
    ap.add_argument("--cwd", default=None, help="Override host cwd (testing).")
    ap.add_argument("--full", action="store_true",
                    help="Also materialize built-in lens agents into the workspace.")
    ap.add_argument("--lenses", action="store_true", help="Print resolved lens list for --depth.")
    ap.add_argument("--depth", default=None, help="Depth mode for --lenses (quick|standard|deep).")
    ap.add_argument("--resolve-agent", default=None, metavar="LENS",
                    help="Print the agent path for a lens (workspace-first, plugin-fallback).")
    args = ap.parse_args(argv)

    ws = resolve_workspace(args.cwd)

    if args.lenses:
        depth = args.depth or load_config(ws).get("depth_default", DEFAULT_DEPTH_DEFAULT)
        print(json.dumps({"depth": depth, "lenses": resolve_lenses(ws, depth)}))
        return 0
    if args.resolve_agent:
        print(resolve_agent(ws, args.plugin_root, args.resolve_agent))
        return 0

    print(json.dumps(prepare(args.plugin_root, args.cwd, full=args.full), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
