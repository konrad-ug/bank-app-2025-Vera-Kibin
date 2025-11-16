from src.account import Account
import pytest

class TestAccount:

    @pytest.fixture
    def make_account(self):
        def _make(pesel, promo=None, first="Vera", last="Kibin"):
            return Account(first, last, pesel, promo)
        return _make

    def test_account_creation(self):
        account = Account("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678910"
        assert account.promo_code == None

## testy PESEL

    @pytest.mark.parametrize("pesel", ["", None, "123", "123123123123", "1234567891A", "mlkhgfedcbA"])
    def test_pesel_invalid(self, make_account, pesel):
        assert make_account(pesel).pesel == "Invalid"

    @pytest.mark.parametrize(
        "pesel, expected",
        [(12345678910, "12345678910"), ("01234567890", "01234567890")],
        ids=["int-OK","leading-zero-OK"]
    )
    def test_pesel_valid(self, make_account, pesel, expected):
        assert make_account(pesel).pesel == expected

## testy PROMO_KOD

    def test_promo_none(self):
        account = Account("Vera", "Kibin", 12345678910)
        assert account.promo_code == None
        assert account.balance == 0.0

    @pytest.mark.parametrize(
        "promo",
        ["PROM_hej", "PROM_123", "PROM_A9b"],
        ids=["letters","digits","mixed"]
    )
    def test_promo_valid(self, make_account, promo):
        a = make_account(81020311161, promo)
        assert a.promo_code == promo
        assert a.balance == 50.0

    @pytest.mark.parametrize(
        "promo",
        ["prom_hej", "PROM_1", "PROM_112233", "BROM_123", "PROM_---", "PROM_12-", "PROM_1 2"],
        ids=["lowercase","too-short","too-long","bad-prefix","non-alnum","dash-at-end","space"]
    )
    def test_promo_invalid(self, make_account, promo):
        a = make_account(81020311161, promo)
        assert a.promo_code is None
        assert a.balance == 0.0

## testy YoB

    @pytest.mark.parametrize(
        "pesel, eligible",
        [
            ("59030112345", False),
            ("60030112345", False),
            ("61030112345", True),
            ("01210512345", True), 
            ("01430112345", True),
            ("02620112345", True),
        ],
        ids=["1959","1960","1961","2001","+40-century","+60-century"]
    )
    def test_promo_by_age(self, make_account, pesel, eligible):
        a = make_account(pesel, "PROM_ABC")
        if eligible:
            assert a.promo_code == "PROM_ABC"
            assert a.balance == 50.0
        else:
            assert a.promo_code is None
            assert a.balance == 0.0

    def test_promo_blocked_when_pesel_invalid(self, make_account):
        a = make_account("1234567ABCD", "PROM_ABC")
        assert a.pesel == "Invalid"
        assert a.promo_code is None
        assert a.balance == 0.0

    def test_promo_blocked_when_month_invalid(self, make_account):
        a = make_account("61000112345", "PROM_ABC")
        assert a.promo_code is None
        assert a.balance == 0.0

    def test_promo_age_1899_not_eligible(self):
        account = Account("Vera", "Kibin", "99920112345", "PROM_ABC")
        assert account.promo_code == None
        assert account.balance == 0.0

