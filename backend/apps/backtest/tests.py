import pytest

from apps.stock.models import Price, Stock
from apps.stock.factories import StockFactory, PriceFactory


# Create your tests here.
@pytest.mark.django_db
class TestBacktest:

    def setup_method(self):
        self.stock1 = StockFactory(name="SPY", ticker="SPY")
        self.stock2 = StockFactory(name="TLT", ticker="TLT")
        self.price_data = [
            PriceFactory(stock=self.stock1, date="2023-01-01", adj_close_price=100),
            PriceFactory(stock=self.stock1, date="2023-01-02", adj_close_price=102),
            PriceFactory(stock=self.stock2, date="2023-01-01", adj_close_price=200),
            PriceFactory(stock=self.stock2, date="2023-01-02", adj_close_price=198),
        ]

    def test_6040_allocation_strategy(self):
        from apps.backtest.strategies import get_static_allocation_strategy

        # Create sample allocations
        allocations = [
            {"ticker": self.stock1, "weight": 0.6},
            {"ticker": self.stock2, "weight": 0.4},
        ]

        # Run the strategy
        backtest = get_static_allocation_strategy(allocations)
        results = backtest.run()

        # Check if the backtest object is created
        assert backtest is not None
        assert hasattr(backtest, "run")
