"""
支出相關的視圖
"""
from django.db.models import Sum
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import ExpenseCategory, ExpenseEntry, FinancialGoal
from ..services import parse_decimal, parse_entry_date, month_bounds
from .utils import _json_error, _json_success, _parse_body, _require_auth, _amount_response


@csrf_exempt
@require_http_methods(["GET", "POST"])
def expense_types(request: HttpRequest) -> JsonResponse:
    """獲取或創建支出類別"""
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    if request.method == "GET":
        types = list(
            ExpenseCategory.objects.filter(user=user).values_list("name", flat=True)
        )
        return _json_success({"types": types})

    try:
        data = _parse_body(request)
        name = data.get("name")
        if not name:
            raise ValueError("'name' is required")
        category, created = ExpenseCategory.objects.get_or_create(user=user, name=name)
        status = 201 if created else 200
        return _json_success({"name": category.name}, status=status)
    except ValueError as exc:
        return _json_error(str(exc))


@require_http_methods(["GET"])
def expense_type_total(request: HttpRequest, name: str) -> JsonResponse:
    """獲取某個支出類別的總額"""
    try:
        user = _require_auth(request)
        total = (
            ExpenseEntry.objects.filter(user=user, category__name=name)
            .aggregate(total=Sum("amount"))
            .get("total")
            or 0
        )
        return _amount_response(name, total)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)


@require_http_methods(["GET"])
def expense_total(request: HttpRequest) -> JsonResponse:
    """獲取所有支出的總額"""
    try:
        user = _require_auth(request)
        total = (
            ExpenseEntry.objects.filter(user=user).aggregate(total=Sum("amount")).get("total")
            or 0
        )
        return _json_success({"total": float(total)})
    except PermissionError as exc:
        return _json_error(str(exc), status=401)


@csrf_exempt
@require_http_methods(["POST"])
def create_expense(request: HttpRequest) -> JsonResponse:
    """創建支出記錄"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Create expense request body: {request.body}")
        user = _require_auth(request)
        data = _parse_body(request)
        logger.info(f"Parsed data: {data}")
        category_name = data.get("type")
        if not category_name:
            raise ValueError("'type' is required")
        amount = parse_decimal(data.get("amount"))
        if amount <= 0:
            raise ValueError("'amount' must be positive")
        category = ExpenseCategory.objects.filter(user=user, name=category_name).first()
        if not category:
            raise ValueError("Category does not exist")
        entry_date = parse_entry_date(data.get("entry_date"))

        # 軟性上限警告：檢查是否超過月度支出目標
        warning: str | None = None
        month_start, month_end = month_bounds(entry_date.replace(day=1))
        month_total = (
            ExpenseEntry.objects.filter(user=user, entry_date__range=(month_start, month_end))
            .aggregate(total=Sum("amount")).get("total") or 0
        )
        goal = (
            FinancialGoal.objects.filter(
                user=user, 
                goal_type=FinancialGoal.GOAL_TYPE_EXPENSE, 
                target_month=month_start
            )
            .order_by("-created_at")
            .first()
        )
        if goal:
            try:
                new_total = month_total + amount
                if new_total > goal.target_amount:
                    warning = f"本月支出 {float(new_total):.0f} 已超過目標 {float(goal.target_amount):.0f}"
            except Exception:
                warning = None

        entry = ExpenseEntry.objects.create(
            user=user,
            category=category,
            amount=amount,
            note=data.get("note", ""),
            entry_date=entry_date,
        )
        
        response_data = {"id": entry.id}
        if warning:
            response_data["warning"] = warning
        
        return _json_success(response_data, status=201)
    except ValueError as exc:
        logger.error(f"ValueError in create_expense: {exc}")
        return _json_error(str(exc))
    except PermissionError as exc:
        logger.error(f"PermissionError in create_expense: {exc}")
        return _json_error(str(exc), status=401)
    except Exception as exc:
        logger.error(f"Unexpected error in create_expense: {exc}", exc_info=True)
        return _json_error("Internal server error", status=500)


@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def expense_entry_detail(request: HttpRequest, entry_id: int) -> JsonResponse:
    """更新或刪除支出記錄"""
    try:
        user = _require_auth(request)
        try:
            entry = ExpenseEntry.objects.get(user=user, id=entry_id)
        except ExpenseEntry.DoesNotExist:
            return _json_error("Entry not found", status=404)

        if request.method == "DELETE":
            entry.delete()
            return _json_success({"deleted": True})

        data = _parse_body(request)
        if "type" in data:
            category_name = data.get("type")
            category = ExpenseCategory.objects.filter(user=user, name=category_name).first()
            if not category:
                return _json_error("Category does not exist")
            entry.category = category
        if "amount" in data:
            amount = parse_decimal(data.get("amount"))
            if amount <= 0:
                return _json_error("'amount' must be positive")
            entry.amount = amount
        if "entry_date" in data:
            entry.entry_date = parse_entry_date(data.get("entry_date"))
        if "note" in data:
            entry.note = data.get("note", "")
        entry.save()
        
        return _json_success({"id": entry.id})
    except ValueError as exc:
        return _json_error(str(exc))
    except PermissionError as exc:
        return _json_error(str(exc), status=401)
