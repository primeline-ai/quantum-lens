# Solution Engine Modes

Three modes for the Solution Engine. Each addresses a different question.

## Mode Detection (Auto)

```
URL present (GitHub, GitLab, etc.)  →  repo-mode
"contra:" prefix                     →  contra-mode
--mode override                      →  always wins
else                                 →  problem-mode
```

---

## repo-mode: Evaluate External Repos

**Question**: "Can we use this? How do we adapt it?"

**Trigger**: URL present (GitHub, GitLab, etc.)

**2-Phase Approach**:

### Phase 1: Quick Scan
- `firecrawl_map` for repo structure
- `firecrawl_scrape` README + top docs (markdown, onlyMainContent)
- Multi-Signal Relevance Score (1-10):
  - README/docs quality (0-3): Clear purpose, examples, architecture docs
  - Code structure relevance (0-3): Patterns/approaches applicable to your domain
  - Gap density (0-2): How many useful things we lack that this provides
  - Activity/maintenance level (0-2): Recent commits, responsive maintainer, release cadence

### Phase 2: Deep Dive (only if Relevance >= 4)
- Clone repo or deeper firecrawl scraping of key files
- Code-level pattern extraction
- Second system-comparator pass with deeper context

**STOP GATE**: Relevance < 4 after Phase 1 - "Not relevant enough for deep analysis." Stop.

**Output**: Adaptation roadmap with specific files, effort estimates, risks.

**Example**:
```
/quantum-solve https://github.com/example/cool-framework
/quantum-solve https://github.com/example/agent-lib --mode repo
```

---

## problem-mode: Solve Internal Limitations

**Question**: "How do we break through this limitation?"

**Trigger**: Problem description, "how can we", "limitation", anything without URL or "contra:" prefix.

**Approach**:
1. Define problem + constraints from user input
2. Map against system (system-comparator reads system-context/ files if available)
3. Reverse-engineer from desired outcome (what must be true for the problem to not exist?)
4. Generate solution paths with adaptation roadmap

**Note**: "improve X" = problem-mode where the problem is "X is not good enough."

**Output**: Solution paths + reverse path + adaptation roadmap.

**Examples**:
```
/quantum-solve "Context window fills too fast during complex multi-agent tasks"
/quantum-solve "How can we make delegation decisions faster?"
/quantum-solve "Our knowledge graph queries are too slow" --mode problem
```

---

## contra-mode: Break Through Accepted Status Quo

**Question**: "Why do we accept this limit? Can we break it?"

**Trigger**: "contra:" prefix, "everyone accepts", "why can't we", "what if we could"

**Approach**:
1. Identify the accepted limit (the "everyone knows X is impossible")
2. Web-search for counter-examples (who has broken this limit elsewhere?)
3. Challenge every assumption - classify each barrier (assumed/mutable/temporal/immutable)
4. Reverse-engineer from the goal (work backward from "limit doesn't exist")

**Cascade** (opt-in via `--cascade` flag):
When contra-mode finds a counter-example AND `--cascade` is set:
1. Trigger repo-mode scan on the counter-example (if it's a repo/tool)
2. Trigger problem-mode adaptation pass (how to adapt the approach)
3. Result: One input, three perspectives, one unified solution

Without `--cascade`: contra-mode runs normally, counter-examples are noted but not deep-analyzed.

**Cascade Fallback**: If web-search finds no counter-examples, skip cascade. Continue contra-mode normally. The limit might actually be real.

**Output**: Barrier elimination map + wavelength change.

**Examples**:
```
/quantum-solve "contra: AI agents can't maintain coherent state across sessions"
/quantum-solve "contra: you need a CS degree to build production AI systems" --cascade
/quantum-solve "Why does everyone accept that context windows are the bottleneck?"
```

---

## Mode Interaction with /quantum-full

When called from `/quantum-full` (after Quantum Lens perception):
- QL insights are parsed, filtered by smart handoff rules
- barrier_type annotations from QL worker lenses are preserved
- Mode auto-detected: URL input = repo, any `assumed` barriers = contra, else = problem
- `--solve-mode` override always wins
