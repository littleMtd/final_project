"""
統一的錯誤處理工具
"""
from rest_framework.response import Response
from rest_framework import status
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ErrorResponse:
    """統一的錯誤響應格式"""
    
    @staticmethod
    def bad_request(message: str, errors: Optional[Dict[str, Any]] = None) -> Response:
        """400 Bad Request"""
        data = {'error': message, 'code': 'BAD_REQUEST'}
        if errors:
            data['details'] = errors
        logger.warning(f"Bad request: {message}")
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def unauthorized(message: str = "Authentication required") -> Response:
        """401 Unauthorized"""
        logger.warning(f"Unauthorized access: {message}")
        return Response(
            {'error': message, 'code': 'UNAUTHORIZED'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(message: str = "Permission denied") -> Response:
        """403 Forbidden"""
        logger.warning(f"Forbidden access: {message}")
        return Response(
            {'error': message, 'code': 'FORBIDDEN'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    @staticmethod
    def not_found(message: str = "Resource not found") -> Response:
        """404 Not Found"""
        logger.info(f"Resource not found: {message}")
        return Response(
            {'error': message, 'code': 'NOT_FOUND'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def server_error(message: str = "Internal server error") -> Response:
        """500 Internal Server Error"""
        logger.error(f"Server error: {message}")
        return Response(
            {'error': message, 'code': 'SERVER_ERROR'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class SuccessResponse:
    """統一的成功響應格式"""
    
    @staticmethod
    def ok(data: Optional[Dict[str, Any]] = None, message: str = "") -> Response:
        """200 OK"""
        response_data = {'success': True}
        if message:
            response_data['message'] = message
        if data:
            response_data['data'] = data
        return Response(response_data, status=status.HTTP_200_OK)
    
    @staticmethod
    def created(data: Optional[Dict[str, Any]] = None, message: str = "Created successfully") -> Response:
        """201 Created"""
        response_data = {'success': True, 'message': message}
        if data:
            response_data['data'] = data
        return Response(response_data, status=status.HTTP_201_CREATED)
