from django.db import models

from django.utils.translation import gettext_lazy as _


# Create your models here.
class StockManager(models.Manager):
    """
    Custom manager for Stock model to handle specific queries.
    """

    def get_distinct_tickers(self) -> models.QuerySet:
        """
        Get distinct stock tickers.
        """
        return self.values_list("ticker", flat=True).distinct()


class Stock(models.Model):
    """
    Model representing a stock.
    """

    objects = StockManager()

    name = models.CharField(verbose_name=_("이름"), max_length=100)
    ticker = models.CharField(verbose_name=_("티커"), max_length=10, unique=True)
    type = models.CharField(
        verbose_name=_("종류"),
        max_length=10,
        choices=[("stock", _("주식")), ("etf", _("ETF"))],
    )
    market = models.CharField(
        verbose_name=_("시장"),
        max_length=10,
        choices=[("kospi", _("KOSPI")), ("nasdaq", _("NASDAQ")), ("nyse", _("NYSE"))],
    )
    listed_date = models.DateField(
        verbose_name=_("상장일"), null=True, blank=True
    )  # Optional field for listing date

    class Meta:
        verbose_name = _("주식")
        verbose_name_plural = _("주식")
        ordering = ["name"]
        unique_together = ("ticker", "type")
        constraints = [
            models.UniqueConstraint(
                fields=["ticker", "type"], name="unique_ticker_type"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.ticker})"


class PriceManager(models.Manager):
    """
    Custom manager for Price model to handle specific queries.
    """

    def get_latest_prices(self, stock: Stock) -> models.QuerySet:
        """
        Get the latest prices for a given stock.
        """
        return self.filter(stock=stock).order_by("-date")

    def get_latest_price_date(self, stock: Stock) -> models.DateField:
        """
        Get the latest price date for a given stock.
        """
        latest_price = self.get_latest_prices(stock).first()
        return latest_price.date if latest_price else None


class Price(models.Model):
    """
    Model representing the price of a stock.
    """

    objects = PriceManager()

    stock = models.ForeignKey(
        Stock, verbose_name=_("주식"), on_delete=models.CASCADE, related_name="prices"
    )
    date = models.DateField(verbose_name=_("날짜"))
    open_price = models.DecimalField(
        verbose_name=_("시가"), max_digits=10, decimal_places=2
    )
    high_price = models.DecimalField(
        verbose_name=_("고가"), max_digits=10, decimal_places=2
    )
    low_price = models.DecimalField(
        verbose_name=_("저가"), max_digits=10, decimal_places=2
    )
    close_price = models.DecimalField(
        verbose_name=_("종가"), max_digits=10, decimal_places=2
    )
    adj_close_price = models.DecimalField(
        verbose_name=_("수정 종가"), max_digits=10, decimal_places=2
    )
    volume = models.BigIntegerField(verbose_name=_("거래량"))

    class Meta:
        verbose_name = _("가격")
        verbose_name_plural = _("가격")
        ordering = ["-date"]
        unique_together = ("stock", "date")
