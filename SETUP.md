# Setup Guide

Concise install guide. For the full manifest (workspace, persistence, config, troubleshooting) see
**[README.md](README.md)** and `knowledge/persistence.md`. Build/test targets live in the
**[Makefile](Makefile)** (`make help`).

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/build-with-claude/claude-code) installed
- **Python 3.8+** on PATH (`python` or `python3`) — runs the deterministic persistence/config
  helpers (`scripts/*.py`). Stdlib only; `jsonschema` is used for full validation if present,
  otherwise a built-in check runs. No MCP required.

## Install

```bash
git clone https://github.com/primeline-ai/quantum-lens
cd quantum-lens
make install          # or: make dev  (adds lint/test tooling); make help for all targets
```

Use it in a project as a Claude Code plugin via any of:

```bash
# symlink (stays current with pulls)
ln -s /path/to/quantum-lens your-project/.claude/plugins/quantum-lens

# or git submodule (version-pinned)
cd your-project
git submodule add https://github.com/primeline-ai/quantum-lens.git vendor/quantum-lens
ln -s ../vendor/quantum-lens .claude/plugins/quantum-lens
```

Then run `claude` in your project. The per-repo `.quantum-lens/` workspace is created automatically
on first use (or run `/quantum-init`); add it to your `.gitignore`.

## Optional: MCP integrations

Quantum Lens works fully without MCPs. Two enhance it:

**Firecrawl** — URL scraping, repo-structure mapping, web search for contra-mode. Install the
Firecrawl MCP per their docs. Without it, URL inputs fall back to `WebFetch` or manual paste.

**Kairn** — persistent cross-analysis insight storage + effectiveness tracking via `/quantum-review`.
Files are always written either way; Kairn is an enhancement (high-scoring records are also saved via
`kn_learn` and linked back). Install:

```bash
pip install kairn-ai && kairn init ~/brain && kairn serve ~/brain
```

Add to your Claude Code MCP config (`.claude/mcp.json` or equivalent):

```json
{ "mcpServers": { "kairn": { "command": "kairn", "args": ["serve", "~/brain"] } } }
```

| Kairn tool | Used for |
|------------|----------|
| `kn_learn` | Save high-scoring insights, barrier classifications, solution candidates |
| `kn_recall` | Retrieve relevant past insights during new analyses |
| `kn_query` | Search past analyses by tags, domain, or date |

## Verify

```bash
make test                                   # Python helper suite (stdlib only)

claude
# then, in Claude:
/quantum-lens "concept: the attention economy" --depth quick
```

You should get a 2-lens quick analysis with all 8 sections, and a record written to
`.quantum-lens/outputs/analyses/`.
