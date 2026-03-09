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
- `.claude/scenarios/quantum-lens/knowledge/quantum-framework.md`
- `.claude/scenarios/quantum-lens/knowledge/lens-definitions.md`
- `.claude/scenarios/quantum-lens/knowledge/anti-convergence-rules.md`

## Workflow

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

**Depth Mode Selection**:
- `quick`: Void Reader + Failure Romantic (2 agents)
- `standard` (default): Void Reader + Paradox Hunter + Boundary Dissolver + Failure Romantic (4 agents)
- `deep`: All 6 worker lenses (Void Reader, Paradox Hunter, Boundary Dissolver, Temporal Archaeologist, Scale Shifter, Failure Romantic)

For EACH selected lens, delegate in PARALLEL (sonnet, max_turns: 8):

1. TASK: Apply {lens_name} cognitive lens to the atomized input
2. EXPECTED OUTCOME: Structured lens output with insights[], tunnels[], tags[], disagreements[]
3. REQUIRED TOOLS: Read
4. MUST DO:
   - Read the lens agent definition from `.claude/scenarios/quantum-lens/agents/{lens}-agent.md`
   - Apply the cognitive mode and quantum instrument specified
   - Produce 3-5 raw insights (unfiltered, wild)
   - Tag each insight with semantic type
   - Produce the REQUIRED output section (Absence Map for Void Reader, Impossibility Register for Paradox Hunter, Boundary Map for Boundary Dissolver, Temporal Dig for Temporal Archaeologist, Scale Map for Scale Shifter, Failure Love Letter for Failure Romantic)
   - Contradict at least 2 claims from the naive reading
   - Reference specific atom IDs as evidence
5. MUST NOT DO: Be helpful. Be agreeable. Resolve tensions. These are perception instruments, not advisors.
6. CONTEXT: Pass the full Phase 0 output (atoms, naive_reading, full_input, domain, divergence_level)

**INTER-PHASE GATE**: Before Phase 2, verify:
- PASS: At least 1 lens produced an insight contradicting the Naive Reading
- FAIL: All lenses affirm the Naive Reading without contradiction -> re-run with note "increase anti-convergence pressure"

### Phase 2: Interfere (Meta-Analysis)

Delegate to **interference-reader-agent** (opus, max_turns: 12):

1. TASK: Read all lens outputs and detect interference patterns
2. EXPECTED OUTCOME: 4-section output (Constructive Map, Destructive Map + Cruxes, Isomorphisms, Killer Question)
3. REQUIRED TOOLS: Read
4. MUST DO:
   - Read `.claude/scenarios/quantum-lens/agents/interference-reader-agent.md` for full procedure
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

1. Read the analysis template: `.claude/scenarios/quantum-lens/templates/analysis-template.md`
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

Based on overall Breakthrough Score:
- Score >= 7: If Kairn available: auto-save via `kn_learn` (type: insight, tags: [quantum-lens, {domain}, {lens_names}]). If Kairn unavailable: save report to `outputs/analyses/{date}-{title}.md`
- Score >= 9: Also save extended analysis to `outputs/analyses/`
- Score < 7: Conversational only (no auto-save)

Always: Present the full analysis following the template (all 8 sections required).

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
