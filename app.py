"""
PowerUp Infinite — Streamlit Multi-Step Questionnaire
Main application entry point.
"""

import base64
from pathlib import Path

import streamlit as st

from config import (
    APP_TITLE, CUSTOM_CSS, STEP_LABELS, HEADER_IMAGE_PATH,
    LABEL_NAME, LABEL_EMAIL, AGE_OPTIONS,
    EMPLOYMENT_DESCRIPTIONS,
    INCOME_DESCRIPTIONS,
    LIABILITY_OPTIONS, LIABILITY_CAPTIONS,
    FORESEE_LIABILITY_OPTIONS, FORESEE_LIABILITY_CAPTIONS,
    MANAGE_LIABILITY_OPTIONS, MANAGE_LIABILITY_CAPTIONS,
    EMERGENCY_FUND_OPTIONS, PORTFOLIO_PREFERENCE_OPTIONS,
    PORTFOLIO_SHORT_LABELS, PORTFOLIO_CAPTIONS,
    INVESTMENT_HORIZON_OPTIONS, FALL_REACTION_OPTIONS, FALL_REACTION_CAPTIONS,
    GOAL_MODULE_MAP, GOALS_WITHOUT_MODULE,
)
from logic import (
    get_employment_options, get_income_options, get_goal_options,
    get_goal_modules, has_no_liabilities, should_skip_all_goal_modules,
    should_show_retirement_module, should_show_post_retirement_module,
    is_retired_status, validate_email,
)
from sheets_writer import write_to_sheet
from goal_modules import retirement, post_retirement, vehicle, home, education, marriage

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title=APP_TITLE, page_icon="📊", layout="centered")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Number of fixed (non-goal) steps: 0-8 = 9 steps
FIXED_STEPS = 9

# ── Module registry ──────────────────────────────────────────────────────────
MODULE_RENDERERS = {
    "retirement": retirement,
    "post_retirement": post_retirement,
    "vehicle": vehicle,
    "home": home,
    "education": education,
    "marriage": marriage,
}

MODULE_TITLES = {
    "retirement": "Retirement Planning",
    "post_retirement": "Post-Retirement Income Planning",
    "vehicle": "Vehicle Purchase",
    "home": "Home Purchase",
    "education": "Children Education",
    "marriage": "Children Marriage",
}


# ═════════════════════════════════════════════════════════════════════════════
# Session-state initialisation
# ═════════════════════════════════════════════════════════════════════════════
def _init_state():
    defaults = {
        "step": 0,
        "name": "",
        "email": "",
        "age": None,
        "employment": None,
        "income_source": None,
        "goals": [],
        "other_goal_text": "",
        "liability_type": None,
        "liability_followup": None,
        # Risk profile (split across steps 6-8)
        "emergency_fund": None,
        "portfolio_preference": None,
        "investment_horizon": None,
        "fall_reaction": None,
        "lumpsum_amount": 0,
        "sip_amount": 0,
        "sip_age": 0,
        "other_investments": "",
        # Goal modules (dicts)
        "retirement": {},
        "post_retirement": {},
        "vehicle": {},
        "home": {},
        "education": {},
        "marriage": {},
        # Bookkeeping
        "submitted": False,
        "submit_timestamp": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()


# ═════════════════════════════════════════════════════════════════════════════
# Helpers
# ═════════════════════════════════════════════════════════════════════════════
def _active_goal_modules() -> list[str]:
    """Return ordered list of goal-module keys that apply to this user."""
    goals = st.session_state.get("goals", [])
    employment = st.session_state.get("employment", "")
    modules = []

    # Retirement planning is shown for non-retired users UNLESS they only picked "No Fixed Goal"
    only_no_fixed = all(g in GOALS_WITHOUT_MODULE for g in goals)
    if employment and not is_retired_status(employment) and not only_no_fixed:
        modules.append("retirement")

    for goal in goals:
        if goal in GOALS_WITHOUT_MODULE:
            continue
        key = GOAL_MODULE_MAP.get(goal)
        if key is None:
            continue
        if key == "retirement":
            continue  # already handled above
        if key == "post_retirement" and not should_show_post_retirement_module(goals, employment):
            continue
        if key not in modules:
            modules.append(key)
    return modules


def _total_steps() -> int:
    """9 fixed steps + N goal modules + 1 summary."""
    return FIXED_STEPS + len(_active_goal_modules()) + 1


def _step_label(step_idx: int) -> str:
    if step_idx < FIXED_STEPS:
        return STEP_LABELS[step_idx]
    goal_mods = _active_goal_modules()
    goal_offset = step_idx - FIXED_STEPS
    if goal_offset < len(goal_mods):
        return MODULE_TITLES.get(goal_mods[goal_offset], "Goal Details")
    return "Summary & Submit"


def _clear_deselected_goals():
    """If user went back and changed goals, wipe data for modules no longer active."""
    active = set(_active_goal_modules())
    for key in MODULE_RENDERERS:
        if key not in active:
            st.session_state[key] = {}


# ═════════════════════════════════════════════════════════════════════════════
# Navigation
# ═════════════════════════════════════════════════════════════════════════════
def _go_next():
    st.session_state.step += 1


def _go_prev():
    st.session_state.step = max(0, st.session_state.step - 1)


def _go_to(step: int):
    st.session_state.step = step


def _nav_buttons(step_key: str, on_next=None, prev=True):
    """
    Render Previous / Next buttons.
    Col1 = Previous (left on desktop), Col2 = Next (right on desktop).
    Mobile: columns stack vertically → Previous top, Next below.
    CSS nav-marker + column-reverse flips the stack on mobile so Next is on top.
    """
    st.markdown('<span class="nav-marker"></span>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if prev:
            if st.button("← Previous", use_container_width=True, key=f"btn_prev_{step_key}"):
                _go_prev()
                st.rerun()
    with col2:
        if st.button("Next →", use_container_width=True, key=f"btn_next_{step_key}"):
            if on_next is None or on_next():
                _go_next()
                st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# Header + progress
# ═════════════════════════════════════════════════════════════════════════════
@st.cache_data
def _load_logo_b64() -> str:
    """Load the header image as a base64 string (cached)."""
    img_path = Path(__file__).parent / HEADER_IMAGE_PATH
    data = img_path.read_bytes()
    return base64.b64encode(data).decode()


def _render_header():
    logo_b64 = _load_logo_b64()
    st.markdown(
        f'<div class="logo-header">'
        f'<img src="data:image/png;base64,{logo_b64}" alt="PowerUp Infinite">'
        f'</div>'
        f'<div class="logo-subtitle">Infinite Questionnaire</div>',
        unsafe_allow_html=True,
    )
    total = _total_steps()
    current = min(st.session_state.step, total - 1)
    progress = (current + 1) / total
    st.progress(progress)
    st.caption(f"Step {current + 1} of {total} — {_step_label(current)}")


# ═════════════════════════════════════════════════════════════════════════════
# STEP RENDERERS
# ═════════════════════════════════════════════════════════════════════════════

# ── Step 0: Personal Info ────────────────────────────────────────────────────
def _step_personal_info():
    st.markdown('<div class="section-title">Personal Information</div>', unsafe_allow_html=True)

    name = st.text_input(LABEL_NAME, value=st.session_state.name, key="inp_name")
    email = st.text_input(LABEL_EMAIL, value=st.session_state.email, key="inp_email")

    def _validate():
        if not name.strip():
            st.error("Please enter your name.")
            return False
        if not validate_email(email.strip()):
            st.error("Please enter a valid email address (must contain @).")
            return False
        st.session_state.name = name.strip()
        st.session_state.email = email.strip()
        return True

    _nav_buttons("0", on_next=_validate, prev=False)


# ── Step 1: Age ──────────────────────────────────────────────────────────────
def _step_age():
    st.markdown('<div class="section-title">Age Group</div>', unsafe_allow_html=True)

    current = st.session_state.age
    idx = AGE_OPTIONS.index(current) if current in AGE_OPTIONS else None
    age = st.radio("What is your age group?", AGE_OPTIONS, index=idx, key="inp_age")

    def _validate():
        if age is None:
            st.error("Please select an age group.")
            return False
        if st.session_state.age != age:
            st.session_state.employment = None
            st.session_state.income_source = None
            st.session_state.goals = []
        st.session_state.age = age
        return True

    _nav_buttons("1", on_next=_validate)


# ── Step 2: Employment ───────────────────────────────────────────────────────
def _step_employment():
    st.markdown('<div class="section-title">Employment Status</div>', unsafe_allow_html=True)

    options = get_employment_options(st.session_state.age)
    captions = [EMPLOYMENT_DESCRIPTIONS.get(opt, "") for opt in options]
    current = st.session_state.employment
    idx = options.index(current) if current in options else None
    emp = st.radio("What is your current employment status?", options, index=idx, captions=captions, key="inp_emp")

    def _validate():
        if emp is None:
            st.error("Please select your employment status.")
            return False
        if st.session_state.employment != emp:
            st.session_state.income_source = None
            st.session_state.goals = []
        st.session_state.employment = emp
        return True

    _nav_buttons("2", on_next=_validate)


# ── Step 3: Income Source ────────────────────────────────────────────────────
def _step_income():
    st.markdown('<div class="section-title">Primary Income Source</div>', unsafe_allow_html=True)

    options = get_income_options(st.session_state.employment)
    captions = [INCOME_DESCRIPTIONS.get(opt, "") for opt in options]
    current = st.session_state.income_source
    idx = options.index(current) if current in options else None
    inc = st.radio("What is your primary source of income?", options, index=idx, captions=captions, key="inp_income")

    def _validate():
        if inc is None:
            st.error("Please select your income source.")
            return False
        st.session_state.income_source = inc
        return True

    _nav_buttons("3", on_next=_validate)


# ── Step 4: Investment Goals ─────────────────────────────────────────────────
def _step_goals():
    st.markdown('<div class="section-title">Investment Goals</div>', unsafe_allow_html=True)

    options = get_goal_options(st.session_state.employment)
    current = st.session_state.goals

    st.write("Select your investment goals (choose all that apply)")
    goals = []
    for opt in options:
        checked = st.checkbox(opt, value=(opt in current), key=f"goal_{opt}")
        if checked:
            goals.append(opt)

    other_text = ""
    if "Other" in goals:
        other_text = st.text_input(
            "Please specify your other goal",
            value=st.session_state.other_goal_text, key="inp_other_goal",
        )

    def _validate():
        if not goals:
            st.error("Please select at least one investment goal.")
            return False
        if "Other" in goals and not other_text.strip():
            st.error("Please specify your other goal.")
            return False
        st.session_state.goals = goals
        st.session_state.other_goal_text = other_text.strip()
        _clear_deselected_goals()
        return True

    _nav_buttons("4", on_next=_validate)


# ── Step 5: Liabilities ─────────────────────────────────────────────────────
def _step_liabilities():
    st.markdown('<div class="section-title">Liabilities</div>', unsafe_allow_html=True)

    current_type = st.session_state.liability_type
    idx = LIABILITY_OPTIONS.index(current_type) if current_type in LIABILITY_OPTIONS else None

    liability = st.radio(
        "What types of liabilities do you have?",
        LIABILITY_OPTIONS, captions=LIABILITY_CAPTIONS, index=idx, key="inp_liability",
    )

    followup_answer = None
    if liability == "None":
        current_fu = st.session_state.liability_followup
        fu_idx = FORESEE_LIABILITY_OPTIONS.index(current_fu) if current_fu in FORESEE_LIABILITY_OPTIONS else None
        followup_answer = st.radio(
            "Do you foresee any of Financial or Dependable liability in near future? (Next 2/3 yrs)",
            FORESEE_LIABILITY_OPTIONS, captions=FORESEE_LIABILITY_CAPTIONS, index=fu_idx, key="inp_foresee",
        )
    elif liability is not None:
        current_fu = st.session_state.liability_followup
        fu_idx = MANAGE_LIABILITY_OPTIONS.index(current_fu) if current_fu in MANAGE_LIABILITY_OPTIONS else None
        followup_answer = st.radio(
            "Can you comfortably meet your liabilities from your current income?",
            MANAGE_LIABILITY_OPTIONS, captions=MANAGE_LIABILITY_CAPTIONS, index=fu_idx, key="inp_manage",
        )

    def _validate():
        if liability is None:
            st.error("Please select a liability option.")
            return False
        if followup_answer is None:
            st.error("Please answer the follow-up question.")
            return False
        st.session_state.liability_type = liability
        st.session_state.liability_followup = followup_answer
        return True

    _nav_buttons("5", on_next=_validate)


# ── Step 6: Risk Appetite (Emergency Fund + Portfolio Preference) ────────────
def _step_risk_appetite():
    ss = st.session_state

    st.markdown('<div class="section-title">Risk Appetite</div>', unsafe_allow_html=True)

    ef_idx = EMERGENCY_FUND_OPTIONS.index(ss.emergency_fund) if ss.emergency_fund in EMERGENCY_FUND_OPTIONS else None
    emergency_fund = st.radio(
        "How many months of emergency fund do you maintain?",
        EMERGENCY_FUND_OPTIONS, index=ef_idx, key="inp_ef",
    )

    st.divider()

    # Map current stored preference → short label index
    cur_pref = ss.portfolio_preference
    if cur_pref in PORTFOLIO_PREFERENCE_OPTIONS:
        short_idx = PORTFOLIO_PREFERENCE_OPTIONS.index(cur_pref)
    else:
        short_idx = None

    chosen_short = st.radio(
        "How would you like your portfolio to grow?",
        PORTFOLIO_SHORT_LABELS,
        captions=PORTFOLIO_CAPTIONS,
        index=short_idx,
        key="inp_pp",
    )

    def _validate():
        if emergency_fund is None:
            st.error("Please select how many months of emergency fund you maintain.")
            return False
        if chosen_short is None:
            st.error("Please select your portfolio growth preference.")
            return False
        ss.emergency_fund = emergency_fund
        # Store the full option string (for Sheets) by mapping from short label
        idx = PORTFOLIO_SHORT_LABELS.index(chosen_short)
        ss.portfolio_preference = PORTFOLIO_PREFERENCE_OPTIONS[idx]
        return True

    _nav_buttons("6", on_next=_validate)


# ── Step 7: Investment Outlook (Horizon + Fall Reaction) ─────────────────────
def _step_investment_outlook():
    ss = st.session_state

    st.markdown('<div class="section-title">Investment Outlook</div>', unsafe_allow_html=True)

    ih_idx = INVESTMENT_HORIZON_OPTIONS.index(ss.investment_horizon) if ss.investment_horizon in INVESTMENT_HORIZON_OPTIONS else None
    invest_horizon = st.radio(
        "What is your investment horizon?",
        INVESTMENT_HORIZON_OPTIONS, index=ih_idx, key="inp_ih",
    )

    st.divider()

    fr_idx = FALL_REACTION_OPTIONS.index(ss.fall_reaction) if ss.fall_reaction in FALL_REACTION_OPTIONS else None
    fall_react = st.radio(
        "If your investments fall by 20% within a few months, what would you do?",
        FALL_REACTION_OPTIONS, captions=FALL_REACTION_CAPTIONS, index=fr_idx, key="inp_fr",
    )

    def _validate():
        if invest_horizon is None:
            st.error("Please select your investment horizon.")
            return False
        if fall_react is None:
            st.error("Please select how you'd react to a market fall.")
            return False
        ss.investment_horizon = invest_horizon
        ss.fall_reaction = fall_react
        return True

    _nav_buttons("7", on_next=_validate)


# ── Step 8: Investment Details (Amounts) ─────────────────────────────────────
def _step_investment_details():
    ss = st.session_state

    st.markdown('<div class="section-title">Investment Details</div>', unsafe_allow_html=True)

    lumpsum = st.number_input(
        "Lumpsum amount you wish to invest with Infinite (Rs.)",
        min_value=0,
        value=None if int(ss.lumpsum_amount) == 0 else int(ss.lumpsum_amount),
        placeholder="Enter amount",
        step=10000, key="inp_lumpsum",
    )
    sip = st.number_input(
        "Monthly SIP amount you wish to invest with Infinite (Rs.)",
        min_value=0,
        value=None if int(ss.sip_amount) == 0 else int(ss.sip_amount),
        placeholder="Enter amount",
        step=1000, key="inp_sip",
    )
    sip_age = st.number_input(
        "Till what age do you plan to continue SIPs?",
        min_value=0,
        value=None if int(ss.sip_age) == 0 else int(ss.sip_age),
        placeholder="e.g. 60",
        step=1, key="inp_sip_age",
        help="By default considered until financial freedom or 60 years of age, whichever is earlier.",
    )
    other_inv = st.text_input(
        "Value of financial investments apart from mutual funds (FD, stocks, PMS, etc.)",
        value=ss.other_investments,
        placeholder="e.g., FD: 5L, Stocks: 10L, PMS: 15L",
        key="inp_other_inv",
    )

    def _save():
        if (lumpsum or 0) == 0 and (sip or 0) == 0:
            st.error("Please enter at least a lumpsum amount or a monthly SIP amount.")
            return False
        ss.lumpsum_amount = lumpsum or 0
        ss.sip_amount = sip or 0
        ss.sip_age = sip_age or 0
        ss.other_investments = other_inv
        return True

    _nav_buttons("8", on_next=_save)


# ── Goal Module Step ─────────────────────────────────────────────────────────
def _step_goal_module(module_key: str):
    renderer = MODULE_RENDERERS[module_key]
    result = renderer.render(dict(st.session_state))

    st.markdown('<span class="nav-marker"></span>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True, key=f"btn_prev_{module_key}"):
            st.session_state[module_key] = result
            _go_prev()
            st.rerun()
    with col2:
        if st.button("Next →", use_container_width=True, key=f"btn_next_{module_key}"):
            st.session_state[module_key] = result
            _go_next()
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# SUMMARY PAGE
# ═════════════════════════════════════════════════════════════════════════════
def _render_summary_section(title: str, items: list[tuple[str, str]]):
    rows = "".join(
        f'<p style="margin:0.2rem 0;"><strong>{label}:</strong> {value}</p>'
        for label, value in items if value
    )
    st.markdown(
        f'<div class="summary-group"><h4>{title}</h4>{rows}</div>',
        unsafe_allow_html=True,
    )


def _step_summary():
    ss = st.session_state

    st.markdown('<div class="section-title">Review Your Answers</div>', unsafe_allow_html=True)
    st.info("Please review all your answers below. Use the edit buttons to go back and change any section.")

    # Personal info
    _render_summary_section("Personal Information", [
        ("Name", ss.name),
        ("Email", ss.email),
    ])
    if st.button("Edit Personal Info", key="edit_0"):
        _go_to(0); st.rerun()

    # Demographics
    _render_summary_section("Demographics", [
        ("Age Group", ss.age),
        ("Employment Status", ss.employment),
        ("Income Source", ss.income_source),
    ])
    if st.button("Edit Demographics", key="edit_1"):
        _go_to(1); st.rerun()

    # Goals
    goals_str = ", ".join(ss.goals)
    if ss.other_goal_text:
        goals_str += f" (Other: {ss.other_goal_text})"
    _render_summary_section("Investment Goals", [
        ("Selected Goals", goals_str),
    ])
    if st.button("Edit Goals", key="edit_4"):
        _go_to(4); st.rerun()

    # Liabilities
    _render_summary_section("Liabilities", [
        ("Liability Type", ss.liability_type),
        ("Liability Outlook", ss.liability_followup),
    ])
    if st.button("Edit Liabilities", key="edit_5"):
        _go_to(5); st.rerun()

    # Risk profile (all 3 sub-steps shown together)
    _render_summary_section("Risk Profile", [
        ("Emergency Fund", ss.emergency_fund),
        ("Portfolio Preference", ss.portfolio_preference),
        ("Investment Horizon", ss.investment_horizon),
        ("Reaction to 20% Fall", ss.fall_reaction),
        ("Lumpsum Amount", f"Rs. {ss.lumpsum_amount:,}"),
        ("Monthly SIP", f"Rs. {ss.sip_amount:,}"),
        ("SIP Continuation Age", str(ss.sip_age) if ss.sip_age else ""),
        ("Other Investments", ss.other_investments if ss.other_investments else "—"),
    ])
    if st.button("Edit Risk Profile", key="edit_6"):
        _go_to(6); st.rerun()

    # Goal modules
    active_mods = _active_goal_modules()
    for i, mod_key in enumerate(active_mods):
        mod_data = ss.get(mod_key, {})
        title = MODULE_TITLES.get(mod_key, mod_key)
        items = []
        for k, v in mod_data.items():
            if isinstance(v, dict):
                for sk, sv in v.items():
                    items.append((f"{k} → {sk}", str(sv)))
            else:
                items.append((k.replace("_", " ").title(), str(v)))
        _render_summary_section(title, items)
        if st.button(f"Edit {title}", key=f"edit_goal_{mod_key}"):
            _go_to(FIXED_STEPS + i); st.rerun()

    st.divider()

    # Navigation
    st.markdown('<span class="nav-marker"></span>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True, key="btn_prev_summary"):
            _go_prev()
            st.rerun()
    with col2:
        if st.button("Submit ✓", use_container_width=True, type="primary", key="btn_submit"):
            _submit()


def _collect_data() -> dict:
    ss = st.session_state
    return {
        "name": ss.name,
        "email": ss.email,
        "age": ss.age,
        "employment": ss.employment,
        "income_source": ss.income_source,
        "goals": ss.goals,
        "other_goal_text": ss.other_goal_text,
        "liability_type": ss.liability_type,
        "liability_followup": ss.liability_followup,
        "emergency_fund": ss.emergency_fund,
        "portfolio_preference": ss.portfolio_preference,
        "investment_horizon": ss.investment_horizon,
        "fall_reaction": ss.fall_reaction,
        "lumpsum_amount": ss.lumpsum_amount,
        "sip_amount": ss.sip_amount,
        "sip_age": ss.sip_age,
        "other_investments": ss.other_investments,
        "retirement": ss.retirement,
        "post_retirement": ss.post_retirement,
        "vehicle": ss.vehicle,
        "home": ss.home,
        "education": ss.education,
        "marriage": ss.marriage,
    }


def _submit():
    data = _collect_data()
    try:
        ts = write_to_sheet(data)
        st.session_state.submitted = True
        st.session_state.submit_timestamp = ts
        st.rerun()
    except Exception as e:
        st.error(
            f"There was a problem saving your responses. Please try again.\n\n"
            f"Error details: {e}"
        )


def _render_success():
    st.balloons()
    st.markdown(
        '<div class="main-header">'
        '<h1>Thank You!</h1>'
        '<p>Your answers have been submitted successfully.</p>'
        '<p>Your circle manager will reach out to you soon.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.success(f"Submitted at: {st.session_state.submit_timestamp}")


# ═════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ═════════════════════════════════════════════════════════════════════════════
STEP_FUNCTIONS = {
    0: _step_personal_info,
    1: _step_age,
    2: _step_employment,
    3: _step_income,
    4: _step_goals,
    5: _step_liabilities,
    6: _step_risk_appetite,
    7: _step_investment_outlook,
    8: _step_investment_details,
}


def main():
    _render_header()

    if st.session_state.submitted:
        _render_success()
        return

    step = st.session_state.step
    total = _total_steps()

    # Clamp step
    if step >= total:
        st.session_state.step = total - 1
        step = total - 1

    # Fixed steps 0–8
    if step in STEP_FUNCTIONS:
        STEP_FUNCTIONS[step]()
    else:
        # Steps 9+: goal modules, then summary
        goal_mods = _active_goal_modules()
        goal_offset = step - FIXED_STEPS

        if goal_offset < len(goal_mods):
            _step_goal_module(goal_mods[goal_offset])
        else:
            _step_summary()


if __name__ == "__main__":
    main()
