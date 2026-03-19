"""Goal Module A — Retirement Planning"""

import streamlit as st
from config import EXPENSE_CHANGE_OPTIONS, YOY_INCREASE_OPTIONS


def render(ss: dict) -> dict:
    """Render retirement planning form. Returns dict of answers."""
    st.markdown('<div class="section-title">Retirement Planning</div>', unsafe_allow_html=True)

    data = ss.get("retirement", {})

    monthly_income = st.number_input(
        "Current monthly income (Rs.)",
        min_value=0, value=int(data.get("monthly_income", 0)),
        step=1000, key="ret_monthly_income",
    )
    monthly_expenses = st.number_input(
        "Current monthly expenses (Rs.)",
        min_value=0, value=int(data.get("monthly_expenses", 0)),
        step=1000, key="ret_monthly_expenses",
    )
    expense_change = st.select_slider(
        "Expected change in expenses post-retirement",
        options=EXPENSE_CHANGE_OPTIONS,
        value=data.get("expense_change", "0%"),
        key="ret_expense_change",
    )
    monthly_investment = st.number_input(
        "Current monthly investment (Rs.)",
        min_value=0, value=int(data.get("monthly_investment", 0)),
        step=1000, key="ret_monthly_investment",
    )
    yoy_increase = st.select_slider(
        "Expected year-on-year increase in investment",
        options=YOY_INCREASE_OPTIONS,
        value=data.get("yoy_increase", "0%"),
        key="ret_yoy_increase",
    )
    other_investments = st.number_input(
        "Value of other financial investments (Rs.)",
        min_value=0, value=int(data.get("other_investments", 0)),
        step=10000, key="ret_other_investments",
    )
    liabilities_detail = st.text_area(
        "Liabilities detail",
        value=data.get("liabilities_detail", ""),
        placeholder="Home Loan: Monthly EMI - Rs XXXXX, Ending year - 20XX",
        key="ret_liabilities_detail",
    )

    return {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "expense_change": expense_change,
        "monthly_investment": monthly_investment,
        "yoy_increase": yoy_increase,
        "other_investments": other_investments,
        "liabilities_detail": liabilities_detail,
    }
