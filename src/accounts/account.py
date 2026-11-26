import uuid
from abc import ABC, abstractmethod
from decimal import Decimal

from src.enums import AccountStatus
from src.models.account_owner import AccountOwner


class AbstractAccount(ABC):
    def __init__(
        self,
        account_number: str | None,
        owner: AccountOwner,
        balance: Decimal = Decimal(0),
        status: AccountStatus = AccountStatus.ACTIVE,
    ):
        self._account_uid = uuid.uuid4()
        self._account_number = account_number
        self._owner: AccountOwner = owner
        self._balance: Decimal = balance
        self._status: AccountStatus = status

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def status(self) -> AccountStatus:
        return self._status

    @abstractmethod
    def deposit(self, amount: Decimal):
        pass

    @abstractmethod
    def withdraw(self, amount: Decimal):
        pass

    @abstractmethod
    def get_account_info(self):
        pass