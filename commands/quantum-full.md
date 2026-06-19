---
keywords: [quantum-full, full quantum, complete analysis, mega, perception-to-solution, full analysis]
description: "Complete perception-to-solution pipeline: Quantum Lens deconstruction + Solution Engine engineering"
argument: "<input> [--depth quick|standard|deep] [--solve-mode repo|problem|contra]"
model: opus
---

# /quantum-full

The mega workflow. Perception (Quantum Lens) + Engineering (Solution Engine) in one pipeline.

QL = observation (wave function, all possibilities). SE = collapse (measurement, forcing concrete reality). This command is not QL + SE. It's QL x SE - the space between wild perception and hard system reality is where breakthroughs happen.

## Arguments

- `input` (required): URL, text, concept, or problem
- `--depth quick|standard|deep`: Depth for QL phase (default: auto-detect)
- `--solve-mode repo|problem|contra`: Force SE mode (overrides auto-detection)

## Workflow

### Step 1: Quantum Lens (Perception)

Run `/quantum-lens` with input + depth.

Execute Phases 0-4 of the QL workflow:
- Phase 0: Intake + Atomization
- Phase 1: Diverge (parallel lens analysis)
- Phase 2: Interfere (meta-analysis)
- Phase 3: Converge (synthesis - sections 1-8)
- Phase 4: Persist (based on Breakthrough Score)

Capture: All insights with Breakthrough Scores, all Tunneling Opportunities with barrier_type annotations.

### Step 2: Smart Filter for SE Handoff

Filter QL insights for Solution Engine relevance:

| Insight Score | Rule |
|--------------|------|
| >= 7 | ALWAYS forward to SE |
| 5-6 | Forward if barrier_type = `assumed` or `temporal` |
| 3-4 | Quick keyword-match against `system-context/SYSTEM-MAP.md` (if available). >= 3 keyword matches: forward. Else: skip |
| 1-2 | Skip |

**If nothing passes filter**: "Perception found no actionable insights for your system." Offer to proceed with SE anyway (user choice).

### Step 3: Auto-Detect SE Mode

If no `--solve-mode` flag:
- Any `assumed` barriers in filtered insights -> contra (challenge the assumptions - takes priority)
- URL input without assumed barriers -> repo
- Else -> problem

`--solve-mode` override always wins.

### Step 4: Solution Engine

Feed filtered insights + barrier_type annotations into `/quantum-solve`:
- Pass all filtered insights as context
- Preserve barrier_type annotations from QL worker lenses
- SE mode from Step 3 or --solve-mode override

### Step 5: Combined Report

Present unified report:

```markdown
# Quantum Full Analysis: {input_title}
**Date**: {date} | **QL Depth**: {depth} | **SE Mode**: {mode}

## Part I: Perception (Quantum Lens)
{Sections 1-8 from QL analysis}

## Part II: Engineering (Solution Engine)
{Sections 0-6 from SE report}

## Combined Metrics
- **Breakthrough Score**: {QL overall score}
- **Usefulness**: {SE confidence band}
- **Success Probability**: {SE confidence band}
- **Barriers**: {N identified by QL, M forwarded to SE, K reclassified, J with solutions}
```

### Step 6: Combined Persistence

**Note**: QL Phase 4 already handles QL-specific persistence (Kairn save at score >= 7, extended analysis at >= 9). Step 6 handles SE-specific persistence ONLY. Do not re-trigger QL saves.

SE Action Gate applies independently:
- >= 70% usefulness: Auto-generate implementation plan draft
- 40-69%: Save to outputs/solutions/
- < 40%: Conversational only

## FAILED Conditions

- QL Phase fails: Stop, report QL error. Do not proceed to SE.
- Smart filter passes nothing AND user declines to proceed: Stop after QL report.
- SE fails: Present QL report alone with note "Solution Engine encountered an error: {reason}"

## Output

Combined report with both QL (8 sections) and SE (7 sections) analyses.

## Examples

```
/quantum-full https://arxiv.org/abs/2502.12018
/quantum-full "AI agents will replace 80% of knowledge workers" --depth deep
/quantum-full concept: the attention economy --solve-mode contra
/quantum-full https://github.com/example/framework --depth standard --solve-mode repo
```
