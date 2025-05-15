from django.contrib import admin

from .models import Stock
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
            _("Type and Market"),
            {
                "fields": ("type", "market"),
                "description": _("Select the type and market of the stock."),
            },
        ),
    )
