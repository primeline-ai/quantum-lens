# Anti-Convergence Rules

Prevent lenses from collapsing into agreement. Inspired by NeurIPS Multi-LLM Debate (2024) finding that same-model debate converges to shared misconceptions.

## The Problem

Sonnet agents follow instructions but tend toward consensus. "Be different" is not enough - structural constraints are required.

## Structural Anti-Convergence (not just prompting)

### 1. Cognitive Mode Isolation
Each lens has a computationally distinct cognitive mode. These are not "different expert opinions" - they are fundamentally different ways of processing information:
- Void Reader sees ABSENCE (negative space)
- Paradox Hunter sees CONTRADICTION (dialectical)
- Boundary Dissolver sees CONTINUITY (holistic)
- These modes cannot converge because they literally look at different aspects of the input.

### 2. Required Output Sections
Each lens MUST produce a unique required section:
- Void Reader: Absence Map
- Paradox Hunter: Impossibility Register
- Boundary Dissolver: Boundary Map- Temporal Archaeologist: Temporal Dig- Scale Shifter: Scale Map- Failure Romantic: Failure Love Letter
These sections force structurally different outputs even if the insights overlap.

### 3. Voice Marker Constraints
Hard constraints on language patterns:
- Void Reader starts insights with "Missing:", "Nowhere mentioned:"
- Paradox Hunter starts with "Impossible but true:", "The contradiction holds:"
- These are NOT suggestions. Violation = failed output.

### 4. Atom-Level Tracking
Each lens must reference specific atom IDs from the AoT decomposition. At least 1 insight per lens must reference a DIFFERENT primary atom than any insight from other lenses. Enforced by the intake processor generating unique atom IDs.

### 5. Naive Reading Contradiction Requirement
Each lens MUST contradict at least 2 claims from the naive reading. If a lens affirms the naive reading entirely, its output is considered failed.

## Detection Rules for Interference Reader

When the Interference Reader processes lens outputs:
- **Convergence = Suspicion**: If all lenses agree on a point, it might be a shared misconception rather than truth. Flag for verification.
- **Divergence = Signal**: Where lenses disagree is where the breakthroughs hide.
- **Unanimous agreement = Failure state**: If ALL lenses affirm the naive reading, the Interference Reader MUST generate a counter-perspective.

## When Convergence IS Valid

Convergence is a genuine signal when:
- Two cognitively distinct lenses (not similar modes) independently reach the same conclusion
- The convergence point is DIFFERENT from the naive reading
- The convergence is on a specific factual claim, not a vague directional agreement

## Escalation

If anti-convergence fails repeatedly (lenses produce nearly identical outputs):
1. First: check if input is genuinely unambiguous (rare but possible)
2. Second: increase structural constraints (add more required sections)
3. Third: upgrade lens agents to opus (more capable of genuine divergence)
4. Fourth: add a new lens with a maximally different cognitive mode