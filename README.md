# Quantum Lens

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0-green.svg)](main)
[![Works with Claude Code](https://img.shields.io/badge/works%20with-Claude%20Code-orange.svg)](main)

**Analysis that sees what you don't.** 7 cognitive lenses run in parallel, each with a structurally distinct way of perceiving your input. Where they agree - high confidence. Where they clash - breakthrough candidates. Where conventional tools give you one perspective, Quantum Lens gives you seven that can't converge even if they tried.

> "Ran /quantum-lens on our pricing strategy doc. The Void Reader found we never
> mentioned churn. The Failure Romantic found our 'competitive advantage' is actually
> a dependency. The Killer Question collapsed 3 weeks of debate into one testable claim."

## Quick Install

```bash
git clone https://github.com/primeline-ai/quantum-lens
cp -R quantum-lens/.claude/scenarios/quantum-lens your-project/.claude/scenarios/quantum-lens
```

Then in your project:
```bash
claude
# /quantum-lens "AI will replace knowledge workers by 2030"
# /quantum-solve https://github.com/example/framework
# /quantum-full concept: the attention economy --depth deep
```

## What Makes This Different

**Two engines, not one.** Perception Engine deconstructs. Solution Engine rebuilds. `/quantum-full` chains both - wild perception filtered through hard engineering constraints. The space between observation and action is where breakthroughs happen.

**Structural anti-convergence.** LLM agents prompted to "disagree" converge anyway (NeurIPS 2024). Quantum Lens enforces divergence through architecture: each lens has a computationally distinct cognitive mode, unique required output sections, and hard voice constraints. Convergence = suspicion, not confidence.

**DSV-gated scoring.** Every score passes through Decompose-Suspend-Validate. No point estimates - confidence bands with stated weakest assumptions. Score says 80%? You see exactly which assumption could make it 40%.

**Barrier taxonomy with teeth.** Every limitation gets classified: assumed (nobody questioned it), mutable (real but changeable), temporal (immutable today, not tomorrow), immutable (hard proof). Default is "assumed" - reverse the burden of proof.

**3 tiers, zero lock-in.** Works with just Claude Code. Add Firecrawl for URL scraping. Add Kairn for persistent memory. Each tier adds capabilities but nothing breaks without it.

## 5-Minute Quick Start

### 1. Analyze something

```bash
/quantum-lens "The attention economy is a myth"
/quantum-lens https://arxiv.org/abs/2502.12018 --depth deep
```

7 lenses decompose the input into atoms, each lens perceives it through a structurally different cognitive mode, interference patterns are detected, cruxes identified, and a Killer Question formulated.

### 2. Solve something

```bash
/quantum-solve "Context window fills too fast during multi-agent tasks"
/quantum-solve https://github.com/example/tool --mode repo
/quantum-solve "contra: you need a CS degree to build production AI" --cascade
```

Three modes: evaluate a repo (repo), break through a limitation (problem), challenge accepted status quo (contra). Contra-mode with `--cascade` finds who already broke the limit, then runs full analysis on their approach.

### 3. Full pipeline

```bash
/quantum-full "AI agents will replace 80% of knowledge workers" --depth deep --solve-mode contra
```

Perception (all 7 lenses) -> Smart Filter -> Solution Engine -> Combined Report. One input, two engines, one actionable output.

## The 7 Cognitive Lenses

| Lens | What It Sees | Cognitive Mode |
|------|-------------|---------------|
| **Void Reader** | What's absent - missing concepts, unstated premises | Negative space cognition |
| **Paradox Hunter** | Self-contradictions that are features, not bugs | Dialectical synthesis |
| **Boundary Dissolver** | Artificial category boundaries | Holistic integration |
| **Temporal Archaeologist** | Frozen processes, arrested trajectories | Dynamic systems thinking |
| **Scale Shifter** | Same pattern at radically different scales | Fractal/spatial reasoning |
| **Failure Romantic** | Information density in dead ends | Inversion reasoning |
| **Interference Reader** | Patterns between patterns (meta) | Cross-domain structural mapping |

Not personas. Not "different expert opinions." Computationally distinct cognitive strategies modeled on neurodiverse processing styles (autistic systemizing, ADHD divergent linking, dyslexic spatial reasoning).

## Commands

| Command | What It Does |
|---------|-------------|
| `/quantum-lens <input>` | Multi-perspective perception analysis (8-section report) |
| `/quantum-solve <input>` | Solution engineering (7-section report) |
| `/quantum-full <input>` | Complete pipeline: perception + solution |
| `/quantum-review` | Review past analyses, track lens effectiveness, surface recurring cruxes |
| `/lens-calibrate` | Customize lenses, adjust depth defaults, add custom lenses |

### Depth Modes (Perception)

| Mode | Lenses | Best For |
|------|--------|---------|
| `quick` | 2 (Void Reader + Failure Romantic) | Tweets, quick takes, time pressure |
| `standard` | 4 (+ Paradox Hunter + Boundary Dissolver) | Articles, frameworks (default) |
| `deep` | 6 (all workers) | Complex papers, paradigm-level ideas |

### Solution Modes

| Mode | Trigger | Question |
|------|---------|----------|
| `repo` | URL present | "Can we use this? How do we adapt it?" |
| `problem` | Problem description | "How do we break through this limitation?" |
| `contra` | "contra:" prefix | "Why do we accept this limit? Who already broke it?" |

## 3 Tiers

| Tier | What You Need | What You Get |
|------|--------------|--------------|
| **Core** | Claude Code only | Full perception engine, solution engine in general analysis mode |
| **Web-enhanced** | + Firecrawl MCP | URL scraping, repo analysis, web search for counter-examples |
| **Full** | + Kairn MCP | Persistent insight storage, cross-analysis patterns, effectiveness tracking |

All tiers work out of the box. See [SETUP.md](SETUP.md) for installation details per tier.

## System Context (Optional)

For the Solution Engine to map insights against YOUR system, fill in the template files in `system-context/`:

- `SYSTEM-MAP.md` - Your component inventory
- `architecture.md` - How components connect
- `project-goals.md` - Current goals and blockers

Without these: perception works fully, solution engine operates in general analysis mode.
With these: system-specific adaptation roadmaps with file paths.

## How It Works

### Perception Pipeline
```
INPUT -> Intake (AoT decomposition) -> Parallel Lenses -> Interference Detection -> Synthesis
```

### Solution Pipeline
```
INPUT -> Mode Detection -> System Scan -> Engineering (reverse-engineer + adapt) -> DSV Synthesis
```

### Combined (/quantum-full)
```
INPUT -> Perception (all phases) -> Smart Filter -> Solution Engine -> Combined Report
```

## Scoring

### Breakthrough Score (Perception)
- 1-3: Conventional reframing
- 4-6: Non-obvious connection
- 7-8: Genuine breakthrough (auto-saved)
- 9-10: Paradigm-level (extended analysis saved)

### Solution Scoring
- Confidence bands, not point estimates (e.g., "60-85%, medium confidence")
- Every score passes a DSV gate (Decompose-Suspend-Validate)
- Action Gate: >= 70% triggers implementation plan draft

## Research Foundations

Built on peer-reviewed research, not vibes:

| Source | What We Took |
|--------|-------------|
| PRISM Framework (Diamond 2025) | Cognitive modes grounded in neuroscience |
| Multi-LLM Debate (NeurIPS 2024) | Anti-convergence rules (same-model debate converges to shared misconceptions) |
| Quantum Abduction (Pareschi 2025) | Synthesis before pruning - let contradictions interfere |
| Atoms of Thought (Teng 2025) | AoT decomposition with Markov property |
| Structure-Mapping (Gentner 1986+) | Cross-lens isomorphism detection |
| Adversarial Collaboration (FRI 2024) | CRUX identification from structured disagreement |
| Superpositional Belief (2026) | Deferred commitment - ambiguity as structured output |

Full source registry: `.claude/scenarios/quantum-lens/knowledge/inspirations/index.md`

## The Ecosystem

Quantum Lens is part of a progression. Each tier works independently - no hard dependencies.

```
You're here          You want this            Install this
-----------          -------------            ------------
Raw Claude Code  ->  Session memory       ->  Starter System (free)
                 ->  Workflow skills      ->  + Skills Bundle (free)
                 ->  Deep planning        ->  + UPF (free)
                 ->  Deep analysis        ->  + Quantum Lens (free) <- you are here
                 ->  AI-powered system    ->  + Course (paid)
```

| Component | What It Does | Link |
|-----------|-------------|------|
| **Starter System** | Session memory, handoffs, context awareness | [GitHub](https://github.com/primeline-ai/claude-code-starter-system) |
| **Skills Bundle** | 5 workflow skills: debugging, delegation, planning, code review, config architecture | [GitHub](https://github.com/primeline-ai/primeline-skills) |
| **UPF** | Universal Planning Framework with deep multi-stage planning | [GitHub](https://github.com/primeline-ai/universal-planning-framework) |
| **Quantum Lens** | Multi-perspective analysis + solution engineering | You're reading it |
| **Course** | Kairn + Synapse: AI-powered memory and knowledge graphs | [primeline.cc](https://primeline.cc) |

### How They Work Together

Quantum Lens references ecosystem components with "if available" language:

- **DSV scoring gates** use the methodology from UPF (included as `knowledge/dsv-reference.md`)
- **Kairn persistence** provides cross-analysis patterns via `/quantum-review` (falls back to local files)
- **Solution Engine** action gate can trigger plan creation (works with any planning tool, enhanced with UPF)

If nothing else is installed, Quantum Lens works perfectly on its own.

## License

MIT - see [LICENSE](LICENSE).

---

**Built by [@PrimeLineAI](https://x.com/PrimeLineAI) - Perception reveals structure. Engineering turns structure into action.**
