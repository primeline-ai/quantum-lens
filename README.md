# Quantum Lens

Radical multi-perspective deconstruction + solution engineering engine.

## Two Engines, One Scenario

**Perception Engine** (Quantum Lens) takes any input and runs it through cognitively distinct analytical lenses in parallel. Each lens sees the input through a fundamentally different perceptual geometry. The system detects interference patterns, identifies cruxes, and formulates a Killer Question.

**Solution Engine** takes insights (from QL or standalone) and engineers concrete solutions. It maps against your system, reverse-engineers from goals, eliminates barriers, and produces executable adaptation roadmaps.

**This is not brainstorming.** Perception reveals hidden structure. Solution engineering turns structure into action.

## Quick Start

```
# Perception only
/quantum-lens https://example.com/article
/quantum-lens "concept: the attention economy"

# Solution only
/quantum-solve "Context window fills too fast during multi-agent tasks"
/quantum-solve https://github.com/example/framework
/quantum-solve "contra: AI agents can't maintain state across sessions" --cascade

# Full pipeline (perception + solution)
/quantum-full https://arxiv.org/abs/2502.12018
/quantum-full "AI will replace knowledge workers" --depth deep --solve-mode contra
```

## The 7 Cognitive Lenses (Perception)

| Lens | What It Sees | Quantum Instrument |
|------|-------------|-------------------|
| **Void Reader** | What's ABSENT - missing concepts, unstated premises | Superposition of Absence |
| **Paradox Hunter** | Self-contradictions that are features, not bugs | Cascading Flips |
| **Boundary Dissolver** | Artificial category boundaries | Superposition |
| **Temporal Archaeologist** | Frozen processes, arrested trajectories | Cascading Flips |
| **Scale Shifter** | Same pattern at radically different scales | Linked Pairs |
| **Failure Romantic** | Information density in dead ends | Tunneling |
| **Interference Reader** | Patterns between patterns (meta) | Collapse Trigger |

## Solution Engine Agents

| Agent | What It Does | Model |
|-------|-------------|-------|
| **Reverse Engineer** | Works backward from goals, challenges every barrier | opus |
| **System Comparator** | Maps external input against your system | sonnet |
| **Adaptation Architect** | Designs executable adaptation paths | sonnet |
| **Solution Synthesizer** | DSV-gated scoring + devil's advocate | opus |

## Solution Modes

| Mode | Trigger | Example |
|------|---------|---------|
| **repo** | URL present | `/quantum-solve https://github.com/example/tool` |
| **problem** | Problem description | `/quantum-solve "How can we reduce token cost?"` |
| **contra** | "contra:" prefix | `/quantum-solve "contra: you need a CS degree"` |
| **cascade** | --cascade flag + contra | Contra finds counter-example -> repo scan -> problem adaptation |

## Barrier Taxonomy

Every barrier gets classified into one of 4 types:

| Type | Meaning | Default? |
|------|---------|----------|
| **assumed** | Nobody questioned it. No evidence of constraint. | YES (default) |
| **mutable** | Real constraint, but changeable via engineering | |
| **temporal** | Immutable today, mutable within known timeframe | |
| **immutable** | Fundamental constraint with HARD PROOF | |

The reverse-engineer principle: every barrier is `assumed` until evidence proves otherwise.

## Depth Modes (Perception)

| Mode | Lenses | Best For |
|------|--------|---------|
| quick | 2 (Void Reader + Failure Romantic) | Tweets, quick takes, time pressure |
| standard | 4 (+ Paradox Hunter + Boundary Dissolver) | Articles, frameworks, most content |
| deep | 6 (all workers) | Complex papers, paradigm-level ideas |

## Output Formats

### Perception (/quantum-lens)
1. Naive Reading
2. Atomic Decomposition
3. Quantum Insights (scored 1-10)
4. Interference Map
5. Killer Question
6. Tunneling Opportunities (with barrier types)
7. Superposition View
8. Meta-Observations

### Solution (/quantum-solve)
0. Score Reasoning (DSV Gate)
1. System Scan (overlap/gap/collision maps)
2. Solution Paths (confidence bands, devil's advocate)
3. Reverse Path (goal -> reality, barrier elimination)
4. Adaptation Roadmap (quick wins, main track, deal breakers)
5. Open Problems
6. Executive Summary

## Architecture

### Perception Pipeline
- **Phase 0**: Intake + AoT decomposition (sonnet)
- **Phase 1**: Parallel lens analysis (sonnet agents)
- **Phase 2**: Interference detection + crux identification (opus)
- **Phase 3**: Convergence + scoring + persistence

### Solution Pipeline
- **S0**: Intake + mode detection
- **S1**: System scan (sonnet)
- **S2**: Engineering - hybrid delegation (opus inline + sonnet delegated)
- **S3**: DSV synthesis + devil's advocate (opus)
- **S4**: Persist + action gate

## When to Use What

| Situation | Command |
|-----------|---------|
| Deep analysis of external content | `/quantum-lens` |
| Evaluate a repo for your system | `/quantum-solve <url>` |
| Break through a limitation | `/quantum-solve "problem..."` |
| Challenge accepted status quo | `/quantum-solve "contra: ..."` |
| Full perception-to-solution pipeline | `/quantum-full` |
| Quick reaction to an idea | Your preferred brainstorming tool |
| Validate reasoning quality | DSV (inline - see `knowledge/dsv-reference.md`) |
| Design/build something | Your preferred ideation tool |
| Plan a project | Your preferred planning tool |

## Scoring

### Perception (Breakthrough Score)
- 1-3: Conventional reframing
- 4-6: Non-obvious connection
- 7-8: Genuine breakthrough (auto-saves to Kairn)
- 9-10: Paradigm-level (extended analysis saved to outputs/analyses/)

### Solution (Usefulness + Success)
- Confidence bands, not point estimates (e.g., "60-85%, medium confidence")
- Action Gate: >= 70% auto-generates implementation plan draft, 40-69% saves to outputs/, < 40% conversational

## Research Inspirations

Built on: PRISM Framework, Quantum Abduction (Pareschi), Atoms of Thought (Teng), Structure-Mapping (Gentner), Multi-LLM Debate (NeurIPS 2024), Adversarial Collaboration (FRI 2024), Team of Rivals, Superpositional Belief.

See `knowledge/inspirations/index.md` for full source registry.
