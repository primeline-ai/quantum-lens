---
keywords: [solve, solution, adapt, repo, problem, contra, quantum-solve, break through, limit, barrier, reverse-engineer]
description: "Engineer concrete solutions from insights - evaluate repos, solve problems, break through status quo"
argument: "<input> [--mode repo|problem|contra] [--quick] [--cascade]"
model: opus
---

# /quantum-solve

Solution Engineering engine. Not perception - action. Works backward from goals, eliminates barriers, produces executable adaptation roadmaps.

## Arguments

- `input` (required): URL (repo-mode), problem description (problem-mode), or "contra: {limit}" (contra-mode)
- `--mode repo|problem|contra`: Force mode (overrides auto-detection)
- `--quick`: Stop after S1 (intake + system scan only). Fast relevance check in ~30s
- `--cascade`: (contra-mode only) When counter-examples found, trigger repo-mode + problem-mode on them

## Mode Auto-Detection

If no `--mode` flag:
- URL present (GitHub, GitLab, etc.) -> repo-mode
- "contra:" prefix -> contra-mode
- Everything else -> problem-mode

## Prerequisites

Read these knowledge files for framework context:
- `.claude/scenarios/quantum-lens/knowledge/solution-modes.md`
- `.claude/scenarios/quantum-lens/knowledge/barrier-taxonomy.md`

## Workflow

### S0: Intake + Mode Detection

1. Detect mode: URL = repo, "contra:" = contra, --mode override, else = problem
2. If from `/quantum-full`: parse QL output, extract filtered insights + barrier_type annotations
3. Mode-specific intake:
   - **repo-mode**: `firecrawl_map` (structure) + `firecrawl_scrape` (README + top docs, markdown, onlyMainContent)
   - **problem-mode**: Structure problem + constraints from user input
   - **contra-mode**: Extract accepted limit + desired goal

### S1: System Scan

Delegate to **system-comparator-agent** (sonnet, max_turns: 8):

1. TASK: Map source material against your system
2. EXPECTED OUTCOME: Overlap/Gap/Collision maps. In repo-mode: Multi-Signal Relevance Score
3. REQUIRED TOOLS: Read, Glob, Grep
4. MUST DO:
   - Read `system-context/SYSTEM-MAP.md`, `system-context/architecture.md`, `system-context/project-goals.md` (if available)
   - Produce all 3 maps (Overlap, Gap, Collision)
   - In repo-mode: produce Multi-Signal Relevance Score FIRST
5. MUST NOT DO: Speculate about system capabilities without reading files
6. CONTEXT: Mode is `{mode}`. Source material: `{intake_output}`. Optional QL context: `{ql_insights}`

**STOP GATE (repo-mode only)**: Multi-Signal Relevance < 4 -> "Not relevant enough for deep analysis." Present score and stop.

**--quick FLAG**: Stop here after S1. Return: Relevance Score + maps. Done.

### S1.5: Deep Dive (repo-mode only, if Relevance >= 4)

1. Deeper firecrawl scraping of key source files identified in S1
2. Code-level pattern extraction
3. Second system-comparator pass with deeper context

### S2: Engineering (HYBRID DELEGATION - mode-dependent)

The delegation model differs by mode to preserve conversation context where it matters:

**repo-mode** (fully delegated - no conversation context needed):

Delegate to **adaptation-architect-agent** (sonnet, max_turns: 8):
1. TASK: Design concrete adaptation paths from comparator output
2. EXPECTED OUTCOME: Priority Matrix + Quick Wins + Main Track + Deal Breakers
3. REQUIRED TOOLS: Read, Glob, Grep
4. MUST DO: Read system-context/SYSTEM-MAP.md (if available), reference specific file paths, include rollback for every adaptation
5. MUST NOT DO: Produce vague recommendations without file paths
6. CONTEXT: Comparator output: `{s1_output}`. Source material: `{source}`. Mode: repo.

Delegate to **reverse-engineer-agent** (opus, max_turns: 12) IN PARALLEL:
1. TASK: Work backward from the integration goal
2. CONTEXT: Desired outcome: "Integrate {source} patterns into your system". Barriers from comparator collision map.

**problem-mode** (hybrid - system-comparator delegated, reverse-engineer + synthesis inline):

- DELEGATED: system-comparator already ran in S1
- INLINE (main agent): Run reverse-engineer analysis yourself. You have the conversation context - the user's problem description, the nuance of WHY this is a limitation. A sub-agent would lose this.
  - Read `.claude/scenarios/quantum-lens/agents/reverse-engineer-agent.md` for the procedure
  - Read `.claude/scenarios/quantum-lens/knowledge/barrier-taxonomy.md` for classification
  - Produce: Goal Statement, Reverse Path Table, Barrier Elimination, Wavelength Change

**contra-mode** (hybrid - web-search + system-comparator delegated, reverse-engineer + synthesis inline):

- DELEGATED: Web-search for counter-examples (firecrawl_search or WebSearch)
- DELEGATED: system-comparator already ran in S1
- INLINE (main agent): Run reverse-engineer analysis yourself with the counter-examples as evidence
  - In contra-mode, web-search is MANDATORY. The point is finding who broke this limit.
  - For each barrier_type = assumed: search for cases where this limit was broken elsewhere
  - Present counter-examples as evidence for barrier reclassification

### S2.5: Cascade (contra-mode only, requires --cascade flag)

Only triggers if: (a) --cascade flag is set AND (b) web-search found counter-examples.

1. Full repo-mode scan on counter-example (system-comparator + adaptation-architect)
2. Full problem-mode adaptation pass (reverse-engineer + adaptation-architect)
3. No reason to limit depth - maximize quality
4. If web-search found nothing: skip cascade, continue normally

Without --cascade flag: contra-mode runs normally, counter-examples noted but not deep-analyzed.

### S3: Synthesis

Delegate to **solution-synthesizer-agent** (opus, max_turns: 12):

1. TASK: Aggregate all outputs, apply DSV gates, produce final synthesis
2. EXPECTED OUTCOME: Solution report following solution-template.md
3. REQUIRED TOOLS: Read
4. MUST DO:
   - Read `.claude/scenarios/quantum-lens/knowledge/barrier-taxonomy.md`
   - Read `.claude/scenarios/quantum-lens/agents/reverse-engineer-agent.md` (output schema)
   - Read `.claude/scenarios/quantum-lens/templates/solution-template.md`
   - DSV gate on every score (confidence bands, not point estimates)
   - Immutability cross-check on any reclassified barriers
   - Devil's Advocate on solutions with Success > 70%
5. MUST NOT DO: Point estimates. Rubber-stamp reclassifications. Skip DSV gate.
6. CONTEXT: All agent outputs: comparator `{s1}`, architect `{s2_architect}`, reverse-engineer `{s2_reverse}` (in problem/contra-mode: inline output following reverse-engineer-agent.md schema). Mode: `{mode}`. If cascade: cascade outputs `{s2.5}`.

### S4: Persist + Action

Based on synthesizer's Action Gate:
- **>= 70% usefulness**: Auto-generate implementation plan draft -> present for user approval
- **40-69%**: Save to `outputs/solutions/` + if Kairn available: `kn_learn` (type: solution-candidate, tags: [quantum-solve, {mode}, barrier-tracking])
- **< 40%**: Conversational only

Barrier tracking (always):
- If Kairn available: `kn_learn` (type: pattern, tags: [barrier:{lifecycle_stage}, {barrier_type}])
- If Kairn unavailable: save barrier log to `outputs/solutions/{date}-{title}.md`

Always: Present full report following `templates/solution-template.md`.

## FAILED Conditions

- **S0**: Can't determine mode and no --mode flag -> ask user
- **S1**: system-context/ files missing or empty -> switch to standalone mode (skip S1, proceed to S2 engineering)
- **S2**: reverse-engineer produces no barrier reclassifications -> flag for prompt review (may indicate all barriers are genuinely immutable, or prompt needs tuning)

## Output

Full solution report following `templates/solution-template.md`. All 7 sections (0-6) required.

## Examples

```
/quantum-solve https://github.com/letta-ai/letta
/quantum-solve "Context window fills too fast during multi-agent tasks"
/quantum-solve "contra: AI agents can't maintain state across sessions"
/quantum-solve "contra: you need a CS degree to build production AI" --cascade
/quantum-solve https://github.com/example/tool --mode repo --quick
```
