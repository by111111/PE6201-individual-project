# Evaluation explainer

## Claim and decision rule

The evaluation tests one narrow claim: **for the same ten SME scenarios and the same model, the structured form plus fixed system prompt increases explicit coverage of five required pilot-plan components compared with asking the model directly.**

Targets declared for the project:

- structured mean score ≥ 4.0/5;
- mean improvement over the raw baseline ≥ 1.0 point.

## Controlled comparison

| Held constant | Deliberately changed |
|---|---|
| ten frozen synthetic cases | structured workflow uses a system prompt and JSON schema |
| model: `openai/gpt-4.1-mini` | raw baseline has one user message only |
| provider and API route | raw baseline has no form-enforced response format |
| low temperature | structured generation requests JSON mode |
| five scoring criteria | — |

Each case produces one structured output and one raw output. The experiment therefore contains 20 plan generations. The evaluation script also makes 20 model-judge calls and records model, latency, usage, reported cost, scores, and evidence.

## Scoring

Each plan receives 0 or 1 on five criteria, for a total from 0 to 5:

1. named test group;
2. at least two dated/numbered stages;
3. numeric target plus baseline/comparison;
4. named feedback instrument plus who/when; and
5. explicit human review/approval before rollout.

The exact decision rules and pass/fail examples are in [`rubric.md`](rubric.md). Score only explicit text; do not infer intent.

## Run the experiment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENROUTER_API_KEY='your-key'
export OPENROUTER_MODEL='openai/gpt-4.1-mini'
python -m scripts.evaluate \
  --input data/evaluation-cases.csv \
  --output results/evaluation-results.json
```

The script prompts securely if the key is not in the environment. Never place a real key in source files. Running the experiment incurs API cost. The committed evidence can be audited without rerunning it.

## Outputs and source of truth

- `results/evaluation-results.json`: all 20 outputs, generation metadata, and initial automated-judge evidence.
- `results/final-scores.csv`: scan-friendly final 0/1 manual adjudication by case.
- `results/PE6201-Evaluation-Results.xlsx`: formatted final record with rubric, notes, summary, pass rates, cost, latency, and chart.

The automated judge produced 5.0/5 structured and 4.0/5 raw. Manual adjudication found false positives for vague feedback, metrics without baselines, and review steps that were not approval gates. Applying the written rubric strictly produced the final reported result: **5.0/5 structured, 3.1/5 raw, +1.9 points**. The original judge evidence is retained rather than silently replaced.

## Manual adjudication procedure

1. Read the saved output without looking at its condition score.
2. Apply each rule in `rubric.md` independently.
3. Quote or identify explicit evidence; if evidence is incomplete, score 0.
4. Record the five binary values and a short note in `final-scores.csv`.
5. Recalculate condition means and per-criterion pass rates.
6. If changing a score, preserve the raw output and explain the reason.

## Metric calculation

- Per-plan total = sum of the five binary criteria.
- Condition mean = sum of ten plan totals ÷ 10.
- Mean improvement = structured mean − raw mean.
- Criterion pass rate = passes for that criterion ÷ 10.

## Limitations

Ten synthetic English-language cases, one model, and one run per condition do not measure real-user value, factual accuracy, run-to-run variance, or transfer to high-risk domains. The structured prompt directly requests the scored fields, so its perfect score mainly demonstrates instruction adherence. Manual adjudication is auditable but not independent; a blinded second scorer and inter-rater agreement would strengthen the evidence.
