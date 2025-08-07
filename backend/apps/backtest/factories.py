import factory


class BacktestStatFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating BacktestStat instances.
    """

    class Meta:
        model = "backtest.BacktestStat"

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    start_date = factory.Faker("date_between", start_date="-5y", end_date="-1y")
    end_date = factory.Faker("date_between", start_date="-1y", end_date="today")

    total_return = factory.Faker(
        "pyfloat", left_digits=2, right_digits=4, positive=True
    )
    cagr = factory.Faker("pyfloat", left_digits=1, right_digits=4, positive=True)
    max_drawdown = factory.Faker(
        "pyfloat", left_digits=1, right_digits=4, positive=True
    )
    volatility = factory.Faker("pyfloat", left_digits=1, right_digits=4, positive=True)
    sharpe_ratio = factory.Faker("pyfloat", left_digits=1, right_digits=4)
    sortino_ratio = factory.Faker("pyfloat", left_digits=1, right_digits=4)
