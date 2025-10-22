class Account:
    def __init__(self, first_name, last_name, pesel, promo_kod=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.pesel = self.to_string_pesel(pesel)
        self.promo_code = promo_kod if self.is_promo_valid(promo_kod) and self.is_rok_urodzienia_ok(self.pesel) else None
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
    
    def yob_from_pesel(self, pesel):
        sprawdzanie = str(pesel)
        if len(sprawdzanie)!=11 or not sprawdzanie.isdigit():
            return None
        yy = int(sprawdzanie[0:2])
        mm = int(sprawdzanie[2:4])
        if 1 <= mm <= 12:
            century = 1900
        elif 21 <= mm <= 32:
            century = 2000
            mm -= 20
        elif 41 <= mm <= 52:
            century = 2100
            mm -= 40
        elif 61 <= mm <= 72:
            century = 2200
            mm -= 60
        elif 81 <= mm <= 92:
            century = 1800
            mm -= 80
        else:
            return None 
        return century + yy
    
    def is_rok_urodzienia_ok(self, pesel):
        rok = self.yob_from_pesel(pesel)
        return rok is not None and rok > 1960
    
    def is_promo_valid(self, promo_kod):
        if promo_kod is None:
            return False
        res = str(promo_kod)
        suffix = res[len("PROM_"):]
        return res.startswith("PROM_") and len(res) == 8 and all(c.isalnum() for c in suffix)
           
    def sprawdzanie_kwoty(self, kwota):
        if isinstance(kwota, str):
            if kwota.isdigit():
                res = int(kwota)
                return res
            return False
        if isinstance(kwota, int): # float? jak nie - dopisac testy
            return kwota
        return False
    
    def przelew_przychodzacy(self, kwota):
        result = self.sprawdzanie_kwoty(kwota)
        if result > 0:
            self.balance = self.balance + result
            return self.balance
        return False
    
    def przelew_wychodzacy(self, kwota):
        result = self.sprawdzanie_kwoty(kwota)
        if result > 0 and self.balance>=result:
            self.balance = self.balance - result
            return self.balance
        return False
