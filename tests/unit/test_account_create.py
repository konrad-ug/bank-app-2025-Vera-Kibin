from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678910"
        assert account.promo_code == None

## testy PESEL

    def test_pesel_empty(self):
        account = Account("Vera", "Kibin", "")
        assert account.pesel == "Invalid"
    def test_pesel_empty_none(self):
        account = Account("Vera", "Kibin", None)
        assert account.pesel == "Invalid"
    def test_pesel_less(self):
        account = Account("Vera", "Kibin", "123")
        assert account.pesel == "Invalid"
    def test_pesel_more(self):
        account = Account("Vera", "Kibin", "123123123123")
        assert account.pesel == "Invalid"
    def test_pesel_litera(self):
        account = Account("Vera", "Kibin", "1234567891A")
        assert account.pesel == "Invalid"
    def test_pesel_litery(self):
        account = Account("Vera", "Kibin", "mlkhgfedcbA")
        assert account.pesel == "Invalid"
    def test_pesel_typ_digit(self):
        account = Account("Vera", "Kibin", 12345678910)
        assert account.pesel == "12345678910"
    def test_pesel_z_zero(self):
        account = Account("Vera", "Kibin", "01234567890")
        assert account.pesel == "01234567890"


## testy PROMO_KOD

    def test_promo_none(self):
        account = Account("Vera", "Kibin", 12345678910)
        assert account.promo_code == None
        assert account.balance == 0
    
    def test_promo_maly_litery(self):
        account = Account("Vera", "Kibin", 12345678910, "prom_hej")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_dobry(self):
        account = Account("Vera", "Kibin", 12345678910, "PROM_hej")
        assert account.promo_code == "PROM_hej"
        assert account.balance == 50

    def test_promo_dobry_cyfry(self):
        account = Account("Vera", "Kibin", 12345678910, "PROM_123")
        assert account.promo_code == "PROM_123"
        assert account.balance == 50

    def test_promo_mixed_case(self):
        account = Account("Vera", "Kibin", 12345678910, "PROM_A9b")
        assert account.promo_code == "PROM_A9b"
        assert account.balance == 50

    def test_promo_zamalo_znakow(self):
        account = Account("Vera", "Kibin", 12345678910, "PROM_1")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_zaduzo_znakow(self):
        account = Account("Vera", "Kibin", 12345678910, "PROM_112233")
        assert account.promo_code == None
        assert account.balance == 0

    def test_niepoprawny_prefix(self):
        account = Account("Vera", "Kibin", 12345678910, "BROM_123")
        assert account.promo_code == None
        assert account.balance == 0

    def test_rozne_znaki(self):
        account = Account("Vera", "Kibin", 12345678910, "PROM_---")
        assert account.promo_code == None
        assert account.balance == 0

    def test_jeden_znak(self):
        account = Account("Vera", "Kibin", 12345678910, "PROM_12-")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_with_space_in_suffix(self):
        account = Account("Vera", "Kibin", 12345678910, "PROM_1 2")
        assert account.promo_code == None
        assert account.balance == 0
