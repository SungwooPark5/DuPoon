import pytest
from datetime import date

from apps.stock.models import Stock
from apps.stock.factories import StockFactory
from apps.backtest import serializers


@pytest.mark.django_db
class TestAssetAllocationSerializer:

    @pytest.fixture
    def stock(self):
        return StockFactory(ticker="TST")

    def test_valid_data(self, stock):
        data = {"ticker": stock.ticker, "weight": 0.5}

        serializer = serializers.AssetAllocationSerializer(data=data)
        assert serializer.is_valid()

        validated_data = serializer.validated_data
        assert validated_data["ticker"].ticker == stock.ticker
        assert validated_data["weight"] == 0.5

    def test_invalid_ticker(self):
        data = {"ticker": "INVALID", "weight": 0.5}

        serializer = serializers.AssetAllocationSerializer(data=data)
        assert not serializer.is_valid()
        assert "ticker" in serializer.errors

    def test_invalid_weight(self):
        data = {"ticker": "TST", "weight": 1.5}

        serializer = serializers.AssetAllocationSerializer(data=data)
        assert not serializer.is_valid()
        assert "weight" in serializer.errors

    def test_missing_ticker(self):
        data = {"weight": 0.5}

        serializer = serializers.AssetAllocationSerializer(data=data)
        assert not serializer.is_valid()
        assert "ticker" in serializer.errors

    def test_missing_weight(self, stock):
        data = {"ticker": stock.ticker}

        serializer = serializers.AssetAllocationSerializer(data=data)
        assert not serializer.is_valid()
        assert "weight" in serializer.errors


@pytest.mark.django_db
class TestBacktestSerializer:
    @pytest.fixture
    def stock1(self):
        return StockFactory(ticker="TST1")

    @pytest.fixture
    def stock2(self):
        return StockFactory(ticker="TST2")

    def test_valid_data(self, stock1, stock2):
        data = {
            "allocations": [
                {"ticker": stock1.ticker, "weight": 0.6},
                {"ticker": stock2.ticker, "weight": 0.4},
            ],
            "strategy_name": "Test Strategy",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "rebalance_freq": "monthly",
            "slippage": 0.01,
        }

        serializer = serializers.BacktestSerializer(data=data)
        assert serializer.is_valid()

        validated_data = serializer.validated_data
        assert validated_data["strategy_name"] == "Test Strategy"
        assert len(validated_data["allocations"]) == 2
        assert validated_data["start_date"] == date(2023, 1, 1)
        assert validated_data["end_date"] == date(2023, 12, 31)
        assert validated_data["rebalance_freq"] == "monthly"
        assert validated_data["slippage"] == 0.01

    def test_invalid_ticker(self):
        data = {
            "allocations": [
                {"ticker": "INVALID", "weight": 0.5},
            ],
            "rebalance_freq": "monthly",
            "strategy_name": "Test Strategy",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
        }

        serializer = serializers.BacktestSerializer(data=data)
        assert not serializer.is_valid()
        assert "allocations" in serializer.errors

    def test_invalid_total_weight(self, stock1, stock2):
        data = {
            "allocations": [
                {"ticker": stock1.ticker, "weight": 0.6},
                {"ticker": stock2.ticker, "weight": 0.5},  # Total weight exceeds 1.0
            ],
            "rebalance_freq": "monthly",
            "strategy_name": "Test Strategy",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
        }

        serializer = serializers.BacktestSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors


# Pass the test for BacktestResultSerializer, PriceDataSerializer and BacktestStatSerializer
# These serializers are for data representation
