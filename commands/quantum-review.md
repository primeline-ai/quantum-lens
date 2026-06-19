---
keywords: [quantum, review, past, analyses, history, lens, effectiveness, patterns]
description: "Review past Quantum Lens analyses - find patterns, track lens effectiveness, surface recurring cruxes"
argument: "[--list | --domain DOMAIN | --lens LENS | --effectiveness | --cruxes]"
model: sonnet
---

# /quantum-review

Review past Quantum Lens analyses and surface cross-run patterns.

## Arguments

- `--list` (default): List all saved analyses with scores, domains, and dates
- `--domain DOMAIN`: Filter analyses by domain (e.g., "AI/ML", "business", "philosophy")
- `--lens LENS`: Show all insights from a specific lens across runs
- `--effectiveness`: Lens effectiveness report - which lenses produce highest-scoring insights
- `--cruxes`: Surface recurring cruxes and unresolved Killer Questions across analyses

## Workflow

### --list

1. If Kairn available: `kn_query` with tags: ["quantum-lens"]. If Kairn unavailable: scan `outputs/analyses/` and `outputs/solutions/` directories for past reports.
2. Display table:

```
| # | Date | Input | Domain | Score | Lenses | Kairn Node |
|---|------|-------|--------|-------|--------|------------|
```

### --effectiveness

1. Query all quantum-lens tagged Kairn entries
2. Parse which lenses contributed to highest-scoring insights
3. Calculate per-lens hit rate (% of runs where lens produced score >= 7 insight)
4. Display:

```
Lens Effectiveness Report (N runs)

| Lens | Runs | Insights >= 7 | Hit Rate | Best Domain |
|------|------|--------------|----------|-------------|
```

5. Flag underperforming lenses (hit rate < 30%) for potential recalibration
6. Flag overperforming lenses (hit rate > 80%) as core strengths

### --cruxes

1. Query all quantum-lens entries
2. Extract CRUX statements from each analysis
3. Group by theme/domain
4. Identify RECURRING cruxes (same factual question appearing across multiple analyses)
5. Display:

```
Recurring Cruxes (appeared in 2+ analyses)

| CRUX | Appearances | Domains | Status |
|------|-------------|---------|--------|
| {factual question} | {count} | {domains} | unresolved/resolved |
```

6. Flag cruxes that could be verified NOW (suggest concrete research actions)

### --domain / --lens

Filter and display relevant subset of the full analysis history.

## Output

Formatted tables and analysis summaries. For --effectiveness, include recommendations for lens recalibration if hit rates suggest issues.

## Examples

```
/quantum-review
/quantum-review --effectiveness
/quantum-review --cruxes
/quantum-review --domain "AI/ML"
/quantum-review --lens void-reader
```
