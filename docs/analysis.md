# Enterprise AI Pilot Planning Assistant — Analysis

**Word count: 1,019 words (excluding headings and this line)**

## Problem and significance

Small and medium-sized enterprises increasingly want to test generative AI, but many lack the time and specialist knowledge to design a disciplined pilot. A manager can ask a general-purpose model for a plan, yet the answer may omit the participant group, dated stages, measurable success threshold, feedback method, or human decision point. These omissions make the plan sound useful without making it operationally testable. A generic template is also insufficient because the appropriate users, constraints, risks, schedule, and evidence depend on the company situation.

This project addresses that gap with an Enterprise AI Pilot Planning Assistant. A short web form collects seven bounded inputs and combines them with a fixed system prompt. A rented foundation model then returns a structured first draft covering an objective, test group, dated stages, a measurable success metric, a feedback instrument, risks and mitigations, and a human approval checkpoint. The product is intentionally an assistant, not an autonomous decision-maker. Its output must be reviewed by a responsible employee before a pilot begins.

## Users, value, and scope

The primary user is an SME manager or project owner preparing a low-risk, short AI pilot. The value proposition is consistency: the tool converts an incomplete business situation into a comparable plan that contains the minimum elements needed for a go/no-go discussion. It may also reduce the time needed to produce an initial plan, although this experiment evaluates completeness rather than time saved by users.

The minimum viable product follows one complete path: enter a fictional or non-confidential company context, validate the inputs, call one model, parse a JSON response, and display the draft. It deliberately excludes accounts, persistent storage, retrieval-augmented generation, document uploads, multi-agent orchestration, and automated rollout. This narrow scope keeps the first version testable and limits privacy and implementation risk.

## Technical design and trade-offs

The interface is implemented in Streamlit and the model request is sent through OpenRouter. The application uses a fixed system prompt containing a JSON schema and explicit requirements. User content is serialised inside delimiters and treated as data rather than instructions. The model temperature is low to favour repeatability. The provider layer records model, latency, usage, and reported cost so the prototype has basic operational observability.

The main trade-off is flexibility versus reliability. A direct conversation lets a user ask anything, but output coverage varies. The structured form restricts what can be entered and the schema restricts what can be returned, increasing the chance that required fields appear. However, presence is not truth: a well-formed plan can still contain impractical dates, invented assumptions, or weak metrics. JSON validation therefore supports format reliability but cannot replace business judgment.

Using a hosted model avoided the cost and delay of training or operating a model. The disadvantages are vendor dependence, network latency, variable pricing, and the risk of sending sensitive content externally. The prototype reduces these risks by banning personal and confidential data, using synthetic evaluation cases, making the model configurable, and requiring human review. A production system would also require contractual data controls, access management, logging policy, retention settings, and monitoring.

## Evaluation method

The teacher’s feedback identified “reliable and comprehensive” as unscorable. The revised claim is therefore narrower and measurable: compared with asking the same model directly, the structured workflow increases explicit coverage of five required plan components.

Ten synthetic SME cases were fixed in advance and committed in `data/evaluation_cases.csv`. Each case was run twice with the same model, `openai/gpt-4.1-mini`: once through the form-derived fixed prompt and once as a raw direct request with no system prompt. Each response received one point for each of the following: a specific test group; at least two dated or numbered stages; a numeric target with a baseline or comparison; a named feedback instrument with who or when; and an explicit human review or approval checkpoint before rollout. Thus each response scored from zero to five.

An automated model judge initially scored the structured condition at 5.0/5 and the raw baseline at 4.0/5. Manual adjudication found that the judge had credited vague language, especially metrics without baselines, generic “feedback,” and review steps that were not approval checkpoints. Applying the written rubric strictly produced the final result: 5.0/5 for the structured workflow and 3.1/5 for the raw baseline, a mean improvement of 1.9 points across ten cases. The structured generations cost US$0.0085 in total, about US$0.0009 per case, and took 5.5 seconds on average. Complete outputs and judge evidence are retained in JSON; reviewed scores and case notes are retained in the Excel workbook.

This is a small, synthetic evaluation, so it supports the component-coverage claim only. It does not establish that the plans are factually correct, safe in every context, preferred by real managers, or capable of producing business value. The manual review also introduces researcher judgment, although the binary rubric and retained evidence make disagreements auditable.

## Responsible use and failure modes

The most important silent failure is a complete-looking but unsuitable plan. Users may over-trust polished text or treat an invented success threshold as expert advice. The interface labels every output as a draft, displays a human approval checkpoint, and excludes high-stakes uses. Input guidance prohibits personal data, client names, credentials, financial figures, contracts, and confidential strategy.

Other risks include prompt injection inside company context, invalid JSON, API failure, provider changes, biased or generic recommendations, and excessive dependence on a single model. Delimiting user input, schema-constrained output, parsing errors, clear failure messages, low temperature, model configurability, and human review mitigate but do not eliminate these problems. The system should not be used to decide employment, credit, health, legal, or security outcomes, nor should its draft be implemented without review by the project owner and relevant domain specialists.

## Conclusion and next step

The prototype demonstrates that a small amount of interface and prompt structure can improve explicit plan completeness over a direct model request in the defined test. The evidence matches the product claim and remains reproducible in the repository. The next valid step is not immediate feature expansion; it is a small usability study with SME managers. Participants should create a plan, identify confusing or unnecessary fields, rate usefulness, and verify whether the proposed dates, metrics, feedback instrument, and approval gate fit their real workflow. Their evidence would determine whether the tool deserves further investment.
