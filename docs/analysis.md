# Final Report: Enterprise AI Pilot Planning Assistant

**Word count: 1,148 words, excluding headings and this line**

## 1. Problem, intervention, and intended difference

Small and medium-sized enterprises are under pressure to “try AI,” yet many do not have a product manager, evaluation specialist, or governance team to design a disciplined pilot. A manager can ask a general-purpose model for a plan, but fluent prose can hide missing operational details: who participates, what happens when, how success is measured, how users give feedback, and who decides whether to proceed. A static template is more consistent but cannot adapt those elements to the company’s use case, duration, constraints, or risk.

The Enterprise AI Pilot Planning Assistant occupies the narrow space between those options. A seven-field web form combines the manager’s situation with a fixed system prompt and JSON schema. A rented foundation model returns a first draft containing a named test group, dated stages, a numeric success target with a baseline, a specified feedback instrument, risks and mitigations, and a human approval checkpoint. The product does not make the decision. Its intended change from today is modest but concrete: replace an unstructured starting conversation with a comparable planning artifact that makes omissions visible before an SME spends time or exposes data.

The primary persona is an SME manager planning a short, low-risk trial of drafting, summarisation, classification, or checklist support. The minimum viable product deliberately excludes accounts, persistent storage, retrieval, uploads, agents, and automatic rollout. This scope reflects the course principle of testing the smallest useful version and reduces privacy, cost, and engineering risk.

## 2. Design reasoning and technical choices

Streamlit provides the interface; Python modules separate validation and prompt construction from the OpenRouter provider. The form rejects missing fields and constrains duration to one–twelve weeks. The fixed prompt specifies dates, metric quality, feedback detail, and human approval, while delimiting user content as data. A low temperature favours consistency. The provider records model, latency, usage, and reported cost, and the parser rejects non-object JSON.

The central trade-off is flexibility versus reliability. Direct chat accepts any request but varies in coverage. The form and schema reduce freedom so required components are more likely to appear. This is useful process scaffolding, not proof of correctness: schema-valid text may still contain impractical dates, invented baselines, weak causal logic, or generic mitigations. The interface therefore labels every result “draft only” and keeps final approval outside the model.

Using a hosted model avoided training and infrastructure work and kept the prototype inexpensive. It also introduced network latency, provider dependence, variable pricing, and data-transfer risk. I mitigated those issues by using only synthetic evaluation data, prohibiting confidential input, making the model configurable, and keeping the provider behind a small module. A production version would require contractual privacy controls, authentication, retention policy, access logs, and service monitoring.

## 3. Evaluation design and outcomes

The original claim—“reliable and comprehensive”—was not scoreable. I converted it into a falsifiable question: using the same model and cases, does the structured workflow improve explicit coverage of five plan components compared with a raw direct request?

Ten synthetic SME scenarios were frozen before evaluation. Each was run twice through `openai/gpt-4.1-mini`: structured form plus fixed system prompt, and a user-only raw request with no system prompt or required schema. Each output received one point for each explicit item: specific test group; at least two dated/numbered stages; numeric target plus baseline/comparison; named feedback instrument plus who/when; and human review or approval before rollout. The predeclared targets were at least 4.0/5 for the structured workflow and at least a 1.0-point mean improvement.

The final manually adjudicated results were 5.0/5 structured and 3.1/5 raw, a 1.9-point improvement. Both targets were met. The structured condition passed every component in all ten cases. Raw outputs always named groups and stages, but passed the metric, feedback, and human-gate tests only 40%, 40%, and 30% of the time. Structured generation cost US$0.0085 for ten outputs (about US$0.0009 each) and averaged 5.5 seconds. The raw condition averaged 7.2 seconds, but latency was an observed operating measure, not a predeclared success criterion.

This outcome supports the narrow coverage claim. It does not show that a 5/5 plan is factually correct, implementable, safe, preferred by managers, or capable of producing business value. The structured score also has a ceiling effect: because the prompt directly requests the five scored fields, 5/5 mainly confirms instruction adherence. A stronger future evaluation should add independent quality dimensions such as feasibility, risk appropriateness, factual grounding, usefulness, and time saved.

## 4. Evaluation critique, difficulties, and tuning

The most important difficulty was evaluator leniency. The automated judge gave the raw baseline 4.0/5 because it credited vague phrases such as “collect feedback,” numeric targets without baselines, and review activity that was not a rollout approval gate. Accepting that score would have weakened the experiment while appearing objective. I tightened the rubric, manually re-read all saved outputs, recorded case-level reasons, and retained both the original judge evidence and final scoring rather than overwriting the discrepancy. This made the evaluation more transparent, although manual adjudication introduces researcher judgment. A blinded second scorer and agreement statistic would reduce that weakness.

Other tuning focused on controllability rather than model sophistication. I added an exact JSON schema, bounded dates to the selected pilot window, required a baseline alongside the target, specified who/when for feedback, lowered temperature, and separated user content with delimiters. I also added validation, explicit provider errors, model/cost/latency capture, unit tests, and continuous integration. These changes improved repeatability and diagnosability; they cannot prevent a plausible but unsuitable recommendation.

The experiment also has sampling limitations. Ten synthetic, English-language, low-risk SME cases are small and intentionally clean. The same start date and short durations reduce diversity. One model and one run per condition do not measure run-to-run variance or model sensitivity. The raw baseline is defensible because it matches the claim about asking directly, but a stronger competitor prompt from an experienced manager might narrow the gap. Finally, cost figures are provider-reported snapshots and may change.

## 5. Rough edges, responsible use, and future path

The application has no authentication, persistence, retry policy, accessibility study, export function, or production monitoring. It does not verify dates against calendars, check whether a proposed metric is practically measurable, or flag every unsafe context. Prompt injection is reduced by delimiters but not eliminated. Its most dangerous failure is not invalid JSON; it is a polished, complete-looking plan that users over-trust.

The next step should therefore be evidence, not feature expansion. I would run a small usability study with SME managers, measuring task completion time, rubric coverage, perceived usefulness, edit distance from draft to approved plan, and critical-error rate. Plans should be reviewed blindly by two domain-aware raters. Repeated runs across several models would test stability and cost-quality trade-offs. Only if users find the artifact useful and reviewers find risks manageable should the project add editable exports, organisation-specific policy checks, or retrieval from approved internal guidance. This path preserves the project’s core principle: AI accelerates preparation, while accountable humans retain judgment and authority.
