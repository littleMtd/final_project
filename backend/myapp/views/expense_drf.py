"""
支出相關的視圖 (DRF 版本)
"""
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import ExpenseCategory, ExpenseEntry
from ..serializers import ExpenseCategorySerializer, ExpenseEntrySerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def expense_types(request):
    """獲取或創建支出類別"""
    if request.method == 'GET':
        categories = ExpenseCategory.objects.filter(user=request.user)
        serializer = ExpenseCategorySerializer(categories, many=True)
        return Response({'types': [c['name'] for c in serializer.data]})
    
    # 限制每用戶最多 50 個類別
    user_category_count = ExpenseCategory.objects.filter(user=request.user).count()
    if user_category_count >= 50:
        return Response(
            {'error': 'Maximum expense categories limit (50) reached'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ExpenseCategorySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        category, created = ExpenseCategory.objects.get_or_create(
            user=request.user,
            name=serializer.validated_data['name'],
            defaults={'description': serializer.validated_data.get('description', '')}
        )
        response_serializer = ExpenseCategorySerializer(category)
        return Response(
            {'name': response_serializer.data['name']},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_type_total(request, name):
    """獲取某個支出類別的總額"""
    total = (
        ExpenseEntry.objects.filter(user=request.user, category__name=name)
        .aggregate(total=Sum("amount"))
        .get("total") or 0
    )
    return Response({'type': name, 'total': float(total)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_total(request):
    """獲取所有支出的總額"""
    total = (
        ExpenseEntry.objects.filter(user=request.user)
        .aggregate(total=Sum("amount"))
        .get("total") or 0
    )
    return Response({'total': float(total)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_expense(request):
    """創建支出記錄"""
    # 限制每用戶最多 10000 筆記錄
    user_expense_count = ExpenseEntry.objects.filter(user=request.user).count()
    if user_expense_count >= 10000:
        return Response(
            {'error': 'Maximum expense entries limit (10000) reached. Please delete old entries.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ExpenseEntrySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        entry = serializer.save()
        response_data = {'id': entry.id}
        if hasattr(entry, '_warning'):
            response_data['warning'] = entry._warning
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def expense_entry_detail(request, entry_id):
    """更新或刪除支出記錄"""
    try:
        entry = ExpenseEntry.objects.get(user=request.user, id=entry_id)
    except ExpenseEntry.DoesNotExist:
        return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        entry.delete()
        return Response({'deleted': True}, status=status.HTTP_200_OK)
    
    serializer = ExpenseEntrySerializer(entry, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'id': entry.id})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
