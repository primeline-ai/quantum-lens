# DSV Reference - Decompose, Suspend, Validate

A reasoning hygiene framework used as a scoring gate throughout Quantum Lens. Extracted from the [Universal Planning Framework](https://github.com/primeline-ai/universal-planning-framework) (MIT License, public repo).

---

## What is DSV

DSV (Decompose-Suspend-Validate) is a method for preventing overconfident reasoning. Most analysis frameworks rush from observation to conclusion. DSV inserts a deliberate pause - the Suspend phase - where you actively look for what you might be wrong about before committing to a score or recommendation.

In Quantum Lens, DSV serves as the quality gate for every numerical score. No score is assigned without first running through all three phases.

---

## The 3 Phases

### 1. Decompose
Break the claim, score, or recommendation into its 2-3 underlying assumptions. Make implicit bets explicit.

**Purpose**: You can't validate what you haven't named. Most overconfident scores come from bundled assumptions where one weak link hides inside a strong bundle.

**Example**: "This solution has 80% success probability" decomposes to:
- Assumption 1: The technical approach is feasible (verified via docs)
- Assumption 2: The team has capacity to implement (unverified)
- Assumption 3: No regulatory blockers exist (assumed, not checked)

### 2. Suspend
The critical phase most people skip. Actively ask: "Am I inflating this score because it's clever? Deflating because it's effort? What alternative interpretation haven't I considered?"

**Purpose**: Cognitive biases are invisible from inside. The Suspend phase forces you to step outside your current frame before committing. This is where the quantum metaphor applies - hold multiple interpretations in superposition before collapsing.

**Key questions**:
- Am I anchored to a number I heard/calculated first?
- Would I score this differently if I encountered it in a different context?
- What's the strongest argument AGAINST my current score?
- Is my confidence based on evidence or pattern-matching?

### 3. Validate
Take the weakest assumption identified in Decompose and verify it independently. If it can't be verified, cap the confidence level.

**Purpose**: One unverified assumption can invalidate an entire chain of reasoning. Validate catches the weakest link before it breaks under load.

**Verification rules**:
- Verified against actual files/data: full confidence allowed
- Most assumptions verified, 1-2 unverifiable: medium confidence (cap scores contextually)
- Multiple unverifiable assumptions: low confidence (cap scores at 60%)

---

## Quick DSV (30 seconds)

For everyday use when full DSV is overkill. Three questions, asked internally before any non-trivial judgment:

1. **What are the 2-3 key claims in this?** (Decompose)
2. **What alternative interpretation haven't I considered?** (Suspend)
3. **Which claim am I least sure about?** (Validate that first)

If question 2 reveals a plausible alternative: raise it before proceeding.

---

## Scoring Gate Usage in Quantum Lens

DSV is used as a mandatory gate in the Solution Engine:

### Where DSV applies
- **Solution Synthesizer**: Every usefulness score, every success probability, every barrier reclassification
- **Reverse Engineer**: Every barrier classification (is it really "assumed" or am I being optimistic?)
- **Interference Reader**: Breakthrough score assignments (is this really a 9, or am I impressed by novelty?)

### The DSV Gate pattern
```markdown
#### Score: {item being scored}
1. **Decompose**: What 2-3 assumptions underlie this score?
   - Assumption 1: {explicit}
   - Assumption 2: {explicit}
2. **Suspend**: Am I inflating because clever? Deflating because effort?
   - {honest self-check}
3. **Validate**: Weakest assumption - verified?
   - {verification result}
   - If unverified: score CAPPED at 60%
```

### Confidence bands (not point estimates)
DSV produces confidence bands, never point estimates:
- **High confidence**: All assumptions verified. Band: +/- 10%
- **Medium confidence**: Most verified, 1-2 unverifiable. Band: +/- 15%
- **Low confidence**: Multiple unverifiable. Band: +/- 25%, cap at 60%

---

*Source: Universal Planning Framework by PrimeLine (MIT License) - https://github.com/primeline-ai/universal-planning-framework*
