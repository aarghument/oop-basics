from contextlib import nullcontext
from decimal import Decimal

import pytest

from src.exceptions import AccountFrozenError, AccountClosedError


class TestPremiumDeposit:

    @pytest.mark.parametrize(
        "account_fixture, amount, expected, expectation",
        [
            # Активный аккаунт
            ("premium_account", "100", "3300", nullcontext()),
            ("premium_account", "5000", "-1600", nullcontext()),
            ("premium_account", "0.01", "3399.99", nullcontext()),

            # Негативные кейсы на активном акке
            ("premium_account", "0", "3500",
             pytest.raises(ValueError)),
            ("premium_account", "-100", "3500",
             pytest.raises(ValueError)),
            ("premium_account", "NaN", "3500",
             pytest.raises(ValueError)),
            ("premium_account", "Infinity", "3500",
             pytest.raises(ValueError)),

            # Замороженный аккаунт
            ("frozen_premium_account", "100", "10000",
             pytest.raises(AccountFrozenError)),
            ("frozen_premium_account", "0.01", "10000",
             pytest.raises(AccountFrozenError)),
            ("frozen_premium_account", "0", "10000",
             pytest.raises(AccountFrozenError)),
            ("frozen_premium_account", "-100", "10000",
             pytest.raises(AccountFrozenError)),

            # Закрытый аккаунт
            ("closed_premium_account", "100", "0",
             pytest.raises(AccountClosedError)),
            ("closed_premium_account", "0.01", "0",
             pytest.raises(AccountClosedError)),
            ("closed_premium_account", "0", "0",
             pytest.raises(AccountClosedError)),
            ("closed_premium_account", "-100", "0",
             pytest.raises(AccountClosedError)),
        ],
    )
    def test_deposit(
        self, request, account_fixture, amount, expected, expectation
    ):
        account = request.getfixturevalue(account_fixture)

        with expectation:
            account.withdraw(Decimal(amount))

        assert account.balance == Decimal(expected)