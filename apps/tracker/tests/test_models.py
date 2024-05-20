from typing import List
import pytest

from tracker.tests.utils import amount_sum_by_transaction_type
from tracker.models import Transaction


@pytest.mark.django_db
def test_queryset_income_method(transactions: List[Transaction]):
    qs = Transaction.objects.get_income()

    assert qs.count() > 0
    assert all(map(lambda t: t.type == Transaction.TypeChoices.INCOME, qs))


@pytest.mark.django_db
def test_queryset_expenses_method(transactions: List[Transaction]):
    qs = Transaction.objects.get_expenses()

    assert qs.count() > 0
    assert all(map(lambda t: t.type == Transaction.TypeChoices.EXPENSE, qs))


@pytest.mark.django_db
def test_queryset_total_income_method(transactions: List[Transaction]):
    total_income = Transaction.objects.get_total_income()
    assert total_income == amount_sum_by_transaction_type(
        transactions, Transaction.TypeChoices.INCOME
    )


@pytest.mark.django_db
def test_queryset_total_expenses_method(transactions: List[Transaction]):
    total_expenses = Transaction.objects.get_total_expenses()
    assert total_expenses == amount_sum_by_transaction_type(
        transactions, Transaction.TypeChoices.EXPENSE
    )
