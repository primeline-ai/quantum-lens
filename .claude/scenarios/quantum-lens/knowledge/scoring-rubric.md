# Breakthrough Scoring Rubric

Calibrated scoring system for Quantum Lens insights. Each insight receives a 1-10 score based on distance from conventional thinking.

## Score Tiers

### 1-3: Conventional Reframing
The insight exists in mainstream discourse. A well-read person in the domain would nod and say "yes, obviously."

**Characteristics**:
- Restates known trade-offs in different words
- Points out well-documented limitations
- Offers standard contrarian takes (the kind you'd find in top HN comments)

**Calibration Examples**:
- "AI will create new jobs while eliminating others" (score 2 - every article says this)
- "Move fast and break things has downsides" (score 2 - standard critique)
- "Open source has sustainability challenges" (score 3 - known but worth stating)

### 4-6: Non-Obvious Connection
Requires domain expertise to see. A specialist would say "huh, I hadn't connected those two things."

**Characteristics**:
- Cross-domain analogy that illuminates
- Second-order consequence that isn't discussed
- Reframing that changes which questions feel important

**Calibration Examples**:
- "SaaS pricing models create the same principal-agent problem as real estate commissions" (score 5)
- "The attention economy's scarcity is manufactured, not discovered - like diamonds" (score 6)
- "AI agent reliability is inversely proportional to value - perfectly reliable agent = script" (score 6)

### 7-8: Genuine Breakthrough
Changes how you think about the input. You can't unsee it. A domain expert would pause and reconsider their mental model.

**Characteristics**:
- Reveals a structural pattern hidden by conventional framing
- Identifies a crux that nobody is testing
- Makes a specific, verifiable prediction that contradicts consensus

**Calibration Examples**:
- "The PDF parsing industry is maintained by the same companies that could eliminate it" (score 8 - structural revelation)
- "AI multiplier applies symmetrically to teams and solos - solo wins ONLY if coordination cost grows faster than the multiplier" (score 7 - reframes the entire debate)
- "Knowledge work category is incoherent - the definition automates a strawman" (score 8 - collapses the premise)

### 9-10: Paradigm-Level
Challenges fundamental assumptions of the field. A domain leader would need to seriously reconsider their strategy.

**Characteristics**:
- Reveals the question itself is wrong
- Identifies a self-reinforcing dynamic that makes the problem unsolvable within current framing
- Shows that the "solution" IS the problem

**Calibration Examples**:
- "Agent platforms inevitably converge into SaaS products - the SaaS model is immortal, only its tenants rotate" (score 9 - collapses the agent-replaces-SaaS thesis)
- "Taste emerges from friction - removing the team removes the creative abrasion that produces taste" (score 9 - inverts the solo-dev thesis)
- "Every solution to the attention economy captures what it claims to liberate" (score 10 - recursive impossibility)

## Scoring Rules

1. **Score the INSIGHT, not the delivery**. Well-written conventional takes are still score 2.
2. **Specificity raises score**. "AI has risks" (2) vs "Hybrid PDF parsers relocate hallucination rather than eliminating it because VLMs still process the hard cases" (7).
3. **Testability raises score**. Unfalsifiable insights cap at 6. Specific, verifiable claims can reach 9-10.
4. **Anti-convergence bonus**: If only ONE lens could have produced this insight (due to its unique cognitive mode), add +1.
5. **Never score higher than 7 without a specific atom reference**.
6. **Score 10 reserved for insights that make the problem disappear** - not solve it, dissolve it.

## Overall Score Calculation

Overall Breakthrough Score = average of top 3 insight scores.

## Persistence Thresholds

| Overall Score | Action |
|--------------|--------|
| < 7 | Conversational only - no auto-save |
| >= 7 | Auto-save to Kairn via `kn_learn`. If Kairn unavailable: save to `outputs/analyses/` |
| >= 9 | Also save extended analysis to `outputs/analyses/` |
