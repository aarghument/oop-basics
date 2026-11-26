from decimal import Decimal

from src.accounts.account import AbstractAccount, AccountOwner
from src.enums import Currency, AccountStatus
from src.exceptions import InsufficientFundsError, InvalidOperationError, AccountFrozenError, AccountClosedError


class BankAccount(AbstractAccount):
    def __init__(
        self,
        owner: AccountOwner,
        balance: Decimal = Decimal("0"),
        currency: str = "RUB",
        account_number: str | None = None,
        status: AccountStatus = AccountStatus.ACTIVE,
    ):

        balance = self._validate_amount(balance, allow_zero=True)

        super().__init__(account_number, owner, balance, status)

        self._currency = Currency(currency)

        self._account_number = (
            account_number.strip()
            if account_number is not None
            else self._generate_account_number()
        )

    def _generate_account_number(self, length: int = 12):
        return str(self._account_uid.int % (10**length)).zfill(length)

    @staticmethod
    def _validate_amount(
        amount,
        allow_zero: bool = False,
    ) -> Decimal:
        try:
            amount = Decimal(str(amount))
        except (InvalidOperationError, ValueError, TypeError):
            raise ValueError("Некорректная сумма")

        if not amount.is_finite():
            raise ValueError("Сумма должна быть конечным числом")

        if amount < 0 or (amount == 0 and not allow_zero):
            raise ValueError("Сумма должна быть больше нуля")

        return amount

    def _validate_status(self) -> None:
        match self._status:
            case AccountStatus.FROZEN:
                raise AccountFrozenError("Счёт заморожен")

            case AccountStatus.CLOSED:
                raise AccountClosedError("Счёт закрыт")

            case AccountStatus.ACTIVE:
                return

    def deposit(self, amount: Decimal) -> None:
        self._validate_status()

        amount = self._validate_amount(amount)
        self._balance += amount

    def withdraw(self, amount: Decimal) -> None:
        self._validate_status()

        amount = self._validate_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError("Недостаточно средств на счёте")

        self._balance -= amount


    def get_account_info(self) -> dict:
        return {
            "account_number": self._account_number,
            "owner": self._owner.full_name,
            "balance": self._balance,
            "currency": self._currency.value,
            "status": self._status.value,
        }

    def __str__(self):
        return (
            f"{type(self).__name__}, "
            f"Клиент: {self._owner.full_name}, "
            f"Номер счёта: ********{self._account_number[-4:]}, "
            f"Статус счёта: {self._status.value}, "
            f"Баланс: {self._balance:.2f}, "
            f"Валюта: {self._currency}"
        )