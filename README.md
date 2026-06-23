# Quantum Lens

Radical multi-perspective deconstruction + solution engineering engine for Claude Code.

**Perception Engine** runs any input through cognitively distinct analytical lenses in parallel,
detects interference patterns, identifies cruxes, and formulates a Killer Question. **Solution
Engine** turns insights into concrete, confidence-banded adaptation roadmaps — maps against your
system, reverse-engineers from goals, eliminates barriers.

**This is not brainstorming.** Perception reveals hidden structure; solution engineering turns it
into action.

## Quick Start

```
# Perception
/quantum-lens "concept: the attention economy"
/quantum-lens https://arxiv.org/abs/2502.12018 --depth deep

# Solution
/quantum-solve "Context window fills too fast during multi-agent tasks"
/quantum-solve https://github.com/example/framework
/quantum-solve "contra: AI agents can't maintain state across sessions" --cascade

# Full pipeline (perception × solution)
/quantum-full "AI will replace knowledge workers" --depth deep --solve-mode contra
```

First use auto-creates a per-repo workspace at `.quantum-lens/` (or run `/quantum-init`). Every run
writes a record there regardless of score. Add `.quantum-lens/` to your `.gitignore`.

## Commands

| Command | Purpose |
|---------|---------|
| `/quantum-init` | Create/seed the `.quantum-lens/` workspace (`--full` localizes lens agents) |
| `/quantum-lens` | Perception analysis (8-section report) |
| `/quantum-solve` | Solution engineering (7-section report) |
| `/quantum-full` | Complete perception → solution pipeline |
| `/lens-calibrate` | Enable/disable/add lenses (per-repo overlay) |
| `/quantum-review` | Review past analyses, recurring cruxes, lens effectiveness |

## The 7 Lenses

Void Reader (what's absent) · Paradox Hunter (productive contradictions) · Boundary Dissolver
(artificial categories) · Temporal Archaeologist (frozen processes) · Scale Shifter (cross-scale
patterns) · Failure Romantic (dead-end signal) · Interference Reader (patterns between patterns,
meta). Depth modes select 2 / 4 / 6 of them. Full catalog, instruments, and solution modes:
**[PMAT_README.md](PMAT_README.md)**.

## When to Use What

| Situation | Command |
|-----------|---------|
| Deep analysis of external content | `/quantum-lens` |
| Evaluate a repo for your system | `/quantum-solve <url>` |
| Break through a limitation | `/quantum-solve "problem..."` |
| Challenge an accepted status quo | `/quantum-solve "contra: ..."` |
| Full perception-to-solution pipeline | `/quantum-full` |

## Documentation

- **[PMAT_README.md](PMAT_README.md)** — comprehensive manifest: lenses, modes, scoring, workspace,
  development, troubleshooting
- **[SETUP.md](SETUP.md)** — install + optional MCP integrations (Firecrawl, Kairn)
- **[CLAUDE.md](CLAUDE.md)** — architecture & operating rules (two-roots model, persistence, config)
- `knowledge/persistence.md` — the persistence + config-overlay contract

## Research Inspirations

PRISM Framework, Quantum Abduction (Pareschi), Atoms of Thought (Teng), Structure-Mapping (Gentner),
Multi-LLM Debate (NeurIPS 2024), Adversarial Collaboration (FRI 2024), Team of Rivals, Superpositional
Belief. Full registry: `knowledge/inspirations/index.md`.

MIT License.
