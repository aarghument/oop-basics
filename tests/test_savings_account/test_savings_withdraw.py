from contextlib import nullcontext
from decimal import Decimal

import pytest

from src.exceptions import (
    InsufficientFundsError, AccountFrozenError, AccountClosedError,
)



class TestSavingsWithdraw:

    @pytest.mark.parametrize(
        "account_fixture, amount, expected, expectation",
        [
            # Успешное снятие
            ("savings_account", "100", "9900", nullcontext()),
            ("savings_account", "5000", "5000", nullcontext()),
            ("savings_account", "0.01", "9999.99", nullcontext()),

            # Граница минимального остатка
            ("savings_account", "8000", "2000", nullcontext()),
            ("savings_account", "7999.99", "2000.01", nullcontext()),

            # Нарушение минимального остатка
            ("savings_account", "8000.01", "10000",
             pytest.raises(InsufficientFundsError)),
            ("savings_account", "10000", "10000",
             pytest.raises(InsufficientFundsError)),

            # Некорректная сумма
            ("savings_account", "0", "10000",
             pytest.raises(ValueError)),
            ("savings_account", "-100", "10000",
             pytest.raises(ValueError)),

            # Замороженный счёт
            ("frozen_savings_account", "100", "10000",
             pytest.raises(AccountFrozenError)),
            ("frozen_savings_account", "10001", "10000",
             pytest.raises(AccountFrozenError)),

            # Закрытый счёт
            ("closed_savings_account", "100", "2000",
             pytest.raises(AccountClosedError)),
            ("closed_savings_account", "10001", "2000",
             pytest.raises(AccountClosedError)),
        ],
    )
    def test_withdraw(
        self, request, account_fixture, amount, expected, expectation
    ):
        account = request.getfixturevalue(account_fixture)

        with expectation:
            account.withdraw(Decimal(amount))

        assert account.balance == Decimal(expected)