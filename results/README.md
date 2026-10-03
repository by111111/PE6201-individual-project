# Results explainer

## Reported outcome

| Measure | Structured | Raw baseline | Difference |
|---|---:|---:|---:|
| Mean five-item score | **5.0/5** | **3.1/5** | **+1.9** |
| Mean generation latency | 5.5 s | 7.2 s | −1.7 s |
| Generation cost for 10 outputs | US$0.0085 | US$0.0128 | −US$0.0042 |

The predeclared quality targets—structured mean ≥4.0/5 and improvement ≥1.0 point—were met. Latency and cost were monitored rather than used as pass/fail criteria.

## Files

- `evaluation_results.json`: all twenty generated plans, generation metadata, and the initial automated-judge scores/evidence.
- `final_scores.csv`: final five binary values per case plus an adjudication note in plain text.
- `PE6201_Evaluation_Results.xlsx`: formatted workbook containing summary metrics, pass rates, case results, rubric, and chart.

The JSON is the source for raw model evidence. The CSV and workbook are the source for final manually adjudicated scores.

## Why automated and final scores differ

The automated judge reported 5.0/5 structured and 4.0/5 raw. It was too permissive with metrics lacking baselines, generic feedback, and quality review that did not gate rollout. Strict application of the prewritten binary rules changed the raw mean to 3.1/5 while the structured mean remained 5.0/5. Raw outputs passed test-group and stage criteria in all cases, but passed metric, feedback, and human-checkpoint criteria in only 40%, 40%, and 30% of cases.

The repository retains the automated evidence and the final correction so the discrepancy is auditable. See `evals/README.md` and `evals/rubric.md` for the complete protocol.

## Interpretation boundary

The result demonstrates explicit component coverage on ten synthetic cases. It does not demonstrate factual accuracy, plan feasibility, safety in every domain, user preference, causal business impact, or future performance. Costs are provider-reported snapshots and may change. A rerun may differ because hosted models are stochastic and may be updated.
