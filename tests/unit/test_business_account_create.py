from src.business_account import BusinessAccount
import pytest

class TestBusinessAccount:

    @pytest.fixture
    def make_account(self):
        def _make(nip, name="KIBINGUITARS"):
            return BusinessAccount(name, nip)
        return _make
    
    def test_account_creation(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        assert account.company_name == "KIBINGUITARS"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    @pytest.mark.parametrize(
        "nip",
        ["", None, "123", "123123123123", "123456789o", "tujestnipp", "123-456-78-90", " 1234567890 "],
        ids=["empty","none","too-short","too-long","letter-inside","letters","with-dashes","with-spaces"]
    )
    def test_nip_invalid(self, make_account, nip):
        assert make_account(nip).nip == "Invalid"

    @pytest.mark.parametrize(
        "nip, expected",
        [(1234567890, "1234567890"), ("0123456789", "0123456789")],
        ids=["int-10-digits","string-leading-zero"]
    )
    def test_nip_valid(self, make_account, nip, expected):
        assert make_account(nip).nip == expected
