# Quantum Lens — Architecture & Operating Guide

Radical multi-perspective deconstruction (**Perception Engine**) + solution engineering
(**Solution Engine**) packaged as a Claude Code plugin. This file is the architecture overview and
the operating rules for working **inside this repo**. For the comprehensive manifest (lens catalog,
modes, scoring, troubleshooting) see **[PMAT_README.md](PMAT_README.md)**; for install see
**[SETUP.md](SETUP.md)**; user-facing intro is **[README.md](README.md)**.

QL = observation (the wave function, all possibilities). SE = collapse (measurement, forcing
concrete reality). `/quantum-full` is QL × SE, not QL + SE.

---

## Plugin layout

```
commands/      6 slash-command workflows (the orchestrators)
agents/        12 agent definitions (7 perception lenses + 4 SE agents + intake)
knowledge/     framework + rules + the persistence.md contract
schemas/       JSON Schemas for analysis/solution records
scripts/       ql_workspace.py, ql_persist.py, test_ql_persist.py (deterministic IO)
templates/     analysis/solution markdown shapes (rendered from JSON by ql_persist.py)
system-context/ seed templates copied into each host repo's workspace
scenario.json  plugin manifest (agents, commands, workflow phases)
```

Commands: `/quantum-init`, `/quantum-lens`, `/quantum-solve`, `/quantum-full`, `/lens-calibrate`,
`/quantum-review`.

---

## Two roots — the core invariant (READ FIRST)

The plugin install dir is **shared and read-only**; per-repo writable state lives in a **workspace**.
Never confuse them — conflating them caused the original output-logging and `/lens-calibrate` bugs.

| Root | Holds | Addressed by | Writable |
|------|-------|--------------|----------|
| **Plugin** | commands, agents, knowledge, schemas, scripts, templates, default config | `${CLAUDE_PLUGIN_ROOT}` | NO |
| **Workspace** | outputs, index, system-context, lens-config overlay, custom agents | `$QUANTUM_LENS_HOME` else `<cwd>/.quantum-lens/` | YES |

**Rule:** every READ of a plugin asset uses `${CLAUDE_PLUGIN_ROOT}/...`. Every WRITE, and every read
of `system-context`/lens-config, goes to the workspace via the helper scripts. Never write under
`${CLAUDE_PLUGIN_ROOT}` at runtime.

---

## Persistence — JSON is the source of truth

Authoritative contract: **`knowledge/persistence.md`**. The LLM emits ONE schema-validated JSON
record; `scripts/ql_persist.py` does all IO (validate → write canonical `{record_id}.json` → render
`{record_id}.md` deterministically → upsert `outputs/index.json` → return a `kn_learn` payload). Do
**not** hand-write output files or free-form markdown — that drifts under long instructions.

- **File write is the guaranteed floor for every run, any score.** Score only decides whether to
  *also* `kn_learn` + `--link-kairn` (bidirectional), draft a plan, or mark `extended`.
- `/quantum-review` reads `outputs/index.json` (deterministic), not the rendered `.md`.

---

## Lens config — deterministic overlay

Lens selection is resolved in Python, not prompt prose. The canonical depth→lens map lives in
`scripts/ql_workspace.py`; the workspace `scenario.json` overlay applies deltas (`disabled_lenses`,
`custom_lenses`, `depth_default`).

- Select: `python ql_workspace.py --lenses --depth <mode>` → `depth_map − disabled + custom`.
- Resolve an agent: `python ql_workspace.py --resolve-agent <lens>` → **workspace-first,
  plugin-fallback** (custom/edited lenses win; built-ins propagate from the plugin).
- `/lens-calibrate` writes ONLY the workspace overlay + `.quantum-lens/agents/`. `/quantum-init`
  seeds the workspace (`--full` materializes built-in agents locally for editing).

---

## Pipelines

```
Perception : INPUT → P0 intake/atomize → P1 parallel lenses → P2 interference → P3 converge+persist
Solution   : INPUT → S0 mode-detect → S1 system-scan → [S1.5 deep-dive] → S2 engineer
                   → [S2.5 cascade] → S3 DSV synthesis → S4 persist+action
Full       : QL (P0–3) → smart filter → SE (S0–4) → combined report
```

Models: orchestrating commands + Interference Reader + Solution Synthesizer use **opus**; other
agents default to **sonnet** (see PMAT_README.md → Model Notes).

---

## Editing rules (for agents working in this repo)

1. Keep the **two-roots** split: reads `${CLAUDE_PLUGIN_ROOT}`, writes the workspace.
2. All output/config IO goes through `ql_workspace.py` / `ql_persist.py` — extend them, don't
   re-hand-roll paths in command prose.
3. The canonical lens depth map lives once, in `ql_workspace.py`. Don't re-hardcode it elsewhere.
4. Run `make test` (or `python scripts/test_ql_persist.py`) after touching scripts/schemas.
5. Keep docs DRY: catalogs (lenses, modes, scoring, troubleshooting) live in **PMAT_README.md**;
   README/SETUP/CLAUDE link to it rather than duplicating.
