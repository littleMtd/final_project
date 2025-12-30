from __future__ import annotations

from calendar import monthrange
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Tuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Sum

from .models import (
    ExpenseCategory,
    ExpenseEntry,
    FinancialGoal,
    IncomeCategory,
    IncomeEntry,
    MonthlyReport,
)

User = get_user_model()


DECIMAL_ZERO = Decimal("0")


@dataclass
class Summary:
    total_income: Decimal
    total_expense: Decimal
    income_by_category: Dict[str, Decimal]
    expense_by_category: Dict[str, Decimal]
    net: Decimal
    goal_progress: List[Dict[str, float]]


def parse_decimal(value) -> Decimal:
    if value in (None, ""):
        raise ValueError("Amount is required.")
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError) as exc:
        raise ValueError("Invalid amount value.") from exc


def parse_entry_date(value: str | None) -> date:
    if not value:
        return date.today()
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("entry_date must be YYYY-MM-DD") from exc


def month_bounds(target_month: date) -> Tuple[date, date]:
    last_day = monthrange(target_month.year, target_month.month)[1]
    start = target_month.replace(day=1)
    end = target_month.replace(day=last_day)
    return start, end


def _category_totals(model, user, start: date | None = None, end: date | None = None):
    qs = model.objects.filter(user=user)
    if start and end:
        qs = qs.filter(entry_date__range=(start, end))
    data = (
        qs.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("category__name")
    )
    return {row["category__name"]: row["total"] or DECIMAL_ZERO for row in data}


def summarize_month(user, target_month: date | None = None) -> Summary:
    target_month = target_month or date.today().replace(day=1)
    start, end = month_bounds(target_month)
    income_by_category = _category_totals(IncomeEntry, user, start, end)
    expense_by_category = _category_totals(ExpenseEntry, user, start, end)
    total_income = sum(income_by_category.values(), DECIMAL_ZERO)
    total_expense = sum(expense_by_category.values(), DECIMAL_ZERO)
    net = total_income - total_expense
    goals = []
    goal_qs = FinancialGoal.objects.filter(user=user, target_month=start)
    for goal in goal_qs:
        if goal.goal_type == FinancialGoal.GOAL_TYPE_INCOME:
            progress_amount = sum(income_by_category.values(), DECIMAL_ZERO)
        else:
            progress_amount = sum(expense_by_category.values(), DECIMAL_ZERO)
        percentage = (
            (progress_amount / goal.target_amount * Decimal("100"))
            if goal.target_amount
            else Decimal("0")
        )
        goals.append(
            {
                "name": goal.name,
                "type": goal.goal_type,
                "target": float(goal.target_amount),
                "progress": float(progress_amount),
                "percentage": float(round(percentage, 2)),
            }
        )
    return Summary(
        total_income=total_income,
        total_expense=total_expense,
        income_by_category=income_by_category,
        expense_by_category=expense_by_category,
        net=net,
        goal_progress=goals,
    )


def build_insights(summary: Summary) -> List[str]:
    insights: List[str] = []
    if summary.total_expense > summary.total_income:
        deficit = summary.total_expense - summary.total_income
        insights.append(
            f"支出已超過收入 {deficit:.2f}，建議檢視非必要支出。"
        )
    top_expense = max(
        summary.expense_by_category.items(),
        key=lambda item: item[1],
        default=(None, DECIMAL_ZERO),
    )
    if top_expense[0] and summary.total_expense:
        ratio = top_expense[1] / summary.total_expense
        if ratio > Decimal("0.3"):
            percent = (ratio * Decimal("100")).quantize(Decimal("0.1"), rounding="ROUND_DOWN")
            insights.append(
                f"{top_expense[0]} 佔支出 {percent}% ，可考慮設定上限。"
            )
    if summary.net > DECIMAL_ZERO:
        insights.append(
            "本月仍有正現金流，建議將盈餘轉入儲蓄或投資。"
        )
    elif not insights:
        insights.append("維持平衡收支，繼續保持。")
    return insights


def ensure_default_categories(user) -> None:
    default_expense = ["食", "衣", "住", "行", "育", "樂"]
    default_income = ["薪資", "獎助金", "投資", "其他"]
    for name in default_expense:
        ExpenseCategory.objects.get_or_create(user=user, name=name)
    for name in default_income:
        IncomeCategory.objects.get_or_create(user=user, name=name)


def send_monthly_report(user, summary: Summary, target_month: date) -> None:
    subject = f"{target_month:%Y-%m} 財務月報"
    body_lines = [
        f"總收入：{summary.total_income:.2f}",
        f"總支出：{summary.total_expense:.2f}",
        f"淨現金流：{summary.net:.2f}",
        "",
        "目標進度:",
    ]
    for goal in summary.goal_progress:
        body_lines.append(
            f"- {goal['name']} ({goal['type']}): {goal['progress']:.2f}/{goal['target']:.2f} ({goal['percentage']}%)"
        )
    send_mail(
        subject=subject,
        message="\n".join(body_lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email or f"{user.username}@example.com"],
    )
    MonthlyReport.objects.update_or_create(
        user=user,
        month=target_month,
        defaults={
            "summary": {
                "total_income": float(summary.total_income),
                "total_expense": float(summary.total_expense),
                "net": float(summary.net),
                "goal_progress": summary.goal_progress,
            },
            "delivered": True,
        },
    )


def generate_monthly_reports(target_month: date | None = None) -> None:
    target_month = target_month or _previous_month()
    for user in User.objects.all():
        summary = summarize_month(user, target_month)
        send_monthly_report(user, summary, target_month)


def _previous_month() -> date:
    today = date.today().replace(day=1)
    if today.month == 1:
        return today.replace(year=today.year - 1, month=12)
    return today.replace(month=today.month - 1)