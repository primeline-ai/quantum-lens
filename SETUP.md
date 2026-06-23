# Setup Guide

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/build-with-claude/claude-code) installed and working
- **Python 3.8+** on PATH (`python` or `python3`) — used by the deterministic persistence helper
  (`scripts/ql_persist.py`). Standard library only; `jsonschema` is used for full record validation
  if installed, otherwise a built-in check runs. No MCP required.
- A project where you want to use Quantum Lens

## Tier 1: Core (No MCPs Required)

Copy the scenario directory into your project:

```bash
git clone https://github.com/primeline-ai/quantum-lens
cp -R quantum-lens/.claude/scenarios/quantum-lens your-project/.claude/scenarios/quantum-lens
```

Or use a symlink (stays updated with pulls):
```bash
ln -s /path/to/quantum-lens/.claude/scenarios/quantum-lens your-project/.claude/scenarios/quantum-lens
```

Or add as a git submodule (version-pinned):
```bash
cd your-project
git submodule add https://github.com/primeline-ai/quantum-lens.git vendor/quantum-lens
ln -s vendor/quantum-lens/.claude/scenarios/quantum-lens .claude/scenarios/quantum-lens
```

That's it. Run `claude` in your project and use `/quantum-lens`, `/quantum-solve`, or `/quantum-full`.

## Tier 2: Web-Enhanced (+ Firecrawl)

Firecrawl enables URL scraping, repo structure mapping, and web search for counter-examples in contra-mode.

Install the Firecrawl MCP server following their docs. Without Firecrawl, URL inputs fall back to `WebFetch` (built into Claude Code) or manual paste.

## Tier 3: Full (+ Kairn)

Kairn provides persistent insight storage, cross-analysis pattern detection, and effectiveness tracking via `/quantum-review`.

### Install Kairn

```bash
pip install kairn-ai
kairn init ~/brain
kairn serve ~/brain
```

### Configure MCP

Add to your Claude Code MCP config (`.claude/mcp.json` or equivalent):

```json
{
  "mcpServers": {
    "kairn": {
      "command": "kairn",
      "args": ["serve", "~/brain"]
    }
  }
}
```

For Claude Desktop or Cursor, see the [Kairn setup guide](https://github.com/kairn-ai/kairn).

### Key Kairn Tools Used

| Tool | Purpose |
|------|---------|
| `kn_learn` | Save high-scoring insights, barrier classifications, solution candidates |
| `kn_recall` | Retrieve relevant past insights during new analyses |
| `kn_query` | Search past analyses by tags, domain, or date |

Every run **always** writes a structured record to the per-repo workspace (see Persistence below).
Kairn is an *enhancement* on top of that: high-scoring analyses and solution candidates are also
saved via `kn_learn` and bidirectionally linked back to the file record. Without Kairn you lose
cross-analysis recall, not your outputs.

## Persistence & Workspace

Quantum Lens never writes into its (shared, read-only) install dir. All outputs and system-context
live in a **per-repo workspace**, resolved as:

1. `$QUANTUM_LENS_HOME` (explicit override), else
2. `<your-project>/.quantum-lens/` (created on first run)

```
<your-project>/.quantum-lens/
  outputs/index.json                       # join table: one entry per run
  outputs/analyses/{record_id}.json|.md    # /quantum-lens
  outputs/solutions/{record_id}.json|.md   # /quantum-solve
  system-context/{SYSTEM-MAP,architecture,project-goals}.md
  scenario.json                            # lens-config overlay (/lens-calibrate writes here)
  agents/{custom-lens}-agent.md            # custom lenses (built-ins stay in the plugin)
```

The LLM emits a schema-validated JSON record; `scripts/ql_persist.py` writes the canonical JSON,
renders the markdown view deterministically, and updates `index.json`. Full contract:
`knowledge/persistence.md`. **Add `.quantum-lens/` to your host project's `.gitignore`** (these are
local run artifacts).

The workspace is created automatically on first use, or explicitly with **`/quantum-init`**
(`/quantum-init --full` also copies the built-in lens agents locally for editing). `/lens-calibrate`
reads/writes the per-repo lens-config overlay (`.quantum-lens/scenario.json`) — enabling/disabling
or adding lenses never touches the read-only plugin install.

## System Context (Optional, Recommended for Solution Engine)

On first `/quantum-solve` run the 3 template files are **auto-seeded** into
`<your-project>/.quantum-lens/system-context/`. Fill them in to help the Solution Engine understand
your system:

1. **`SYSTEM-MAP.md`** - List your components, their locations, and purposes
2. **`architecture.md`** - Describe how components connect and interact
3. **`project-goals.md`** - Current goals, blockers, and priorities

While they remain stub/empty, the Solution Engine operates in "general analysis mode" -
reverse-engineering and barrier analysis still work, but system-specific adaptation roadmaps are skipped.

## Model Notes

- **Opus recommended**: The Interference Reader and Solution Synthesizer agents are designed for opus-level reasoning. They work with sonnet but with reduced synthesis quality.
- **Sonnet works**: All other agents (6 perception lenses, intake processor, system comparator, adaptation architect) run on sonnet by default.
- The orchestrating commands (`/quantum-lens`, `/quantum-solve`, `/quantum-full`) use opus.

## Output Directories

Quantum Lens writes all output to the per-repo workspace (`.quantum-lens/` or `$QUANTUM_LENS_HOME`):
- `outputs/analyses/{record_id}.{json,md}` - perception analyses (written for **every** run)
- `outputs/solutions/{record_id}.{json,md}` - solution reports incl. classified barriers (every run)
- `outputs/index.json` - the join table used by `/quantum-review`

The JSON is the source of truth; the `.md` is a deterministic rendering. Add `.quantum-lens/` to
your host project's `.gitignore`. (The plugin's own `outputs/.gitkeep` placeholders are unused at
runtime — kept only so the repo tree is legible.)

## Verification

After setup, verify by running:
```bash
claude
# Then type:
/quantum-lens "concept: the attention economy" --depth quick
```

You should see a 2-lens quick analysis with all 8 template sections.
