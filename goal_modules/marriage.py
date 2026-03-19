"""Goal Module F — Children Marriage"""

import streamlit as st
from config import MAX_CHILDREN


def render(ss: dict) -> dict:
    """Render children marriage form. Returns dict of answers."""
    st.markdown('<div class="section-title">Children Marriage Planning</div>', unsafe_allow_html=True)

    data = ss.get("marriage", {})

    num_children = st.selectbox(
        "How many children's marriage do you want to plan for?",
        options=list(range(1, MAX_CHILDREN + 1)),
        index=max(0, int(data.get("num_children", 1)) - 1),
        key="mar_num_children",
    )

    result = {"num_children": num_children}

    for i in range(1, num_children + 1):
        st.markdown(f"**Child {i} Marriage**")
        child_data = data.get(f"child_{i}", {})

        name = st.text_input(
            f"Child {i} — Name",
            value=child_data.get("name", ""),
            key=f"mar_c{i}_name",
        )
        timeframe = st.text_input(
            f"Child {i} — Expected marriage timeframe",
            value=child_data.get("timeframe", ""),
            placeholder="e.g., 12-14 years",
            key=f"mar_c{i}_timeframe",
        )
        _mb = int(child_data.get("budget", 0))
        budget = st.number_input(
            f"Child {i} — Estimated budget in today's value (Rs.)",
            min_value=0, value=_mb if _mb else None,
            placeholder="Enter amount", step=50000, key=f"mar_c{i}_budget",
        )

        result[f"child_{i}"] = {
            "name": name,
            "timeframe": timeframe,
            "budget": budget or 0,
        }

    return result
