#!/usr/bin/env python3
"""Tests for ql_persist / ql_workspace. Stdlib only. Run: python scripts/test_ql_persist.py

Uses a temp dir as the host cwd (via --cwd / cwd=) and the plugin repo root as plugin_root so
schema validation + system-context seeding exercise the real files.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ql_persist  # noqa: E402
import ql_workspace  # noqa: E402

PLUGIN_ROOT = str(Path(__file__).resolve().parents[1])
_failures = []


def check(cond, msg):
    if cond:
        print(f"  PASS: {msg}")
    else:
        print(f"  FAIL: {msg}")
        _failures.append(msg)


def sample_analysis():
    return {
        "kind": "analysis",
        "input_title": "The Attention Economy",
        "input": "concept: the attention economy",
        "input_mode": "concept",
        "domain": "economics",
        "depth": "quick",
        "naive_reading": "Attention is the scarce resource.",
        "atoms": [{"id": "a1", "tag": "claim", "text": "attention is scarce"}],
        "insights": [
            {"title": "Absence of the clock", "lens": "void-reader", "text": "Time is unpriced.",
             "breakthrough_score": 4, "action_path": "price time"},
            {"title": "Scarcity inverts", "lens": "failure-romantic", "text": "Abundance is the real state.",
             "breakthrough_score": 3},
        ],
        "interference": {"constructive": ["both lenses point at unpriced time"],
                          "destructive": [{"claim_a": "scarce", "claim_b": "abundant", "crux": "is supply fixed?"}]},
        "killer_question": {"q": "Is attention actually scarce?", "why": "frames the market",
                             "if_yes": "markets valid", "if_no": "model collapses"},
        "tunnels": [{"barrier": "attention is fixed", "barrier_type": "assumed",
                      "frame_shift": "expand via tools", "other_side": "abundance"}],
        "superposition_view": ["If goal is profit: collapse to scarcity"],
        "meta_observations": "Void reader carried the run.",
        "overall_score": 4,
        "lenses": ["void-reader", "failure-romantic"],
    }


def sample_solution():
    return {
        "kind": "solution",
        "input_title": "Context window fills too fast",
        "source": "Context window fills too fast during multi-agent tasks",
        "mode": "problem",
        "solution_paths": [
            {"title": "Summarize sub-agent outputs", "gap": "no compaction", "approach": "add a reducer",
             "files": ["orchestrator.py"], "usefulness_band": "60-80%", "success_band": "55-75%",
             "effort": "M", "priority": "high", "devils_advocate": "fails if outputs are non-summarizable"},
        ],
        "reverse_path": {"goal": "fit multi-agent run in budget",
                          "barriers": [{"name": "context ceiling", "classification": "mutable",
                                         "evidence": "200k cap", "elimination": "compaction"}],
                          "wavelength_change": "stream summaries not transcripts", "residual": []},
        "roadmap": {"quick_wins": [{"title": "Trim tool echoes", "files": ["io.py"], "effort": "S",
                                     "steps": ["detect", "drop"], "rollback": "revert"}]},
        "open_problems": [{"title": "lossy summaries", "why": "may drop facts", "probability": "40-60%"}],
        "executive_summary": "Compaction is the highest-leverage fix.",
        "usefulness_band": "60-80% (medium)",
        "success_band": "55-75% (medium)",
        "action_gate": "note",
    }


def run():
    with tempfile.TemporaryDirectory() as td:
        print("[1] analysis persist (low score still writes a file)")
        res = ql_persist.persist(sample_analysis(), PLUGIN_ROOT, cwd=td)
        check(res.get("ok"), "persist returned ok")
        ws = Path(td) / ".quantum-lens"
        jp, mp = Path(res["json_path"]), Path(res["md_path"])
        check(jp.exists() and mp.exists(), "json + md written")
        check(jp.parent == ws / "outputs" / "analyses", "written under .quantum-lens/outputs/analyses")
        idx = json.loads((ws / "outputs" / "index.json").read_text())
        check(len(idx["records"]) == 1 and idx["records"][0]["record_id"] == res["record_id"],
              "index has 1 record matching record_id")
        check(res["kairn_payload"]["type"] == "insight" and "quantum-lens" in res["kairn_payload"]["tags"],
              "kairn_payload shaped for kn_learn")
        md = mp.read_text()
        check("## 1. Naive Reading" in md and "Breakthrough Score (overall)" in md, "md rendered from JSON")

        print("[2] idempotent re-write by record_id")
        rec2 = sample_analysis(); rec2["record_id"] = res["record_id"]; rec2["overall_score"] = 9
        res2 = ql_persist.persist(rec2, PLUGIN_ROOT, cwd=td)
        idx = json.loads((ws / "outputs" / "index.json").read_text())
        check(res2["record_id"] == res["record_id"] and len(idx["records"]) == 1,
              "re-persist same record_id does not duplicate index")
        check(idx["records"][0]["score"] == 9, "index score updated on re-write")

        print("[3] link-kairn updates record + md + index")
        lk = ql_persist.link_kairn(res["record_id"], "node-abc123", "analysis", PLUGIN_ROOT, cwd=td)
        check(lk.get("ok"), "link_kairn ok")
        rec_on_disk = json.loads(jp.read_text())
        check(rec_on_disk["kairn_node_id"] == "node-abc123", "record json carries kairn_node_id")
        idx = json.loads((ws / "outputs" / "index.json").read_text())
        check(idx["records"][0]["kairn_node_id"] == "node-abc123", "index carries kairn_node_id")
        check("node-abc123" in mp.read_text(), "md re-rendered with kairn link")

        print("[4] solution persist")
        sres = ql_persist.persist(sample_solution(), PLUGIN_ROOT, cwd=td)
        check(sres.get("ok"), "solution persist ok")
        check(Path(sres["json_path"]).parent == ws / "outputs" / "solutions", "solution under outputs/solutions")
        check(sres["kairn_payload"]["type"] == "solution-candidate", "solution kairn_payload type")
        idx = json.loads((ws / "outputs" / "index.json").read_text())
        check(len(idx["records"]) == 2, "index now has 2 records (analysis + solution)")

        print("[5] schema rejection on missing required field")
        bad = sample_analysis(); del bad["overall_score"]
        bres = ql_persist.persist(bad, PLUGIN_ROOT, cwd=td)
        check(not bres.get("ok") and "validation failed" in bres.get("error", ""),
              "missing required field rejected")

        print("[6] workspace seeds system-context; freshly seeded reads as 'template' not 'filled'")
        prep = ql_workspace.prepare(PLUGIN_ROOT, cwd=td)
        for name in ql_workspace.SYSTEM_CONTEXT_FILES:
            check((ws / "system-context" / name).exists(), f"seeded system-context/{name}")
        check(all(v == "template" for v in prep["system_context_status"].values()),
              "freshly seeded files report 'template' (uncustomized), not 'filled'")
        # user customizes one file -> it should now read 'filled'
        (ws / "system-context" / "SYSTEM-MAP.md").write_text("# My real system\n- api: src/api\n", encoding="utf-8")
        st = ql_workspace.system_context_status(ws, PLUGIN_ROOT)
        check(st["SYSTEM-MAP.md"] == "filled", "edited file reports 'filled'")
        check(st["architecture.md"] == "template", "untouched file still 'template'")

        print("[7] QUANTUM_LENS_HOME override is honored")
        with tempfile.TemporaryDirectory() as td2:
            os.environ["QUANTUM_LENS_HOME"] = td2
            try:
                r = ql_persist.persist(sample_analysis(), PLUGIN_ROOT)
                check(Path(r["json_path"]).is_relative_to(Path(td2)), "override workspace used")
            finally:
                del os.environ["QUANTUM_LENS_HOME"]

        print("[8] lens config overlay: seed, resolution, agent precedence, --full")
        with tempfile.TemporaryDirectory() as tdc:
            prep = ql_workspace.prepare(PLUGIN_ROOT, cwd=tdc)
            wsc = Path(tdc) / ".quantum-lens"
            check(prep["seeded_config"] and (wsc / "scenario.json").exists(), "config overlay seeded")
            check((wsc / "agents").is_dir(), "workspace agents/ dir created")
            check(ql_workspace.resolve_lenses(wsc, "quick") == ["void-reader", "failure-romantic"],
                  "quick base lenses resolved")
            check(len(ql_workspace.resolve_lenses(wsc, "deep")) == 6, "deep base = 6 lenses")
            # apply overlay: disable one, add a custom lens for deep only
            cfg = json.loads((wsc / "scenario.json").read_text())
            cfg["disabled_lenses"] = ["scale-shifter"]
            cfg["custom_lenses"] = [{"name": "my-lens", "depth_modes": ["deep"]}]
            (wsc / "scenario.json").write_text(json.dumps(cfg), encoding="utf-8")
            deep = ql_workspace.resolve_lenses(wsc, "deep")
            check("scale-shifter" not in deep, "disabled lens removed from deep")
            check("my-lens" in deep, "custom lens added to deep")
            check("my-lens" not in ql_workspace.resolve_lenses(wsc, "standard"),
                  "custom lens absent from non-matching depth")
            # agent resolution precedence: built-in -> plugin, override -> workspace
            ap_builtin = ql_workspace.resolve_agent(wsc, PLUGIN_ROOT, "void-reader").replace("\\", "/")
            check(ap_builtin.endswith("void-reader-agent.md") and "/.quantum-lens/" not in ap_builtin,
                  "built-in lens agent resolves to plugin")
            (wsc / "agents" / "void-reader-agent.md").write_text("custom body", encoding="utf-8")
            ap_ws = ql_workspace.resolve_agent(wsc, PLUGIN_ROOT, "void-reader").replace("\\", "/")
            check("/.quantum-lens/" in ap_ws, "workspace lens agent overrides plugin")
            # --full materializes the remaining built-in agents (doesn't clobber the custom one)
            ql_workspace.prepare(PLUGIN_ROOT, cwd=tdc, full=True)
            check(len(list((wsc / "agents").glob("*-agent.md"))) >= 7, "--full materialized built-in agents")
            check((wsc / "agents" / "void-reader-agent.md").read_text() == "custom body",
                  "--full did not clobber existing workspace agent")

    print()
    if _failures:
        print(f"RESULT: {len(_failures)} FAILED")
        return 1
    print("RESULT: ALL PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(run())
