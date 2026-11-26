from contextlib import nullcontext
from decimal import Decimal

import pytest

from src.accounts.savings_account import SavingsAccount
from src.exceptions import (
    InsufficientFundsError,
)


class TestSavingsAccountCreation:

    @pytest.mark.parametrize(
        "balance, min_balance, rate, expectation",
        [
            ("10000", "2000", "0.02", nullcontext()),
            ("2000", "2000", "0.02", nullcontext()),
            ("0", "0", "0", nullcontext()),
            ("1000", "2000", "0.02",
             pytest.raises(InsufficientFundsError)),
            ("10000", "-100", "0.02",
             pytest.raises(ValueError)),
            ("10000", "2000", "-0.01",
             pytest.raises(ValueError)),
            ("10000", "2000", "1.01",
             pytest.raises(ValueError)),
            ("10000", "2000", "NaN",
             pytest.raises(ValueError)),
        ],
    )
    def test_creation(
        self, owner, balance, min_balance, rate, expectation
    ):
        with expectation:
            account = SavingsAccount(
                owner=owner,
                balance=Decimal(balance),
                min_balance=Decimal(min_balance),
                interest_rate=Decimal(rate),
            )

            assert account.balance == Decimal(balance)
            assert account.min_balance == Decimal(min_balance)
            assert account.interest_rate == Decimal(rate)