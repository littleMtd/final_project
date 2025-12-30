from __future__ import annotations

from datetime import date

from django.core.management.base import BaseCommand, CommandError

from myapp.services import generate_monthly_reports


class Command(BaseCommand):
    help = "Generate last month's personal finance reports and email them to users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--month",
            dest="month",
            type=str,
            help="Report month in YYYY-MM format. Defaults to previous month.",
        )

    def handle(self, *args, **options):
        month_str = options.get("month")
        target_month = None
        if month_str:
            try:
                target_month = date.fromisoformat(f"{month_str}-01")
            except ValueError as exc:
                raise CommandError("--month must follow YYYY-MM format") from exc
        generate_monthly_reports(target_month)
        self.stdout.write(
            self.style.SUCCESS(
                f"Monthly reports sent for {(target_month or 'previous month')}"
            )
        )
