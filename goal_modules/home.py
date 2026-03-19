"""Goal Module D — Home Purchase"""

import streamlit as st
from config import HOME_PURCHASE_YEARS, DOWN_PAYMENT_OPTIONS


def render(ss: dict) -> dict:
    """Render home purchase form. Returns dict of answers."""
    st.markdown('<div class="section-title">Home Purchase</div>', unsafe_allow_html=True)

    data = ss.get("home", {})

    purchase_year = st.selectbox(
        "Expected purchase year",
        options=HOME_PURCHASE_YEARS,
        index=HOME_PURCHASE_YEARS.index(data["purchase_year"]) if data.get("purchase_year") in HOME_PURCHASE_YEARS else 0,
        key="home_purchase_year",
    )
    value = st.number_input(
        "Estimated home value in today's prices (Rs.)",
        min_value=0, value=int(data.get("value", 0)),
        step=100000, key="home_value",
    )
    flexibility = st.slider(
        "Flexibility to shift purchase timeline (years)",
        min_value=0, max_value=5,
        value=int(data.get("flexibility", 0)),
        key="home_flexibility",
    )
    loan = st.radio(
        "Open to a home loan?",
        options=["Yes", "No"],
        index=0 if data.get("loan", "Yes") == "Yes" else 1,
        key="home_loan", horizontal=True,
    )

    down_payment = ""
    if loan == "Yes":
        down_payment = st.select_slider(
            "Estimated down payment %",
            options=DOWN_PAYMENT_OPTIONS,
            value=data.get("down_payment", "10%"),
            key="home_down_payment",
        )

    monthly_rent = st.number_input(
        "Current monthly rent (Rs.)",
        min_value=0, value=int(data.get("monthly_rent", 0)),
        step=1000, key="home_rent",
        help="Applicable only if buying this home will offset your rent.",
    )

    return {
        "purchase_year": purchase_year,
        "value": value,
        "flexibility": flexibility,
        "loan": loan,
        "down_payment": down_payment,
        "monthly_rent": monthly_rent,
    }
