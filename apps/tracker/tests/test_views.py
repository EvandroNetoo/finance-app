from django.test.client import Client
from django.urls import reverse
from typing import List
import pytest

from tracker.tests.utils import amount_sum_by_transaction_type
from tracker.models import Transaction


@pytest.mark.django_db
def test_total_values_appear_on_list_page(
    user_transactions: List[Transaction], client: Client
):
    user = user_transactions[0].user
    client.force_login(user)

    total_income = amount_sum_by_transaction_type(
        user_transactions, Transaction.TypeChoices.INCOME
    )
    total_expense = amount_sum_by_transaction_type(
        user_transactions, Transaction.TypeChoices.EXPENSE
    )
    net_income = total_income - total_expense

    response = client.get(reverse('transactions-list'))

    assert response.context.get('total_income') == total_income
    assert response.context.get('total_expenses') == total_expense
    assert response.context.get('net_income') == net_income
