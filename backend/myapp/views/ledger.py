"""
交易記錄清單相關的視圖
"""
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import ExpenseEntry, IncomeEntry
from .utils import _json_error, _json_success, _require_auth


@require_http_methods(["GET"])
def ledger(request: HttpRequest) -> JsonResponse:
    """
    綜合交易記錄清單
    
    Query參數:
      - kind: 'expense' | 'income' | 'all' (默認 'all')
      - type: 可選的類別名稱過濾
      - page: 頁碼，從1開始 (默認 1)
      - page_size: 每頁條數 (默認 10, 最大 100)
    
    返回:
      {
        "items": [
          {"id": 1, "kind": "expense", "type": "餐飲", "amount": 120.0, "date": "2025-12-01", "note": "..."},
          ...
        ],
        "page": 1,
        "page_size": 10,
        "total": 123
      }
    """
    try:
        user = _require_auth(request)
    except PermissionError as exc:
        return _json_error(str(exc), status=401)

    kind = (request.GET.get("kind") or "all").lower()
    if kind not in {"expense", "income", "all"}:
        return _json_error("kind must be 'expense', 'income' or 'all'")
    
    type_name = request.GET.get("type") or None
    
    try:
        page = max(1, int(request.GET.get("page") or 1))
        page_size = min(100, max(1, int(request.GET.get("page_size") or 10)))
    except ValueError:
        return _json_error("page and page_size must be integers")

    # 收集支出和收入記錄
    expense_entries = []
    income_entries = []

    if kind in {"expense", "all"}:
        expense_qs = ExpenseEntry.objects.filter(user=user)
        if type_name:
            expense_qs = expense_qs.filter(category__name=type_name)
        expense_entries = list(
            expense_qs.values(
                "id", "entry_date", "category__name", "amount", "note"
            ).order_by("-entry_date", "-id")
        )
        for e in expense_entries:
            e["kind"] = "expense"
            e["type"] = e.pop("category__name")
            e["date"] = e.pop("entry_date").strftime("%Y-%m-%d")
            e["amount"] = float(e["amount"])

    if kind in {"income", "all"}:
        income_qs = IncomeEntry.objects.filter(user=user)
        if type_name:
            income_qs = income_qs.filter(category__name=type_name)
        income_entries = list(
            income_qs.values(
                "id", "entry_date", "category__name", "amount", "note"
            ).order_by("-entry_date", "-id")
        )
        for e in income_entries:
            e["kind"] = "income"
            e["type"] = e.pop("category__name")
            e["date"] = e.pop("entry_date").strftime("%Y-%m-%d")
            e["amount"] = float(e["amount"])

    # 合併並按日期排序
    combined = expense_entries + income_entries
    combined.sort(
        key=lambda x: (x["date"], -x["id"]),
        reverse=True
    )

    # 分頁
    total = len(combined)
    offset = (page - 1) * page_size
    paginated = combined[offset : offset + page_size]

    return _json_success({
        "items": paginated,
        "page": page,
        "page_size": page_size,
        "total": total,
    })
