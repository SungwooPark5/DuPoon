from rest_framework import serializers

from .models import Asset, AssetBalance, AssetTransaction


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"

class AssetBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetBalance
        fields = "__all__"
        
class AssetTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTransaction
        fields = "__all__"