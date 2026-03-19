"""
PowerUp Infinite — Conditional Logic
Pure functions that return options/flags based on previous answers.
"""

from config import (
    EMPLOYMENT_OPTIONS,
    INCOME_OPTIONS_WORKING,
    INCOME_OPTIONS_RETIRED,
    GOALS_WORKING,
    GOALS_RETIRED,
    GOAL_MODULE_MAP,
    GOALS_WITHOUT_MODULE,
)


def get_employment_options(age: str) -> list[str]:
    """Return employment-status options based on selected age bracket."""
    return EMPLOYMENT_OPTIONS.get(age, [])


def is_working_status(employment: str) -> bool:
    """True if the person is actively working or soon to retire."""
    return employment in ("Actively Working", "Soon to be Retiring (within 5 yrs)")


def is_retired_status(employment: str) -> bool:
    """True if the person is retired (early or regular)."""
    return employment in ("Retired Early", "Retired")


def get_income_options(employment: str) -> list[str]:
    """Return income-source options based on employment status."""
    if is_working_status(employment):
        return INCOME_OPTIONS_WORKING
    if is_retired_status(employment):
        return INCOME_OPTIONS_RETIRED
    return []


def get_goal_options(employment: str) -> list[str]:
    """Return investment-goal options based on employment status."""
    if is_working_status(employment):
        return GOALS_WORKING
    if is_retired_status(employment):
        return GOALS_RETIRED
    return []


def get_goal_modules(selected_goals: list[str]) -> list[str]:
    """
    Return an ordered list of goal-module keys that need dedicated forms.
    Skips goals that have no dedicated module (e.g. "No Fixed Goal", "Wealth Conservation", "Other").
    """
    modules = []
    for goal in selected_goals:
        if goal not in GOALS_WITHOUT_MODULE and goal in GOAL_MODULE_MAP:
            modules.append(GOAL_MODULE_MAP[goal])
    return modules


def has_no_liabilities(liability_type: str) -> bool:
    """True if user selected 'None' for liabilities."""
    return liability_type == "None"


def should_show_retirement_module(selected_goals: list[str], employment: str) -> bool:
    """Retirement module shown only if goal selected AND user is working/soon retiring."""
    return "Retirement Planning" in selected_goals and is_working_status(employment)


def should_show_post_retirement_module(selected_goals: list[str], employment: str) -> bool:
    """Post-Retirement module shown only if goal selected AND user is retired."""
    return "Post-Retirement Income Planning" in selected_goals and is_retired_status(employment)


def should_skip_all_goal_modules(selected_goals: list[str]) -> bool:
    """True if every selected goal has no dedicated module form."""
    return all(g in GOALS_WITHOUT_MODULE for g in selected_goals)


def validate_email(email: str) -> bool:
    """Basic email validation — must contain @."""
    return "@" in email and len(email) >= 3
