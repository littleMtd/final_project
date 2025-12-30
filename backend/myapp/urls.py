from django.urls import path

from .views import (
    # Auth
    signup_view,
    signin_view,
    signout_view,
    me_view,
    csrf_view,
    # Expense
    expense_types,
    expense_type_total,
    expense_total,
    create_expense,
    expense_entry_detail,
    # Income
    income_types,
    income_type_total,
    income_total,
    create_income,
    income_entry_detail,
    # Goal
    purpose,
    purpose_detail,
    # Report
    report_overview,
    insights,
    report_status,
    # Ledger
    ledger,
)

urlpatterns = [
    # CSRF cookie fetch
    path("csrf/", csrf_view),
    # Expense endpoints
    path("expense/types/", expense_types),
    path("expense/types/<str:name>/", expense_type_total),
    path("expense/total/", expense_total),
    path("expense/", create_expense),
    path("expense/<int:entry_id>/", expense_entry_detail),
    
    # Income endpoints
    path("income/types/", income_types),
    path("income/types/<str:name>/", income_type_total),
    path("income/total/", income_total),
    path("income/", create_income),
    path("income/<int:entry_id>/", income_entry_detail),
    
    # Goal endpoints
    path("purpose/", purpose),
    path("purpose/<str:name>/", purpose_detail),
    
    # Report endpoints
    path("report/overview/", report_overview),
    path("report/status/", report_status),
    path("insights/", insights),
    
    # Auth endpoints
    path("signup/", signup_view),
    path("signin/", signin_view),
    path("signout/", signout_view),
    path("me/", me_view),
    
    # Ledger endpoint
    path("ledger/", ledger),
]
