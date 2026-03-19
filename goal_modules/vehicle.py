"""Goal Module C — Vehicle Purchase"""

import streamlit as st
from config import VEHICLE_PURCHASE_YEARS, DOWN_PAYMENT_OPTIONS


def render(ss: dict) -> dict:
    """Render vehicle purchase form. Returns dict of answers."""
    st.markdown('<div class="section-title">Vehicle Purchase</div>', unsafe_allow_html=True)

    data = ss.get("vehicle", {})

    purchase_year = st.selectbox(
        "Expected purchase year",
        options=VEHICLE_PURCHASE_YEARS,
        index=VEHICLE_PURCHASE_YEARS.index(data["purchase_year"]) if data.get("purchase_year") in VEHICLE_PURCHASE_YEARS else 0,
        key="veh_purchase_year",
    )
    value = st.number_input(
        "Estimated vehicle value in today's prices (Rs.)",
        min_value=0, value=int(data.get("value", 0)),
        step=50000, key="veh_value",
    )
    flexibility = st.slider(
        "Flexibility to shift purchase timeline (years)",
        min_value=0, max_value=5,
        value=int(data.get("flexibility", 0)),
        key="veh_flexibility",
    )
    loan = st.radio(
        "Open to a vehicle loan?",
        options=["Yes", "No"],
        index=0 if data.get("loan", "Yes") == "Yes" else 1,
        key="veh_loan", horizontal=True,
    )

    down_payment = ""
    if loan == "Yes":
        down_payment = st.select_slider(
            "Estimated down payment %",
            options=DOWN_PAYMENT_OPTIONS,
            value=data.get("down_payment", "10%"),
            key="veh_down_payment",
        )

    return {
        "purchase_year": purchase_year,
        "value": value,
        "flexibility": flexibility,
        "loan": loan,
        "down_payment": down_payment,
    }
