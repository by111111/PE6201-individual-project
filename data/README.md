# Data explainer

## Purpose

`evaluation-cases.csv` is the frozen input set for comparing the structured workflow with a raw direct-model request. It contains ten fictional SME situations and no personal, client, or confidential data.

## Provenance and creation

The cases were drafted from the specification in `synthetic-case-generation-prompt.md`, reviewed for low-risk scope and variety, and frozen before the two conditions were run. They are not scraped, purchased, or derived from real companies. Version control preserves the exact inputs used for the reported results.

The sample varies industry, company size, assistance task, participant role/group size, duration, pain point, and constraint. All cases share the same start date to simplify schedule comparison. Permitted tasks are drafting, summarising, classifying public/anonymised text, or creating internal checklists/surveys.

## Schema

| Column | Type | Meaning |
|---|---|---|
| `case_id` | string | stable identifier C01–C10 |
| `industry` | string | fictional company type and approximate size |
| `use_case` | string | low-risk AI-assisted task |
| `target_user` | string | intended participant role and group size |
| `duration_weeks` | integer | two or three weeks in this dataset |
| `pain_point` | string | current operational problem |
| `constraint` | string | privacy or operational boundary |
| `start_date` | ISO date | common pilot start date |

## How the data is used

Every row is evaluated under two conditions:

1. **Structured:** the fields are validated and passed through the fixed system prompt in `pilotplanner/core.py`.
2. **Raw baseline:** the same values are rendered into one direct user request with no system prompt or required JSON structure.

Both outputs are scored using the rules in `evals/rubric.md`. No case is used for model training or fine-tuning.

## Data quality and limitations

The set covers ten industries and avoids duplicate use cases, but it is small, synthetic, English-only, and intentionally clean. It under-represents ambiguous requirements, long pilots, multilingual users, accessibility needs, hostile inputs, real organisational politics, and messy or incomplete business data. Therefore it supports a controlled component-coverage test only; it cannot establish market representativeness or real-world effectiveness.

## Integrity checks

- ten rows with unique `case_id` values;
- all required columns populated;
- durations within the application's 1–12 week boundary;
- no real organisation names, personal identifiers, credentials, contracts, or high-stakes decisions;
- identical row set used by both experimental conditions.
