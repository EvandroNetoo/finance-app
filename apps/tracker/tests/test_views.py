from django.test.client import Client
from django.urls import reverse
from django_htmx.http import HttpResponseClientRedirect

from datetime import datetime, timedelta
from typing import List
import pytest
from pytest_django.asserts import assertTemplateUsed

from tracker.tests.utils import amount_sum_by_transaction_type
from tracker.models import Transaction, Category, User


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

    response = client.get(reverse('list-transactions'))

    assert response.context.get('total_income') == total_income
    assert response.context.get('total_expenses') == total_expense
    assert response.context.get('net_income') == net_income


@pytest.mark.django_db
def test_transaction_type_filter(
    user_transactions: List[Transaction], client: Client
):
    user = user_transactions[0].user
    client.force_login(user)

    GET_params = {'transaction_type': 'income'}
    response = client.get(reverse('list-transactions'), GET_params)
    qs = response.context.get('filter').qs

    assert all(map(lambda t: t.type == 'income', qs))


@pytest.mark.django_db
def test_start_end_date_filter(
    user_transactions: List[Transaction], client: Client
):
    user = user_transactions[0].user
    client.force_login(user)

    start_date_cutoff = datetime.now().date() - timedelta(days=120)
    end_date_cutoff = datetime.now().date() - timedelta(days=30)

    GET_params = {'start_date': start_date_cutoff, 'end_date': end_date_cutoff}
    response = client.get(reverse('list-transactions'), GET_params)
    qs = response.context.get('filter').qs

    assert all(
        map(lambda t: start_date_cutoff <= t.date <= end_date_cutoff, qs)
    )


@pytest.mark.django_db
def test_category_filter(user_transactions: List[Transaction], client: Client):
    user = user_transactions[0].user
    client.force_login(user)

    category_pks = Category.objects.all()[:2].values_list('pk', flat=True)

    GET_params = {'category': category_pks}
    response = client.get(reverse('list-transactions'), GET_params)
    qs = response.context.get('filter').qs

    assert all(map(lambda t: t.category.pk in category_pks, qs))


@pytest.mark.django_db
def test_add_transaction_request(
    user: User, transactions_dict_params: dict[str, str | int], client: Client
):
    client.force_login(user)
    user_transaction_count = Transaction.objects.filter(user=user).count()

    headers = {'HTTP_HX-Request': True}
    response = client.post(
        reverse('create-transaction'),
        transactions_dict_params,
        **headers,
    )

    assert (
        Transaction.objects.filter(user=user).count()
        == user_transaction_count + 1
    )
    assert isinstance(response, HttpResponseClientRedirect)
    assert (
        'HX-Redirect',
        reverse('list-transactions'),
    ) in response.headers.items()


@pytest.mark.django_db
def test_cannot_add_transaction_with_negative_amount(
    user: User, transactions_dict_params: dict[str, str | int], client: Client
):
    client.force_login(user)
    user_transaction_count = Transaction.objects.filter(user=user).count()

    transactions_dict_params['amount'] = -1
    headers = {'HTTP_HX-Request': True}
    response = client.post(
        reverse('create-transaction'),
        transactions_dict_params,
        **headers,
    )

    assert user_transaction_count == Transaction.objects.filter(user=user).count()
    assertTemplateUsed('partials/create-transaction.html')
    assert (
        'HX-Retarget',
        '#transaction-block',
    ) in response.headers.items()
    assert response.context['form'].has_error('amount') == True
