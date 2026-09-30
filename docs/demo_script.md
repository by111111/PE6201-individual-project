# Demo video script (approximately 4–5 minutes)

## 0:00–0:35 — Problem and claim

Show the repository title and explain: SME managers can ask a model for an AI pilot plan, but direct answers often omit operational details. The project tests whether a structured form plus a fixed system prompt improves explicit coverage of five required components.

## 0:35–1:05 — Repository and reproducibility

Briefly show `README.md`, `data/evaluation_cases.csv`, and `tests/test_core.py`. Point out that the ten synthetic cases were fixed before evaluation, no real company data is included, and secrets are excluded.

## 1:05–2:30 — End-to-end application

Run `streamlit run app.py`. Enter one low-risk example, such as a 40-person fashion retailer drafting replies to repetitive customer-service emails. Use five service associates, a two-week duration, the pain point that drafting takes too long, and the constraint that no customer names or order IDs may be entered. Generate the plan.

Show the returned test group, dated stages, numeric success metric with baseline, feedback instrument, risks, and human approval checkpoint. Emphasise the “draft only” warning and that a responsible employee must approve the plan.

## 2:30–3:35 — Controlled comparison

Open `results/PE6201_Evaluation_Results.xlsx`. Explain that the same ten cases were sent to the same model under two conditions: structured workflow and raw direct request. Describe the five binary rubric items. Show the final means: structured 5.0/5, raw 3.1/5, improvement 1.9 points.

Mention that the automated judge originally gave the raw baseline 4.0/5, but strict manual adjudication rejected vague evidence. This is why the workbook is the final scoring record and the JSON preserves the raw outputs and initial judge evidence.

## 3:35–4:20 — Cost, limitations, and responsible use

State the measured structured-generation cost, approximately US$0.0085 for ten outputs, and average latency, 5.5 seconds. Explain that the experiment demonstrates component coverage, not factual correctness or business impact. Identify the main silent failure: a complete-looking but unsuitable plan.

## 4:20–4:45 — Close

Conclude that the MVP supports a human planning decision but does not make one. The next step is a usability study with SME managers before adding more features or considering deployment.

## Recording checklist

- Hide all API keys, browser bookmarks, notifications, and personal data.
- Record at 1080p if possible and keep code text readable.
- Use one continuous end-to-end run; trim only waiting time if needed.
- Verify audio and exported video before submission.
- Add the final video link to the README after uploading it to the permitted submission platform.

