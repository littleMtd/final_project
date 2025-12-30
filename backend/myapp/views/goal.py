"""
財務目標相關的視圖
"""
from datetime import date
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import FinancialGoal
from ..services import parse_decimal, summarize_month
from .utils import _json_error, _json_success, _parse_body, _require_auth


@csrf_exempt
@require_http_methods(["GET", "POST"])
def purpose(request: HttpRequest) -> JsonResponse:
    """獲取或創建財務目標"""
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    if request.method == "GET":
        month_value = request.GET.get("month")
        if month_value:
            try:
                target_month = date.fromisoformat(month_value).replace(day=1)
            except ValueError:
                return _json_error("month must be YYYY-MM or YYYY-MM-DD")
        else:
            target_month = date.today().replace(day=1)
        
        summary = summarize_month(user, target_month)
        return _json_success({"goals": summary.goal_progress})

    try:
        data = _parse_body(request)
        name = data.get("name")
        if not name:
            raise ValueError("'name' is required")
        goal_type = data.get("type", "income")
        if goal_type not in ("income", "expense"):
            raise ValueError("type must be 'income' or 'expense'")
        
        target_amount = parse_decimal(data.get("target_amount"))
        if target_amount <= 0:
            raise ValueError("target_amount must be positive")
        
        month_value = data.get("target_month")
        if month_value:
            try:
                target_month = date.fromisoformat(month_value).replace(day=1)
            except ValueError:
                raise ValueError("target_month must be YYYY-MM or YYYY-MM-DD")
        else:
            target_month = date.today().replace(day=1)
        
        goal, created = FinancialGoal.objects.get_or_create(
            user=user,
            name=name,
            goal_type=goal_type,
            target_month=target_month,
            defaults={"target_amount": target_amount},
        )
        if not created:
            goal.target_amount = target_amount
            goal.save(update_fields=["target_amount", "updated_at"])
        
        return _json_success({"name": goal.name}, status=201)
    except ValueError as exc:
        return _json_error(str(exc))


@require_http_methods(["GET"])
def purpose_detail(request: HttpRequest, name: str) -> JsonResponse:
    """獲取特定目標的詳細信息"""
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    goal_qs = FinancialGoal.objects.filter(user=user, name=name)
    goal_type = request.GET.get("type")
    if goal_type:
        goal_qs = goal_qs.filter(goal_type=goal_type)
    
    month_value = request.GET.get("month")
    if month_value:
        try:
            month_date = date.fromisoformat(month_value).replace(day=1)
        except ValueError:
            return _json_error("month must be YYYY-MM or YYYY-MM-DD")
        goal_qs = goal_qs.filter(target_month=month_date)
    
    goal = goal_qs.order_by("-target_month").first()
    if not goal:
        return _json_error("Goal not found", status=404)
    
    summary = summarize_month(user, goal.target_month)
    for progress in summary.goal_progress:
        if progress["name"] == goal.name and progress["type"] == goal.goal_type:
            return _json_success(progress)
    
    return _json_success({
        "name": goal.name,
        "type": goal.goal_type,
        "target": float(goal.target_amount),
        "progress": 0,
        "percentage": 0,
    })
