"""
報表和洞察相關的視圖
"""
from datetime import date
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import MonthlyReport
from ..services import summarize_month, build_insights
from .utils import _json_error, _json_success, _require_auth


@require_http_methods(["GET", "DELETE"])
def report_overview(request: HttpRequest) -> JsonResponse:
    """獲取或刪除月度財務報表概覽"""
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
    
    # 刪除特定月份的報表記錄
    if request.method == "DELETE":
        deleted_count = MonthlyReport.objects.filter(
            user=user,
            month=target_month
        ).delete()[0]
        return _json_success({
            "deleted": True,
            "count": deleted_count,
            "month": target_month.strftime("%Y-%m")
        })
    
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


@require_http_methods(["GET", "DELETE"])
def insights(request: HttpRequest) -> JsonResponse:
    """獲取指定月份財務洞察建議或清除指定月份所有數據"""
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    # 解析月份參數
    month_value = request.GET.get("month")
    if month_value:
        try:
            target_month = date.fromisoformat(month_value).replace(day=1)
        except ValueError:
            return _json_error("month must be YYYY-MM or YYYY-MM-DD")
    else:
        target_month = date.today().replace(day=1)

    # DELETE 方法：清除指定月份所有收入/支出記錄
    if request.method == "DELETE":
        from ..models import ExpenseEntry, IncomeEntry
        from calendar import monthrange
        
        # 獲取指定月份的第一天和最後一天
        first_day = target_month
        last_day = target_month.replace(day=monthrange(target_month.year, target_month.month)[1])
        
        # 刪除該月的收入和支出記錄
        expense_deleted = ExpenseEntry.objects.filter(
            user=user,
            entry_date__gte=first_day,
            entry_date__lte=last_day
        ).delete()[0]
        
        income_deleted = IncomeEntry.objects.filter(
            user=user,
            entry_date__gte=first_day,
            entry_date__lte=last_day
        ).delete()[0]
        
        return _json_success({
            "deleted": True,
            "expense_count": expense_deleted,
            "income_count": income_deleted,
            "month": first_day.strftime("%Y-%m")
        })

    summary = summarize_month(user, target_month)
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
