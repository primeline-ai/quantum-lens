#!/usr/bin/env python3
"""Quantum Lens persistence helper — deterministic, JSON-source-of-truth.

WHY THIS EXISTS: free-form markdown writes under long prompt instructions drift and lose
coherence, and bare-relative paths resolved against the wrong cwd (the original bug). So the
LLM emits ONE schema-bounded JSON record and this script does ALL of the IO:
  1. validate the record against schemas/{analysis,solution}_record.schema.json
  2. resolve the per-repo workspace (via ql_workspace)
  3. write the canonical {record_id}.json  (source of truth)
  4. render {record_id}.md  (structure/headers/tables are code; only prose comes from the model)
  5. upsert outputs/index.json by record_id  (the join table for /quantum-review + Kairn)
  6. print a result JSON including `kairn_payload` (compact record ready for kn_learn)

Validation uses `jsonschema` when importable; otherwise a built-in required-key/type check.

CLI:
  python ql_persist.py --plugin-root P [--in record.json]            # persist (stdin if no --in)
  python ql_persist.py --link-kairn --record <id> --node <id> [--kind analysis|solution]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import uuid
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ql_workspace  # noqa: E402

REQUIRED = {
    "analysis": ["kind", "input_title", "insights", "overall_score", "lenses"],
    "solution": ["kind", "input_title", "mode", "executive_summary"],
}
KIND_DIR = {"analysis": "analyses", "solution": "solutions"}


# --------------------------------------------------------------------------- helpers
def _slug(text: str, maxlen: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (s[:maxlen].rstrip("-")) or "untitled"


def _today() -> str:
    return _dt.date.today().isoformat()


def make_record_id(rec: dict) -> str:
    if rec.get("record_id"):
        return rec["record_id"]
    date = rec.get("date") or _today()
    return f"{date}-{_slug(rec.get('input_title', ''))}-{uuid.uuid4().hex[:8]}"


def _err(msg: str) -> "dict":
    return {"ok": False, "error": msg}


# --------------------------------------------------------------------------- validation
def validate(rec: dict, plugin_root: str | None) -> list[str]:
    """Return a list of validation error strings (empty = valid)."""
    kind = rec.get("kind")
    if kind not in REQUIRED:
        return [f"unknown or missing 'kind': {kind!r} (expected 'analysis' or 'solution')"]

    # Try full JSON-Schema validation if jsonschema + the schema file are available.
    if plugin_root:
        schema_path = Path(plugin_root) / "schemas" / f"{kind}_record.schema.json"
        try:
            import jsonschema  # type: ignore
            if schema_path.exists():
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                v = jsonschema.Draft202012Validator(schema)
                return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
                        for e in sorted(v.iter_errors(rec), key=lambda e: list(e.path))]
        except ImportError:
            pass  # fall through to built-in check

    # Built-in fallback: required keys present + a couple of type sanity checks.
    errs = [f"missing required field: {k}" for k in REQUIRED[kind] if k not in rec or rec[k] in (None, "", [])]
    if kind == "analysis" and isinstance(rec.get("overall_score"), (int, float)):
        if not (1 <= rec["overall_score"] <= 10):
            errs.append("overall_score must be 1..10")
    return errs


# --------------------------------------------------------------------------- md rendering
def _table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def render_analysis_md(rec: dict) -> str:
    L = []
    L.append(f"# Quantum Lens Analysis: {rec.get('input_title', '')}")
    L.append(f"**Date**: {rec.get('date', '')} | **Depth**: {rec.get('depth', '')} | "
             f"**Domain**: {rec.get('domain', '')}")
    L.append(f"**Input**: {rec.get('input', '')}")
    L.append(f"**Record**: `{rec.get('record_id', '')}`" +
             (f" | **Kairn**: `{rec['kairn_node_id']}`" if rec.get("kairn_node_id") else ""))
    L.append("\n---\n")

    L.append("## 1. Naive Reading\n" + (rec.get("naive_reading") or "_n/a_"))

    L.append("\n## 2. Atomic Decomposition")
    for a in rec.get("atoms", []):
        L.append(f"- [{a.get('tag','')}] ({a.get('id','')}) {a.get('text','')}")

    L.append("\n## 3. Quantum Insights")
    for i, ins in enumerate(rec.get("insights", []), 1):
        L.append(f"\n### Insight {i}: {ins.get('title', ins.get('lens',''))}")
        L.append(f"- **Lens**: {ins.get('lens','')} | **Instrument**: {ins.get('instrument','')}")
        if ins.get("cognitive_mode"):
            L.append(f"- **Cognitive Mode**: {ins['cognitive_mode']}")
        L.append(f"- **The Insight**: {ins.get('text','')}")
        if ins.get("evidence_atoms"):
            L.append(f"- **Evidence Atoms**: {', '.join(ins['evidence_atoms'])}")
        if ins.get("action_path"):
            L.append(f"- **Action Path**: {ins['action_path']}")
        L.append(f"- **Breakthrough Score**: {ins.get('breakthrough_score','')}")

    inter = rec.get("interference") or {}
    L.append("\n## 4. Interference Map")
    L.append("### Constructive")
    for c in inter.get("constructive", []):
        L.append(f"- {c}")
    L.append("### Destructive")
    for d in inter.get("destructive", []):
        L.append(f"- {d.get('claim_a','')} **vs** {d.get('claim_b','')}")
        if d.get("crux"):
            L.append(f"  - **CRUX**: {d['crux']}")
    if inter.get("isomorphisms"):
        L.append("### Isomorphisms")
        for iso in inter["isomorphisms"]:
            L.append(f"- {iso}")

    kq = rec.get("killer_question") or {}
    L.append("\n## 5. The Killer Question")
    L.append(kq.get("q", "_n/a_"))
    if kq.get("why"):
        L.append(f"**Why this question**: {kq['why']}")
    if kq.get("if_yes"):
        L.append(f"**If YES**: {kq['if_yes']}")
    if kq.get("if_no"):
        L.append(f"**If NO**: {kq['if_no']}")

    L.append("\n## 6. Tunneling Opportunities")
    for t in rec.get("tunnels", []):
        L.append(f"- **Barrier**: {t.get('barrier','')}")
        L.append(f"  - **Barrier Type**: {t.get('barrier_type','')}")
        if t.get("frame_shift"):
            L.append(f"  - **Frame-Shift**: {t['frame_shift']}")
        if t.get("other_side"):
            L.append(f"  - **Other Side**: {t['other_side']}")

    if rec.get("superposition_view"):
        L.append("\n## 7. Superposition View (Deferred Commitment)")
        for s in rec["superposition_view"]:
            L.append(f"- {s}")

    if rec.get("meta_observations"):
        L.append("\n## 8. Meta-Observations\n" + rec["meta_observations"])

    L.append("\n---")
    L.append(f"**Breakthrough Score (overall)**: {rec.get('overall_score','')}")
    L.append(f"**Lenses**: {', '.join(rec.get('lenses', []))}")
    L.append(f"**Persistence**: file (always) " +
             ("+ Kairn node `%s`" % rec["kairn_node_id"] if rec.get("kairn_node_id") else "(file only)"))
    return "\n".join(L) + "\n"


def render_solution_md(rec: dict) -> str:
    L = []
    L.append(f"# Solution Engine Report: {rec.get('input_title','')}")
    L.append(f"**Date**: {rec.get('date','')} | **Mode**: {rec.get('mode','')} | "
             f"**Source**: {rec.get('source','')}")
    L.append(f"**From QL**: {rec.get('from_ql', False)} | **Cascade**: {rec.get('cascade', False)}")
    L.append(f"**Record**: `{rec.get('record_id','')}`" +
             (f" | **Kairn**: `{rec['kairn_node_id']}`" if rec.get("kairn_node_id") else ""))
    L.append("\n---\n")

    maps = rec.get("maps") or {}
    L.append("## 1. System Scan")
    if rec.get("relevance_score") is not None:
        L.append(f"**Multi-Signal Relevance**: {rec['relevance_score']}")
    if maps.get("overlap"):
        L.append("\n### Overlap Map\n" + _table(
            ["External Concept", "Our Equivalent", "Match", "Location"],
            [[m.get("external", ""), m.get("ours", ""), m.get("match", ""), m.get("location", "")]
             for m in maps["overlap"]]))
    if maps.get("gap"):
        L.append("\n### Gap Map\n" + _table(
            ["External Concept", "What We Lack", "Impact", "Effort"],
            [[m.get("external", ""), m.get("lack", ""), m.get("impact", ""), m.get("effort", "")]
             for m in maps["gap"]]))
    if maps.get("collision"):
        L.append("\n### Collision Map\n" + _table(
            ["External Approach", "Our Approach", "Conflict", "Resolution"],
            [[m.get("theirs", ""), m.get("ours", ""), m.get("conflict", ""), m.get("resolution", "")]
             for m in maps["collision"]]))

    if rec.get("solution_paths"):
        L.append("\n## 2. Solution Paths")
        L.append(_table(
            ["#", "Solution", "Usefulness", "Success", "Effort", "Priority"],
            [[i, p.get("title", ""), p.get("usefulness_band", ""), p.get("success_band", ""),
              p.get("effort", ""), p.get("priority", "")]
             for i, p in enumerate(rec["solution_paths"], 1)]))
        for i, p in enumerate(rec["solution_paths"], 1):
            L.append(f"\n### Solution Path {i}: {p.get('title','')}")
            if p.get("gap"):
                L.append(f"- **Problem/Gap**: {p['gap']}")
            if p.get("approach"):
                L.append(f"- **Approach**: {p['approach']}")
            if p.get("files"):
                L.append(f"- **Files affected**: {', '.join(p['files'])}")
            if p.get("risk_rollback"):
                L.append(f"- **Risk + rollback**: {p['risk_rollback']}")
            if p.get("validation"):
                L.append(f"- **Validation**: {p['validation']}")
            if p.get("devils_advocate"):
                L.append(f"- **Devil's Advocate**: {p['devils_advocate']}")

    rp = rec.get("reverse_path") or {}
    if rp:
        L.append("\n## 3. Reverse Path")
        if rp.get("goal"):
            L.append("### Goal Statement\n" + rp["goal"])
        if rp.get("table"):
            L.append("\n### Reverse Path Table\n" + _table(
                ["Step", "Must Be True", "Current Reality", "Gap", "Barrier Type"],
                [[r.get("step", ""), r.get("must_be_true", ""), r.get("current_reality", ""),
                  r.get("gap", ""), r.get("barrier_type", "")] for r in rp["table"]]))
        for b in rp.get("barriers", []):
            L.append(f"\n#### Barrier: {b.get('name','')}")
            L.append(f"- **Classification**: {b.get('classification','')}"
                     + (f" ({b['lifecycle_stage']})" if b.get("lifecycle_stage") else ""))
            if b.get("evidence"):
                L.append(f"- **Evidence**: {b['evidence']}")
            if b.get("challenge"):
                L.append(f"- **Challenge**: {b['challenge']}")
            if b.get("elimination"):
                L.append(f"- **Elimination path**: {b['elimination']}")
        if rp.get("wavelength_change"):
            L.append("\n### Wavelength Change\n" + rp["wavelength_change"])
        if rp.get("residual"):
            L.append("\n### Residual Barriers")
            for r in rp["residual"]:
                L.append(f"- {r}")

    road = rec.get("roadmap") or {}
    if road:
        L.append("\n## 4. Adaptation Roadmap")
        for label, key in (("Quick Wins", "quick_wins"), ("Main Track", "main_track"),
                            ("Deal Breakers", "deal_breakers")):
            items = road.get(key) or []
            if items:
                L.append(f"\n### {label}")
                for it in items:
                    L.append(f"#### {it.get('title','')}")
                    if it.get("files"):
                        L.append(f"- **Files**: {', '.join(it['files'])}")
                    for fld in ("effort", "risk", "dependencies", "steps", "rollback", "validation",
                                "why", "alternative"):
                        if it.get(fld):
                            val = it[fld]
                            val = "; ".join(val) if isinstance(val, list) else val
                            L.append(f"- **{fld.title()}**: {val}")

    if rec.get("open_problems"):
        L.append("\n## 5. Open Problems")
        for i, op in enumerate(rec["open_problems"], 1):
            L.append(f"\n### Open Problem {i}: {op.get('title','')}")
            for fld in ("why", "probability", "direction"):
                if op.get(fld):
                    L.append(f"- **{fld.title()}**: {op[fld]}")

    L.append("\n## 6. Executive Summary\n" + (rec.get("executive_summary") or "_n/a_"))

    L.append("\n---")
    L.append(f"**Usefulness**: {rec.get('usefulness_band','')}")
    L.append(f"**Success Probability**: {rec.get('success_band','')}")
    L.append(f"**Action Gate**: {rec.get('action_gate','')}")
    L.append(f"**Persistence**: file (always) " +
             ("+ Kairn node `%s`" % rec["kairn_node_id"] if rec.get("kairn_node_id") else "(file only)"))
    return "\n".join(L) + "\n"


RENDERERS = {"analysis": render_analysis_md, "solution": render_solution_md}


# --------------------------------------------------------------------------- index
def _load_index(index_path: Path) -> dict:
    if index_path.exists():
        try:
            return json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"version": 1, "records": []}


def _index_entry(rec: dict, json_path: Path, md_path: Path) -> dict:
    score = rec.get("overall_score") if rec.get("kind") == "analysis" else rec.get("usefulness_band")
    return {
        "record_id": rec["record_id"],
        "kind": rec["kind"],
        "date": rec.get("date", ""),
        "title": rec.get("input_title", ""),
        "domain": rec.get("domain", ""),
        "mode": rec.get("mode", ""),
        "depth": rec.get("depth", ""),
        "score": score,
        "lenses": rec.get("lenses", []),
        "json_path": str(json_path),
        "md_path": str(md_path),
        "kairn_node_id": rec.get("kairn_node_id"),
    }


def _upsert_index(index_path: Path, entry: dict) -> None:
    idx = _load_index(index_path)
    idx["records"] = [r for r in idx.get("records", []) if r.get("record_id") != entry["record_id"]]
    idx["records"].append(entry)
    index_path.write_text(json.dumps(idx, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------- operations
def persist(rec: dict, plugin_root: str | None, cwd: str | None = None) -> dict:
    errs = validate(rec, plugin_root)
    if errs:
        return _err("validation failed: " + "; ".join(errs))

    rec.setdefault("date", _today())
    rec["record_id"] = make_record_id(rec)
    rec.setdefault("kairn_node_id", None)

    paths = ql_workspace.prepare(plugin_root, cwd)
    kind = rec["kind"]
    out_dir = Path(paths["outputs_dir"]) / KIND_DIR[kind]
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{rec['record_id']}.json"
    md_path = out_dir / f"{rec['record_id']}.md"
    index_path = Path(paths["index_path"])

    json_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(RENDERERS[kind](rec), encoding="utf-8")
    _upsert_index(index_path, _index_entry(rec, json_path, md_path))

    return {
        "ok": True,
        "record_id": rec["record_id"],
        "kind": kind,
        "json_path": str(json_path),
        "md_path": str(md_path),
        "index_path": str(index_path),
        "workspace": paths["workspace"],
        "kairn_payload": {
            "type": "insight" if kind == "analysis" else "solution-candidate",
            "content": json.dumps({k: rec[k] for k in rec if k != "kairn_node_id"}, ensure_ascii=False),
            "tags": (["quantum-lens"] + rec.get("lenses", []) + ([rec["domain"]] if rec.get("domain") else []))
            if kind == "analysis"
            else ["quantum-solve", rec.get("mode", ""), "barrier-tracking"],
        },
    }


def link_kairn(record_id: str, node_id: str, kind: str | None, plugin_root: str | None,
               cwd: str | None = None) -> dict:
    paths = ql_workspace.prepare(plugin_root, cwd)
    kinds = [kind] if kind else ["analysis", "solution"]
    for k in kinds:
        json_path = Path(paths["outputs_dir"]) / KIND_DIR[k] / f"{record_id}.json"
        if not json_path.exists():
            continue
        rec = json.loads(json_path.read_text(encoding="utf-8"))
        rec["kairn_node_id"] = node_id
        json_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
        md_path = json_path.with_suffix(".md")
        md_path.write_text(RENDERERS[k](rec), encoding="utf-8")
        # patch index
        index_path = Path(paths["index_path"])
        idx = _load_index(index_path)
        for r in idx.get("records", []):
            if r.get("record_id") == record_id:
                r["kairn_node_id"] = node_id
        index_path.write_text(json.dumps(idx, indent=2), encoding="utf-8")
        return {"ok": True, "record_id": record_id, "kairn_node_id": node_id, "json_path": str(json_path)}
    return _err(f"record not found: {record_id}")


# --------------------------------------------------------------------------- cli
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Persist a Quantum Lens record (JSON source of truth).")
    ap.add_argument("--plugin-root", default=os.environ.get("CLAUDE_PLUGIN_ROOT"))
    ap.add_argument("--in", dest="infile", default=None, help="record JSON file (default: stdin)")
    ap.add_argument("--cwd", default=None, help="override host cwd (testing)")
    ap.add_argument("--link-kairn", action="store_true", help="link an existing record to a Kairn node")
    ap.add_argument("--record", default=None)
    ap.add_argument("--node", default=None)
    ap.add_argument("--kind", default=None, choices=["analysis", "solution"])
    args = ap.parse_args(argv)

    if args.link_kairn:
        if not (args.record and args.node):
            print(json.dumps(_err("--link-kairn requires --record and --node")))
            return 2
        res = link_kairn(args.record, args.node, args.kind, args.plugin_root, args.cwd)
        print(json.dumps(res, indent=2))
        return 0 if res.get("ok") else 1

    raw = Path(args.infile).read_text(encoding="utf-8") if args.infile else sys.stdin.read()
    try:
        rec = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps(_err(f"input is not valid JSON: {e}")))
        return 2
    res = persist(rec, args.plugin_root, args.cwd)
    print(json.dumps(res, indent=2))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
