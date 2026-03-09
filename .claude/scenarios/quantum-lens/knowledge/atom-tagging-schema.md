# Atom Tagging Schema

Semantic tags for Atoms of Thought (AoT) decomposition. Inspired by Atom-Searcher (Deng 2025) and adapted for Quantum Lens interference detection.

## Tags

### [claim]
Factual assertion that can be verified.
- Example: "PDFs were never designed to be machine-readable"
- Test: Can you check if this is true? If yes, it's a claim.
- Interference value: Claims can be directly contradicted by lenses.

### [assumption]
Unstated premise the input relies on. May or may not be stated explicitly - the key is that the argument depends on it.
- Example: "Tagged PDF is effectively useless for most real-world documents"
- Test: If this were false, would the argument still hold? If no, it's an assumption.
- Interference value: HIGH. Assumptions are the highest-value targets for lenses because they're load-bearing but unexamined.

### [prediction]
Forward-looking statement about what will or might happen.
- Example: "PDFs are not going anywhere"
- Test: Does this make a claim about the future? If yes, it's a prediction.
- Interference value: Predictions can be tested against cascading flip analysis and temporal archaeology.

### [observation]
Direct description without inference. Reports what IS without claiming what it MEANS.
- Example: "Document parsing evolved from pipeline-based to model-based approaches"
- Test: Is this describing a fact without interpreting it? If yes, it's an observation.
- Interference value: LOW for individual lenses (hard to disagree with observations), HIGH for interference detection (lenses may agree on observations but diverge on inferences drawn from them).

### [inference]
Conclusion drawn from observations. The reasoning step between what is seen and what is concluded.
- Example: "Text extraction plus Vision is the right architecture"
- Test: Does this conclude something from evidence? If yes, it's an inference.
- Interference value: Inferences are where lenses most productively disagree - same observations, different conclusions.

### [value-judgment]
Normative statement. Says what SHOULD be, what's BETTER, what's IMPORTANT.
- Example: "Solving this problem matters for AI agents at scale"
- Test: Does it use "should", "better", "important", "right", "wrong"? If yes, it's a value-judgment.
- Interference value: Value-judgments reveal the input's priorities. Lenses can challenge by asking "important for WHOM?"

## How Tags Enable Interference Detection

The Interference Reader uses tags to detect precise interference patterns:

| Interference Pattern | What It Means |
|---------------------|---------------|
| Lenses agree on [observation], disagree on [inference] | The facts are clear, the meaning is contested - high-value CRUX territory |
| Lenses disagree on [assumption] | Load-bearing premise is contested - potential paradigm shift |
| Lenses agree on [prediction] from different reasoning | Strong convergence signal - high confidence |
| Lenses disagree on [claim] | Factual dispute - verifiable, good CRUX candidate |
| Lenses challenge same [value-judgment] | Input's priorities are misaligned with reality |

## Tagging Rules for Intake Processor

1. Each atom gets exactly ONE primary tag
2. If ambiguous, prefer [assumption] over [claim] (more analytically valuable)
3. If a statement is both [prediction] and [value-judgment], prefer [prediction] (testable)
4. Target: 5-12 atoms per input, mix of tags
5. Every input should have at least 1 [assumption] (there's always an unstated premise)
6. Atoms should be INDEPENDENT - each should be judgeable on its own without needing the others
