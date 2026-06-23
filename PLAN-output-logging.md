# Output-Logging Redesign — Implemented

**Status:** implemented (2026-06-22). Authoritative runtime contract: `knowledge/persistence.md`.

## Problem (root cause)

Reads were anchored (`${CLAUDE_PLUGIN_ROOT}/...`) but writes and `system-context` reads were
**bare-relative** (`outputs/analyses/...`, `system-context/SYSTEM-MAP.md`), resolving against the
host repo cwd, not the plugin — so outputs targeted nonexistent paths and never registered. The
bundled `outputs/*/.gitkeep` dirs were never write targets. File-save was also double-gated behind
`score>=7 AND Kairn-unavailable`, so with Kairn on, analyses skipped files entirely.

## Solution (JSON source-of-truth + deterministic Python persistence)

The LLM emits ONE schema-validated JSON record; Python does all IO — no free-form markdown writes,
no model-chosen paths. This removes the prompt-coherence drift that plagued long-instruction md writes.

**New files**
- `schemas/analysis_record.schema.json`, `schemas/solution_record.schema.json` — record schemas.
- `scripts/ql_workspace.py` — resolves the per-repo workspace (`$QUANTUM_LENS_HOME` → `<cwd>/.quantum-lens/`),
  creates the tree, seeds `system-context` templates if absent.
- `scripts/ql_persist.py` — validates (jsonschema if present, else built-in), writes canonical
  `{record_id}.json`, renders `{record_id}.md` deterministically, upserts `outputs/index.json`,
  returns a `kairn_payload`; `--link-kairn` writes a Kairn node_id back into record+md+index.
- `scripts/test_ql_persist.py` — 22 stdlib tests (all passing).
- `knowledge/persistence.md` — the contract (workspace resolution, CLIs, record_id scheme, Kairn
  link protocol, and the single Extension Point for later evolving-lite / Kairn-primary modes).

**Key behavior changes**
- **File write is the guaranteed floor for every run** (any score). Score/usefulness only decides
  whether to *also* `kn_learn` + link, draft a plan, or set `extended`.
- All writes + `system-context` reads go to the workspace; plugin install dir stays read-only.
- `/quantum-review` reads `outputs/index.json` deterministically instead of scanning md.

**Edited**: `commands/quantum-lens.md` (Phase 4), `commands/quantum-solve.md` (S1 seed+read, S4
persist), `commands/quantum-full.md` (Step 6), `commands/quantum-review.md` (index.json),
`agents/solution-synthesizer-agent.md` (emit record, not file), `SETUP.md` (python prereq,
workspace, gitignore).

## Follow-ups
- **DONE:** `/lens-calibrate` read-only-install bug — lens config moved to the per-repo overlay
  `.quantum-lens/scenario.json` + `.quantum-lens/agents/`, `quantum-lens` Phase 1 now resolves lenses
  from it (was a hardcoded no-op), and `/quantum-init` seeds the workspace. See the "Config overlay"
  section of `knowledge/persistence.md`.
- evolving-lite integration / Kairn-as-primary-store — the `persistence.md` Extension Point is the seam.

## Verify
`python scripts/test_ql_persist.py` → ALL PASSED. Manual: run `/quantum-lens "concept: x" --depth
quick` in a scratch dir → file appears under `.quantum-lens/outputs/analyses/` regardless of score.
