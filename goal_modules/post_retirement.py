"""Goal Module B — Post-Retirement Income Planning"""

import streamlit as st


def render(ss: dict) -> dict:
    """Render post-retirement planning form. Returns dict of answers."""
    st.markdown('<div class="section-title">Post-Retirement Income Planning</div>', unsafe_allow_html=True)

    data = ss.get("post_retirement", {})

    _pp = int(data.get("passive_pension_income", 0))
    passive_pension_income = st.number_input(
        "Total monthly passive + pension income (Rs.)",
        min_value=0, value=_pp if _pp else None,
        placeholder="Enter amount", step=1000, key="pr_passive_pension",
    )
    _le = int(data.get("living_expenses", 0))
    living_expenses = st.number_input(
        "Monthly living expenses (Rs.)",
        min_value=0, value=_le if _le else None,
        placeholder="Enter amount", step=1000, key="pr_living_expenses",
    )
    _de = int(data.get("discretionary_expenses", 0))
    discretionary_expenses = st.number_input(
        "Annual discretionary expenses (Rs.)",
        min_value=0, value=_de if _de else None,
        placeholder="Enter amount", step=5000, key="pr_discretionary",
    )
    other_instruments = st.text_input(
        "Value of other financial instruments (FD, stocks, PMS, etc.)",
        value=data.get("other_instruments", ""),
        placeholder="e.g., FD: 5L, Stocks: 10L",
        key="pr_other_instruments",
    )

    return {
        "passive_pension_income": passive_pension_income or 0,
        "living_expenses": living_expenses or 0,
        "discretionary_expenses": discretionary_expenses or 0,
        "other_instruments": other_instruments,
    }
