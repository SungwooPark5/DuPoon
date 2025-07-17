from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Strategy(models.Model):
    """
    Model representing a trading strategy.
    """

    STRATEGY_TYPES = [
        ("STATIC", "Static"),
        ("DYNAMIC", "Dynamic"),
        ("COMPLEX", "Complex"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=STRATEGY_TYPES, default="STATIC")

    # allocations is valid only for static strategies
    # For dynamic strategies, allocations will be handled differently
    # and will not be stored in the database.
    allocations = models.JSONField(
        blank=True,
        null=True,
        help_text="Asset allocations for the strategy in JSON format",
    )

    parameters = models.JSONField(blank=True, null=True)

    rebalance_frequency = models.CharField(
        max_length=20,
        choices=[
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("yearly", "Yearly"),
        ],
        default="monthly",
        help_text="Rebalance frequency for the strategy",
    )
    include_cash = models.BooleanField(
        default=False,
        help_text="Whether to include cash in the strategy",
    )
    cash_ticker = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        default="CASH",
        help_text="Ticker symbol for cash asset in the strategy",
    )
    cash_weight = models.FloatField(
        null=True,
        blank=True,
        default=0.0,
        help_text="Weight of cash in the strategy (0.0 to 1.0)",
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_static(self):
        return self.type == "STATIC"

    class Meta:
        verbose_name = _("전략")
        verbose_name_plural = _("전략")
        ordering = ["-created_at"]
