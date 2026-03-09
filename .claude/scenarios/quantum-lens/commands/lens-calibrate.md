---
keywords: [lens, calibrate, customize, configure, quantum-lens, lenses, adjust]
description: "Customize Quantum Lens configuration - enable/disable lenses, adjust depth defaults, add custom lenses"
argument: "[--show | --enable LENS | --disable LENS | --add-lens | --depth-default MODE]"
model: sonnet
---

# /lens-calibrate

View and customize Quantum Lens configuration.

## Arguments

- `--show` (default): Display current lens configuration and depth mode defaults
- `--enable LENS`: Enable a specific lens (e.g., `--enable boundary-dissolver`)
- `--disable LENS`: Disable a specific lens (keeps file, skips in workflow)
- `--add-lens`: Interactive custom lens creation following the Extension Protocol
- `--depth-default MODE`: Change the default depth mode (quick|standard|deep)

## Workflow

### --show (default)

1. Read `.claude/scenarios/quantum-lens/scenario.json`
2. Read `.claude/scenarios/quantum-lens/knowledge/lens-definitions.md`
3. Read `.claude/scenarios/quantum-lens/commands/quantum-lens.md` (authoritative depth mode assignments in Phase 1)
4. Display configuration table:

```
| # | Lens | Status | Cognitive Mode | Depth Modes |
|---|------|--------|---------------|-------------|
| 1 | Boundary Dissolver | active | Holistic integration | standard, deep |
| 2 | Temporal Archaeologist | active | Dynamic systems | deep |
| 3 | Scale Shifter | active | Fractal/spatial | deep |
| 4 | Failure Romantic | active | Inversion reasoning | quick, standard, deep |
| 5 | Void Reader | active | Negative space | quick, standard, deep |
| 6 | Paradox Hunter | active | Dialectical synthesis | standard, deep |

Current default depth: standard (4 lenses)
```

### --add-lens

Interactive custom lens creation:

1. Ask: "What cognitive mode does this lens use? (How does it THINK, not what domain it covers)"
2. Derive perceptual geometry from the cognitive mode
3. Ask: "What is the core question this lens always asks?"
4. Assign quantum instrument (suggest based on cognitive mode)
5. Define voice markers (hard constraints on language)
6. Specify required output section name
7. Identify the anti-pattern this lens catches
8. Generate the agent file following the existing agent template pattern
9. Write to `.claude/scenarios/quantum-lens/agents/{lens-name}-agent.md`
10. Update `scenario.json` agents array
11. Update `lens-definitions.md` with new lens spec

### --enable / --disable

1. Read `scenario.json`
2. Add a `"disabled": true` property to the lens entry in the `agents` array (or remove the property to re-enable)
3. Update depth mode lens selections if affected

## Output

Configuration table showing all lenses with status, cognitive mode, and depth mode assignment.
