# Quantum Lens - Project Manifest & Setup

**Authors:** primeline-ai, JacobSal  
**License:** MIT  
**Python Version:** 3.8+  
**Package Manager:** uv  

---

## Project Overview

Quantum Lens is a radical multi-perspective deconstruction and solution engineering engine. It combines two powerful engines:

- **Perception Engine**: Decomposes input through 7 cognitively distinct analytical lenses in parallel, detects interference patterns, identifies cruxes, and generates a "Killer Question."
- **Solution Engine**: Engineers concrete solutions from insights, reverse-engineers from goals, eliminates barriers, and produces executable adaptation roadmaps with confidence-banded scoring.

## Quick Start

### Prerequisites
- Python 3.8+ with `uv` package manager
- Claude Code installed and configured
- Git (for repository access)

### Installation

```bash
# Clone the repository
git clone https://github.com/primeline-ai/quantum-lens.git
cd quantum-lens

# Install with uv
make install

# Or install development dependencies
make dev
```

### First Run

```bash
# After setting up Claude Code, run:
claude

# Then in Claude, use one of these commands:
/quantum-lens "concept: the attention economy" --depth quick
/quantum-solve "How can we reduce token cost?"
/quantum-full https://arxiv.org/abs/2502.12018
```

## Project Structure

```
quantum-lens/
├── agents/                 # Lens agent definitions (12 agents)
├── assets/                 # Static assets and resources
├── commands/               # CLI command definitions (5 quantum commands)
├── knowledge/              # Knowledge base and schemas
│   ├── anti-convergence-rules.md
│   ├── barrier-taxonomy.md
│   ├── lens-definitions.md
│   ├── scoring-rubric.md
│   └── solution-modes.md
├── scripts/                # Python utilities
│   ├── ql_persist.py       # Deterministic JSON-to-MD persistence
│   ├── ql_workspace.py     # Workspace resolution & seeding
│   └── test_ql_persist.py  # Test suite
├── schemas/                # JSON schemas for validation
│   ├── analysis_record.schema.json
│   └── solution_record.schema.json
├── outputs/                # (Generated) Analysis and solution outputs
├── templates/              # Output templates
├── system-context/         # Per-repo system documentation (optional)
├── CLAUDE.md               # Architecture overview
├── README.md               # Main documentation
└── SETUP.md                # Detailed setup guide
```

## Core Utilities

### `ql_persist.py`
Deterministic persistence layer for analysis and solution records.

**Features:**
- JSON schema validation (with jsonschema if available)
- Renders JSON to markdown deterministically
- Maintains per-repo workspace with outputs/index.json
- Generates Kairn payloads for knowledge persistence

**Usage:**
```bash
python scripts/ql_persist.py --plugin-root . --in record.json
```

### `ql_workspace.py`
Workspace resolution and seeding engine.

**Features:**
- Resolves per-repo workspace (via `$QUANTUM_LENS_HOME` or `.quantum-lens/`)
- Seeds system-context templates
- Manages lens configuration overlays
- Resolves agent paths

**Usage:**
```bash
python scripts/ql_workspace.py --plugin-root . --full
python scripts/ql_workspace.py --lenses --depth standard
```

### `test_ql_persist.py`
Comprehensive test suite (stdlib only, no external dependencies).

**Run tests:**
```bash
make test
# Or directly:
python scripts/test_ql_persist.py
```

## The 7 Perception Lenses

| Lens | Cognitive Mode | Purpose |
|------|-----------------|---------|
| **Void Reader** | Negative space cognition | Finds what's conspicuously absent |
| **Paradox Hunter** | Dialectical synthesis | Surfaces self-contradictions that are features |
| **Boundary Dissolver** | Holistic integration | Questions artificial category boundaries |
| **Temporal Archaeologist** | Dynamic systems thinking | Identifies frozen processes & arrested trajectories |
| **Scale Shifter** | Fractal/spatial reasoning | Reveals patterns at 100x and 0.01x scales |
| **Failure Romantic** | Inversion reasoning | Extracts information density from dead ends |
| **Interference Reader** | Cross-domain mapping | Detects patterns between patterns (meta-lens) |

## Depth Modes

- **quick** (2 lenses): Void Reader + Failure Romantic — for tweets and quick takes
- **standard** (4 lenses): + Paradox Hunter + Boundary Dissolver — default for articles and frameworks
- **deep** (6 lenses): all workers — for complex papers and paradigm-level ideas

## Solution Modes

| Mode | Trigger | Use Case |
|------|---------|----------|
| **repo** | URL present | "Can we use this? How do we adapt it?" |
| **problem** | Problem description | "How do we break through this limitation?" |
| **contra** | "contra:" prefix | "Why do we accept this limit?" |
| **cascade** | --cascade flag | Chains repo → problem → adaptation |

## Barrier Taxonomy

Every barrier is classified as one of:

- **assumed**: Nobody questioned it; no evidence of constraint (DEFAULT)
- **mutable**: Real constraint, but changeable via engineering
- **temporal**: Immutable today, mutable within known timeframe
- **immutable**: Fundamental constraint with HARD PROOF

## Output Format

### Perception Analysis (/quantum-lens)
1. Naive Reading
2. Atomic Decomposition
3. Quantum Insights (scored 1-10)
4. Interference Map
5. Killer Question
6. Tunneling Opportunities
7. Superposition View
8. Meta-Observations

### Solution Report (/quantum-solve)
0. Score Reasoning (DSV Gate)
1. System Scan
2. Solution Paths (confidence bands)
3. Reverse Path (goal → reality)
4. Adaptation Roadmap (quick wins → main track)
5. Open Problems
6. Executive Summary

## Workspace Setup

On first run, Quantum Lens creates a per-repo workspace at `.quantum-lens/`:

```
.quantum-lens/
├── outputs/
│   ├── analyses/          # Perception analysis records
│   ├── solutions/         # Solution records
│   └── index.json         # Join table for /quantum-review
├── system-context/
│   ├── SYSTEM-MAP.md      # Your component inventory
│   ├── architecture.md    # How components interact
│   └── project-goals.md   # Current priorities & blockers
└── scenario.json          # Lens config overlay (from /lens-calibrate)
```

**Recommendation:** Add `.quantum-lens/` to your `.gitignore` — these are local runtime artifacts.

## Configuration

### Custom Lenses

Customize lenses with `/lens-calibrate`:
- Enable/disable specific lenses
- Add custom lenses
- Adjust depth defaults
- Changes stored in `.quantum-lens/scenario.json`

### System Context (Optional, Recommended)

For better Solution Engine results, fill in `.quantum-lens/system-context/`:

1. **SYSTEM-MAP.md**: List components, locations, purposes
2. **architecture.md**: Describe how components interact
3. **project-goals.md**: Current goals, blockers, priorities

Without these, the Solution Engine operates in "general analysis mode" — reverse-engineering and barrier analysis still work, but system-specific adaptation is skipped.

## Development

### Code Standards

- **Python 3.8+ compatible** (type hints optional for backward compatibility)
- **Stdlib only** for core utilities (jsonschema is optional for validation)
- **No external dependencies** required for core functionality
- **Schema-validated**: All records validated against JSON schemas

### Testing

```bash
make test
# With verbose output:
python scripts/test_ql_persist.py -v
```

### Building & Packaging

```bash
make clean     # Remove artifacts
make lint      # Check code quality
make fmt       # Format (when configured)
```

## Integration with Claude Code

Quantum Lens runs as a **Claude Code scenario**. To use it:

1. Install this repository in your project (clone, symlink, or submodule)
2. Run `claude` in your project directory
3. Use commands:
   - `/quantum-lens <input>` — Perception analysis
   - `/quantum-solve <input>` — Solution engineering
   - `/quantum-full <input>` — Complete pipeline
   - `/lens-calibrate` — Customize lenses
   - `/quantum-review` — Review past analyses

## Optional Enhancements

### Firecrawl MCP (Web Integration)
Enable URL scraping, repo structure mapping, and web search for contra-mode:

```bash
pip install firecrawl
# Configure MCP server per Firecrawl docs
```

### Kairn (Persistent Knowledge)
Store insights cross-analysis and track effectiveness:

```bash
pip install kairn-ai
kairn init ~/brain
kairn serve ~/brain
# Add to .claude/mcp.json per Kairn setup guide
```

## Scoring & Evaluation

### Breakthrough Score (Perception)
1-3: Conventional reframing  
4-6: Non-obvious connection  
7-8: Genuine breakthrough (auto-saved)  
9-10: Paradigm-level (extended analysis)

### Usefulness Score (Solution)
Confidence bands, not point estimates (e.g., "60-85%, medium confidence")  
Action Gate: ≥70% auto-generates implementation draft, 40-69% saved, <40% conversational

## Troubleshooting

### "Workspace not found"
Ensure `.quantum-lens/` is created via `/quantum-init` or by running any command.

### "Schema validation failed"
Check `jsonschema` is installed: `pip install jsonschema`  
Fallback validation (no external deps) also available.

### Lenses not loading
Verify `.quantum-lens/scenario.json` exists (created by `/lens-calibrate`)  
Check `agents/` directory has all 12 agent files.

## Research Inspirations

- PRISM Framework
- Quantum Abduction (Pareschi)
- Atoms of Thought (Teng)
- Structure-Mapping Theory (Gentner)
- Multi-LLM Debate (NeurIPS 2024)
- Adversarial Collaboration (FRI 2024)
- Team of Rivals
- Superpositional Belief

See `knowledge/inspirations/index.md` for full source registry.

## Support & Contributing

- **Issues:** Report via GitHub issues
- **Documentation:** See [README.md](README.md), [CLAUDE.md](CLAUDE.md), [SETUP.md](SETUP.md)
- **Knowledge Base:** See `knowledge/` directory

## License

MIT License © 2026 quantum-lens contributors

See [LICENSE](LICENSE) for full terms.
