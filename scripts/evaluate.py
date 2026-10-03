"""Run and persist the controlled 10-case, two-condition experiment.

For every frozen CSV row, this module generates one structured plan and one
raw user-only baseline, then asks the same model to apply the five-item rubric.
It preserves outputs, evidence, latency, usage, and cost. Final manual scores
are maintained separately because the automated judge proved too permissive.
"""
import argparse
import csv
import getpass
import json
import os
from pathlib import Path

from pilotplanner.core import build_judge_messages, build_raw_baseline_message, build_structured_messages
from pilotplanner.provider import OpenRouterProvider, parse_plan

def call_record(provider, messages, *, json_mode):
    """Make one provider call and return text plus captured telemetry."""
    text = provider.generate(messages, json_mode=json_mode)
    return text, {
        "model": provider.model,
        "latency_seconds": provider.last_latency_seconds,
        "usage": provider.last_usage,
        "cost_usd": provider.last_cost_usd,
    }

def judge(provider, plan_text):
    """Score one saved plan with the automated five-item judge."""
    raw, meta = call_record(provider, build_judge_messages(plan_text), json_mode=True)
    result = parse_plan(raw)
    scores = result.get("scores", {})
    result["total"] = sum(int(scores.get(k, 0)) for k in (
        "test_group_named", "stages_dated", "success_metric_named",
        "feedback_instrument_specified", "human_checkpoint_named",
    ))
    return result, meta

def main():
    """Parse CLI arguments, execute all cases, and write the JSON artifact."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/evaluation-cases.csv")
    parser.add_argument("--output", default="results/evaluation-results.json")
    args = parser.parse_args()
    if not os.getenv("OPENROUTER_API_KEY"):
        os.environ["OPENROUTER_API_KEY"] = getpass.getpass("OpenRouter API key: ")
    provider = OpenRouterProvider()
    results = []
    with open(args.input, newline="", encoding="utf-8") as f:
        for case in csv.DictReader(f):
            payload = {**case, "duration_weeks": int(case["duration_weeks"])}
            structured_text, structured_meta = call_record(provider, build_structured_messages(payload), json_mode=True)
            structured = parse_plan(structured_text)
            raw_text, raw_meta = call_record(provider, build_raw_baseline_message(payload), json_mode=False)
            structured_judgment, structured_judge_meta = judge(provider, json.dumps(structured, ensure_ascii=False))
            raw_judgment, raw_judge_meta = judge(provider, raw_text)
            results.append({
                "case_id": case["case_id"],
                "structured": {"output": structured, "judgment": structured_judgment, "generation": structured_meta, "judging": structured_judge_meta},
                "raw_baseline": {"output": raw_text, "judgment": raw_judgment, "generation": raw_meta, "judging": raw_judge_meta},
            })
            print(f"{case['case_id']}: structured={structured_judgment['total']}/5 raw={raw_judgment['total']}/5", flush=True)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    structured_mean = sum(r["structured"]["judgment"]["total"] for r in results) / len(results)
    raw_mean = sum(r["raw_baseline"]["judgment"]["total"] for r in results) / len(results)
    total_cost = sum(
        float(block[meta].get("cost_usd") or 0)
        for r in results for block in (r["structured"], r["raw_baseline"])
        for meta in ("generation", "judging")
    )
    artifact = {
        "method": "Same 10 synthetic cases; structured form + fixed system prompt versus direct raw-model request. Both outputs scored by the same strict five-item 0/1 rubric, with evidence retained for review.",
        "automated_judge_summary": {"n_cases": len(results), "structured_mean": structured_mean, "raw_mean": raw_mean, "mean_difference": structured_mean - raw_mean, "total_api_cost_usd": total_cost},
        "manual_adjudication": {"status": "not produced by this script", "instructions": "Apply evals/rubric.md to the saved outputs and record final scores in results/final-scores.csv."},
        "results": results,
    }
    Path(args.output).write_text(json.dumps(artifact, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.output}")

if __name__ == "__main__":
    main()
