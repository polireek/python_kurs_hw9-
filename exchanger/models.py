from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet

from django.utils import timezone
# Create your models here.


class ExchangeRate(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    id = models.CharField(max_length=6, primary_key=True)
    currency_a = models.CharField(max_length=5)
    currency_b = models.CharField(max_length=5)
    buy = models.DecimalField(decimal_places=2, max_digits=12)
    buy_status = models.DecimalField(decimal_places=0, default=0, max_digits=1)
    sell = models.DecimalField(decimal_places=2, max_digits = 12)
    sell_status = models.DecimalField(decimal_places=0, default=0, max_digits = 1)
    created_time = models.DateTimeField(default=timezone.now)
    def get_status(self,status):
        if status == 1:
            return "UP"
        elif status == -1:
            return "DOWM"
        elif status == 0:
            return "HOLD"
    def to_dict(self):
        currency_a = self.currency_a.lower()
        return {
            f"{currency_a}_buy": self.buy,
            f"{currency_a}_sell": self.sell,
            f"{currency_a}_buy_s": self.get_status(self.buy_status),
            f"{currency_a}_sell_s": self.get_status(self.sell_status),
        }

