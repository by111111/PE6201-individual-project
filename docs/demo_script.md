# Demo video script (target: 5 minutes)

Use a picture-in-picture layout so your face and computer screen remain visible. Aim for precision, articulation, and succinctness. Do not read the repository verbatim.

## 0:00–0:40 — Problem and measurable claim

“SME managers can ask a model for an AI pilot plan, but a fluent answer may omit the test group, dates, measurable comparison, feedback method, or decision gate. My project tests whether a structured form plus a fixed system prompt improves explicit coverage of those five components. The output is a draft for human review, not an autonomous decision.”

Show the repository title and the target-versus-result table.

## 0:40–1:15 — Transparent repository

Show the submission map in `README.md`, then briefly open:

- `data/README.md` and `data/evaluation_cases.csv`;
- `evals/README.md` and `evals/rubric.md`; and
- `docs/product_documentation.md` with the architecture diagram.

State that the ten cases are synthetic, frozen before evaluation, and contain no real company or personal data.

## 1:15–2:45 — End-to-end product run

Run `streamlit run app.py`. Enter a fictional example: a 40-person fashion retailer testing draft replies with five service associates for two weeks. The pain point is slow repetitive drafting; the constraint is that customer names and order IDs cannot be entered.

Generate the plan and point to the named group, dated stages, target plus baseline, feedback instrument, risks, and approval gate. Show the “draft only” warning and technical record. Explain that deterministic Python validates and packages the request; the hosted LLM supplies the proposed plan; a human retains authority.

## 2:45–3:50 — Evaluation and results

Open `results/PE6201_Evaluation_Results.xlsx` or `results/final_scores.csv`. Explain the controlled comparison: same ten cases, same model, structured versus user-only raw request, five binary criteria.

State the results: 5.0/5 structured, 3.1/5 raw, +1.9 points; targets were ≥4.0 and ≥1.0. Mention that the raw condition already did well on groups and stages, while metrics, feedback instruments, and approval gates were weak.

Explain the evaluation correction: the automated judge initially gave the raw condition 4.0/5 but credited vague evidence. You manually reapplied the strict rubric, documented every change, and retained the original outputs and judge evidence.

## 3:50–4:35 — Critique and rough edges

State that the experiment proves component coverage only—not factual correctness, feasibility, safety, user value, or business impact. The sample is small and synthetic, with one model and one run per condition. The most dangerous failure is a polished but unsuitable plan. The prototype also lacks authentication, persistence, retry policy, and production monitoring.

Mention the operating observations: approximately US$0.0085 for ten structured generations and 5.5 seconds mean latency.

## 4:35–5:00 — Future path and close

“The next step is not more features. It is a usability study with SME managers and two independent reviewers, measuring time saved, edit distance, usefulness, critical errors, and agreement. The project shows that small interface and prompt constraints can make an AI draft more operationally complete while keeping the final decision human.”

## Recording checklist

- Face and screen visible together throughout the explanation.
- Target five minutes; never exceed eight minutes.
- Record at 1080p where possible and enlarge code/text.
- Hide API keys, bookmarks, notifications, and personal data.
- Rehearse once; use signposting and short sentences.
- Verify audio, playback, repository permissions, and video access.
- Add the final MP4 or URL under `video/` and update the root README status.
