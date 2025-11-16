from src.account import Account
import pytest
from pytest import approx

class TestAccount_Transfers:

    @pytest.fixture
    def account(self):
        return Account("Vera", "Kibin", 81020311161)
    
    @pytest.mark.parametrize("kwota", ["50.0", 50.0, 50], ids=["str-float","float","int"])
    def test_przelew_prz_jeden_param(self, account, kwota):
        account.przelew_przychodzacy(kwota)
        assert account.balance == 50.0
    
    @pytest.mark.parametrize(
        "sekwencja,oczekiwany",
        [
            (["50.0","50.0","50.0"], 150.0),
            ([50.0, 50.0, 50.0], 150.0),
            (["50.0", 50.0, "50"], 150.0),
            (["50.0","Hello","50.0"], 100.0),
            ([-5.0, 50.0, -5.0, 50.0], 100.0)
        ],
        ids=["all-str","all-float","mix", "niepoprawny pośrodku", "ujemne ignorowane"],
    )
    def test_przelew_prz_wiele_param(self, account, sekwencja, oczekiwany):
        for k in sekwencja:
            account.przelew_przychodzacy(k)
        assert account.balance == oczekiwany

    @pytest.mark.parametrize("bad", [0.0,"0.0",-5.0,"-5.0","Hello","10.0-","50.0.0","50,0",None,[], " 05.0 ","1e2"])
    def test_przelew_prz_niepoprawne_param(self, account, bad):
        before = (account.balance, list(account.history))
        assert account.przelew_przychodzacy(bad) is False
        assert (account.balance, account.history) == before

    @pytest.mark.parametrize(
        "start, kwota, expected",
        [
            (50.0, 45.0, 5.0),
            (50.0, "45.0", 5.0),
            (50.0, 0.0, 50.0),
            (50.0, -5.0, 50.0),
            (50.0, 51.0, 50.0),
            (50.0, 50.1, 50.0),
            (10.0, "05.0", 5.0),
            (50.0, "51.0", 50.0)
        ],
        ids=["ok-float","ok-str","zero","negative","too-much", "trochę więcej", "wiersz z prefiksem zerowym", "too-much jako str"]
    )
    def test_przelew_wych_param(self, account, start, kwota, expected):
        account.przelew_przychodzacy(start)
        account.przelew_wychodzacy(kwota)
        assert account.balance == expected

    @pytest.mark.parametrize("bad", ["hej","10.k","!)-"," 05.0 ","1e2"])
    def test_przelew_wych_invalid_inputs(self, account, bad):
        account.przelew_przychodzacy(10.0)
        before = (account.balance, list(account.history))
        assert account.przelew_wychodzacy(bad) is False
        assert (account.balance, account.history) == before

    @pytest.mark.parametrize(
        "start, kwota, expected, hist_tail",
        [
            (50.0, 45.0, 4.0,  [-45.0, -1.0]),
            (50.0, 50.0, -1.0, [-50.0, -1.0]),
            (50.0, 51.0, 50.0, []),
            (50.0, "45.0", 4.0, [-45.0, -1.0]),
            (50.0, "51.0", 50.0, [])
        ],
        ids=["ok","edge-allows-negative","reject-too-big", "ok-string", "reject-too-big jako str"]
    )
    def test_przelew_ekspresowy_param(self, account, start, kwota, expected, hist_tail):
        account.przelew_przychodzacy(start)
        before = list(account.history)
        account.przelew_ekspresowy(kwota)
        assert account.balance == expected
        assert account.history == before + hist_tail

    @pytest.mark.parametrize(
    "ops, expected_balance, expected_history_tail",
    [
        ([("in","100.00"), ("out",25), ("in",12.34), ("exp",50.0)], 36.34, [-25.0, 12.34, -50.0, -1.0]),
    ]
    )
    def test_chain(self, account, ops, expected_balance, expected_history_tail):
        before = list(account.history)
        for kind, val in ops:
            {"in":account.przelew_przychodzacy,
            "out":account.przelew_wychodzacy,
            "exp":account.przelew_ekspresowy}[kind](val)
        assert account.balance == approx(expected_balance, abs=1e-9)
        assert account.history[-len(expected_history_tail):] == expected_history_tail

## przelew przychodzacy

    def test_przelew_prz_zero_na_koniec(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(0.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        assert account.balance == 200.0

    def test_przelew_prz_z_mniej_niz_zero(self, account):
        account.przelew_przychodzacy(-5.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(-5.0)
        account.przelew_przychodzacy(50.0)
        assert account.balance == 100.0

    def test_przelew_prz_promo_dobry(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_przychodzacy("50.0")
        assert account.balance == 100.0

    def test_przelew_prz_male_float(self, account):
        account.przelew_przychodzacy(0.1)
        account.przelew_przychodzacy(0.2)
        assert round(account.balance, 2) == round(0.3, 2)

## przelew wychodzacy

    def test_przelew_wych_pusty_balance(self, account):
        account.przelew_wychodzacy(10.0)
        assert account.balance == 0.0

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
    
    def test_przelew_wych_kilka_int(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(1.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(51.0)
        account.przelew_wychodzacy(37.0)
        assert account.balance == 11.0

    def test_przelew_wych_kilka_string(self, account):
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("1.0")
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("51.0")
        account.przelew_wychodzacy("37.0")
        assert account.balance == 11.0

    def test_przelew_wych_kilka_mieszana(self, account):
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy(1.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy("51.0")
        account.przelew_wychodzacy(37.0)
        assert account.balance == 11.0

    def test_przelew_wych_promo_dobry(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_wychodzacy("50.0")
        assert account.balance == 0.0

## przelewy ekspresowe

    def test_przelew_ekspresowy_z_prom(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_ekspresowy(45.0)
        assert account.kwota_express == 1.0
        assert account.balance == 4.0

    def test_przelew_ekspresowy_kilka(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(10.0)
        account.przelew_ekspresowy(10.0)
        account.przelew_ekspresowy(10.0)
        account.przelew_ekspresowy(10.0)
        assert account.balance == 6.0

    def test_przelew_ekspresowy_kilka_string(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy("10.0")
        account.przelew_ekspresowy("10.0")
        account.przelew_ekspresowy("10.0")
        account.przelew_ekspresowy("10.0")
        assert account.balance == 6.0

    def test_przelew_ekspresowy_string_bledny(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy("51.0k")
        assert account.balance == 50.0


## history

    def test_history_pusty(self, account):
        assert account.history == []

    def test_history_przelew_niepoprawny_typ(self, account):
        account.przelew_przychodzacy("money")
        assert account.history == []

    def test_history_przelew_wych_jeden_int(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(45.0)
        assert account.history == [50.0,-45.0]

    def test_history_przelew_wych_jeden_int_z_balance(self, account):
        account.balance = 50.0
        account.przelew_wychodzacy(45.0)
        assert account.history == [-45.0]

    def test_history_przelew_wych_kilka_int_z_balance(self, account):
        account.balance = 50.0
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        assert account.history == [-5.0,-5.0,-5.0,-5.0]

    def test_history_przelew_wych_kilka_int_z_balance_z_przelew_prz(self, account):
        account.balance = 50.0
        account.przelew_wychodzacy(5.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(5.0)
        assert account.history == [-5.0,50.0,-5.0,50.0,-5.0,50.0,-5.0]

    def test_history_przelew_ekspresowy(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_ekspresowy(45.0)
        assert account.kwota_express == 1.0
        assert account.balance == 4.0
        assert account.history == [-45.0,-1.0]

    def test_history_przelew_ekspresowy_i_dodatkowy_przelew_prz(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_ekspresowy(45.0)
        account.przelew_przychodzacy(4.0)
        assert account.kwota_express == 1.0
        assert account.balance == 8.0
        assert account.history == [-45.0,-1.0,4.0]

    def test_history_przelew_ekspresowy_i_dodatkowy_przelew_wych(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_ekspresowy(45.0)
        account.przelew_wychodzacy(4.0)
        assert account.kwota_express == 1.0
        assert account.balance == 0.0
        assert account.history == [-45.0,-1.0,-4.0]

    def test_history_no_entry_when_outgoing_insufficient(self, account):
        account.przelew_przychodzacy(10.0)
        assert account.przelew_wychodzacy(11.0) is False
        assert account.history == [10.0] 
        assert account.balance == 10.0

    def test_history_no_entry_when_outgoing_zero_or_negative(self, account):
        account.przelew_przychodzacy(10.0)
        assert account.przelew_wychodzacy(0.0) is False
        assert account.przelew_wychodzacy(-5.0) is False
        assert account.history == [10.0]
        assert account.balance == 10.0

    def test_history_express_no_entry_when_amount_gt_balance(self, account):
        account.przelew_przychodzacy(10.0)
        assert account.przelew_ekspresowy(11.0) is False
        assert account.history == [10.0]
        assert account.balance == 10.0

## kredyt

    def test_loan_rule1_three_last_deposits_grants(self, account):
        account.przelew_przychodzacy(10.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_przychodzacy(20.0)
        account.przelew_przychodzacy(30.0)
        account.przelew_przychodzacy(40.0) 
        start = account.balance
        ok = account.submit_for_loan(100.0)
        assert ok is True
        assert account.history[-1] == 100.0
        assert account.balance == start + 100.0

    def test_loan_rule1_fails_when_last_three_not_all_positive(self, account):
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(30.0)
        account.przelew_wychodzacy(1.0) 
        before_len = len(account.history)
        start = account.balance
        ok = account.submit_for_loan(10.0)
        assert ok is False
        assert len(account.history) == before_len
        assert account.balance == start

    def test_loan_rule2_sum5_greater_grants(self, account):
        account.przelew_przychodzacy(100.0)
        account.przelew_wychodzacy(50.0)
        account.przelew_przychodzacy(60.0)
        account.przelew_wychodzacy(10.0)
        account.przelew_przychodzacy(5.0)
        before_len = len(account.history)
        start = account.balance
        ok = account.submit_for_loan(100.0) 
        assert ok is True
        assert len(account.history) == before_len + 1
        assert account.history[-1] == 100.0
        assert account.balance == start + 100.0

    def test_loan_rule2_equal_sum_fails(self, account):
        account.przelew_przychodzacy(100.0)
        account.przelew_wychodzacy(50.0)
        account.przelew_przychodzacy(60.0)
        account.przelew_wychodzacy(10.0)
        account.przelew_przychodzacy(5.0)
        before_len = len(account.history)
        start = account.balance
        ok = account.submit_for_loan(105.0) 
        assert ok is False
        assert len(account.history) == before_len
        assert account.balance == start

    def test_loan_rule2_requires_at_least_five_transactions(self, account):
        account.przelew_przychodzacy(40.0)
        account.przelew_przychodzacy(30.0)
        account.przelew_wychodzacy(10.0)
        account.przelew_przychodzacy(5.0)
        before_len = len(account.history)
        start = account.balance
        ok = account.submit_for_loan(50.0)
        assert ok is False
        assert len(account.history) == before_len
        assert account.balance == start

    def test_loan_invalid_amounts_rejected(self, account):
        before = (account.balance, list(account.history))
        for bad in [0, -10, "abc", None]:
            assert account.submit_for_loan(bad) is False
        assert account.balance == before[0]
        assert account.history == before[1]

    def test_loan_string_amount_ok_with_rule1(self, account):
        account.przelew_przychodzacy(1.0)
        account.przelew_przychodzacy(2.0)
        account.przelew_przychodzacy(3.0) 
        start = account.balance
        ok = account.submit_for_loan("100.0")
        assert ok is True
        assert account.history[-1] == 100.0
        assert account.balance == start + 100.0

    def test_loan_after_express_last_three_positive_still_grants(self, account):
        account.przelew_przychodzacy(100.0)
        account.przelew_ekspresowy(10.0)
        account.przelew_przychodzacy(2.0)
        account.przelew_przychodzacy(3.0)
        account.przelew_przychodzacy(4.0)   
        start = account.balance
        ok = account.submit_for_loan(50.0)
        assert ok is True
        assert account.history[-1] == 50.0
        assert account.balance == start + 50.0