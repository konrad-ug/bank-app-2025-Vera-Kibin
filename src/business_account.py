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