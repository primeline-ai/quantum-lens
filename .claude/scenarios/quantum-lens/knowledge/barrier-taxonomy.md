# Barrier Taxonomy

4-type classification system for barriers encountered during Quantum Lens perception and Solution Engine engineering.

## The Principle

> Every barrier is `assumed` until evidence proves otherwise. Deliberate bias toward action.

---

## The 4 Types

### assumed (DEFAULT)

The limit exists because nobody questioned it. No evidence of actual constraint.

**Test**: "Has anyone actually verified this?"

**Examples**:
- "We always use X for Y" (never tested alternatives)
- "That's too expensive" (never calculated the actual cost)
- "The API doesn't support that" (never checked the docs)
- "Users won't accept that" (never asked them)
- "That approach doesn't scale" (never benchmarked it)

**Action**: Challenge it. Search for counter-examples. What happens if we just try?

**Classification rule**: This is the DEFAULT. If you can't prove it's mutable, temporal, or immutable, it's assumed.

### mutable

Constraint exists but conditions are changeable via engineering effort.

**Test**: "Can I change this by modifying code, config, or architecture?"

**Examples**:
- Caching strategy (can be changed)
- Provider choice (can switch providers)
- File structure (can be reorganized)
- API rate limits (can upgrade plan or implement batching)
- Database schema (can migrate)

**Action**: What specifically changes the condition? Estimate cost/effort of the change.

**Classification rule**: Requires evidence that the constraint IS real but IS changeable. Without evidence of the constraint's existence, it's `assumed`.

### temporal

Immutable today, but likely mutable within a known timeframe.

**Test**: "Is there a known timeline for this changing?"

**Examples**:
- "Model X can't do Y" (but next release adds it, announced for Q3)
- "API doesn't support Z" (but Z is in beta, shipping next month)
- "Tool doesn't exist for this" (but 3 teams are building it, ETA 6 weeks)
- "Regulation prevents X" (but new framework takes effect Jan 1)

**Action**: Set monitoring trigger. Design the solution AS IF the barrier doesn't exist. Build everything except the blocked piece. When the timeline arrives, plug it in.

**Classification rule**: Requires a KNOWN timeline (not "someday"). Must point to a specific event, release, or date.

### immutable

Fundamental constraint with HARD PROOF. Cannot be changed by any engineering effort.

**Test**: "Is this imposed by external reality that no engineering can change?"

**Examples**:
- Model context window hard limit (physics of current architecture)
- Speed of light / network latency floor
- Mathematical impossibility (proven, not just assumed)
- Legal requirement with no workaround
- Third-party API that genuinely has no alternative

**Action**: Accept. Design around it. What's the nearest achievable goal that respects this constraint?

**Classification rule**: Requires HARD PROOF. Not "it seems impossible" but "here is the specific constraint and evidence it cannot be changed." The burden of proof is on immutability.

---

## Classification Procedure

```
1. Start: assume `assumed` (default)
2. Evidence check: Does evidence exist that the constraint is real?
   - No evidence  → stays `assumed`
   - Evidence exists → continue to step 3
3. Changeability: Can engineering effort change it?
   - Yes → `mutable`
   - Not today, but known timeline → `temporal`
   - No, with hard proof → `immutable`
   - Unclear → stays `assumed` (benefit of the doubt toward action)
```

---

## Barrier Lifecycle

Track each barrier through its lifecycle. If Kairn available: use Kairn tags. If Kairn unavailable: log barrier stages in `outputs/solutions/` with tags as YAML frontmatter.

```
identified → classified → reclassified (if evidence changes) → solution-proposed → implemented → verified
```

| Stage | Tag | Meaning |
|-------|-----|---------|
| identified | `barrier:identified` | Barrier recognized during analysis |
| classified | `barrier:classified` | Type assigned (assumed/mutable/temporal/immutable) |
| reclassified | `barrier:reclassified` | Type changed based on new evidence |
| solution-proposed | `barrier:solution-proposed` | Solution path exists for this barrier |
| implemented | `barrier:implemented` | Solution has been built |
| verified | `barrier:verified` | Solution confirmed working |

**Success KPI**: Barriers Eliminated = count of barriers reaching `verified` status.

---

## The Reverse-Engineer Principle

The reverse-engineer agent treats EVERY barrier as `assumed` until it personally verifies evidence to the contrary. This is deliberate:

- Never: "Unfortunately this is impossible"
- Always: "Classified as X because [evidence]. If [condition changes], barrier dissolves."
- Never accept a barrier without: "Says who? Based on what evidence? When was this last tested?"

This bias toward action means some barriers will be incorrectly classified as softer than they are. That's acceptable. The cost of trying and failing is lower than the cost of never trying because you assumed something was impossible.

---

## Immutability Cross-Check

When the reverse-engineer reclassifies a barrier from `immutable` to `assumed`:
- The solution-synthesizer MUST independently verify: "What evidence supports this reclassification?"
- No evidence found = barrier stays `immutable` in the final report
- This prevents overly optimistic reclassification from cascading into unrealistic solutions
