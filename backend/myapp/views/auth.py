"""
身份驗證相關的視圖
"""
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..services import ensure_default_categories
from .utils import _json_error, _json_success, _parse_body, _require_auth


@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request: HttpRequest) -> JsonResponse:
    """用戶註冊"""
    try:
        data = _parse_body(request)
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise ValueError("username and password are required")
        
        if User.objects.filter(username=username).exists():
            raise ValueError("Username already exists")
        
        user = User.objects.create_user(username=username, password=password)
        ensure_default_categories(user)
        login(request, user)
        
        return _json_success({"user": {"id": user.id, "username": user.username}}, status=201)
    except ValueError as exc:
        return _json_error(str(exc))


@csrf_exempt
@require_http_methods(["POST"])
def signin_view(request: HttpRequest) -> JsonResponse:
    """用戶登入"""
    try:
        data = _parse_body(request)
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise ValueError("username and password are required")
        
        user = authenticate(request, username=username, password=password)
        if user is None:
            return _json_error("Invalid credentials", status=401)
        
        login(request, user)
        return _json_success({"user": {"id": user.id, "username": user.username}})
    except ValueError as exc:
        return _json_error(str(exc))


@csrf_exempt
@require_http_methods(["POST"])
def signout_view(request: HttpRequest) -> JsonResponse:
    """用戶登出"""
    logout(request)
    return _json_success({"message": "Logged out"})


@csrf_exempt
@require_http_methods(["GET"])
def me_view(request: HttpRequest) -> JsonResponse:
    """獲取當前用戶信息"""
    try:
        user = _require_auth(request)
        return _json_success({"user": {"id": user.id, "username": user.username}})
    except PermissionError as exc:
        return _json_error(str(exc), status=401)
