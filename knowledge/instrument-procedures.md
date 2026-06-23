# Quantum Instrument Procedures

Step-by-step procedures for each analytical instrument used by the lenses.

## 1. Superposition Holder

**Used by**: Boundary Dissolver
**Purpose**: Hold all interpretations simultaneously without collapsing

### Procedure
1. Take atom (e.g., A3: "Real-world PDFs have no concept of tables")
2. List ALL valid interpretations:
   - [observation] Tables don't exist as PDF primitives
   - [assumption] This is a permanent limitation
   - [value-judgment] This matters for document processing
   - [inference] Solutions must work around this
3. Tag each: `[observation]`, `[inference]`, `[assumption]`, `[prediction]`, `[value-judgment]`
4. DO NOT rank. DO NOT select "best." The superposition IS the output.
5. Note: which interpretations does the input's framing encourage you to favor? That bias is data.

### Anti-Pattern
Collapsing prematurely by selecting the "most reasonable" interpretation. Reasonableness is a bias.

## 1b. Superposition of Absence

**Used by**: Void Reader
**Purpose**: Detect what is conspicuously ABSENT from the input

### Procedure
1. Take atom (e.g., A8: "Text extraction plus Vision is the right architecture")
2. List what the atom SAYS explicitly
3. List what the atom IMPLIES but does not state
4. List what the atom EXCLUDES by framing (what becomes invisible when you accept this frame?)
5. List what a hostile critic would demand is missing
6. Hold all absences in superposition - do not rank yet
7. Note: which absences does the input's framing PREVENT you from noticing? Those are highest value.

### Anti-Pattern
Confusing "not mentioned" with "absent." True absence is CONSPICUOUS - the thing you'd expect to find that isn't there. A blog post about PDF parsing not mentioning quantum physics is irrelevant. Not mentioning competing parsers is diagnostic.

## 2. Linked Pairs

**Used by**: Scale Shifter, Boundary Dissolver
**Purpose**: Identify concept pairs where changing one forces change in the other

### Procedure
1. Identify concept A from an atom
2. Ask: "What concept B changes NECESSARILY if A changes?"
3. State the link: "If A changes to A', then B MUST become B'"
4. Map the pair: `{A -> A'} entails {B -> B'}`
5. Test reversibility: Does changing B also force A to change? (bidirectional = strong entanglement)
6. Test scope: Is this link local (within the input) or universal (true everywhere)?

### Example
- A: "PDFs are the dominant document format" -> A': "PDFs become minority format"
- B: "Document parsing is a hard problem" -> B': "Document parsing becomes trivial"
- Link: The difficulty of parsing is entangled with PDF dominance. If PDFs lose dominance, the problem doesn't get solved - it disappears.

### Anti-Pattern
Claiming correlation as entanglement. Linked pairs require NECESSARY coupling, not just association.

## 3. Cascading Flips

**Used by**: Temporal Archaeologist, Paradox Hunter
**Purpose**: Trace chain reactions from one decision/change

### Procedure
1. Start with one atomic decision or change (the "flip")
2. Ask: "If this flips, what MUST change next?" (flip1 -> consequence1)
3. For consequence1, ask: "And what does THIS force?" (consequence1 -> flip2)
4. Continue: flip2 -> consequence2 -> flip3 -> ...
5. Stop when: chain loops back to start (circular), or stabilizes (no more forced changes)
6. Document the full chain with each link justified

### Example
Starting flip: "Tagged PDF becomes universally enforced"
- -> Document parsing difficulty drops 90%
- -> Parsing startups lose product-market fit
- -> AI document understanding pivots to other modalities (audio, video)
- -> PDF becomes a solved/boring input format
- -> Innovation moves to creation tools, not extraction tools
- -> Chain stabilizes: new equilibrium with semantic PDFs

### Anti-Pattern
Speculative chains where links are "might" rather than "must." Each link should be a forced consequence, not a possible one.

## 4. Tunneling Detector

**Used by**: Failure Romantic, all lenses in Phase 2
**Purpose**: Find paths through "impossible" barriers by changing the frame

### Procedure
1. Identify the "impossible" or dead end (stated or implied in input)
2. Strip the frame: what assumptions define the walls of this impossibility?
3. For each assumption: "Under what frame-shift, scale-change, or domain-swap does this assumption break?"
4. Document the tunnel:
   - **Barrier**: {the impossibility as stated}
   - **Frame that creates it**: {the assumption holding the walls up}
   - **Tunnel**: {the frame-shift that dissolves the wall}
   - **Other side**: {what becomes possible}
5. Verify: is the tunnel genuinely reachable, or does it require its own frame-shift? (nested tunnels = higher breakthrough potential)

### Example
- Barrier: "PDFs are fundamentally hard to parse"
- Frame: "We must extract meaning from the rendering format"
- Tunnel: "What if we don't extract FROM PDFs but generate semantic metadata ALONGSIDE them at creation time?"
- Other side: PDF stays as visual format, a parallel semantic layer provides machine-readability. The parsing problem becomes a creation-time annotation problem.

### Anti-Pattern
"Tunnels" that are actually just solutions to the stated problem. Real tunneling requires dissolving the problem, not solving it.

## 5. Collapse Trigger

**Used by**: Interference Reader (Phase 2 only)
**Purpose**: Formulate the single question that eliminates the most interpretive ambiguity

### Procedure
1. Survey all remaining superpositions across all lens outputs
2. For each, estimate entropy: how many interpretations remain unresolved?
3. Find the highest-entropy superposition - the one with most open interpretations
4. Formulate as a binary question:
   - MUST reference a specific atom from the decomposition
   - MUST name a concrete concept (not "X" or "this")
   - MUST have explicit YES implications (what changes, what actions follow)
   - MUST have explicit NO implications (what changes, what actions follow)
5. Verify specificity: Could this question apply to ANY input? If yes, it has failed. Rewrite.
6. This is the Killer Question.

### Quality Check
- Generic: "What is the role of AI in document processing?" - FAIL
- Specific: "Does removing the text-extraction layer from hybrid PDF parsers reduce accuracy by >15% on PubTabNet when using GPT-4V at 2026 pricing?" - PASS
- The specificity test: replace all domain nouns with blanks. If the question still makes sense, it's too generic.

### Anti-Pattern
Questions that are interesting but have no resolution power. The Killer Question must COLLAPSE the most disagreements if answered, not just be thought-provoking.
