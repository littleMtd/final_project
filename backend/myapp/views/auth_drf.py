"""
身份驗證相關的視圖 (DRF 版本)
"""
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..serializers import SignupSerializer, SigninSerializer, UserSerializer
from ..services import ensure_default_categories
from .response_utils import ErrorResponse, SuccessResponse


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf_view(request):
    """Set CSRF cookie for subsequent session-auth POSTs"""
    return Response({'csrf': 'ok'})

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """用戶註冊"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Signup request data: {request.data}")
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        ensure_default_categories(user)
        login(request, user)
        user_serializer = UserSerializer(user)
        return SuccessResponse.created({'user': user_serializer.data}, "Account created successfully")
    
    logger.warning(f"Signup validation errors: {serializer.errors}")
    return ErrorResponse.bad_request("Invalid signup data", serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def signin_view(request):
    """用戶登入"""
    serializer = SigninSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return ErrorResponse.unauthorized('Invalid credentials')
        
        login(request, user)
        user_serializer = UserSerializer(user)
        return SuccessResponse.ok({'user': user_serializer.data}, "Login successful")
    return ErrorResponse.bad_request("Invalid login data", serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def signout_view(request):
    """用戶登出"""
    logout(request)
    return SuccessResponse.ok(message='Logged out successfully')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def me_view(request):
    """獲取當前用戶信息"""
    serializer = UserSerializer(request.user)
    return SuccessResponse.ok({'user': serializer.data})
