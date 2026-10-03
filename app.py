"""Presentation layer for the Enterprise AI Pilot Planning Assistant.

This module renders the Streamlit form, enforces user-facing safety guidance,
passes validated inputs to the prompt/provider modules, and displays the
structured draft. It intentionally contains no persistence or approval logic:
the final decision remains with a human project owner.
"""
import json
import os
from datetime import date

import streamlit as st

from pilot_planner.core import build_structured_messages, validate_input
from pilot_planner.provider import OpenRouterProvider, ProviderError, parse_plan

st.set_page_config(page_title="Enterprise AI Pilot Planning Assistant", page_icon="🧭")
st.title("Enterprise AI Pilot Planning Assistant")
st.caption("A structured first draft for low-risk SME AI pilots. Human review is required before any pilot starts.")

with st.sidebar:
    st.header("Safety boundary")
    st.write("Do not enter personal data, client names, credentials, financial figures, contracts, or confidential strategy.")
    st.write("This tool is not for health, credit, hiring, legal, security, or other high-stakes decisions.")
    st.caption("The app does not persist form submissions.")

with st.form("pilot_form"):
    industry = st.text_input("Industry / company type", placeholder="e.g., 40-person fashion retailer")
    use_case = st.text_input("AI use case to test", placeholder="e.g., draft replies to common customer-service emails")
    target_user = st.text_input("Pilot participant role and number", placeholder="e.g., five customer-service associates")
    duration_weeks = st.number_input("Pilot duration (weeks)", min_value=1, max_value=12, value=2)
    pain_point = st.text_area("Current pain point", placeholder="e.g., agents spend too long drafting repetitive replies")
    constraint = st.text_area("One constraint", placeholder="e.g., no customer names or order details may be sent to the model")
    start_date = st.date_input("Pilot start date", value=date.today())
    submitted = st.form_submit_button("Generate draft pilot plan")

if submitted:
    payload = {
        "industry": industry, "use_case": use_case, "target_user": target_user,
        "duration_weeks": int(duration_weeks), "pain_point": pain_point,
        "constraint": constraint, "start_date": start_date.isoformat(),
    }
    errors = validate_input(payload)
    if errors:
        st.error("Please complete the required information: " + "; ".join(errors))
    elif not os.getenv("OPENROUTER_API_KEY"):
        st.error("OPENROUTER_API_KEY is not configured. Add it to your environment, then restart Streamlit.")
    else:
        try:
            provider = OpenRouterProvider()
            raw = provider.generate(build_structured_messages(payload))
            plan = parse_plan(raw)
            st.warning("Draft only: a human project owner must review and approve this plan before any pilot begins.")
            for key, label in [
                ("objective", "Objective"), ("test_group", "Test group"),
                ("stages", "Dated stages"), ("success_metric", "Success metric"),
                ("feedback_instrument", "Feedback instrument"), ("risks_and_mitigations", "Risks and mitigations"),
                ("human_approval_checkpoint", "Human approval checkpoint"),
            ]:
                st.subheader(label)
                value = plan.get(key, "Not provided")
                if isinstance(value, (dict, list)):
                    st.json(value)
                else:
                    st.write(value)
            with st.expander("Technical record"):
                st.code(json.dumps({"model": provider.model, "estimated_cost_usd": provider.last_cost_usd}, indent=2))
        except ProviderError as exc:
            st.error(f"The model request failed: {exc}")
