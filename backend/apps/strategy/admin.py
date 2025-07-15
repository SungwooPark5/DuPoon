from django.contrib import admin

from .models import Strategy
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    """
    Admin view for Strategy model.
    """

    list_display = ("name", "type", "created_at")
    search_fields = ("name",)
    list_filter = ("type",)
    ordering = ("-created_at",)
    list_per_page = 20
    fieldsets = (
        (None, {"fields": ("name", "description")}),
        (
            _("Strategy Details"),
            {
                "fields": ("type", "parameters"),
                "description": _("Select the type and parameters for the strategy."),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")