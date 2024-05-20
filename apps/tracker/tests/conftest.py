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
