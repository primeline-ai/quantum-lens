# Setup Guide

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/build-with-claude/claude-code) installed and working
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

Without Kairn, all persistence falls back to local files in `outputs/analyses/` and `outputs/solutions/`.

## System Context (Optional, Recommended for Solution Engine)

Fill in the template files in `system-context/` to help the Solution Engine understand your system:

1. **`system-context/SYSTEM-MAP.md`** - List your components, their locations, and purposes
2. **`system-context/architecture.md`** - Describe how components connect and interact
3. **`system-context/project-goals.md`** - Current goals, blockers, and priorities

Without these files, the Solution Engine operates in "general analysis mode" - reverse-engineering and barrier analysis still work, but system-specific adaptation roadmaps are skipped.

## Model Notes

- **Opus recommended**: The Interference Reader and Solution Synthesizer agents are designed for opus-level reasoning. They work with sonnet but with reduced synthesis quality.
- **Sonnet works**: All other agents (6 perception lenses, intake processor, system comparator, adaptation architect) run on sonnet by default.
- The orchestrating commands (`/quantum-lens`, `/quantum-solve`, `/quantum-full`) use opus.

## Output Directories

Quantum Lens creates output files in:
- `outputs/analyses/` - Saved perception analyses (score >= 7, or >= 9 for extended)
- `outputs/solutions/` - Saved solution reports and barrier logs

These directories are gitignored by default (only `.gitkeep` files are tracked).

## Verification

After setup, verify by running:
```bash
claude
# Then type:
/quantum-lens "concept: the attention economy" --depth quick
```

You should see a 2-lens quick analysis with all 8 template sections.
