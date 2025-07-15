from django.contrib import admin

from .models import BacktestResult

# Register your models here.
@admin.register(BacktestResult)
class BacktestResultAdmin(admin.ModelAdmin):
    """
    Admin view for BacktestResult model.
    """

    list_display = (
        "strategy",
        "start_date",
        "end_date",
        "total_return",
        "cagr",
        "max_drawdown",
        "volatility",
        "sharpe_ratio",
        "sortino_ratio",
        "created_at",
    )
    search_fields = ("strategy__name",)
    list_filter = ("strategy__type",)
    ordering = ("-created_at",)
    list_per_page = 20
    fieldsets = (
        (None, {"fields": ("strategy", "start_date", "end_date")}),
        (
            "Performance Metrics",
            {
                "fields": (
                    "total_return",
                    "cagr",
                    "max_drawdown",
                    "volatility",
                    "sharpe_ratio",
                    "sortino_ratio",
                ),
            },
        ),
    )