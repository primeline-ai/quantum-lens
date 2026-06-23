# Solution Engine Report: {input_title}
**Date**: {date} | **Mode**: {repo|problem|contra|cascade} | **Source**: {URL or description}
**From QL**: {yes/no} | **Cascade**: {yes/no - contra triggered repo+problem}

---

## 0. Score Reasoning (DSV Gate)

{DSV gate results for each scored item. Required when confidence is not high. May be collapsed to inline footnotes in high-confidence cases.}

For each score:
1. **Decompose**: What 2-3 assumptions underlie this score?
2. **Suspend**: Inflating because clever? Deflating because effort?
3. **Validate**: Weakest assumption verified against system files?

---

## 1. System Scan

### Overlap Map
| External Concept | Our Equivalent | Match Quality | Location |
|---|---|---|---|
| {concept} | {our component} | exact / partial / conceptual | {file path} |

### Gap Map
| External Concept | What We Lack | Impact if Added | Effort |
|---|---|---|---|
| {concept} | {missing capability} | {impact} | S / M / L / XL |

### Collision Map
| External Approach | Our Approach | Conflict Type | Resolution Direction |
|---|---|---|---|
| {their way} | {our way} | philosophical / architectural / implementation | {direction} |

---

## 2. Solution Paths

| # | Solution | Usefulness | Success | Effort | Priority |
|---|----------|-----------|---------|--------|----------|
| {N} | {title} | {low-high}% | {low-high}% | S/M/L/XL | {priority score} |

(Confidence bands, not point estimates. Each with weakest assumption.)

### Solution Path {N}: {title}
- **Problem/Gap addressed**: {specific limitation or gap}
- **Approach**: {concrete steps with file paths}
- **Files affected**: {specific paths}
- **Risk + rollback**: {what could go wrong, how to undo}
- **Validation method**: {how to verify it works}
- **Devil's Advocate**: "This fails when..." {plausible failure scenario}

---

## 3. Reverse Path

### Goal Statement
{Desired end state, 1-2 sentences}

### Reverse Path Table
| Step (N to 1) | What Must Be True | Current Reality | Gap | Barrier Type |
|---|---|---|---|---|
| {step} | {condition} | {current state} | {delta} | {assumed/mutable/temporal/immutable} |

### Barrier Elimination

#### Barrier: {name}
- **Classification**: {type} | **Evidence**: {supporting evidence}
- **Challenge**: {Says who? Based on what? When last tested?}
- **Elimination path**: {concrete steps}

### Wavelength Change
{Single biggest frame-shift eliminating most barriers simultaneously}

### Residual Barriers
{Genuinely immutable constraints only. If none: "No residual barriers."}

---

## 4. Adaptation Roadmap

### Quick Wins
#### QW{N}: {title}
- **Files**: {paths} | **Effort**: S
- **Steps**: 1. ... 2. ... 3. ...
- **Rollback**: {how to undo}
- **Validation**: {how to verify}

### Main Track
#### MT{N}: {title}
- **Files**: {paths} | **Effort**: M/L | **Risk**: low/med/high
- **Dependencies**: {prereqs}
- **Steps**: 1. ... 2. ... 3. ... 4. ... 5. ...
- **Rollback**: {undo strategy}
- **Validation**: {verification method}

### Deal Breakers
#### DB{N}: {title}
- **Why**: {risk/effort concern}
- **What would need to change**: {conditions for feasibility}
- **Alternative**: {80% approach}
- **Rollback if attempted**: {safety net}

---

## 5. Open Problems

### Open Problem {N}: {title}
- **Why it matters**: {impact on system}
- **Probability of solution**: {band}%
- **Exploration direction**: {where to look}

---

## 6. Executive Summary

{3-5 paragraphs, standalone readable. Plain language. Clear recommendation.}

{DSV uncertainties + devil's advocate findings noted.}

{If cascade: summary of all 3 mode results and how they reinforced/contradicted each other.}

---

**Usefulness**: {low-high}% ({confidence} confidence, weakest assumption: {X})
**Success Probability**: {low-high}% ({confidence} confidence, weakest assumption: {Y})
**Action Gate**: {auto-plan | note | conversational}
**Barriers**: {N identified, M reclassified, K with solutions}
**Persistence**: {Kairn saved | Experience created | Conversational only}
