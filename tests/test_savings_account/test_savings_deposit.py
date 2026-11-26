from contextlib import nullcontext
from decimal import Decimal

import pytest

from src.exceptions import AccountFrozenError, AccountClosedError


class TestSavingsDeposit:

    @pytest.mark.parametrize(
        "account_fixture, amount, expected, expectation",
        [
            ("savings_account", "100", "10100", nullcontext()),
            ("savings_account", "0.01", "10000.01", nullcontext()),

            ("savings_account", "0", "10000",
             pytest.raises(ValueError)),
            ("savings_account", "-100", "10000",
             pytest.raises(ValueError)),
            ("frozen_savings_account", "100", "10000",
             pytest.raises(AccountFrozenError)),
            ("frozen_savings_account", "-100", "10000",
             pytest.raises(AccountFrozenError)),
            ("closed_savings_account", "100", "0",
             pytest.raises(AccountClosedError)),
            ("closed_savings_account", "-100", "0",
             pytest.raises(AccountClosedError)),
        ],
    )
    def test_deposit(
        self, request, account_fixture, amount, expected, expectation
    ):
        account = request.getfixturevalue(account_fixture)

        with expectation:
            account.deposit(Decimal(amount))

        assert account.balance == Decimal(expected)