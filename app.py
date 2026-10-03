"""Presentation layer for the Enterprise AI Pilot Planning Assistant.

This module renders the Streamlit interface, communicates the product's safety
boundary, validates user inputs, calls the provider, and presents a structured
draft for human review. It intentionally contains no persistence or automated
approval logic: the final decision always remains with a human project owner.
"""

import json
import os
from datetime import date
from html import escape

import streamlit as st

from pilotplanner.core import build_structured_messages, validate_input
from pilotplanner.provider import OpenRouterProvider, ProviderError, parse_plan


st.set_page_config(
    page_title="Enterprise AI Pilot Planner",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --navy: #102a43;
        --teal: #0f8b8d;
        --orange: #f28c52;
        --canvas: #f4f7fa;
        --ink: #1f2933;
        --muted: #627d98;
        --line: #d9e2ec;
    }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 92% 4%, rgba(15, 139, 141, .10), transparent 24rem),
            linear-gradient(180deg, #f8fbfd 0%, var(--canvas) 100%);
    }
    [data-testid="stHeader"] { background: rgba(248, 251, 253, .84); }
    [data-testid="stMainBlockContainer"] {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 5rem;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d2438 0%, #153a50 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }
    [data-testid="stSidebar"] * { color: #eef7f7; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.16); }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.6rem 2.8rem 2.4rem;
        border-radius: 26px;
        color: white;
        background: linear-gradient(125deg, #0b2239 0%, #123e55 58%, #0f8b8d 135%);
        box-shadow: 0 18px 45px rgba(16, 42, 67, .18);
        margin-bottom: 1.35rem;
    }
    .hero::after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -70px;
        top: -110px;
        border-radius: 50%;
        border: 54px solid rgba(255,255,255,.08);
    }
    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .36rem .7rem;
        border: 1px solid rgba(255,255,255,.22);
        border-radius: 999px;
        background: rgba(255,255,255,.09);
        color: #dff7f4;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .09em;
        text-transform: uppercase;
    }
    .hero h1 {
        max-width: 760px;
        margin: 1rem 0 .65rem;
        color: white;
        font-size: clamp(2rem, 4vw, 3.35rem);
        line-height: 1.05;
        letter-spacing: -.045em;
    }
    .hero p {
        max-width: 760px;
        margin: 0;
        color: #cfe0ea;
        font-size: 1.05rem;
        line-height: 1.65;
    }
    .hero-note {
        display: flex;
        gap: .55rem;
        align-items: center;
        margin-top: 1.25rem;
        color: #f7d6c2;
        font-size: .88rem;
        font-weight: 600;
    }
    .process-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: .8rem;
        margin: 1rem 0 1.55rem;
    }
    .process-card {
        display: flex;
        align-items: center;
        gap: .8rem;
        padding: .9rem 1rem;
        border: 1px solid var(--line);
        border-radius: 14px;
        background: rgba(255,255,255,.78);
    }
    .process-no {
        display: grid;
        place-items: center;
        width: 34px;
        height: 34px;
        flex: 0 0 34px;
        border-radius: 10px;
        background: var(--navy);
        color: white;
        font-weight: 800;
        font-size: .78rem;
    }
    .process-card strong { display: block; color: var(--ink); font-size: .91rem; }
    .process-card span { color: var(--muted); font-size: .76rem; }
    .section-kicker {
        margin: .25rem 0 .15rem;
        color: var(--teal);
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .1em;
        text-transform: uppercase;
    }
    .section-title {
        margin: 0 0 .25rem;
        color: var(--navy);
        font-size: 1.45rem;
        letter-spacing: -.025em;
    }
    .section-copy { margin: 0 0 1rem; color: var(--muted); font-size: .9rem; }
    [data-testid="stForm"] {
        padding: 1.6rem 1.65rem 1.4rem;
        border: 1px solid #d8e3eb;
        border-radius: 20px;
        background: rgba(255,255,255,.94);
        box-shadow: 0 10px 30px rgba(16, 42, 67, .07);
    }
    [data-testid="stForm"] label p { color: #334e68; font-weight: 650; }
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input {
        border-color: #cbd8e2;
        background: #fbfdfe;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--teal);
        box-shadow: 0 0 0 1px var(--teal);
    }
    [data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 3.15rem;
        margin-top: .55rem;
        border: 0;
        border-radius: 12px;
        background: linear-gradient(100deg, #0f8b8d 0%, #136f83 100%);
        color: white;
        font-weight: 750;
        box-shadow: 0 8px 18px rgba(15,139,141,.20);
    }
    [data-testid="stFormSubmitButton"] button:hover {
        color: white;
        background: linear-gradient(100deg, #0d7d7f 0%, #0f6073 100%);
        transform: translateY(-1px);
    }
    .sidebar-brand {
        margin: .6rem 0 1.4rem;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,.13);
        border-radius: 16px;
        background: rgba(255,255,255,.06);
    }
    .sidebar-brand strong { display: block; margin-bottom: .25rem; font-size: 1rem; }
    .sidebar-brand span { color: #b9d4df !important; font-size: .78rem; line-height: 1.45; }
    .sidebar-label {
        margin: 1rem 0 .55rem;
        color: #8edbd4 !important;
        font-size: .7rem;
        font-weight: 800;
        letter-spacing: .1em;
        text-transform: uppercase;
    }
    .check-item {
        display: flex;
        gap: .55rem;
        margin: .48rem 0;
        color: #dbeaf0 !important;
        font-size: .8rem;
    }
    .check-item b { color: #8edbd4 !important; }
    .safety-box {
        padding: .9rem 1rem;
        border-left: 3px solid var(--orange);
        border-radius: 7px 12px 12px 7px;
        background: rgba(242,140,82,.10);
        color: #dbeaf0 !important;
        font-size: .78rem;
        line-height: 1.5;
    }
    .result-header {
        margin: 2rem 0 1rem;
        padding: 1.35rem 1.5rem;
        border: 1px solid #bde4df;
        border-radius: 18px;
        background: linear-gradient(110deg, #e7f7f5 0%, #f7fbfc 100%);
    }
    .result-header h2 { margin: 0 0 .3rem; color: var(--navy); font-size: 1.5rem; }
    .result-header p { margin: 0; color: #486581; font-size: .88rem; }
    .output-card {
        min-height: 145px;
        padding: 1.2rem 1.25rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: white;
        box-shadow: 0 7px 20px rgba(16,42,67,.05);
    }
    .output-label {
        margin-bottom: .5rem;
        color: var(--teal);
        font-size: .7rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
    }
    .output-value { color: var(--ink); font-size: .92rem; line-height: 1.55; }
    .approval-card {
        margin: .8rem 0;
        padding: 1rem 1.15rem;
        border-left: 4px solid var(--orange);
        border-radius: 10px;
        background: #fff7f0;
        color: #5d4031;
        line-height: 1.55;
    }
    .footer-note {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--line);
        color: var(--muted);
        text-align: center;
        font-size: .76rem;
    }
    @media (max-width: 760px) {
        .hero { padding: 2rem 1.4rem; border-radius: 20px; }
        .process-grid { grid-template-columns: 1fr; }
        [data-testid="stForm"] { padding: 1.15rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def output_card(label: str, value: object) -> None:
    """Render an escaped summary card for a scalar plan field."""
    safe_value = escape(str(value or "Not provided"))
    st.markdown(
        f'<div class="output-card"><div class="output-label">{escape(label)}</div>'
        f'<div class="output-value">{safe_value}</div></div>',
        unsafe_allow_html=True,
    )


def render_plan(plan: dict, technical_record: dict) -> None:
    """Present the generated plan as reviewer-friendly cards, tables, and evidence."""
    st.markdown(
        """
        <div class="result-header">
            <h2>Draft pilot plan ready</h2>
            <p>Review every field below. This output is a planning draft, not an implementation approval.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns(2, gap="medium")
    with left:
        output_card("Objective", plan.get("objective"))
    with right:
        output_card("Named test group", plan.get("test_group"))
    metric_col, feedback_col = st.columns(2, gap="medium")
    with metric_col:
        output_card("Measurable success metric", plan.get("success_metric"))
    with feedback_col:
        output_card("Feedback instrument", plan.get("feedback_instrument"))

    overview_tab, risk_tab, evidence_tab = st.tabs(["Dated stages", "Risks & controls", "Technical record"])
    with overview_tab:
        stages = plan.get("stages", [])
        if isinstance(stages, list) and stages:
            st.dataframe(stages, use_container_width=True, hide_index=True)
        else:
            st.info("No stages were returned.")
    with risk_tab:
        risks = plan.get("risks_and_mitigations", [])
        if isinstance(risks, list) and risks:
            st.dataframe(risks, use_container_width=True, hide_index=True)
        else:
            st.info("No risks and mitigations were returned.")
    with evidence_tab:
        m1, m2, m3 = st.columns(3)
        m1.metric("Model", technical_record.get("model", "—"))
        m2.metric("Latency", f"{technical_record.get('latency_seconds', 0):.2f}s")
        cost = technical_record.get("estimated_cost_usd")
        m3.metric("Reported cost", f"US${cost:.5f}" if isinstance(cost, (int, float)) else "Not reported")
        st.caption("Provider-reported operational metadata for this generation. Values may vary between runs.")

    checkpoint = escape(str(plan.get("human_approval_checkpoint", "Not provided")))
    st.markdown(
        f'<div class="approval-card"><strong>Human approval checkpoint</strong><br>{checkpoint}</div>',
        unsafe_allow_html=True,
    )
    st.download_button(
        "Download plan as JSON",
        data=json.dumps(plan, ensure_ascii=False, indent=2),
        file_name="ai_pilot_plan.json",
        mime="application/json",
        use_container_width=True,
    )


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <strong>AI Pilot Planner</strong>
            <span>A focused decision-support prototype for low-risk SME experiments.</span>
        </div>
        <div class="sidebar-label">Every draft includes</div>
        <div class="check-item"><b>01</b> A named test group</div>
        <div class="check-item"><b>02</b> Dated pilot stages</div>
        <div class="check-item"><b>03</b> A baseline and target</div>
        <div class="check-item"><b>04</b> A feedback instrument</div>
        <div class="check-item"><b>05</b> A human approval gate</div>
        <hr>
        <div class="sidebar-label">Safety boundary</div>
        <div class="safety-box">
            Do not enter personal data, client names, credentials, financial figures,
            contracts, or confidential strategy. Do not use this tool for high-stakes decisions.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Form submissions are not persisted by this application.")


st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">PE6201 · Individual Project</div>
        <h1>Turn an AI idea into a testable pilot.</h1>
        <p>Describe one low-risk business use case. The planner converts it into a structured,
        measurable pilot draft that a human owner can inspect before making a decision.</p>
        <div class="hero-note">◆ Draft first · Review always · Approve deliberately</div>
    </section>
    <div class="process-grid">
        <div class="process-card"><div class="process-no">01</div><div><strong>Define the context</strong><span>Company, users and business need</span></div></div>
        <div class="process-card"><div class="process-no">02</div><div><strong>Generate the pilot</strong><span>Fixed prompt and structured output</span></div></div>
        <div class="process-card"><div class="process-no">03</div><div><strong>Review the evidence</strong><span>Metrics, feedback and approval gate</span></div></div>
    </div>
    <div class="section-kicker">Pilot brief</div>
    <h2 class="section-title">Describe the experiment you want to run</h2>
    <p class="section-copy">Use fictional or non-confidential information. All fields are required.</p>
    """,
    unsafe_allow_html=True,
)

with st.form("pilot_form"):
    context_left, context_right = st.columns(2, gap="large")
    with context_left:
        industry = st.text_input(
            "Industry / company type",
            placeholder="e.g., 40-person fashion retailer",
            help="Include approximate company size so the proposed pilot remains realistic.",
        )
    with context_right:
        use_case = st.text_input(
            "AI use case to test",
            placeholder="e.g., draft replies to common service emails",
            help="Choose one narrow, low-risk workflow rather than a company-wide transformation.",
        )
    participant_col, duration_col, date_col = st.columns([1.5, 0.75, 1], gap="large")
    with participant_col:
        target_user = st.text_input(
            "Pilot participant role and number",
            placeholder="e.g., five service associates",
        )
    with duration_col:
        duration_weeks = st.number_input(
            "Duration (weeks)", min_value=1, max_value=12, value=2
        )
    with date_col:
        start_date = st.date_input("Start date", value=date.today())
    pain_col, constraint_col = st.columns(2, gap="large")
    with pain_col:
        pain_point = st.text_area(
            "Current pain point",
            placeholder="What is slow, inconsistent, costly, or difficult today?",
            height=125,
        )
    with constraint_col:
        constraint = st.text_area(
            "Safety or operating constraint",
            placeholder="e.g., no customer names or order details may be sent to the model",
            height=125,
        )
    st.caption("The generated plan will explicitly name the test group, dates, metric, feedback method, risks, and approval checkpoint.")
    submitted = st.form_submit_button("Generate structured pilot plan  →")


if submitted:
    st.session_state.pop("generated_plan", None)
    st.session_state.pop("technical_record", None)
    payload = {
        "industry": industry,
        "use_case": use_case,
        "target_user": target_user,
        "duration_weeks": int(duration_weeks),
        "pain_point": pain_point,
        "constraint": constraint,
        "start_date": start_date.isoformat(),
    }
    errors = validate_input(payload)
    if errors:
        st.error("Please complete the required information: " + "; ".join(errors))
    elif not os.getenv("OPENROUTER_API_KEY"):
        st.error("OPENROUTER_API_KEY is not configured. Add it to the environment, then restart Streamlit.")
    else:
        try:
            with st.spinner("Building a measurable, human-reviewable pilot plan…"):
                provider = OpenRouterProvider()
                raw = provider.generate(build_structured_messages(payload))
                plan = parse_plan(raw)
            st.session_state["generated_plan"] = plan
            st.session_state["technical_record"] = {
                "model": provider.model,
                "estimated_cost_usd": provider.last_cost_usd,
                "latency_seconds": provider.last_latency_seconds or 0,
            }
        except ProviderError as exc:
            st.error(f"The model request failed: {exc}")

if st.session_state.get("generated_plan"):
    render_plan(
        st.session_state["generated_plan"],
        st.session_state.get("technical_record", {}),
    )

st.markdown(
    '<div class="footer-note">Enterprise AI Pilot Planner · Structured decision support, with human judgment in the loop.</div>',
    unsafe_allow_html=True,
)
