import pytest
from typing import List

from tracker.factories import TransactionFactory, UserFactory
from tracker.models import Transaction


@pytest.fixture
def transactions() -> List[Transaction]:
    return TransactionFactory.create_batch(20)


@pytest.fixture
def user_transactions() -> List[Transaction]:
    user = UserFactory()
    return TransactionFactory.create_batch(20, user=user)


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def transactions_dict_params(user):
    transactions = TransactionFactory.create(user=user)
    return {
        'type': transactions.type,
        'category': transactions.category_id,
        'date': transactions.date,
        'amount': transactions.amount,
    }
