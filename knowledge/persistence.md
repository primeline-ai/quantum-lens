# Persistence Contract

**Authoritative spec for how Quantum Lens writes outputs and links to Kairn.** Commands and
agents MUST follow this instead of hand-writing file paths. Free-form markdown writes under long
instructions drift and lose coherence, and bare-relative paths resolve against the wrong cwd — so
the model emits ONE structured JSON record and a Python helper does all the IO deterministically.

---

## Two roots — never confuse them

| Root | What | Addressed by | Writable? |
|------|------|--------------|-----------|
| **Plugin root** | shared, read-only plugin install (knowledge, agents, templates, schemas, scripts) | `${CLAUDE_PLUGIN_ROOT}` | NO |
| **Workspace** | per-repo, writable state (outputs, index, system-context) | resolved per host repo (below) | YES |

**Rule:** every READ of plugin assets uses `${CLAUDE_PLUGIN_ROOT}/...`. Every WRITE, and every
read of `system-context`, goes to the **workspace**. Never write under `${CLAUDE_PLUGIN_ROOT}`.

### Workspace resolution (first match wins)
1. `$QUANTUM_LENS_HOME` (explicit override)
2. `<host-cwd>/.quantum-lens/` (created on first write)

### Workspace layout
```
<workspace>/
  outputs/index.json                       # join table (see schema below)
  outputs/analyses/{record_id}.json|.md    # /quantum-lens
  outputs/solutions/{record_id}.json|.md   # /quantum-solve
  system-context/{SYSTEM-MAP,architecture,project-goals}.md   # seeded from plugin templates
  scenario.json                            # lens-config overlay (see "Config overlay" below)
  agents/{custom-lens}-agent.md            # custom lens bodies (built-ins stay in the plugin)
```
`record_id = {date}-{slug}-{8hex}` (Python generates it; do not invent your own).

---

## The two scripts (the only sanctioned IO path)

Invoke with `python` (fallback `python3`). Always pass `--plugin-root "${CLAUDE_PLUGIN_ROOT}"`.

### 1. `scripts/ql_workspace.py` — resolve + seed
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_workspace.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}"
```
Resolves the workspace, creates the tree, **seeds** the 3 `system-context` templates if absent,
and prints JSON: `{workspace, outputs_dir, analyses_dir, solutions_dir, index_path,
system_context_dir, seeded:[...], system_context_status:{file: missing|stub|template|filled}}`
(`template` = present but byte-identical to the seed template = not yet customized; `filled` =
user-edited). Call this in `/quantum-solve` S1 **before** reading system-context. System-aware
comparison runs only when at least one file is `filled`; otherwise tell the user to fill the seeded
files and proceed in general analysis mode.

### 2. `scripts/ql_persist.py` — persist a record
```bash
echo '<record-json>' | python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_persist.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}"
# or: --in record.json
```
Validates the record against `schemas/{analysis,solution}_record.schema.json` (uses `jsonschema`
if importable, else a built-in required-key/type check), writes the canonical `{record_id}.json`,
renders `{record_id}.md` from the JSON (structure is code; only prose fields come from the model),
upserts `outputs/index.json` by `record_id` (idempotent), and prints:
`{ok, record_id, kind, json_path, md_path, index_path, workspace, kairn_payload}`.

`kairn_payload` is ready to hand to `kn_learn` (`{type, content, tags}`). On a validation error it
prints `{ok:false, error}` and exits non-zero — surface the error, fix the record, retry.

### Link a record to a Kairn node (after kn_learn returns)
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_persist.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}" \
  --link-kairn --record <record_id> --node <kairn_node_id> --kind analysis|solution
```
Writes `kairn_node_id` back into the record JSON, re-renders the md, and patches the index —
giving a bidirectional, machine-checkable plugin↔Kairn link joined through `index.json`.

---

## Record schemas (source of truth)
- `schemas/analysis_record.schema.json` — `/quantum-lens` (required: `kind`, `input_title`,
  `insights`, `overall_score`, `lenses`).
- `schemas/solution_record.schema.json` — `/quantum-solve` (required: `kind`, `input_title`,
  `mode`, `executive_summary`).

`index.json`: `{ "version": 1, "records": [ {record_id, kind, date, title, domain, mode, depth,
score, lenses[], json_path, md_path, kairn_node_id} ] }`.

---

## Config overlay (lens calibration)

`/lens-calibrate` must never write the read-only plugin dir. All lens config is a per-repo
**overlay** at `.quantum-lens/scenario.json`, seeded minimal by `ql_workspace.py`:

```json
{ "depth_default": "standard",
  "depth_map": { "quick": [...], "standard": [...], "deep": [...] },
  "disabled_lenses": [], "custom_lenses": [ {"name": "...", "depth_modes": ["deep"]} ] }
```

The canonical default `depth_map`/`depth_default` live as constants in `ql_workspace.py`; the
overlay carries deltas. **Lens selection is resolved deterministically by the helper, not in prompt
prose:**

- `python ql_workspace.py --lenses --depth <mode>` -> `{depth, lenses}` where
  `lenses = depth_map[mode] − disabled_lenses + custom_lenses (whose depth_modes include mode)`.
  Omit `--depth` to use `depth_default`.
- `python ql_workspace.py --resolve-agent <lens> --plugin-root P` -> the lens agent path,
  **workspace-first** (`.quantum-lens/agents/{lens}-agent.md`) then plugin fallback. So custom and
  user-edited lenses win; built-ins still come from the plugin (updates propagate).

`/quantum-lens` Phase 1 calls these; `/lens-calibrate` edits the overlay + writes custom lens bodies
to `.quantum-lens/agents/`. `--full` (via `/quantum-init`) materializes built-in agents locally for
editing. Built-in lens agents are otherwise never copied.

## Persistence policy (the gate)

**File write is the guaranteed floor — every run writes a record, regardless of score.** The score
only decides *additional* actions:

| Command | Always | If gate met |
|---------|--------|-------------|
| `/quantum-lens` | persist record (file) | `overall_score>=7` AND Kairn available → `kn_learn` with `kairn_payload`, then `--link-kairn`. `>=9` → set `extended:true` in the record. |
| `/quantum-solve` | persist record (file) | usefulness `>=70%` → also draft an implementation plan; `40-69%` → if Kairn available, `kn_learn` + `--link-kairn`. Barrier tracking via `kn_learn` when Kairn available. |

Kairn is an **enhancement**, never an exclusive — files are written either way.

---

## Extension Point (later integration — NOT active)

`ql_persist.persist()` is the single seam for future integration. To route persistence into
**evolving-lite** (option A) or make a **Kairn structured DB the primary store** (option B2),
change only the tail of `persist()` (and the policy table above) — the 5 command/agent files that
call the script do not change. Keep the file-write floor unless explicitly removing isolation.

- **(A) evolving-lite:** after the file write, also emit the record to evolving-lite's experience
  store (its learning loop consumes the same JSON; `record_id` is the shared key).
- **(B2) Kairn-primary:** keep the file as a cache/export; treat the Kairn node as canonical and
  store `record_id` in the node so `index.json` and the DB stay joinable.
