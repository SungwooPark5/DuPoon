from django.contrib import admin

from .models import Stock, Price
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """
    Admin view for Stock model.
    """

    list_display = ("name", "ticker", "type", "market", "listed_date")
    search_fields = ("name", "ticker")
    list_filter = ("type", "market")
    ordering = ("name",)
    list_per_page = 20
    fieldsets = (
        (None, {"fields": ("name", "ticker", "listed_date")}),
        (
            _("유형과 시장"),
            {
                "fields": ("type", "market"),
                "description": _("주식의 유형과 시장을 선택하세요."),
            },
        ),
    )


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """
    Admin view for Price model.
    """

    list_display = ("stock", "date", "open_price", "high_price", "low_price")
    search_fields = ("stock__name", "stock__ticker")
    list_filter = ("stock__type", "stock__market")
    ordering = ("-date",)
    list_per_page = 20
    fieldsets = (
        (None, {"fields": ("stock", "date")}),
        (
            _("가격 정보 입력"),
            {
                "fields": (
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price",
                    "volume",
                ),
                "description": _("가격 정보를 입력하세요."),
            },
        ),
    )
