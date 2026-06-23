---
keywords: [quantum, lens, deconstruct, analyze, radical, multi-perspective, quantum-lens, perception]
description: "Run a radical multi-perspective deconstruction analysis using quantum-inspired cognitive lenses"
argument: "<input> [--depth quick|standard|deep] [--lenses LENS1,LENS2]"
model: opus
---

# /quantum-lens

Radical multi-perspective deconstruction engine. Not brainstorming - perception.

## Arguments

- `input` (required): URL, pasted text, or concept (prefix with "concept: ")
- `--depth MODE`: Force depth mode (quick|standard|deep). Default: auto-detect from input length
- `--lenses LENS1,LENS2`: Force specific lenses (override depth mode selection)

## Natural Language Depth Detection

If no explicit `--depth` flag is provided, detect depth from the user's phrasing:

| Phrase | Depth |
|--------|-------|
| "volles quantum", "full quantum", "deep quantum", "alle lenses", "all lenses", "volle analyse", "maximum depth" | `deep` |
| "quick quantum", "schnelles quantum", "kurze analyse", "quick lens" | `quick` |
| (no depth signal) | `standard` (or auto-detect from input length) |

## Prerequisites

Read these knowledge files for framework context:
- `${CLAUDE_PLUGIN_ROOT}/knowledge/quantum-framework.md`
- `${CLAUDE_PLUGIN_ROOT}/knowledge/lens-definitions.md`
- `${CLAUDE_PLUGIN_ROOT}/knowledge/anti-convergence-rules.md`
- `${CLAUDE_PLUGIN_ROOT}/knowledge/persistence.md` (how Phase 4 writes outputs — read before persisting)

## Workflow

### Phase 0a: Ensure workspace (the catch)

Before anything else, ensure the per-repo workspace exists and read the lens config (per
`${CLAUDE_PLUGIN_ROOT}/knowledge/persistence.md`):
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_workspace.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}"
```
This creates `.quantum-lens/` (idempotent) and seeds the lens-config overlay if absent. (Fallback:
`python3`.)

### Phase 0: Intake + Atomization

Delegate to **intake-processor-agent** (sonnet, max_turns: 6):

1. TASK: Process the raw input into atoms
2. EXPECTED OUTCOME: JSON with atoms[], naive_reading, domain, depth, input_mode, divergence_level
3. REQUIRED TOOLS: Read, firecrawl_scrape (if URL)
4. MUST DO:
   - Detect input type (URL/text/concept)
   - If URL: scrape with firecrawl (markdown, onlyMainContent)
   - Length-adaptive routing (compact <100w, standard 100-5000w, section >5000w)
   - AoT decomposition into 5-12 tagged atoms
   - Generate naive reading (1-2 paragraphs)
   - Detect domain and divergence level
5. MUST NOT DO: Analyze or interpret. Just decompose.
6. CONTEXT: Input is `{input}`. Depth override: `{depth}`.

**Firecrawl unavailable**: intake-processor-agent falls back to WebFetch automatically. URL inputs still work.
**FAILED**: If all fetch methods fail and no fallback text available, stop and tell the user.

### Phase 1: Diverge (Parallel Lens Analysis)

**Depth Mode Selection** — resolved from the workspace config overlay, NOT hardcoded. This honors
`/lens-calibrate` (disabled lenses, custom lenses, `depth_default`). Run:
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_workspace.py" --lenses --depth {depth}
```
(When the user gave no `--depth` and no natural-language depth signal, omit `--depth` so the helper
applies the configured `depth_default`.) Use the returned `lenses` list as the exact set to run.
The defaults are quick=2, standard=4, deep=6 (canonical map lives in `ql_workspace.py`); the overlay
may add/remove lenses.

Then, as the orchestrator (you have Bash), resolve each lens's agent definition path up front so the
sub-agents need only `Read`:
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_workspace.py" --resolve-agent {lens} --plugin-root "${CLAUDE_PLUGIN_ROOT}"
```
(workspace-first, so custom/edited lenses win; built-ins fall back to the plugin).

For EACH lens in the resolved list, delegate in PARALLEL (sonnet, max_turns: 8):

1. TASK: Apply {lens_name} cognitive lens to the atomized input
2. EXPECTED OUTCOME: Structured lens output with insights[], tunnels[], tags[], disagreements[]
3. REQUIRED TOOLS: Read
4. MUST DO:
   - Read the lens agent definition at the resolved path passed in CONTEXT (`{agent_path}`)
   - Apply the cognitive mode and quantum instrument specified
   - Produce 3-5 raw insights (unfiltered, wild)
   - Tag each insight with semantic type
   - Produce the REQUIRED output section (Absence Map for Void Reader, Impossibility Register for Paradox Hunter, Boundary Map for Boundary Dissolver, Temporal Dig for Temporal Archaeologist, Scale Map for Scale Shifter, Failure Love Letter for Failure Romantic)
   - Contradict at least 2 claims from the naive reading
   - Reference specific atom IDs as evidence
5. MUST NOT DO: Be helpful. Be agreeable. Resolve tensions. These are perception instruments, not advisors.
6. CONTEXT: Pass the resolved `{agent_path}` for this lens, plus the full Phase 0 output (atoms, naive_reading, full_input, domain, divergence_level)

**INTER-PHASE GATE**: Before Phase 2, verify:
- PASS: At least 1 lens produced an insight contradicting the Naive Reading
- FAIL: All lenses affirm the Naive Reading without contradiction -> re-run with note "increase anti-convergence pressure"

### Phase 2: Interfere (Meta-Analysis)

Delegate to **interference-reader-agent** (opus, max_turns: 12):

1. TASK: Read all lens outputs and detect interference patterns
2. EXPECTED OUTCOME: 4-section output (Constructive Map, Destructive Map + Cruxes, Isomorphisms, Killer Question)
3. REQUIRED TOOLS: Read
4. MUST DO:
   - Read `${CLAUDE_PLUGIN_ROOT}/agents/interference-reader-agent.md` for full procedure
   - Aggregate all lens outputs
   - Map constructive interference (convergence points)
   - Map destructive interference (contradictions)
   - Identify CRUXes (minimal factual claims resolving disagreements)
   - Find cross-lens isomorphisms via structure-mapping
   - Apply relevance filter (80/20 - surface only high-signal findings)
   - Formulate the Killer Question (MUST be specific, MUST reference an atom, MUST have YES/NO implications)
5. MUST NOT DO: Produce a generic Killer Question. If the question could apply to any input, it has failed.
6. CONTEXT: Pass labeled lens output blocks (one per active lens):
   ```
   --- LENS: void-reader ---
   {output}
   --- LENS: paradox-hunter ---
   {output}
   --- LENS: boundary-dissolver ---
   {output}
   (... additional lenses based on depth mode ...)
   ```
   Plus metadata: atoms[], naive_reading, domain, depth, input_title

**FAILED**: If Killer Question is generic (no specific concept, no testable condition), note this for prompt revision.

### Phase 3: Converge (Synthesis)

Do this INLINE (not delegated):

1. Read the analysis template: `${CLAUDE_PLUGIN_ROOT}/templates/analysis-template.md`
2. Assemble sections 1-8 following the template
3. Select top 3-5 insights from across all lenses
4. For each insight: concrete action path (what the user could DO)
5. Assign Breakthrough Score (1-10) per insight using this rubric:
   - 1-3: Conventional reframing (exists in mainstream discourse)
   - 4-6: Non-obvious connection (requires domain expertise)
   - 7-8: Genuine breakthrough (changes how you think about the input)
   - 9-10: Paradigm-level (challenges fundamental assumptions)
6. Present Superposition View (NOT forced synthesis - per Superpositional Belief research)
7. Offer goal-conditioned collapse: "If your goal is X, then..."
8. Calculate overall Breakthrough Score (average of top 3 insights)

### Phase 4: Persist

Persistence follows `${CLAUDE_PLUGIN_ROOT}/knowledge/persistence.md` (read it). Do NOT hand-write
file paths or free-form markdown — emit a structured record and let the Python helper do the IO.

1. **Build the analysis record JSON** conforming to
   `${CLAUDE_PLUGIN_ROOT}/schemas/analysis_record.schema.json` (`kind:"analysis"`, the 8 sections'
   data as fields: `naive_reading`, `atoms[]`, `insights[]`, `interference`, `killer_question`,
   `tunnels[]`, `superposition_view[]`, `meta_observations`, plus `overall_score`, `lenses[]`,
   `domain`, `depth`, `input_title`). Set `extended: true` if overall score >= 9.
2. **Persist (always — the guaranteed floor, any score):**
   ```bash
   echo '<record-json>' | python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_persist.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}"
   ```
   On `{ok:false, error}`, fix the record per the error and retry. Capture `record_id` and
   `kairn_payload` from the result.
3. **If overall score >= 7 AND Kairn available:** `kn_learn` with the returned `kairn_payload`
   (`type`, `content`, `tags`), then link it back:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/ql_persist.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}" \
     --link-kairn --record <record_id> --node <kairn_node_id> --kind analysis
   ```
   If Kairn is unavailable, the file write in step 2 already preserved everything — nothing else to do.

Always: Present the full analysis following the template (all 8 sections required). The record/md
are an artifact, not a replacement for the in-conversation report.

## Output

Full analysis following `templates/analysis-template.md`. All 8 sections required. This is the floor, not the ceiling.

## Examples

```
/quantum-lens https://arxiv.org/abs/2502.12018
/quantum-lens "AI agents will replace 80% of knowledge workers by 2030"
/quantum-lens concept: the attention economy
/quantum-lens "long article text pasted here..." --depth standard
/quantum-lens https://blog.example.com/post --depth quick
```
