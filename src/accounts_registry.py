from src.account import Account
from typing import Optional, List

class AccountsRegistry:
    def __init__(self) -> None:
        self.accounts: List[Account] = []

    def add_account(self, account: Account) -> None:
        if not isinstance(account, Account):
            raise TypeError("Only personal Account instances are allowed")
        self.accounts.append(account)

    def find_by_pesel(self, pesel) -> Optional[Account]:
        key = str(pesel)
        for acc in self.accounts:
            if acc.pesel == key:
                return acc
        return None

    def all_accounts(self) -> List[Account]:
        return list(self.accounts)

    def count(self) -> int:
        return len(self.accounts)
    
    def remove_by_pesel(self, pesel: str) -> bool:
        acc = self.find_by_pesel(pesel)
        if not acc:
            return False
        self.accounts.remove(acc)
        return True