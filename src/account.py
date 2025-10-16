class Account:
    def __init__(self, first_name, last_name, pesel, promo_kod=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.pesel = self.to_string_pesel(pesel)
        self.promo_code = promo_kod if self.is_promo_valid(promo_kod) else None
        if self.promo_code:
            self.balance += 50

    def to_string_pesel(self, pesel):
        if self.is_pesel_valid(pesel):
            return str(pesel)
        return "Invalid"

    def is_pesel_valid(self, pesel):
        if pesel is None:
            return False
        res = str(pesel)
        return len(res) == 11 and all('0' <= c <= '9' for c in res)
    
    def is_promo_valid(self, promo_kod):
        if promo_kod is None:
            return False
        res = str(promo_kod)
        suffix = res[len("PROM_"):]
        return res.startswith("PROM_") and len(res) == 8 and all(c.isalnum() for c in suffix)
           