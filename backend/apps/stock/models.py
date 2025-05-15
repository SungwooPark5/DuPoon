from django.db import models

from django.utils.translation import gettext_lazy as _


# Create your models here.
class Stock(models.Model):
    """
    Model representing a stock.
    """

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
