from decimal import Decimal

import pytest

from src.accounts.savings_account import SavingsAccount
from src.exceptions import AccountFrozenError, AccountClosedError

class TestMonthlyInterestActiveAccount:

    @pytest.mark.parametrize(
        "balance, rate, expected_balance",
        [
            ("10000", "0.02", "10200"),
            ("10000", "0.01",  "10100"),
            ("10000", "0.05", "10500"),
            ("10000", "0", "10000"),
            ("0", "0.02", "0"),
        ],
    )
    def test_monthly_interest(
        self,
        owner,
        balance,
        rate,
        expected_balance,
    ):
        account = SavingsAccount(
            owner=owner,
            balance=Decimal(balance),
            min_balance=Decimal("0"),
            interest_rate=Decimal(rate),
        )
        account._apply_monthly_interest()

        assert account._balance == Decimal(expected_balance)


class TestMonthlyInterestFrozenAccount:
    @pytest.mark.parametrize(
        "account_fixture, balance, rate, expectation",
        [
            ("frozen_savings_account","10000", "0.02", pytest.raises(AccountFrozenError)),
            ("frozen_savings_account", "10000", "0",  pytest.raises(AccountFrozenError)),
            ("frozen_savings_account", "10000", "0.02", pytest.raises(AccountFrozenError)),
        ],
    )
    def test_monthly_interest(
        self,
        request,
        account_fixture,
        balance,
        rate,
        expectation
    ):
        account = request.getfixturevalue(account_fixture)
        with expectation:
            account._apply_monthly_interest()

        assert account._balance == Decimal(balance)


class TestMonthlyInterestClosedAccount:
    @pytest.mark.parametrize(
        "account_fixture, balance, rate, expectation",
        [
            ("closed_savings_account","0", "0.02", pytest.raises(AccountClosedError)),
            ("closed_savings_account", "0", "0",  pytest.raises(AccountClosedError)),
            ("closed_savings_account", "0", "0.02", pytest.raises(AccountClosedError)),
        ],
    )
    def test_monthly_interest(
        self,
        request,
        account_fixture,
        balance,
        rate,
        expectation
    ):
        account = request.getfixturevalue(account_fixture)
        with expectation:
            account._apply_monthly_interest()

        assert account._balance == Decimal(balance)