from decimal import Decimal

from pygments.lexers import q

from src.accounts.bank_account import BankAccount
from src.enums import AccountStatus
from src.exceptions import InsufficientFundsError
from src.models import AccountOwner


class PremiumAccount(BankAccount):
    def __init__(
            self,
            owner: AccountOwner,
            balance: Decimal = Decimal("0"),
            currency: str = "RUB",
            account_number: str | None = None,
            status: AccountStatus = AccountStatus.ACTIVE,
            fee: Decimal = Decimal("0"),
            overdraft_limit: Decimal = Decimal("1000"),
    ):
        super().__init__(owner, balance, currency, account_number, status)

        self._overdraft_limit = self._validate_amount(
            overdraft_limit,
            allow_zero=True,
        )

        self._fee = self._validate_amount(
            fee,
            allow_zero=True,
        )

    @property
    def fee(self) -> Decimal:
        return self._fee


    @property
    def available_balance(self) -> Decimal:
        return max(
            Decimal("0"),
            self._balance + self._overdraft_limit - self._fee
        )

    @property
    def overdraft_used(self) -> Decimal:
        return max(Decimal("0"), -self._balance)

    @property
    def overdraft_remaining(self) -> Decimal:
        return self._overdraft_limit - self.overdraft_used

    def withdraw(self, amount: Decimal):
        self._validate_status()
        self._validate_amount(amount)
        total = amount + self._fee

        if self._balance - total < -self._overdraft_limit:
            raise InsufficientFundsError(
                "Превышен лимит овердрафта"
            )

        self._balance -= total

    def get_account_info(self) -> dict:
        return {
            "account_number": self._account_number,
            "owner": self._owner.full_name,
            "balance": self.available_balance,
            "currency": self._currency.value,
            "status": self._status.value,
            "overdraft_limit": self._overdraft_limit,
            "fee": self._fee.value,
        }

    def __str__(self):
        return (
            f"{type(self).__name__}, "
            f"Клиент: {self._owner.full_name}, "
            f"Номер счёта: ********{self._account_number[-4:]}, "
            f"Статус счёта: {self._status.value}, "
            f"Баланс: {self.available_balance:.2f}, "
            f"Валюта: {self._currency}"
            f"Комиссия: {self._fee}, "
            f"Овердрафт: {self.overdraft_remaining}"
        )