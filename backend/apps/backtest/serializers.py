import math
from rest_framework import serializers

from apps.stock.models import Stock
from .models import BacktestStat


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
    strategy_name = serializers.CharField(
        required=False, allow_null=True, help_text="Name for strategy"
    )
    start_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Start date for the backtest (YYYY-MM-DD)",
    )
    end_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="End date for the backtest (YYYY-MM-DD)",
    )
    rebalance_freq = serializers.ChoiceField(
        required=True,
        allow_null=False,
        choices=[
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("yearly", "Yearly"),
        ],
        help_text="Rebalance frequency for the portfolio",
    )
    slippage = serializers.FloatField(
        required=False,
        allow_null=True,
        default=0.0,
        min_value=0.0,
        help_text="Slippage percentage for the backtest (default is 0.0)",
    )
    include_cash = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Include cash in the portfolio (default is False)",
    )
    cash_ticker = serializers.CharField(
        required=False,
        allow_blank=True,
        default="CASH",
        help_text="Ticker symbol for cash asset (default is 'CASH')",
    )
    cash_weight = serializers.FloatField(
        required=False,
        allow_null=True,
        default=0.0,
        min_value=0.0,
        max_value=1.0,
        help_text="Weight of cash in the portfolio (default is 0.0)",
    )

    def validate(self, data):
        total_weight = sum(allocation["weight"] for allocation in data["allocations"])
        if data.get("include_cash", False):
            total_weight += data.get("cash_weight", 0.0)
        if total_weight < 0.99999999 or total_weight > 1.00000001:
            raise serializers.ValidationError(
                "Total weight of allocations must equal 1.0"
            )
        return data

    class Meta:
        swagger_schema_fields = {
            "example": {
                "strategy_name": "60/40 Allocation",
                "allocations": [
                    {"ticker": "SPY", "weight": 0.6},
                    {"ticker": "TLT", "weight": 0.4},
                ],
                "start_date": "2000-01-01",
                "end_date": "2021-01-01",
                "rebalance_freq": "monthly",
                "slippage": 0.0,
                "include_cash": False,
                "cash_ticker": "CASH",
                "cash_weight": 0.0,
            }
        }


class PriceDataSerializer(serializers.Serializer):
    """
    Serializer for price data.
    """

    date = serializers.DateField()
    price = serializers.FloatField()


class BacktestResultSerializer(serializers.Serializer):
    """
    Serializer for backtest result data.
    """

    name = serializers.CharField(required=False, allow_blank=True)
    stats = serializers.DictField()
    lookback_returns = serializers.DictField()
    price = serializers.ListField(child=PriceDataSerializer())

    def clean_invalid_floats(self, obj):
        if isinstance(obj, dict):
            return {k: self.clean_invalid_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.clean_invalid_floats(i) for i in obj]
        elif isinstance(obj, float):
            return None if math.isnan(obj) or math.isinf(obj) else obj
        else:
            return obj

    def to_representation(self, instance):
        """
        Clean the data before serialization.
        """
        cleaned_data = self.clean_invalid_floats(instance)
        return super().to_representation(cleaned_data)


class BacktestStatSerializer(serializers.ModelSerializer):
    """
    Serializer for backtest statistics data.
    """

    class Meta:
        model = BacktestStat
        fields = "__all__"
