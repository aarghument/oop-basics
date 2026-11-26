from decimal import Decimal

import pytest

from src.accounts.bank_account import BankAccount
from src.enums import AccountStatus, Currency
from src.models import AccountOwner


@pytest.fixture(scope='session')
def owner():
    return AccountOwner(
        full_name='Иван Иванов',
        email='ivan.ivanov@mail.me',
        phone='+79888888888'
    )


@pytest.fixture
def active_account(owner: AccountOwner) -> BankAccount:
    return BankAccount(
        owner=owner,
        balance=Decimal("1000"),
        currency=Currency.RUB,
        status=AccountStatus.ACTIVE,
    )


@pytest.fixture
def frozen_account(owner: AccountOwner) -> BankAccount:
    return BankAccount(
        owner=owner,
        balance=Decimal("2000"),
        currency=Currency.USD,
        status=AccountStatus.FROZEN,
    )