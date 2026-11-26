from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AccountOwner:
    full_name: str
    email: str
    phone: str = ""
