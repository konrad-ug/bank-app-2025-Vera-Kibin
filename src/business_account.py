from src.base_account import BaseAccount

class BusinessAccount(BaseAccount):
    def __init__(self, company_name, nip):
        super().__init__()
        self.kwota_express = 5.0
        self.company_name = company_name
        self.nip = self.to_string_nip(nip)

    def to_string_nip(self, nip):
        if self.is_nip_valid(nip):
            return str(nip)
        return "Invalid"

    def is_nip_valid(self, nip):
        if nip is None:
            return False
        res = str(nip)
        return len(res) == 10 and all('0' <= c <= '9' for c in res)
    
    def has_zus_transfer(self) -> bool:
        return any(x == -1775.0 for x in self.history)

    def submit_for_loan(self, amount):
        amt = self.sprawdzanie_kwoty(amount)
        if not amt or amt <= 0:
            return False
        if self.balance >= 2 * amt and self.has_zus_transfer():
            self.balance += amt
            self.history.append(amt)
            return True
        return False