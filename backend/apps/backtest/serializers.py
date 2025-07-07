from rest_framework import serializers

from apps.stock.models import Stock


class AssetAllocationSerializer(serializers.Serializer):
    """
    Serializer for asset allocation data.
    """

    ticker = serializers.SlugRelatedField(
        slug_field="ticker",
        queryset=Stock.objects.all(),
        allow_null=False,
        required=True,
    )
    weight = serializers.FloatField(
        min_value=0.0,
        max_value=1.0,
        allow_null=False,
        required=True,
        help_text="Weight of the asset in the portfolio (0.0 to 1.0)",
    )


class BacktestSerializer(serializers.Serializer):
    """
    Serializer for backtest data.
    """

    allocations = AssetAllocationSerializer(many=True, required=True)

    def validate(self, data):
        total_weight = sum(allocation["weight"] for allocation in data["allocations"])
        if total_weight != 1.0:
            raise serializers.ValidationError(
                "Total weight of allocations must equal 1.0"
            )
        return data


class BacktestResultSerializer(serializers.Serializer):
    """
    Serializer for backtest result data.
    """

    pass
