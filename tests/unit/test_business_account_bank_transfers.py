from pytest_mock import mocker
from src.business_account import BusinessAccount
import pytest


@pytest.fixture(autouse=True)
def _stub_mf(mocker):
    mocker.patch.object(BusinessAccount, "verify_nip_with_mf", return_value=True)
    
class TestBusinessAccount_Transfers:

    @pytest.fixture
    def account(self):
            return BusinessAccount("KIBINGUITARS", "1234567890")
    
    ## przelew przychodzacy

    @pytest.mark.parametrize("kwota", ["50.0", 50.0, 50])
    def test_przelew_prz_jeden(self, account, kwota):
        account.przelew_przychodzacy(kwota)
        assert account.balance == 50.0

    @pytest.mark.parametrize("kwoty", [["50.0", "50.0", "50.0"],
                                    [50.0, 50.0, 50.0]])
    def test_przelew_prz_trzy_razy_50(self, account, kwoty):
        for k in kwoty:
            account.przelew_przychodzacy(k)
        assert account.balance == 150.0

    @pytest.mark.parametrize("kwota", [0.0, "0.0"])
    def test_przelew_prz_zero(self, account, kwota):
        account.przelew_przychodzacy(kwota)
        assert account.balance == 0.0

    def test_przelew_prz_zero_na_koniec(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(0.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        assert account.balance == 200.0

    @pytest.mark.parametrize("kwota", [-5.0, "-5.0"])
    def test_przelew_prz_ujemne_ignorowane(self, account, kwota):
        account.przelew_przychodzacy(kwota)
        assert account.balance == 0.0

    def test_przelew_prz_nieprawidlowy_string_sposrod(self, account):
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy("Hello")
        account.przelew_przychodzacy("50.0")
        assert account.balance == 100.0

    @pytest.mark.parametrize("bad", ["Hello", "10.0-", "50.0.0", "50,0"])
    def test_przelew_prz_bledne_stringi_nie_zmieniaja_stanu(self, account, bad):
        before = (account.balance, list(account.history))
        ret = account.przelew_przychodzacy(bad)
        assert ret is False
        assert (account.balance, account.history) == before

    def test_przelew_prz_mix_typow(self, account):
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50)
        assert account.balance == 200.0

    def test_przelew_prz_male_float(self, account):
        account.przelew_przychodzacy(0.1)
        account.przelew_przychodzacy(0.2)
        assert round(account.balance, 2) == round(0.3, 2)

## przelew wychodzacy

    def test_przelew_wych_pusty_balance(self, account):
        account.przelew_wychodzacy(10.0)
        assert account.balance == 0.0

    def test_przelew_wych_mniej_niz_zero_int(self, account):
        account.przelew_przychodzacy(5.0)
        account.przelew_wychodzacy(-5.0)
        assert account.balance == 5.0

    @pytest.mark.parametrize("kwota", [45.0, "45.0"])
    def test_przelew_wych_jeden(self, account, kwota):
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(kwota)
        assert account.balance == 5.0

    @pytest.mark.parametrize("kwota", [0.0, "0.0"])
    def test_przelew_wych_zero(self, account, kwota):
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(kwota)
        assert account.balance == 50.0

    @pytest.mark.parametrize("kwota", [51.0, 50.1, "51.0"])
    def test_przelew_wych_za_duzo(self, account, kwota):
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(kwota)
        assert account.balance == 50.0

    def test_przelew_wych_wiecej_sposrod_int(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(100.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(51.0)
        assert account.balance == 50.0

    def test_przelew_wych_wiecej_sposrod_string(self, account):
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("100.0")
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("51.0")
        assert account.balance == 50.0
    
    @pytest.mark.parametrize(
        "ops",
        [
            [( "in", 50.0), ("out",  1.0), ("in", 50.0), ("out", 51.0), ("out", 37.0)],
            [("in","50.0"), ("out","1.0"), ("in","50.0"), ("out","51.0"), ("out","37.0")],
            [("in","50.0"), ("out", 1.0),  ("in", 50.0), ("out","51.0"), ("out", 37.0)],
        ]
    )
    def test_przelew_wych_kilka_scenariusze(self, account, ops):
        for kind, val in ops:
            {"in": account.przelew_przychodzacy,
            "out": account.przelew_wychodzacy}[kind](val)
        assert account.balance == 11.0

    @pytest.mark.parametrize("bad", ["hej", "10.0k", "!)-", " 05.0 ", "1e2", {"kwota": 5}])
    def test_przelew_wych_bledne_wejscia(self, account, bad):
        account.przelew_przychodzacy(10.0)
        before = (account.balance, list(account.history))
        ret = account.przelew_wychodzacy(bad)
        assert ret is False
        assert (account.balance, account.history) == before

## przelewy ekspresowe

    def test_przelew_ekspresowy_z_prom(self, account):
        account.przelew_ekspresowy(45.0)
        assert account.kwota_express == 5.0
        assert account.balance == 0.0

    @pytest.mark.parametrize(
        "kwota, expected_balance",
        [
            (45.0,   0.0),
            (50.0,  -5.0),
            (51.0,  50.0),
            ("51.0", 50.0),
        ]
    )
    def test_przelew_ekspresowy_warianty(self, account, kwota, expected_balance):
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(kwota)
        assert account.balance == expected_balance
        
    @pytest.mark.parametrize("kwota", [10.0, "10.0"])
    def test_przelew_ekspresowy_kilka(self, account, kwota):
        account.przelew_przychodzacy(50.0)
        for _ in range(4):
            account.przelew_ekspresowy(kwota)
        assert account.balance == 5.0

    def test_przelew_ekspresowy_string_bledny(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy("51.0k")
        assert account.balance == 50.0

    def test_chain_of_operations_mixed(self, account):
        account.przelew_przychodzacy("100.00")
        account.przelew_wychodzacy(25)
        account.przelew_przychodzacy(12.34)
        account.przelew_ekspresowy(50.0)  
        assert round(account.balance, 4) == round(32.34, 4)

## history

    def test_history_pusty_business(self, account):
        assert account.history == []

    def test_history_przelew_niepoprawny_typ_business(self, account):
        account.przelew_przychodzacy("money")
        assert account.history == []

    @pytest.mark.parametrize("kwota", [50.0, "50.0"])
    def test_history_jeden_przelew_prz_business(self, account, kwota):
        account.przelew_przychodzacy(kwota)
        assert account.history == [50.0]

    def test_history_przelew_prz_int_i_str_kilka_business(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy(50.0)
        assert account.history == [50.0, 50.0, 50.0]

    @pytest.mark.parametrize("kwota", [45.0, "45.0"])
    def test_history_przelew_wych_jeden_business(self, account, kwota):
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(kwota)
        assert account.history == [50.0, -45.0]

    def test_history_przelew_wych_kilka_int_business(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        assert account.history == [50.0, -5.0, -5.0, -5.0, -5.0]

    def test_history_przelew_wych_kilka_z_przelewami_przych_business(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(5.0)
        assert account.history == [50.0, -5.0, 50.0, -5.0, 50.0, -5.0, 50.0, -5.0]

    def test_history_przelew_ekspresowy_business(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(45.0)
        assert account.kwota_express == 5.0
        assert account.balance == 0.0
        assert account.history == [50.0, -45.0, -5.0]

    def test_history_przelew_ekspresowy_plus_przych_business(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(45.0)
        account.przelew_przychodzacy(4.0)
        assert account.kwota_express == 5.0
        assert account.balance == 4.0
        assert account.history == [50.0, -45.0, -5.0, 4.0]

    def test_history_przelew_ekspresowy_plus_wych_business(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(45.0)
        account.przelew_wychodzacy(4.0)
        assert account.kwota_express == 5.0
        assert account.balance == 0.0 
        assert account.history == [50.0, -45.0, -5.0]

    def test_history_no_entry_when_outgoing_insufficient_business(self, account):
        account.przelew_przychodzacy(10.0)
        assert account.przelew_wychodzacy(11.0) is False
        assert account.history == [10.0]
        assert account.balance == 10.0

    def test_history_no_entry_when_outgoing_zero_or_negative_business(self, account):
        account.przelew_przychodzacy(10.0)
        assert account.przelew_wychodzacy(0.0) is False
        assert account.przelew_wychodzacy(-5.0) is False
        assert account.history == [10.0]
        assert account.balance == 10.0

    def test_history_express_no_entry_when_amount_gt_balance_business(self, account):
        account.przelew_przychodzacy(10.0)
        assert account.przelew_ekspresowy(11.0) is False
        assert account.history == [10.0]
        assert account.balance == 10.0

## kredyt

    @pytest.fixture
    def account_with_zus(self, account):
        account.przelew_przychodzacy(10_000.0)
        account.przelew_wychodzacy(1775.0)
        assert -1775.0 in account.history
        return account

    @pytest.mark.parametrize(
        "start_balance, amount, ok_expected, final_balance",
        [
            (4000.0, 1000.0, True,  5000.0),
            (2000.0, 1000.0, True,  3000.0),
            (1999.99,1000.0, False, 1999.99),
        ],
        ids=["gt-2x","eq-2x","lt-2x"]
    )
    def test_submit_for_loan_threshold_with_zus(self, account_with_zus, start_balance, amount, ok_expected, final_balance):
        account_with_zus.balance = start_balance
        before_hist = list(account_with_zus.history)
        ok = account_with_zus.submit_for_loan(amount)
        assert ok is ok_expected
        assert account_with_zus.balance == pytest.approx(final_balance, abs=1e-9)
        if ok_expected:
            assert account_with_zus.history == before_hist + [float(amount)]
        else:
            assert account_with_zus.history == before_hist

    def test_submit_for_loan_requires_zus_transfer(self, account):
        account.przelew_przychodzacy(10_000.0)
        snap = (account.balance, list(account.history))
        assert account.submit_for_loan(1000.0) is False
        assert (account.balance, account.history) == snap

    @pytest.mark.parametrize("bad", [0, -10, "abc", None])
    def test_submit_for_loan_rejects_bad_amounts(self,account_with_zus, bad):
        snap = (account_with_zus.balance, list(account_with_zus.history))
        assert account_with_zus.submit_for_loan(bad) is False
        assert (account_with_zus.balance, account_with_zus.history) == snap

    def test_submit_for_loan_accepts_string_amount(self, account_with_zus):
        account_with_zus.balance = 4000.0
        ok = account_with_zus.submit_for_loan("1000.0")
        assert ok is True
        assert account_with_zus.balance == 5000.0
        assert account_with_zus.history[-1] == 1000.0

    def test_zus_must_be_exact(self, account):
        account.przelew_przychodzacy(10_000.0)
        account.przelew_wychodzacy(1775.01)
        snap = (account.balance, list(account.history))
        assert account.submit_for_loan(1000.0) is False
        assert (account.balance, account.history) == snap