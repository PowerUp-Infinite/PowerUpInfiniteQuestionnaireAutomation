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

HEADER_IMAGE_PATH = "Header image.png"

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
    "No Fixed Goal",
    "Other",
]
GOALS_RETIRED = [
    "Post-Retirement Income Planning",
    "Wealth Conservation",
    "Home Purchase",
    "Children Education",
    "Vehicle Purchase",
    "Children Marriage",
    "No Fixed Goal",
    "Other",
]

# Goals that do NOT trigger a goal-specific module form
GOALS_WITHOUT_MODULE = {"No Fixed Goal", "Wealth Conservation", "Other"}

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
    "Yes — fully covered without strain",
    "Just about managing",
    "No — struggling to service them",
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

# Short labels used in the radio (map by index to PORTFOLIO_PREFERENCE_OPTIONS)
PORTFOLIO_SHORT_LABELS = [
    "Safe Growth",
    "Slow & Steady",
    "Balanced Growth",
    "High Growth",
]

# Captions shown below each portfolio radio option
PORTFOLIO_CAPTIONS = [
    "Very Low Risk · ~6% p.a. · Worst -1% / Best +10%",
    "Low Risk · ~9% p.a. · Worst -3% / Best +15%",
    "Moderate Risk · ~12% p.a. · Worst -7% / Best +20%",
    "High Risk · ~15% p.a. · Worst -10% / Best +25%",
]

INVESTMENT_HORIZON_OPTIONS = [
    "Short-term (less than 3 years)",
    "Medium-term (3-5 years)",
    "Medium to long-term (5-8 years)",
    "Long-term (more than 8 years)",
]

FALL_REACTION_OPTIONS = [
    "Exit all investments immediately",
    "Exit partially",
    "Stay invested",
    "Invest more",
]

FALL_REACTION_CAPTIONS = [
    "To prevent further loss",
    "Shift to safer options",
    "I'm comfortable with market fluctuations",
    "I will average my cost",
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
    /* Force light background — overrides phone dark mode */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
    }
    [data-testid="stSidebar"] { background-color: #f8fafc !important; }

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
        padding-top: 1rem !important;
    }

    /* Header area — full-width banner image */
    .logo-header {
        text-align: center;
        padding: 0.5rem 0 0 0;
    }
    .logo-header img {
        width: 100%;
        max-width: 520px;
        height: auto;
        border-radius: 12px;
        object-fit: contain;
        margin-bottom: 0.35rem;
    }
    .logo-subtitle {
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a56db;
        letter-spacing: 1px;
        margin: 0.4rem 0 0.8rem 0;
        text-transform: uppercase;
    }

    /* Progress bar track + fill */
    .stProgress > div > div {
        background-color: #dbeafe !important;
        border-radius: 999px;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1a56db, #3b82f6) !important;
        border-radius: 999px;
        transition: width 0.45s ease;
    }

    /* Section cards */
    .section-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        animation: fadeInUp 0.3s ease-out;
    }
    .section-title {
        color: #1a56db;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #dbeafe;
    }

    /* Navigation buttons */
    div.stButton > button {
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
        background-color: #ffffff;
        color: #1a56db;
        border: 1.5px solid #1a56db;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(26,86,219,0.18);
        background-color: #eef2ff;
    }
    div.stButton > button[kind="primary"] {
        background-color: #1a56db !important;
        color: #ffffff !important;
        border: none !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1e40af !important;
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

    /* Thank-you header */
    .main-header {
        background: linear-gradient(135deg, #1a56db 0%, #1e40af 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white !important;
        text-align: center;
    }
    .main-header h1 { margin: 0; font-size: 2rem; font-weight: 700; color: white !important; }
    .main-header p  { margin: 0.25rem 0 0 0; font-size: 1rem; opacity: 0.9; color: white !important; }

    /* Radio spacing */
    div[data-baseweb="radio"] > div { gap: 0.2rem; }

    /* ── Nav button order ──
       Desktop: natural order → Previous col1 (left), Next col2 (right). ✅
       Mobile (<640px): columns stack → Previous on top by default.
       Fix: reverse ALL stacked column blocks on mobile so Next/Submit
       appears above Previous. */
    .nav-marker { display: none; }
    @media (max-width: 639px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column-reverse !important;
        }
    }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
"""
