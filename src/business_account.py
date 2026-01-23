import os
import datetime as dt
import requests
from src.base_account import BaseAccount
from datetime import date
from smtp.smtp import SMTPClient

class BusinessAccount(BaseAccount):
    histoty_email_text_template = "Company account history: {}"
    def __init__(self, company_name, nip):
        super().__init__()
        self.kwota_express = 5.0
        self.company_name = company_name
        self.nip = self.to_string_nip(nip)

        if isinstance(self.nip, str) and len(self.nip) == 10:
            ok = self.verify_nip_with_mf(self.nip)
            if not ok:
                raise ValueError("Company not registered!!")

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

    def verify_nip_with_mf(self, nip: str) -> bool:
        base = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl").rstrip("/")
        date = dt.date.today().isoformat()  
        url = f"{base}/api/search/nip/{nip}?date={date}"
        try:
            resp = requests.get(url, timeout=5)
            try:
                data = resp.json()
            except Exception:
                data = {"raw": resp.text}
            print(f"[MF] GET {url} -> {resp.status_code} {data}")
            if resp.status_code != 200:
                return False
            result = (data.get("result") or {})
            subject = (result.get("subject") or {})
            return subject.get("statusVat") == "Czynny"
        except Exception as e:
            print(f"[MF] request error: {e}")
            return False
        
    def send_history_via_email(self, email_address: str) -> bool:
        today_date = date.today().strftime("%Y-%m-%d")
        subject = "Account Transfer History "+ today_date
        text = self.histoty_email_text_template.format(self.history)
        return SMTPClient.send(subject, text, email_address)