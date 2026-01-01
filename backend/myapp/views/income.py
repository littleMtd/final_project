"""
收入相關的視圖
"""
from django.db.models import Sum
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import IncomeCategory, IncomeEntry
from ..services import parse_decimal, parse_entry_date
from .utils import _json_error, _json_success, _parse_body, _require_auth, _amount_response


@csrf_exempt
@require_http_methods(["GET", "POST"])
def income_types(request: HttpRequest) -> JsonResponse:
    """獲取或創建收入類別"""
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    if request.method == "GET":
        types = list(
            IncomeCategory.objects.filter(user=user).values_list("name", flat=True)
        )
        return _json_success({"types": types})

    # 限制每用戶最多 50 個類別
    user_category_count = IncomeCategory.objects.filter(user=user).count()
    if user_category_count >= 50:
        return _json_error("Maximum income categories limit (50) reached")

    try:
        data = _parse_body(request)
        name = data.get("name")
        if not name:
            raise ValueError("'name' is required")
        category, created = IncomeCategory.objects.get_or_create(user=user, name=name)
        status = 201 if created else 200
        return _json_success({"name": category.name}, status=status)
    except ValueError as exc:
        return _json_error(str(exc))


@require_http_methods(["GET"])
def income_type_total(request: HttpRequest, name: str) -> JsonResponse:
    """獲取某個收入類別的總額"""
    try:
        user = _require_auth(request)
        total = (
            IncomeEntry.objects.filter(user=user, category__name=name)
            .aggregate(total=Sum("amount"))
            .get("total")
            or 0
        )
        return _amount_response(name, total)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)


@require_http_methods(["GET"])
def income_total(request: HttpRequest) -> JsonResponse:
    """獲取所有收入的總額"""
    try:
        user = _require_auth(request)
        total = (
            IncomeEntry.objects.filter(user=user).aggregate(total=Sum("amount")).get("total")
            or 0
        )
        return _json_success({"total": float(total)})
    except PermissionError as exc:
        return _json_error(str(exc), status=401)


@csrf_exempt
@require_http_methods(["POST"])
def create_income(request: HttpRequest) -> JsonResponse:
    """創建收入記錄"""
    try:
        user = _require_auth(request)
        
        # 限制每用戶最多 10000 筆記錄
        user_income_count = IncomeEntry.objects.filter(user=user).count()
        if user_income_count >= 10000:
            return _json_error("Maximum income entries limit (10000) reached. Please delete old entries.")
        
        data = _parse_body(request)
        category_name = data.get("type")
        if not category_name:
            raise ValueError("'type' is required")
        amount = parse_decimal(data.get("amount"))
        if amount <= 0:
            raise ValueError("'amount' must be positive")
        category = IncomeCategory.objects.filter(user=user, name=category_name).first()
        if not category:
            raise ValueError("Category does not exist")
        entry_date = parse_entry_date(data.get("entry_date"))

        entry = IncomeEntry.objects.create(
            user=user,
            category=category,
            amount=amount,
            note=data.get("note", ""),
            entry_date=entry_date,
        )
        
        return _json_success({"id": entry.id}, status=201)
    except ValueError as exc:
        return _json_error(str(exc))
    except PermissionError as exc:
        return _json_error(str(exc), status=401)


@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def income_entry_detail(request: HttpRequest, entry_id: int) -> JsonResponse:
    """更新或刪除收入記錄"""
    try:
        user = _require_auth(request)
        try:
            entry = IncomeEntry.objects.get(user=user, id=entry_id)
        except IncomeEntry.DoesNotExist:
            return _json_error("Entry not found", status=404)

        if request.method == "DELETE":
            entry.delete()
            return _json_success({"deleted": True})

        data = _parse_body(request)
        if "type" in data:
            category_name = data.get("type")
            category = IncomeCategory.objects.filter(user=user, name=category_name).first()
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
