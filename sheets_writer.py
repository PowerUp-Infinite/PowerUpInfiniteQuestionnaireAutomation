"""
PowerUp Infinite — Google Sheets Writer
Writes one row per client submission to Google Sheets via gspread.
"""

from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

from config import MAX_CHILDREN

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def _get_client() -> gspread.Client:
    """Authenticate and return a gspread client using Streamlit secrets."""
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


def _get_sheet() -> gspread.Worksheet:
    """Open the configured spreadsheet and return Sheet1."""
    client = _get_client()
    spreadsheet_id = st.secrets["sheets"]["spreadsheet_id"]
    spreadsheet = client.open_by_key(spreadsheet_id)
    return spreadsheet.sheet1


# ── Header row (written once if sheet is empty) ─────────────────────────────
def _build_header() -> list[str]:
    headers = [
        "Timestamp", "Name", "Email", "Age", "Employment Status",
        "Income Source", "Goals", "Liability Type", "Liability Followup Answer",
        "Emergency Fund", "Portfolio Preference", "Investment Horizon",
        "Fall Reaction", "Lumpsum Amount", "SIP Amount",
        "SIP Continuation Age", "Other Investments Value",
        # Retirement
        "Ret: Monthly Income", "Ret: Monthly Expenses",
        "Ret: Expense Change %", "Ret: Monthly Investment",
        "Ret: YoY Investment Increase %", "Ret: Other Financial Investments",
        "Ret: Liabilities Detail",
        # Post-Retirement
        "PostRet: Passive+Pension Income", "PostRet: Living Expenses",
        "PostRet: Discretionary Expenses", "PostRet: Other Instruments",
        # Vehicle
        "Vehicle: Purchase Year", "Vehicle: Value",
        "Vehicle: Flexibility Yrs", "Vehicle: Loan Y/N",
        "Vehicle: Down Payment %",
        # Home
        "Home: Purchase Year", "Home: Value",
        "Home: Flexibility Yrs", "Home: Loan Y/N",
        "Home: Down Payment %", "Home: Monthly Rent",
    ]
    # Education — 4 children × 4 fields
    for i in range(1, MAX_CHILDREN + 1):
        headers += [
            f"Edu: Child {i} UG Year", f"Edu: Child {i} UG Cost",
            f"Edu: Child {i} PG Year", f"Edu: Child {i} PG Cost",
        ]
    # Marriage — 4 children × 3 fields
    for i in range(1, MAX_CHILDREN + 1):
        headers += [
            f"Marriage: Child {i} Name", f"Marriage: Child {i} Timeframe",
            f"Marriage: Child {i} Budget",
        ]
    return headers


def _build_row(data: dict) -> list:
    """Build a flat row list from the session-state data dict."""
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("name", ""),
        data.get("email", ""),
        data.get("age", ""),
        data.get("employment", ""),
        data.get("income_source", ""),
        ", ".join(data.get("goals", [])),
        data.get("liability_type", ""),
        data.get("liability_followup", ""),
        data.get("emergency_fund", ""),
        data.get("portfolio_preference", ""),
        data.get("investment_horizon", ""),
        data.get("fall_reaction", ""),
        data.get("lumpsum_amount", 0),
        data.get("sip_amount", 0),
        data.get("sip_age", 0),
        data.get("other_investments", 0),
    ]

    # Retirement
    ret = data.get("retirement", {})
    row += [
        ret.get("monthly_income", ""),
        ret.get("monthly_expenses", ""),
        ret.get("expense_change", ""),
        ret.get("monthly_investment", ""),
        ret.get("yoy_increase", ""),
        ret.get("other_investments", ""),
        ret.get("liabilities_detail", ""),
    ]

    # Post-Retirement
    pr = data.get("post_retirement", {})
    row += [
        pr.get("passive_pension_income", ""),
        pr.get("living_expenses", ""),
        pr.get("discretionary_expenses", ""),
        pr.get("other_instruments", ""),
    ]

    # Vehicle
    v = data.get("vehicle", {})
    row += [
        v.get("purchase_year", ""),
        v.get("value", ""),
        v.get("flexibility", ""),
        v.get("loan", ""),
        v.get("down_payment", ""),
    ]

    # Home
    h = data.get("home", {})
    row += [
        h.get("purchase_year", ""),
        h.get("value", ""),
        h.get("flexibility", ""),
        h.get("loan", ""),
        h.get("down_payment", ""),
        h.get("monthly_rent", ""),
    ]

    # Education
    edu = data.get("education", {})
    num_edu = edu.get("num_children", 0)
    for i in range(1, MAX_CHILDREN + 1):
        if i <= num_edu:
            child = edu.get(f"child_{i}", {})
            row += [
                child.get("ug_year", ""),
                child.get("ug_cost", ""),
                child.get("pg_year", ""),
                child.get("pg_cost", ""),
            ]
        else:
            row += ["", "", "", ""]

    # Marriage
    mar = data.get("marriage", {})
    num_mar = mar.get("num_children", 0)
    for i in range(1, MAX_CHILDREN + 1):
        if i <= num_mar:
            child = mar.get(f"child_{i}", {})
            row += [
                child.get("name", ""),
                child.get("timeframe", ""),
                child.get("budget", ""),
            ]
        else:
            row += ["", "", ""]

    return row


def write_to_sheet(data: dict) -> str:
    """
    Write a single row to Google Sheets.
    Returns the timestamp string on success, raises on failure.
    """
    sheet = _get_sheet()

    # Ensure header row exists
    existing = sheet.row_values(1)
    header = _build_header()
    if not existing:
        sheet.append_row(header, value_input_option="USER_ENTERED")

    row = _build_row(data)
    sheet.append_row(row, value_input_option="USER_ENTERED")
    return row[0]  # timestamp
