from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "asset_type", "is_active")
    list_filter = ("asset_type", "is_active")

@admin.register(models.AssetBalance)
class AssetBalanceAdmin(admin.ModelAdmin):
    list_display = ("id", "asset", "year", "month", "ending_balance", "balance_date")
    list_filter = ("year", "month", "balance_date")
    
@admin.register(models.AssetTransaction)
class AssetTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "asset", "year", "month", "type", "amount", "transaction_date")
    list_filter = ("year", "month", "type", "transaction_date")