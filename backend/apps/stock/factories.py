import factory
from apps.stock.models import Stock, Price


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

    name = "Test Stock"
    ticker = "TST"
    type = factory.Iterator(["stock", "etf"])
    market = factory.Iterator(["kospi", "nasdaq", "nyse"])
    listed_date = factory.Faker("date_this_decade")


class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price

    stock = factory.SubFactory(StockFactory)
    date = factory.Faker("date_this_year")
    open_price = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    high_price = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    low_price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    close_price = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    volume = factory.Faker("random_int", min=100, max=10000)
