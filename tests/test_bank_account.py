from contextlib import nullcontext

import pytest
from decimal import Decimal

from src.enums import AccountStatus
from src.exceptions import AccountFrozenError, InsufficientFundsError, InvalidOperationError


class TestAccountCreation:
    def test_create_active_account(self, active_account):
        assert active_account.status == AccountStatus.ACTIVE
        assert active_account.balance == Decimal("1000")


    def test_create_frozen_account(self, frozen_account):
        assert frozen_account.status == AccountStatus.FROZEN
        assert frozen_account.balance == Decimal("2000")


class TestDeposit:
    @pytest.mark.parametrize(
        "account_fixture, amount, expected, expectation",
        [
            # Активный счёт
            ("active_account", "100", "1100", nullcontext()),
            ("active_account", "500", "1500", nullcontext()),
            ("active_account", "1000", "2000", nullcontext()),
            ("active_account", "0.01", "1000.01", nullcontext()),

            # Некорректная сумма
            ("active_account", "0", "1000", pytest.raises(ValueError)),
            ("active_account", "-100", "1000", pytest.raises(ValueError)),

            # Замороженный счёт
            ("frozen_account", "100", "2000", pytest.raises(AccountFrozenError)),
            ("frozen_account", "500", "2000", pytest.raises(AccountFrozenError)),
            ("frozen_account", "0.01", "2000", pytest.raises(AccountFrozenError)),
            ("frozen_account", "0", "2000", pytest.raises(AccountFrozenError)),
            ("frozen_account", "-100", "2000", pytest.raises(AccountFrozenError)),
        ],
    )
    def test_deposit(
        self,
        request,
        account_fixture,
        amount,
        expected,
        expectation,
    ):
        account = request.getfixturevalue(account_fixture)

        with expectation:
            account.deposit(Decimal(amount))

        assert account.balance == Decimal(expected)

class TestWithdraw:

    @pytest.mark.parametrize(
        "account_fixture, amount, expected, expectation",
        [
            # Активный счёт
            ("active_account", "100", "900", nullcontext()),
            ("active_account", "500", "500", nullcontext()),
            ("active_account", "1000", "0", nullcontext()),
            ("active_account", "0.01", "999.99", nullcontext()),

            # Недостаточно средств
            ("active_account", "1000.01", "1000",
             pytest.raises(InsufficientFundsError)),
            ("active_account", "1001", "1000",
             pytest.raises(InsufficientFundsError)),

            # Некорректная сумма
            ("active_account", "0", "1000",
             pytest.raises(ValueError)),
            ("active_account", "-100", "1000",
             pytest.raises(ValueError)),

            # Замороженный счёт
            ("frozen_account", "500", "2000",
             pytest.raises(AccountFrozenError)),
            ("frozen_account", "1000", "2000",
             pytest.raises(AccountFrozenError)),
            ("frozen_account", "0.01", "2000",
             pytest.raises(AccountFrozenError)),
            ("frozen_account", "0", "2000",
             pytest.raises(AccountFrozenError)),
            ("frozen_account", "-100", "2000",
             pytest.raises(AccountFrozenError)),
        ],
    )
    def test_withdraw(
        self,
        request,
        account_fixture,
        amount,
        expected,
        expectation,
    ):
        account = request.getfixturevalue(account_fixture)

        with expectation:
            account.withdraw(Decimal(amount))

        assert account.balance == Decimal(expected)
