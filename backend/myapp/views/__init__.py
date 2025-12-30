"""
Views package initialization
Import all view functions for easy access
"""
from .auth_drf import signup_view, signin_view, signout_view, me_view, csrf_view
from .expense_drf import (
    expense_types,
    expense_type_total,
    expense_total,
    create_expense,
    expense_entry_detail,
)
from .income import (
    income_types,
    income_type_total,
    income_total,
    create_income,
    income_entry_detail,
)
from .goal import purpose, purpose_detail
from .report import report_overview, insights, report_status
from .ledger import ledger

__all__ = [
    # Auth
    "signup_view",
    "signin_view",
    "signout_view",
    "me_view",
    "csrf_view",
    # Expense
    "expense_types",
    "expense_type_total",
    "expense_total",
    "create_expense",
    "expense_entry_detail",
    # Income
    "income_types",
    "income_type_total",
    "income_total",
    "create_income",
    "income_entry_detail",
    # Goal
    "purpose",
    "purpose_detail",
    # Report
    "report_overview",
    "insights",
    "report_status",
    # Ledger
    "ledger",
]
