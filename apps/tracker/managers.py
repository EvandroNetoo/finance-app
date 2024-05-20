from django.db import models
from django.apps import apps


class TransactionQuerySet(models.QuerySet):
    if apps.models_ready:
        model = apps.get_model('tracker', 'Transaction')

    def get_expenses(self):
        return self.filter(type=self.model.TypeChoices.EXPENSE)

    def get_income(self):
        return self.filter(type=self.model.TypeChoices.INCOME)

    def get_total_expenses(self):
        return (
            self.get_expenses().aggregate(total=models.Sum('amount'))['total']
            or 0
        )

    def get_total_income(self):
        return (
            self.get_income().aggregate(total=models.Sum('amount'))['total']
            or 0
        )
