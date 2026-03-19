"""
PowerUp Infinite — Questionnaire Configuration
All question text, options, and descriptions live here as constants.
"""

# ── App Branding ──────────────────────────────────────────────────────────────
APP_TITLE = "PowerUp Infinite"
APP_SUBTITLE = "Mutual Fund Advisory — Client Questionnaire"

# ── Step labels (used in progress bar) ────────────────────────────────────────
STEP_LABELS = [
    "Personal Info",
    "Age",
    "Employment",
    "Income Source",
    "Investment Goals",
    "Liabilities",
    "Risk Appetite",
    "Investment Outlook",
    "Investment Details",
    # goal-specific steps are appended dynamically
    "Summary & Submit",
]

HEADER_IMAGE_PATH = "InfiniteImage.jpeg"

# ── Step 1 — Personal Info ────────────────────────────────────────────────────
LABEL_NAME = "Full Name"
LABEL_EMAIL = "Email Address"

# ── Step 2 — Age ─────────────────────────────────────────────────────────────
AGE_OPTIONS = ["<35", "36-45", "46-55", "56+"]

# ── Step 3 — Employment Status ───────────────────────────────────────────────
EMPLOYMENT_OPTIONS = {
    "<35": ["Actively Working", "Soon to be Retiring (within 5 yrs)"],
    "36-45": ["Actively Working", "Soon to be Retiring (within 5 yrs)"],
    "46-55": ["Actively Working", "Soon to be Retiring (within 5 yrs)", "Retired Early"],
    "56+": ["Actively Working", "Soon to be Retiring (within 5 yrs)", "Retired"],
}

EMPLOYMENT_DESCRIPTIONS = {
    "Actively Working": "You are currently employed or self-employed and earning regular active income.",
    "Soon to be Retiring (within 5 yrs)": "You plan to retire within the next 5 years and are transitioning out of active work.",
    "Retired Early": "You have retired before the traditional retirement age and no longer earn active income.",
    "Retired": "You have retired from active work and are in the post-retirement phase of life.",
}

# ── Step 4 — Primary Income Source ───────────────────────────────────────────
INCOME_OPTIONS_WORKING = [
    "Active Income Only",
    "Active + Passive Income",
]
INCOME_OPTIONS_RETIRED = [
    "Passive Income Only",
    "Pension Income Only",
    "Passive + Pension Income",
    "No Regular Source of Income",
]

INCOME_DESCRIPTIONS = {
    "Active Income Only": "Your entire income comes from salary, business, or freelance work.",
    "Active + Passive Income": "You earn from work plus passive sources like rent, dividends, or interest.",
    "Passive Income Only": "Your income comes entirely from investments, rent, dividends, or interest.",
    "Pension Income Only": "Your income comes entirely from pension or retirement benefits.",
    "Passive + Pension Income": "You receive both pension benefits and passive income from investments.",
    "No Regular Source of Income": "You do not have a regular or predictable source of income currently.",
}

# ── Step 5 — Investment Goals ────────────────────────────────────────────────
GOALS_WORKING = [
    "Retirement Planning",
    "Home Purchase",
    "Children Education",
    "Vehicle Purchase",
    "Children Marriage",
    "No Fixed Goal (Wealth Appreciation)",
    "Other",
]
GOALS_RETIRED = [
    "Post-Retirement Income Planning",
    "Wealth Conservation",
    "Home Purchase",
    "Children Education",
    "Vehicle Purchase",
    "Children Marriage",
    "No Fixed Goal (Wealth Appreciation)",
    "Other",
]

# Goals that do NOT trigger a goal-specific module form
GOALS_WITHOUT_MODULE = {"No Fixed Goal (Wealth Appreciation)", "Wealth Conservation", "Other"}

# ── Step 6 — Liabilities ────────────────────────────────────────────────────
LIABILITY_OPTIONS = [
    "None",
    "Financial Liabilities Only",
    "Dependent Liabilities Only",
    "Both Financial & Dependent Liabilities",
]

FORESEE_LIABILITY_OPTIONS = [
    "No, I don't foresee any",
    "Financial liabilities only",
    "Dependent liabilities only",
    "Both financial & dependent liabilities",
]

MANAGE_LIABILITY_OPTIONS = [
    "Yes — comfortably",
    "Just about managing",
    "No — struggling to meet them",
]

# ── Step 7 — Risk Profile Questions ─────────────────────────────────────────
EMERGENCY_FUND_OPTIONS = [
    "Up to 6 months",
    "7-12 months",
    "13-24 months",
    "More than 24 months",
]

PORTFOLIO_PREFERENCE_OPTIONS = [
    "Grow safely, even if returns are low — Very low risk, ~6% p.a., worst -1% / best +10%",
    "Grow slowly with some safety — Low risk, ~9% p.a., worst -3% / best +15%",
    "Grow well with some ups and downs — Moderate risk, ~12% p.a., worst -7% / best +20%",
    "Grow faster, even if it means high risk — High risk, ~15% p.a., worst -10% / best +25%",
]

INVESTMENT_HORIZON_OPTIONS = [
    "Short-term (less than 3 years)",
    "Medium-term (3-5 years)",
    "Medium to long-term (5-8 years)",
    "Long-term (more than 8 years)",
]

FALL_REACTION_OPTIONS = [
    "Exit all investments immediately",
    "Exit partially and hold the rest",
    "Stay invested and wait for recovery",
    "Invest more to take advantage of lower prices",
]

# ── Goal Module Labels ───────────────────────────────────────────────────────
# Mapping from goal name → module key used in session_state
GOAL_MODULE_MAP = {
    "Retirement Planning": "retirement",
    "Post-Retirement Income Planning": "post_retirement",
    "Vehicle Purchase": "vehicle",
    "Home Purchase": "home",
    "Children Education": "education",
    "Children Marriage": "marriage",
}

# ── Vehicle Module ───────────────────────────────────────────────────────────
VEHICLE_PURCHASE_YEARS = list(range(2026, 2042))  # 2026–2041
HOME_PURCHASE_YEARS = list(range(2026, 2047))      # 2026–2046
EDUCATION_YEARS = list(range(2026, 2061))           # 2026–2060

DOWN_PAYMENT_OPTIONS = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]

EXPENSE_CHANGE_OPTIONS = ["-40%", "-30%", "-20%", "-10%", "0%", "10%", "20%", "30%", "40%"]
YOY_INCREASE_OPTIONS = ["0%", "5%", "10%", "15%", "20%", "25%", "30%"]

MAX_CHILDREN = 4

# ── Custom CSS ───────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
    /* Brand colours */
    :root {
        --pu-blue: #1a56db;
        --pu-blue-light: #e8eefb;
        --pu-white: #ffffff;
    }

    /* Smooth fade-in for page content */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .block-container {
        animation: fadeInUp 0.35s ease-out;
    }

    /* Header area — logo + subtitle */
    .logo-header {
        text-align: center;
        padding: 1rem 0 0.25rem 0;
    }
    .logo-header img {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 0.35rem;
    }
    .logo-subtitle {
        text-align: center;
        font-size: 1.35rem;
        font-weight: 600;
        color: #1a56db;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }

    /* Progress bar override */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1a56db, #3b82f6);
        transition: width 0.4s ease;
    }

    /* Section cards */
    .section-card {
        background: var(--pu-white);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        animation: fadeInUp 0.3s ease-out;
    }
    .section-title {
        color: #1a56db;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e8eefb;
    }

    /* Navigation buttons */
    div.stButton > button {
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(26,86,219,0.15);
    }

    /* Summary section */
    .summary-group {
        background: #f8fafc;
        border-left: 4px solid #1a56db;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        border-radius: 0 8px 8px 0;
    }
    .summary-group h4 {
        color: #1a56db;
        margin: 0 0 0.5rem 0;
    }

    /* Thank-you header (reused on success) */
    .main-header {
        background: linear-gradient(135deg, #1a56db 0%, #1e40af 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .main-header h1 { margin: 0; font-size: 2rem; font-weight: 700; }
    .main-header p  { margin: 0.25rem 0 0 0; font-size: 1rem; opacity: 0.9; }

    /* Radio / select spacing */
    div[data-baseweb="radio"] > div { gap: 0.15rem; }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
