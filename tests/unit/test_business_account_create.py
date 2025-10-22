from src.business_account import BusinessAccount

class TestBusinessAccount:
    def test_account_creation(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        assert account.company_name == "KIBINGUITARS"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_nip_empty(self):
        account = BusinessAccount("KIBINGUITARS", "")
        assert account.nip == "Invalid"

    def test_nip_none(self):
        account = BusinessAccount("KIBINGUITARS", None)
        assert account.nip == "Invalid"

    def test_nip_less(self):
        account = BusinessAccount("KIBINGUITARS", "123")
        assert account.nip == "Invalid"

    def test_nip_more(self):
        account = BusinessAccount("KIBINGUITARS", "123123123123")
        assert account.nip == "Invalid"

    def test_nip_litera(self):
        account = BusinessAccount("KIBINGUITARS", "123456789o")
        assert account.nip == "Invalid"

    def test_nip_litery(self):
        account = BusinessAccount("KIBINGUITARS", "tujestnipp")
        assert account.nip == "Invalid"

    def test_nip_cyfry(self):
        account = BusinessAccount("KIBINGUITARS", 1234567890)
        assert account.nip == "1234567890"