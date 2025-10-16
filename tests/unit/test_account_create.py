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
        account = Account("Vera", "Kibin", 81020311161, "prom_hej")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_dobry(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        assert account.promo_code == "PROM_hej"
        assert account.balance == 50

    def test_promo_dobry_cyfry(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_123")
        assert account.promo_code == "PROM_123"
        assert account.balance == 50

    def test_promo_mixed_case(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_A9b")
        assert account.promo_code == "PROM_A9b"
        assert account.balance == 50

    def test_promo_zamalo_znakow(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_1")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_zaduzo_znakow(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_112233")
        assert account.promo_code == None
        assert account.balance == 0

    def test_niepoprawny_prefix(self):
        account = Account("Vera", "Kibin", 81020311161, "BROM_123")
        assert account.promo_code == None
        assert account.balance == 0

    def test_rozne_znaki(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_---")
        assert account.promo_code == None
        assert account.balance == 0

    def test_jeden_znak(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_12-")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_with_space_in_suffix(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_1 2")
        assert account.promo_code == None
        assert account.balance == 0

## testy YoB

    def test_promo_mixed_case_pesel_niepoprawny(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_A9b")
        assert account.promo_code == "PROM_A9b"
        assert account.balance == 50

    def test_promo_niepoprawny_pesel(self):
        account = Account("Vera", "Kibin", 12345678919, "PROM_A9b")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_nieporawne_pesel_poprawny(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_---")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_age_before_threshold_1959(self):
        account = Account("Vera", "Kibin", "59030112345", "PROM_ABC")
        assert account.promo_code is None
        assert account.balance == 0

    def test_promo_age_at_threshold_1960(self):
        account = Account("Vera", "Kibin", "60030112345", "PROM_ABC")
        assert account.promo_code is None
        assert account.balance == 0

    def test_promo_age_after_threshold_1961(self):
        account = Account("Vera", "Kibin", "61030112345", "PROM_ABC")
        assert account.promo_code == "PROM_ABC"
        assert account.balance == 50

    def test_promo_age_2001_example(self):
        account = Account("Vera", "Kibin", "01210512345", "PROM_X9z")
        assert account.promo_code == "PROM_X9z"
        assert account.balance == 50

    def test_promo_age_1899_not_eligible(self):
        account = Account("Vera", "Kibin", "99920112345", "PROM_ABC")
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_blocked_when_pesel_invalid(self):
        account = Account("Vera", "Kibin", "1234567ABCD", "PROM_ABC") 
        assert account.pesel == "Invalid"
        assert account.promo_code == None
        assert account.balance == 0

    def test_promo_blocked_when_month_invalid(self):
        account = Account("Vera", "Kibin", "61000112345", "PROM_ABC")
        assert account.promo_code is None
        assert account.balance == 0


