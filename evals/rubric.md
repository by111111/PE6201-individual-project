# Five-item binary evaluation rubric

Use only text explicitly present in the candidate plan. Award 1 only when the full pass rule is satisfied; otherwise award 0.

| Criterion | Pass (1) | Fail (0) |
|---|---|---|
| `test_group_named` | names a participant role and a number or unambiguous group size | “staff,” “users,” or a role with no identifiable group size |
| `stages_dated` | at least two stages each use a calendar date, explicit deadline, or numbered week/day | generic sequence such as “first/then,” or only one dated stage |
| `success_metric_named` | states a numeric target **and** a baseline or comparison | target without baseline, qualitative success, or measurement method only |
| `feedback_instrument_specified` | names an instrument (survey, questionnaire, interview, structured rating form, etc.) **and** states who completes it or when | “collect feedback,” informal comments, or an unnamed channel |
| `human_checkpoint_named` | requires explicit human review/approval before implementation, expansion, or rollout | routine quality checking with no go/no-go authority, or review after rollout |

## Adjudication examples

- “Reduce median drafting time by 25% versus the pre-pilot two-week baseline” passes the metric rule.
- “Reach 80% accuracy” fails if no baseline or comparison is stated.
- “Five service associates complete a five-question survey every Friday” passes feedback.
- “Gather user feedback” fails feedback.
- “The project owner signs off before expansion to the full team” passes the checkpoint.
- “A supervisor reviews generated drafts” fails unless that review gates implementation or rollout.

## Policy for ambiguity

Do not infer missing context or reward good intentions. If a phrase could satisfy a rule only after adding an assumption, score 0 and document the missing element. Keep the source output unchanged so another reviewer can reproduce or contest the decision.
