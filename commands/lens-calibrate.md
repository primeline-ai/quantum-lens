---
keywords: [lens, calibrate, customize, configure, quantum-lens, lenses, adjust]
description: "Customize Quantum Lens configuration - enable/disable lenses, adjust depth defaults, add custom lenses"
argument: "[--show | --enable LENS | --disable LENS | --add-lens | --depth-default MODE]"
model: sonnet
---

# /lens-calibrate

View and customize Quantum Lens configuration. **All writes go to the per-repo workspace overlay
`.quantum-lens/scenario.json` and `.quantum-lens/agents/` — never to the read-only plugin dir.** See
`${CLAUDE_PLUGIN_ROOT}/knowledge/persistence.md` (Config overlay).

## Arguments

- `--show` (default): Display the effective lens configuration (plugin defaults + workspace overlay)
- `--enable LENS`: Re-enable a lens (remove it from `disabled_lenses`)
- `--disable LENS`: Disable a lens (add it to `disabled_lenses`; skipped in every run)
- `--add-lens`: Interactive custom lens creation following the Extension Protocol
- `--depth-default MODE`: Change the default depth mode (quick|standard|deep)

## Phase 0: Ensure workspace (the catch)

Always run first (idempotent — creates `.quantum-lens/` + seeds the config overlay if absent):
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_workspace.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}"
```
The overlay file to read/edit is `<workspace>/scenario.json` (path from the helper's `config_path`).
Its shape: `{depth_default, depth_map, disabled_lenses[], custom_lenses[]}`.

## Workflow

### --show (default)

1. Read the workspace overlay `<workspace>/scenario.json`.
2. Read `${CLAUDE_PLUGIN_ROOT}/knowledge/lens-definitions.md` for cognitive-mode/depth descriptions.
3. For each depth, the effective lens set is what the resolver returns:
   `python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_workspace.py" --lenses --depth {quick|standard|deep}`.
4. Display a table marking each built-in lens `active`/`disabled` (per `disabled_lenses`) plus any
   `custom_lenses`, and show the current `depth_default`:

```
| # | Lens | Status | Cognitive Mode | Depth Modes |
|---|------|--------|---------------|-------------|
| 1 | Boundary Dissolver | active | Holistic integration | standard, deep |
| ... | ... | ... | ... | ... |
| + | {custom lens} | custom | {mode} | {its depth_modes} |

Current default depth: {depth_default}
```

### --enable / --disable

1. Read `<workspace>/scenario.json`.
2. `--disable LENS`: add `LENS` to `disabled_lenses` (no duplicates). `--enable LENS`: remove it.
3. Write the file back. No depth-map edits needed — the resolver subtracts `disabled_lenses` at
   selection time, so the change takes effect on the next `/quantum-lens` run.

### --depth-default MODE

1. Read `<workspace>/scenario.json`, set `depth_default` to MODE (validate quick|standard|deep),
   write back.

### --add-lens

Interactive custom lens creation (Extension Protocol). All artifacts land in the workspace:

1. Ask: "What cognitive mode does this lens use? (How does it THINK, not what domain it covers)"
2. Derive perceptual geometry from the cognitive mode
3. Ask: "What is the core question this lens always asks?"
4. Assign quantum instrument (suggest based on cognitive mode)
5. Define voice markers (hard constraints on language)
6. Specify required output section name
7. Identify the anti-pattern this lens catches
8. Ask which depth modes it participates in (quick|standard|deep)
9. Generate the agent file following the existing agent template pattern (read an existing
   `${CLAUDE_PLUGIN_ROOT}/agents/*-agent.md` as the structural example)
10. **Write it to `<workspace>/agents/{lens-name}-agent.md`** (NOT the plugin dir)
11. **Append to `custom_lenses`** in `<workspace>/scenario.json`:
    `{"name": "{lens-name}", "depth_modes": [...]}` — this makes the resolver include it and
    `quantum-lens` Phase 1 read it (workspace-first).

## Output

Configuration table showing all lenses (built-in active/disabled + custom) with cognitive mode and
depth modes, plus the current default depth — all reflecting the workspace overlay.
