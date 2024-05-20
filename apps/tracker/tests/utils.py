from typing import List

from tracker.models import Transaction


def amount_sum_by_transaction_type(
    transactions: List[Transaction], type: Transaction.TypeChoices
) -> float:
    return sum(
        map(
            lambda t: t.amount,
            filter(
                lambda t: t.type == type,
                transactions,
            ),
        )
    )
