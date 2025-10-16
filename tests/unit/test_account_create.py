from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678910"
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
