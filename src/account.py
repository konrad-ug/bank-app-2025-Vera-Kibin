class Account:
    def __init__(self, first_name, last_name, pesel):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.pesel = self.to_string_pesel(pesel)

    def to_string_pesel(self, pesel):
        if self.is_pesel_valid(pesel):
            return str(pesel)
        return "Invalid"

    def is_pesel_valid(self, pesel):
        if pesel is None:
            return False
        res = str(pesel)
        return len(res) == 11 and all('0' <= c <= '9' for c in res)
           