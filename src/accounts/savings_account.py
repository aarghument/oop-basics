from decimal import Decimal

from src.accounts.account import AccountOwner
from src.accounts.bank_account import BankAccount
from src.enums import AccountStatus
from src.exceptions import InsufficientFundsError


class SavingsAccount(BankAccount):
    def __init__(
            self,
            owner: AccountOwner,
            balance: Decimal = Decimal("0"),
            currency: str = "RUB",
            account_number: str | None = None,
            min_balance: Decimal = Decimal("100"),
            interest_rate: Decimal = Decimal("0.12"),
            status: AccountStatus = AccountStatus.ACTIVE,
    ):
        super().__init__(owner, balance, currency, account_number, status)

        self._validate_amount(min_balance, allow_zero=True)
        self.min_balance = min_balance

        self._validate_rate(interest_rate)
        self._interest_rate = interest_rate

        if self._balance < self.min_balance:
            raise InsufficientFundsError(
                "Начальный баланс меньше минимального остатка"
            )

    @staticmethod
    def _validate_rate(rate: Decimal):
        if not isinstance(rate, Decimal):
            raise TypeError(
                "Процентная ставка должна иметь тип Decimal"
            )
        if not rate.is_finite() or not Decimal("0") <= rate <= Decimal("1"):
            raise ValueError(
                "Процентная ставка должна быть от 0 до 1"
            )

    @property
    def interest_rate(self):
        return self._interest_rate

    @property
    def available_balance(self) -> Decimal:
        return self._balance - self.min_balance

    def _apply_monthly_interest(self):
        self._validate_status()

        interest = self._balance * self._interest_rate
        if interest > 0:
            self.deposit(interest)

    def withdraw(self, amount: Decimal):
        self._validate_status()

        amount = self._validate_amount(amount)

        if amount > self.available_balance:
            raise InsufficientFundsError("Недостаточно средств на счёте")

        self._balance -= amount

    def get_account_info(self):
        return {
            **super().get_account_info(),
            "min_balance": str(self.min_balance),
            "monthly_interest_rate": str(self.interest_rate),
            "available_balance": str(self.available_balance),
        }

    def __str__(self):
        return (
            f"{type(self).__name__}, "
            f"Клиент: {self._owner.full_name}, "
            f"Номер счёта: ********{self._account_number[-4:]}, "
            f"Статус счёта: {self._status.value}, "
            f"Баланс: {self.available_balance:.2f}, "
            f"Ставка доходности: {self.interest_rate:.2f}"
            f"Валюта: {self._currency}"
        )