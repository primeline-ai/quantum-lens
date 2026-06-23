---
keywords: [init, initialize, setup, workspace, quantum-init, knowledge base, kb]
description: "Initialize the per-repo Quantum Lens workspace (.quantum-lens/): outputs, system-context, lens config, and optionally local lens agents"
argument: "[--full]"
model: sonnet
---

# /quantum-init

Create and seed the per-repo Quantum Lens workspace in the current project. This is normally
automatic — every command ensures the workspace on first use — but `/quantum-init` lets you set it
up explicitly (and customize before running an analysis).

See `${CLAUDE_PLUGIN_ROOT}/knowledge/persistence.md` for the full workspace contract.

## Arguments

- (none): create `.quantum-lens/` with `outputs/`, `system-context/` (seeded templates),
  `scenario.json` (lens-config overlay), and an empty `agents/`.
- `--full`: additionally **materialize** the built-in lens agents into `.quantum-lens/agents/` so
  you can edit them locally (built-ins otherwise stay in the read-only plugin and are read
  workspace-first / plugin-fallback).

## Workflow

1. Run the workspace helper (idempotent — safe to run repeatedly):
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_workspace.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}"${ARGS:+ }$ARGS
   ```
   where `$ARGS` is `--full` when the user passed it. (Fallback: `python3` if `python` is absent.)
2. Parse the printed JSON and report to the user:
   - `workspace` path
   - what was seeded (`seeded`, `seeded_config`, `materialized_agents`)
   - `system_context_status` — if all files are `template`/`stub`, tell the user to fill
     `<workspace>/system-context/*.md` to unlock system-aware adaptation in `/quantum-solve`
   - `config_status` — current `depth_default`, `disabled_lenses`, `custom_lenses`
3. Remind the user to add `.quantum-lens/` to their host project's `.gitignore` (local artifacts).

## Output

A short summary of the created/seeded workspace and the current lens configuration. Suggest next
steps: fill `system-context/*.md`, run `/lens-calibrate --show`, or start with `/quantum-lens`.

## Examples

```
/quantum-init
/quantum-init --full
```
