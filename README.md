# PE6201 Individual Project

## Enterprise AI Pilot Planning Assistant

A structured web form sends one controlled prompt to a rented foundation model and returns a draft, human-reviewable AI pilot plan. This repository contains the complete PE6201 submission package: problem statement, analysis, runnable code, evaluation evidence, and a demo recording script.

## Submission artifacts

- [Problem Statement](docs/PE6201_Enterprise_AI_Pilot_Planning_Assistant.pdf)
- [Analysis (≤1200 words)](docs/analysis.md)
- [Runnable application](app.py)
- [Ten-case evaluation dataset](data/evaluation_cases.csv)
- [Final reviewed results](results/PE6201_Evaluation_Results.xlsx)
- [Complete model outputs and judge evidence](results/evaluation_results.json)
- [Demo video script and checklist](docs/demo_script.md)

> The final recorded video is intentionally not fabricated in this repository. Record the application with the supplied script, upload it to the permitted submission platform, and add the link here before submission.

## Scope

- One low-risk SME scenario -> one OpenRouter model call -> one structured draft plan.
- No agent, RAG, document upload, user accounts, or persistent form storage.
- The output is a draft only. A human project owner must approve it before implementation.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENROUTER_API_KEY='your-key'  # never commit this value
export OPENROUTER_MODEL='openai/gpt-4.1-mini'  # optional
streamlit run app.py
```

The app opens at `http://localhost:8501`. Use fictional or non-confidential inputs only.

## Tests

```bash
python -m unittest discover -s tests -v
```

The unit tests require only Python. GitHub Actions runs them on every push and pull request.

## Evaluation

The version-controlled synthetic dataset has 10 cases in `data/evaluation_cases.csv`. The script tests each case twice:

1. Structured workflow: form fields plus fixed system prompt.
2. Raw baseline: the same case sent directly, with no form and no fixed system prompt.

Each output is scored 0/1 for five components: named test group, dated stages, measurable success metric, feedback instrument, and human checkpoint.

### Completed experiment

The 10-case experiment used `openai/gpt-4.1-mini` through OpenRouter. Final scores were manually adjudicated against the strict rubric after the initial automated judge proved too lenient on several raw outputs.

- Structured workflow mean: **5.0/5**
- Raw-model baseline mean: **3.1/5**
- Mean improvement: **1.9 points**
- Structured generation cost: **US$0.0085 for 10 outputs**, or approximately **US$0.0009 per output**
- Structured mean generation latency: **5.5 seconds**

The complete model outputs and initial judge evidence are saved in `results/evaluation_results.json`. The reviewed scores, rubric, chart, and case notes are in `results/PE6201_Evaluation_Results.xlsx`.

```bash
python -m scripts.evaluate --input data/evaluation_cases.csv --output results/evaluation_results.json
```

Running the evaluation makes model and judge calls and therefore incurs API cost. The committed results are sufficient to inspect the completed experiment.

## Repository structure

```text
.
├── app.py                         # Streamlit interface
├── pilot_planner/                 # prompt, validation, provider, parsing
├── scripts/evaluate.py            # controlled two-condition experiment
├── tests/                         # dependency-free unit tests
├── data/                          # frozen synthetic cases and generation spec
├── docs/                          # problem statement, analysis, demo script
└── results/                       # reviewed workbook and raw evidence
```

## Safety boundary

Do not enter personal data, client names, financial data, credentials, contracts, or confidential strategy. Do not use this system for health, credit, hiring, legal, security, or other high-stakes decisions. A human project owner must review and approve every draft before implementation.
