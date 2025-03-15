from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "asset_type", "is_active")
    list_filter = ("asset_type", "is_active")
