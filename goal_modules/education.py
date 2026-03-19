"""Goal Module E — Children Education"""

import streamlit as st
from config import EDUCATION_YEARS, MAX_CHILDREN


def render(ss: dict) -> dict:
    """Render children education form. Returns dict of answers."""
    st.markdown('<div class="section-title">Children Education Planning</div>', unsafe_allow_html=True)

    data = ss.get("education", {})

    num_children = st.selectbox(
        "How many children's education do you want to plan for?",
        options=list(range(1, MAX_CHILDREN + 1)),
        index=max(0, int(data.get("num_children", 1)) - 1),
        key="edu_num_children",
    )

    result = {"num_children": num_children}

    for i in range(1, num_children + 1):
        st.markdown(f"**Child {i} Education**")
        child_data = data.get(f"child_{i}", {})

        col1, col2 = st.columns(2)
        with col1:
            ug_year = st.selectbox(
                f"Child {i} — UG start year",
                options=EDUCATION_YEARS,
                index=EDUCATION_YEARS.index(child_data["ug_year"]) if child_data.get("ug_year") in EDUCATION_YEARS else 0,
                key=f"edu_c{i}_ug_year",
            )
            pg_year = st.selectbox(
                f"Child {i} — PG start year",
                options=EDUCATION_YEARS,
                index=EDUCATION_YEARS.index(child_data["pg_year"]) if child_data.get("pg_year") in EDUCATION_YEARS else 0,
                key=f"edu_c{i}_pg_year",
            )
        with col2:
            _uc = int(child_data.get("ug_cost", 0))
            ug_cost = st.number_input(
                f"Child {i} — Estimated UG cost today (Rs.)",
                min_value=0, value=_uc if _uc else None,
                placeholder="Enter amount", step=50000, key=f"edu_c{i}_ug_cost",
            )
            _pc = int(child_data.get("pg_cost", 0))
            pg_cost = st.number_input(
                f"Child {i} — Estimated PG cost today (Rs., 0 if N/A)",
                min_value=0, value=_pc if _pc else None,
                placeholder="Enter amount", step=50000, key=f"edu_c{i}_pg_cost",
            )

        result[f"child_{i}"] = {
            "ug_year": ug_year,
            "ug_cost": ug_cost or 0,
            "pg_year": pg_year,
            "pg_cost": pg_cost or 0,
        }

    return result
