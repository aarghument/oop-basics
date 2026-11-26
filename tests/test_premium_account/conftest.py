from decimal import Decimal

import pytest

from src.accounts.premium_account import PremiumAccount
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
def premium_account(owner):
    return PremiumAccount(
        owner=owner,
        balance=Decimal("3500"),
        overdraft_limit=Decimal("20000"),
        fee=Decimal("100"),
    )


@pytest.fixture
def frozen_premium_account(owner):
    return PremiumAccount(
        owner=owner,
        balance=Decimal("10000"),
        overdraft_limit=Decimal("20000"),
        fee=Decimal("50"),
        status=AccountStatus.FROZEN,
    )


@pytest.fixture
def closed_premium_account(owner):
    return PremiumAccount(
        owner=owner,
        balance=Decimal("0"),
        overdraft_limit=Decimal("20000"),
        fee=Decimal("100"),
        status=AccountStatus.CLOSED,
    )
