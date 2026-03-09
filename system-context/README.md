# System Context (Optional)

These template files help the Solution Engine understand YOUR system. Fill them in to get personalized adaptation roadmaps, overlap/gap/collision maps, and system-aware recommendations.

**Without these files**: Quantum Lens perception works 100%. Solution Engine works in "general analysis mode" - reverse-engineering and barrier analysis still function, but system comparison and file-path-specific adaptations are skipped.

**With these files**: Solution Engine maps external insights against your actual system, identifies gaps, and produces executable adaptation plans with specific file paths.

## How to Fill In

### SYSTEM-MAP.md
Your system's component inventory. What exists, where it lives, what it does. Think of it as a table of contents for your codebase/project.

### architecture.md
How your components connect. Data flows, dependency chains, integration points. The "wiring diagram" of your system.

### project-goals.md
Current goals, active blockers, and priorities. What you're working toward and what's in the way. This helps the Solution Engine filter solutions by relevance and feasibility.

## Tips

- Start minimal. Even a few bullet points per file is better than empty files.
- Update after major changes. These files are snapshots, not live data.
- The Solution Engine reads these before every analysis - keep them current for best results.
