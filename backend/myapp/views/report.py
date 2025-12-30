"""
報表和洞察相關的視圖
"""
from datetime import date
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import MonthlyReport
from ..services import summarize_month, build_insights
from .utils import _json_error, _json_success, _require_auth


@require_http_methods(["GET"])
def report_overview(request: HttpRequest) -> JsonResponse:
    """獲取月度財務報表概覽"""
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    month_value = request.GET.get("month")
    if month_value:
        try:
            target_month = date.fromisoformat(month_value).replace(day=1)
        except ValueError:
            return _json_error("month must be YYYY-MM or YYYY-MM-DD")
    else:
        target_month = date.today().replace(day=1)
    
    summary = summarize_month(user, target_month)
    payload = {
        "month": target_month.strftime("%Y-%m"),
        "income": {k: float(v) for k, v in summary.income_by_category.items()},
        "expense": {k: float(v) for k, v in summary.expense_by_category.items()},
        "total_income": float(summary.total_income),
        "total_expense": float(summary.total_expense),
        "net": float(summary.net),
        "goals": summary.goal_progress,
    }
    return _json_success(payload)


@require_http_methods(["GET"])
def insights(request: HttpRequest) -> JsonResponse:
    """獲取本月財務洞察建議"""
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    summary = summarize_month(user)
    insight_lines = build_insights(summary)
    return _json_success({"insights": insight_lines})


@require_http_methods(["GET"])
def report_status(request: HttpRequest) -> JsonResponse:
    """獲取報表生成狀態"""
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    latest = MonthlyReport.objects.filter(user=user).order_by("-month").first()
    if not latest:
        return _json_success({"month": None, "delivered": False})
    
    return _json_success({
        "month": latest.month.strftime("%Y-%m"),
        "delivered": latest.delivered,
        "generated_at": latest.updated_at.isoformat(),
    })
