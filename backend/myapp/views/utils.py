"""
通用的工具函數和裝飾器
"""
import json
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User


def _json_error(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"error": message}, status=status)


def _json_success(payload: dict, status: int = 200) -> JsonResponse:
    return JsonResponse(payload, status=status)


def _parse_body(request: HttpRequest) -> dict:
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError("Body must be valid JSON") from exc
    if not isinstance(data, dict):
        raise ValueError("JSON body must be an object")
    return data


def _require_auth(request: HttpRequest) -> User:
    if not request.user.is_authenticated:
        raise PermissionError("Authentication required")
    return request.user


def _amount_response(name: str, total) -> JsonResponse:
    return _json_success({"name": name, "total": float(total)})
