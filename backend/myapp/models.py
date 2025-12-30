from datetime import date

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class CategoryBase(TimeStampedModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255, blank=True)

	class Meta:
		abstract = True
		unique_together = ("user", "name")
		ordering = ["name"]

	def __str__(self) -> str:
		return f"{self.user.username}:{self.name}"


class ExpenseCategory(CategoryBase):
	class Meta(CategoryBase.Meta):
		verbose_name = "Expense Category"
		verbose_name_plural = "Expense Categories"


class IncomeCategory(CategoryBase):
	class Meta(CategoryBase.Meta):
		verbose_name = "Income Category"
		verbose_name_plural = "Income Categories"


class EntryBase(TimeStampedModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	note = models.CharField(max_length=255, blank=True)
	entry_date = models.DateField(default=date.today)

	class Meta:
		abstract = True
		ordering = ["-entry_date", "-created_at"]


class ExpenseEntry(EntryBase):
	category = models.ForeignKey(
		ExpenseCategory, related_name="entries", on_delete=models.CASCADE
	)

	def __str__(self) -> str:
		return f"Expense {self.category.name} {self.amount}"


class IncomeEntry(EntryBase):
	category = models.ForeignKey(
		IncomeCategory, related_name="entries", on_delete=models.CASCADE
	)

	def __str__(self) -> str:
		return f"Income {self.category.name} {self.amount}"


def first_day_of_current_month() -> date:
	today = date.today()
	return today.replace(day=1)


class FinancialGoal(TimeStampedModel):
	GOAL_TYPE_EXPENSE = "expense"
	GOAL_TYPE_INCOME = "income"
	GOAL_TYPE_CHOICES = (
		(GOAL_TYPE_EXPENSE, "Expense"),
		(GOAL_TYPE_INCOME, "Income"),
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=60)
	goal_type = models.CharField(max_length=10, choices=GOAL_TYPE_CHOICES)
	target_amount = models.DecimalField(max_digits=12, decimal_places=2)
	target_month = models.DateField(
		default=first_day_of_current_month,
		help_text="First day of the month the goal applies to.",
	)

	class Meta:
		unique_together = ("user", "name", "goal_type", "target_month")
		ordering = ["-target_month", "name"]

	def __str__(self) -> str:
		return f"{self.name} ({self.goal_type})"


class MonthlyReport(TimeStampedModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	month = models.DateField(help_text="First day of reported month.")
	summary = models.JSONField(default=dict)
	delivered = models.BooleanField(default=False)

	class Meta:
		unique_together = ("user", "month")
		ordering = ["-month"]

	def __str__(self) -> str:
		return f"Report {self.user.username} {self.month:%Y-%m}"
