from django.db import models

from django.utils.translation import gettext_lazy as _

# Create your models here.
class Strategy(models.Model):
    """
    Model representing a trading strategy."""
    
    STRATEGY_TYPES = [
        ('STATIC', 'Static'),
        ('DYNAMIC', 'Dynamic'),
        ('COMPLEX', 'Complex'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=STRATEGY_TYPES, default='STATIC')
    parameters = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("전략")
        verbose_name_plural = _("전략")
        ordering = ['-created_at']