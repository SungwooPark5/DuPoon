from django.db import models

from .enums import AssetType, TransactionType


# Create your models here.
class Asset(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    asset_type = models.CharField(
        max_length=20, choices=[(tag.name, tag.value) for tag in AssetType]
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AssetType(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_investable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class AssetBalance(models.Model):

    asset = models.ForeignKey("Asset", on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    ending_balance = models.DecimalField(max_digits=20, decimal_places=2)
    balance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year}-{self.month} {self.asset.name} {self.ending_balance}"


class AssetTransaction(models.Model):

    asset = models.ForeignKey("Asset", on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField(
        max_length=20, choices=[(tag.name, tag.value) for tag in TransactionType]
    )
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year}-{self.month} {self.asset.name} {self.type} {self.amount}"
