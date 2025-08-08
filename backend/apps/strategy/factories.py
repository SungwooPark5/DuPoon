import factory

from apps.strategy.models import Strategy


class StrategyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Strategy

    name = factory.Faker("name")
    description = factory.Faker("text")
    type = factory.Iterator(["STATIC", "DYNAMIC", "COMPLEX"])
    rebalance_frequency = factory.Iterator(
        [
            "daily",
            "weekly",
            "monthly",
            "quarterly",
            "yearly",
        ]
    )
