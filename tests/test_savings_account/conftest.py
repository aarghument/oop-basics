from decimal import Decimal

import pytest

from src.accounts.savings_account import SavingsAccount
from src.enums import AccountStatus
from src.models import AccountOwner


@pytest.fixture
def owner():
    return AccountOwner(
        full_name='Иван Иванов',
        email='ivan.ivanov@mail.me',
        phone='+79888888888'
    )



@pytest.fixture
def savings_account(owner):
    return SavingsAccount(
        owner=owner,
        balance=Decimal("10000"),
        min_balance=Decimal("2000"),
        interest_rate=Decimal("0.02"),
    )


@pytest.fixture
def frozen_savings_account(owner):
    return SavingsAccount(
        owner=owner,
        balance=Decimal("10000"),
        min_balance=Decimal("2000"),
        interest_rate=Decimal("0.02"),
        status=AccountStatus.FROZEN,
    )


@pytest.fixture
def closed_savings_account(owner):
    return SavingsAccount(
        owner=owner,
        balance=Decimal("0"),
        min_balance=Decimal("0"),
        interest_rate=Decimal("0.35"),
        status=AccountStatus.CLOSED,
    )