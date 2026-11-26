from contextlib import nullcontext

import pytest
from decimal import Decimal

from src.accounts.premium_account import PremiumAccount


class TestPremiumAccountCreation:

    @pytest.mark.parametrize(
        "overdraft_limit, fee, expectation",
        [
            # Правильные овердрафт и комиссия
            ("20000", "50", nullcontext()),
            ("0", "50", nullcontext()),
            ("20000", "0", nullcontext()),
            ("0", "0", nullcontext()),
            ("0.01", "0.01", nullcontext()),

            # Неверный овердрафт
            ("-20000", "50", pytest.raises(ValueError)),
            ("-0.01", "50", pytest.raises(ValueError)),
            ("NaN", "50", pytest.raises(ValueError)),
            ("Infinity", "50", pytest.raises(ValueError)),

            # Неверная комиссия
            ("20000", "-50", pytest.raises(ValueError)),
            ("20000", "-0.01", pytest.raises(ValueError)),
            ("20000", "NaN", pytest.raises(ValueError)),
            ("20000", "Infinity", pytest.raises(ValueError)),
        ],
    )
    def test_creation(
        self, owner, overdraft_limit, fee, expectation
    ):
        with expectation:
            account = PremiumAccount(
                owner=owner,
                balance=Decimal("10000"),
                overdraft_limit=Decimal(overdraft_limit),
                fee=Decimal(fee),
            )

            assert account._overdraft_limit == Decimal(overdraft_limit)
            assert account._fee == Decimal(fee)