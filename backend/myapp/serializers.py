"""
Django REST Framework Serializers
"""
from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    ExpenseCategory,
    IncomeCategory,
    ExpenseEntry,
    IncomeEntry,
    FinancialGoal,
    MonthlyReport,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id']


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ExpenseEntrySerializer(serializers.ModelSerializer):
    type = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = ExpenseEntry
        fields = ['id', 'type', 'amount', 'note', 'entry_date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value

    def validate_type(self, value):
        user = self.context['request'].user
        if not ExpenseCategory.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("Category does not exist")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        category_name = validated_data.pop('type')
        category = ExpenseCategory.objects.get(user=user, name=category_name)
        validated_data['user'] = user
        validated_data['category'] = category
        
        # Check goal warning
        entry = ExpenseEntry(**validated_data)
        warning = self._check_goal_warning(user, entry)
        entry.save()
        
        # Attach warning to instance for response
        if warning:
            entry._warning = warning
        return entry

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if 'type' in validated_data:
            category_name = validated_data.pop('type')
            instance.category = ExpenseCategory.objects.get(user=user, name=category_name)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def _check_goal_warning(self, user, entry):
        from datetime import date
        from django.db.models import Sum
        from .services import month_bounds
        
        month_start, month_end = month_bounds(entry.entry_date.replace(day=1))
        month_total = (
            ExpenseEntry.objects.filter(user=user, entry_date__range=(month_start, month_end))
            .aggregate(total=Sum("amount")).get("total") or Decimal('0')
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
            new_total = month_total + entry.amount
            if new_total > goal.target_amount:
                return f"本月支出 {float(new_total):.0f} 已超過目標 {float(goal.target_amount):.0f}"
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(instance, '_warning'):
            data['warning'] = instance._warning
        return data


class IncomeEntrySerializer(serializers.ModelSerializer):
    type = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = IncomeEntry
        fields = ['id', 'type', 'amount', 'note', 'entry_date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value

    def validate_type(self, value):
        user = self.context['request'].user
        if not IncomeCategory.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("Category does not exist")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        category_name = validated_data.pop('type')
        category = IncomeCategory.objects.get(user=user, name=category_name)
        validated_data['user'] = user
        validated_data['category'] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if 'type' in validated_data:
            category_name = validated_data.pop('type')
            instance.category = IncomeCategory.objects.get(user=user, name=category_name)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class FinancialGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        fields = ['id', 'name', 'goal_type', 'target_amount', 'target_month', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_target_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Target amount must be positive")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MonthlyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyReport
        fields = ['id', 'month', 'summary', 'delivered', 'created_at']
        read_only_fields = ['id', 'created_at']
