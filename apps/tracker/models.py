from django.db import models
from django.contrib.auth.models import AbstractUser
from tracker.managers import TransactionQuerySet


class User(AbstractUser):
    ...


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    class TypeChoices(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'

    user = models.ForeignKey(User, models.CASCADE)
    category = models.ForeignKey(Category, models.CASCADE)
    type = models.CharField(
        max_length=7,
        choices=TypeChoices.choices,
    )
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField()

    objects = TransactionQuerySet.as_manager()

    def __str__(self) -> str:
        return f'{self.type} of {self.amount} on {self.date} by {self.user}'

    class Meta:
        ordering = ['-date']
