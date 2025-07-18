from django.db import models

from apps.strategy.models import Strategy

from django.utils.translation import gettext_lazy as _


# Create your models here.
class BacktestStat(models.Model):
    """
    Model representing the backtest statistics for a strategy.
    This model stores the results of a backtest, including performance metrics
    such as total return, CAGR, max drawdown, volatility, Sharpe ratio, and
    Sortino ratio.
    """

    strategy = models.ForeignKey(
        Strategy, on_delete=models.CASCADE, related_name="backtest_results"
    )

    name = models.CharField(max_length=255, verbose_name=_("결과 이름"))
    description = models.TextField(
        blank=True,
        verbose_name=_("결과 설명"),
        help_text=_("백테스트 결과에 대한 설명을 입력하세요."),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_return = models.FloatField(help_text="Total Return Percentage")
    cagr = models.FloatField(help_text="Compound Annual Growth Rate")
    max_drawdown = models.FloatField(help_text="Maximum Drawdown")
    volatility = models.FloatField(help_text="Volatility")
    sharpe_ratio = models.FloatField(help_text="Sharpe Ratio")
    sortino_ratio = models.FloatField(help_text="Sortino Ratio")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Backtest Stats for {self.strategy.name} from {self.start_date} to {self.end_date}"

    class Meta:
        verbose_name = _("백테스트 요약")
        verbose_name_plural = _("백테스트 요약")
        ordering = ["-created_at"]
