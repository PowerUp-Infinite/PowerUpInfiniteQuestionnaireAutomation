"""Goal Module B — Post-Retirement Income Planning"""

import streamlit as st


def render(ss: dict) -> dict:
    """Render post-retirement planning form. Returns dict of answers."""
    st.markdown('<div class="section-title">Post-Retirement Income Planning</div>', unsafe_allow_html=True)

    data = ss.get("post_retirement", {})

    passive_pension_income = st.number_input(
        "Total monthly passive + pension income (Rs.)",
        min_value=0, value=int(data.get("passive_pension_income", 0)),
        step=1000, key="pr_passive_pension",
    )
    living_expenses = st.number_input(
        "Monthly living expenses (Rs.)",
        min_value=0, value=int(data.get("living_expenses", 0)),
        step=1000, key="pr_living_expenses",
    )
    discretionary_expenses = st.number_input(
        "Annual discretionary expenses (Rs.)",
        min_value=0, value=int(data.get("discretionary_expenses", 0)),
        step=5000, key="pr_discretionary",
    )
    other_instruments = st.number_input(
        "Value of other financial instruments (Rs.)",
        min_value=0, value=int(data.get("other_instruments", 0)),
        step=10000, key="pr_other_instruments",
    )

    return {
        "passive_pension_income": passive_pension_income,
        "living_expenses": living_expenses,
        "discretionary_expenses": discretionary_expenses,
        "other_instruments": other_instruments,
    }
