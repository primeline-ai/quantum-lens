# Quantum Lens

Radical multi-perspective deconstruction + solution engineering engine for Claude Code.

**Authors:** primeline-ai, JacobSal · **License:** MIT · **Python:** 3.8+ · **Package manager:** uv

**Perception Engine** runs any input through 7 cognitively distinct analytical lenses in parallel
with structurally enforced anti-convergence, detects interference patterns, identifies cruxes, and
formulates a "Killer Question." **Solution Engine** turns insights into concrete, confidence-banded
adaptation roadmaps — maps against your system, reverse-engineers from goals, eliminates barriers.

**This is not brainstorming.** Perception reveals hidden structure; solution engineering turns it
into action. QL = observation (the wave function, all possibilities); SE = collapse (measurement,
forcing concrete reality). `/quantum-full` is QL × SE, not QL + SE.

> Architecture & operating rules: **[CLAUDE.md](CLAUDE.md)**. Install + MCP integrations:
> **[SETUP.md](SETUP.md)**. Persistence + config contract: `knowledge/persistence.md`.

---

## Quick Start

```
# Perception
/quantum-lens "concept: the attention economy" --depth quick
/quantum-lens https://arxiv.org/abs/2502.12018 --depth deep

# Solution
/quantum-solve "How can we reduce token cost?"
/quantum-solve https://github.com/example/framework
/quantum-solve "contra: AI agents can't maintain state across sessions" --cascade

# Full pipeline (perception × solution)
/quantum-full https://arxiv.org/abs/2502.12018
/quantum-full "AI will replace knowledge workers" --depth deep --solve-mode contra
```

First use auto-creates a per-repo workspace at `.quantum-lens/` (or run `/quantum-init`). Every run
writes a record there regardless of score. Add `.quantum-lens/` to your `.gitignore`.

## Installation

```bash
git clone https://github.com/primeline-ai/quantum-lens
cd quantum-lens
make install          # uv-based; see `make help` for all targets
```

Then enable it as a Claude Code plugin in your project (clone, symlink, or submodule) and run
`claude`. Full instructions + optional MCP integrations: **[SETUP.md](SETUP.md)**.

## Commands

| Command | Purpose |
|---------|---------|
| `/quantum-init` | Create/seed the `.quantum-lens/` workspace (`--full` localizes lens agents) |
| `/quantum-lens <input>` | Perception analysis (8-section report) |
| `/quantum-solve <input>` | Solution engineering (7-section report) |
| `/quantum-full <input>` | Complete perception → solution pipeline |
| `/lens-calibrate` | Enable/disable/add lenses (writes the per-repo overlay, never the plugin) |
| `/quantum-review` | Review past analyses, recurring cruxes, lens effectiveness (reads `index.json`) |

## Project Structure

```
quantum-lens/
├── agents/                 # Lens + SE agent definitions (12 agents)
├── assets/                 # Static assets
├── commands/               # Slash-command definitions (6 quantum commands)
├── knowledge/              # Framework, rules, schemas, persistence.md contract
│   ├── anti-convergence-rules.md
│   ├── barrier-taxonomy.md
│   ├── lens-definitions.md
│   ├── persistence.md      # Persistence + config-overlay contract
│   ├── scoring-rubric.md
│   └── solution-modes.md
├── scripts/                # Python utilities (deterministic IO)
│   ├── ql_persist.py       # JSON-to-MD persistence + index
│   ├── ql_workspace.py     # Workspace resolution, seeding, lens config
│   └── test_ql_persist.py  # Test suite (stdlib only)
├── schemas/                # JSON schemas for record validation
│   ├── analysis_record.schema.json
│   └── solution_record.schema.json
├── templates/              # Output shapes (rendered from JSON by ql_persist.py)
├── system-context/         # Seed templates copied into each host repo's workspace
├── CLAUDE.md               # Architecture & operating guide
├── README.md               # This file — ground-truth documentation
├── SETUP.md                # Install + MCP integrations
└── Makefile                # install / dev / lint / test / clean / run
```

## Core Utilities

The LLM emits one schema-validated JSON record; Python does all IO. This avoids the path/coherence
drift of free-form markdown writes. Full contract: `knowledge/persistence.md`.

### `ql_persist.py`
Deterministic persistence for analysis/solution records: JSON schema validation (via `jsonschema`
if available, else a stdlib fallback), deterministic JSON→markdown rendering, per-repo
`outputs/index.json` upsert, and a Kairn `kn_learn` payload.
```bash
echo '<record-json>' | python scripts/ql_persist.py --plugin-root . --in record.json
```

### `ql_workspace.py`
Workspace resolution + seeding + lens-config resolution: resolves `$QUANTUM_LENS_HOME` or
`.quantum-lens/`, seeds `system-context` templates and the lens-config overlay, resolves the
effective lens set and agent paths (workspace-first, plugin-fallback).
```bash
python scripts/ql_workspace.py --plugin-root . --full
python scripts/ql_workspace.py --lenses --depth standard
python scripts/ql_workspace.py --resolve-agent void-reader --plugin-root .
```

### `test_ql_persist.py`
Comprehensive test suite (stdlib only, no external deps).
```bash
make test          # or: python scripts/test_ql_persist.py
```

## The 7 Perception Lenses

| Lens | Cognitive Mode | What It Sees | Instrument |
|------|----------------|--------------|------------|
| **Void Reader** | Negative space cognition | What's conspicuously absent — missing concepts, unstated premises | Superposition of Absence |
| **Paradox Hunter** | Dialectical synthesis | Self-contradictions that are features, not bugs | Cascading Flips |
| **Boundary Dissolver** | Holistic integration | Artificial category boundaries | Superposition |
| **Temporal Archaeologist** | Dynamic systems thinking | Frozen processes, arrested trajectories | Cascading Flips |
| **Scale Shifter** | Fractal/spatial reasoning | The same pattern at 100x and 0.01x | Linked Pairs |
| **Failure Romantic** | Inversion reasoning | Information density in dead ends | Tunneling |
| **Interference Reader** | Cross-domain mapping | Patterns between patterns; cruxes, isomorphisms, the Killer Question (meta) | Collapse Trigger |

### Depth Modes

- **quick** (2 lenses): Void Reader + Failure Romantic — tweets, quick takes
- **standard** (4 lenses): + Paradox Hunter + Boundary Dissolver — default, for articles & frameworks
- **deep** (6 lenses): all workers — complex papers, paradigm-level ideas

Lens selection is resolved deterministically by `ql_workspace.py` (canonical defaults) with deltas
from the per-repo overlay — see [Configuration](#configuration).

## Solution Engine Agents

| Agent | Role | Model |
|-------|------|-------|
| **Reverse Engineer** | Works backward from goals, challenges every barrier, finds wavelength changes | opus |
| **System Comparator** | Maps external input against your system (overlap/gap/collision) | sonnet |
| **Adaptation Architect** | Designs executable adaptation paths with rollback | sonnet |
| **Solution Synthesizer** | Meta-agent: DSV-gated scoring, devil's advocate, final synthesis | opus |

Orchestrating commands + Interference Reader + Solution Synthesizer use **opus**; other agents
default to **sonnet**.

### Solution Modes

| Mode | Trigger | Use Case |
|------|---------|----------|
| **repo** | URL present | "Can we use this? How do we adapt it?" |
| **problem** | Problem description | "How do we break through this limitation?" |
| **contra** | "contra:" prefix | "Why do we accept this limit?" |
| **cascade** | `--cascade` flag + contra | Chains repo → problem → adaptation on a counter-example |

## Barrier Taxonomy

Every barrier is classified as one of four types. The reverse-engineer principle: every barrier is
`assumed` until evidence proves otherwise.

| Type | Meaning | Default? |
|------|---------|----------|
| **assumed** | Nobody questioned it; no evidence of constraint | YES |
| **mutable** | Real constraint, but changeable via engineering | |
| **temporal** | Immutable today, mutable within a known timeframe | |
| **immutable** | Fundamental constraint with HARD PROOF | |

## Output Format

### Perception Analysis (`/quantum-lens`)
1. Naive Reading
2. Atomic Decomposition
3. Quantum Insights (scored 1-10)
4. Interference Map
5. Killer Question
6. Tunneling Opportunities (with barrier types)
7. Superposition View
8. Meta-Observations

### Solution Report (`/quantum-solve`)
0. Score Reasoning (DSV Gate)
1. System Scan (overlap/gap/collision maps)
2. Solution Paths (confidence bands, devil's advocate)
3. Reverse Path (goal → reality, barrier elimination)
4. Adaptation Roadmap (quick wins → main track → deal breakers)
5. Open Problems
6. Executive Summary

## When to Use What

| Situation | Command |
|-----------|---------|
| Deep analysis of external content | `/quantum-lens` |
| Evaluate a repo for your system | `/quantum-solve <url>` |
| Break through a limitation | `/quantum-solve "problem..."` |
| Challenge an accepted status quo | `/quantum-solve "contra: ..."` |
| Full perception-to-solution pipeline | `/quantum-full` |
| Validate reasoning quality | DSV (inline — see `knowledge/dsv-reference.md`) |

## Workspace & Persistence

The shared plugin install dir (`${CLAUDE_PLUGIN_ROOT}`) is **read-only**; all writable state lives
in a per-repo workspace (`$QUANTUM_LENS_HOME` or `.quantum-lens/`):

```
.quantum-lens/
├── outputs/
│   ├── analyses/{record_id}.{json,md}   # Perception records (json = source of truth)
│   ├── solutions/{record_id}.{json,md}  # Solution records
│   └── index.json                        # Join table for /quantum-review
├── system-context/
│   ├── SYSTEM-MAP.md      # Your component inventory
│   ├── architecture.md    # How components interact
│   └── project-goals.md   # Current priorities & blockers
├── scenario.json          # Lens-config overlay (from /lens-calibrate)
└── agents/                # Custom lens bodies (built-ins stay in the plugin)
```

A record is written for **every** run (the file is the guaranteed floor); the JSON is the source of
truth and the `.md` is rendered deterministically. Add `.quantum-lens/` to your `.gitignore`.

## Configuration

### Custom Lenses
`/lens-calibrate` edits the per-repo overlay (`.quantum-lens/scenario.json`) — never the read-only
plugin: enable/disable lenses, add custom lenses (bodies written to `.quantum-lens/agents/`), adjust
the default depth. The canonical depth→lens map lives in `ql_workspace.py`; the overlay applies
deltas. Verify with `python scripts/ql_workspace.py --lenses --depth deep`.

### System Context (Optional, Recommended)
On first `/quantum-solve` (or `/quantum-init`) the 3 templates are seeded into
`.quantum-lens/system-context/`. Fill them in for system-aware adaptation:

1. **SYSTEM-MAP.md** — components, locations, purposes
2. **architecture.md** — how components interact
3. **project-goals.md** — goals, blockers, priorities

Until customized, the Solution Engine runs in "general analysis mode" — reverse-engineering and
barrier analysis still work, but system-specific adaptation is skipped.

## Scoring & Evaluation

Every run writes a record to the workspace regardless of score (the file is the guaranteed floor).
The score only decides *additional* actions on top of that file.

### Breakthrough Score (Perception)
1-3: Conventional reframing · 4-6: Non-obvious connection · 7-8: Genuine breakthrough (file + Kairn
`kn_learn` when available) · 9-10: Paradigm-level (also marked `extended`).

### Usefulness Score (Solution)
Confidence bands, not point estimates (e.g., "60-85%, medium confidence"). Action Gate on top of the
always-written file: ≥70% auto-generates an implementation draft, 40-69% also `kn_learn` when Kairn
is available, <40% file only.

## Development

```bash
make help      # list targets
make install   # install deps (uv)
make dev       # + lint/test tooling
make test      # run the suite
make lint      # compile-check the scripts
make clean     # remove artifacts and caches
```

**Code standards:** Python 3.8+ compatible; stdlib only for core utilities (`jsonschema` optional);
no external deps required for core functionality; all records schema-validated.

## Integration with Claude Code

Quantum Lens runs as a Claude Code plugin. Install it in your project (clone, symlink, or submodule),
run `claude`, and use the [commands](#commands) above. The per-repo `.quantum-lens/` workspace is
created automatically on first use (or via `/quantum-init`).

## Optional Enhancements

- **Firecrawl MCP** — URL scraping, repo-structure mapping, web search for contra-mode. Without it,
  URL inputs fall back to `WebFetch` or manual paste.
- **Kairn** — persistent cross-analysis insight storage + effectiveness tracking via
  `/quantum-review`. Files are always written; Kairn is an enhancement.

Setup for both: **[SETUP.md](SETUP.md)**.

## Troubleshooting

- **"Workspace not found"** — run `/quantum-init` (any command also auto-creates `.quantum-lens/`);
  override the location with `$QUANTUM_LENS_HOME`.
- **"Schema validation failed"** — `ql_persist.py` prints the offending field. `jsonschema` gives
  full validation (`pip install jsonschema`); a stdlib fallback runs otherwise.
- **A disabled lens still runs / lenses not loading** — check the resolver:
  `python scripts/ql_workspace.py --lenses --depth deep`. Selection comes from
  `.quantum-lens/scenario.json` over the canonical defaults; built-in agents resolve from the plugin,
  custom/edited ones from `.quantum-lens/agents/`.

## Documentation

- **[CLAUDE.md](CLAUDE.md)** — architecture & operating rules (two-roots model, persistence, config)
- **[SETUP.md](SETUP.md)** — install + optional MCP integrations
- `knowledge/persistence.md` — persistence + config-overlay contract
- `knowledge/` — framework, lens definitions, scoring rubric, barrier taxonomy, solution modes

## Research Inspirations

PRISM Framework · Quantum Abduction (Pareschi) · Atoms of Thought (Teng) · Structure-Mapping Theory
(Gentner) · Multi-LLM Debate (NeurIPS 2024) · Adversarial Collaboration (FRI 2024) · Team of Rivals ·
Superpositional Belief. Full registry: `knowledge/inspirations/index.md`.

## Support & Contributing

- **Issues:** report via GitHub issues
- **Knowledge base:** see the `knowledge/` directory

## License

MIT License © 2026 quantum-lens contributors. See [LICENSE](LICENSE) for full terms.
