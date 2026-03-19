"""Goal Module A — Retirement Planning"""

import streamlit as st
from config import EXPENSE_CHANGE_OPTIONS, YOY_INCREASE_OPTIONS


def render(ss: dict) -> dict:
    """Render retirement planning form. Returns dict of answers."""
    st.markdown('<div class="section-title">Retirement Planning</div>', unsafe_allow_html=True)

    data = ss.get("retirement", {})

    _mi = int(data.get("monthly_income", 0))
    monthly_income = st.number_input(
        "Current monthly income (Rs.)",
        min_value=0, value=_mi if _mi else None,
        placeholder="Enter amount", step=1000, key="ret_monthly_income",
    )
    _me = int(data.get("monthly_expenses", 0))
    monthly_expenses = st.number_input(
        "Current monthly expenses (Rs.)",
        min_value=0, value=_me if _me else None,
        placeholder="Enter amount", step=1000, key="ret_monthly_expenses",
    )
    expense_change = st.select_slider(
        "Expected change in expenses post-retirement",
        options=EXPENSE_CHANGE_OPTIONS,
        value=data.get("expense_change", "0%"),
        key="ret_expense_change",
    )
    _minv = int(data.get("monthly_investment", 0))
    monthly_investment = st.number_input(
        "Current monthly investment (Rs.)",
        min_value=0, value=_minv if _minv else None,
        placeholder="Enter amount", step=1000, key="ret_monthly_investment",
    )
    yoy_increase = st.select_slider(
        "Expected year-on-year increase in investment",
        options=YOY_INCREASE_OPTIONS,
        value=data.get("yoy_increase", "0%"),
        key="ret_yoy_increase",
    )
    other_investments = st.text_input(
        "Value of other financial investments (FD, stocks, PMS, etc.)",
        value=data.get("other_investments", ""),
        placeholder="e.g., FD: 5L, Stocks: 10L, PMS: 15L",
        key="ret_other_investments",
    )
    liabilities_detail = st.text_area(
        "Liabilities detail",
        value=data.get("liabilities_detail", ""),
        placeholder="Home Loan: Monthly EMI - Rs XXXXX, Ending year - 20XX",
        key="ret_liabilities_detail",
    )

    return {
        "monthly_income": monthly_income or 0,
        "monthly_expenses": monthly_expenses or 0,
        "expense_change": expense_change,
        "monthly_investment": monthly_investment or 0,
        "yoy_increase": yoy_increase,
        "other_investments": other_investments,
        "liabilities_detail": liabilities_detail,
    }
