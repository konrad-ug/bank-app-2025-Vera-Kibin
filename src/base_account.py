class BaseAccount:
    def __init__(self):
         self.balance = 0.0
         self.history = []

    kwota_express = 0.0

    def sprawdzanie_kwoty(self, kwota):
        if isinstance(kwota, str):
            if kwota.replace(".", "",1).isdigit():
                res = float(kwota)
                return res
            return False
        if isinstance(kwota, (float, int)):
            res = float(kwota)
            return res
        return False
    
    def przelew_przychodzacy(self, kwota):
        result = self.sprawdzanie_kwoty(kwota)
        if result > 0:
            self.balance = self.balance + result
            self.history.append(result)
            return self.balance
        return False
    
    def przelew_wychodzacy(self, kwota):
        result = self.sprawdzanie_kwoty(kwota)
        if result > 0 and self.balance>=result:
            self.balance = self.balance - result
            self.history.append(-result)
            return self.balance
        return False
    
    def przelew_ekspresowy(self, kwota):
        result = self.sprawdzanie_kwoty(kwota)
        kwota_res = self.kwota_express
        if result > 0 and self.balance>=result:
            self.balance = self.balance - (result+kwota_res)
            self.history.extend([-result, -kwota_res])
            return self.balance
        return False
     