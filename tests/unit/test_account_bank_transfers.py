from src.account import Account

class TestAccount_Transfers:

## przelew przychodzacy

    def test_jeden_przelew_prz_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        assert account.balance == 50.0

    def test_jeden_przelew_prz_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        assert account.balance == 50.0

    def test_przelew_prz_string_kilka(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy("50.0")
        assert account.balance == 150.0

    def test_przelew_prz_int_kilka(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        assert account.balance == 150.0

    def test_przelew_prz_zero_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(0.0)
        assert account.balance == 0.0

    def test_przelew_prz_zero_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("0.0")
        assert account.balance == 0.0

    def test_przelew_prz_zero_na_koniec(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(0.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        assert account.balance == 200.0

    def test_przelew_prz_mniej_niz_zero_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(-5.0)
        assert account.balance == 0.0

    def test_przelew_prz_mniej_niz_zero_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("-5.0")
        assert account.balance == 0.0

    def test_przelew_prz_z_mniej_niz_zero(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(-5.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(-5.0)
        account.przelew_przychodzacy(50.0)
        assert account.balance == 100.0

    def test_przelew_prz_nieprawidlowy_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("Hello")
        assert account.balance == 0.0

    def test_przelew_prz_nieprawidlowy_string_sposrod(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy("Hello")
        account.przelew_przychodzacy("50.0")
        assert account.balance == 100.0

    def test_przelew_prz_nieprawidlowy_string_koniec(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("10.0-")
        assert account.balance == 0.0

    def test_przelew_prz_promo_dobry(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_przychodzacy("50.0")
        assert account.balance == 100.0

    def test_przelew_prz_dwie_kropki_tekst(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0.0")
        assert account.balance == 0.0

    def test_przelew_prz_comma_tekst(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50,0")
        assert account.balance == 0.0

    def test_przelew_prz_mix_typow(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50)
        assert account.balance == 200.0

    def test_przelew_prz_male_float(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(0.1)
        account.przelew_przychodzacy(0.2)
        assert round(account.balance, 2) == round(0.3, 2)

    def test_incoming_invalid_type_none(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(None)  
        assert account.balance == 0.0

    def test_incoming_invalid_type_list(self):
        account = Account("Vera", "Kibin", 81020311161)
        ret = account.przelew_przychodzacy([])    
        assert ret is False
        assert account.balance == 0.0

## przelew wychodzacy

    def test_przelew_wych_pusty_balance(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_wychodzacy(10.0)
        assert account.balance == 0.0

    def test_przelew_wych_jeden_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(45.0)
        assert account.balance == 5.0

    def test_przelew_wych_jeden_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("45.0")
        assert account.balance == 5.0

    def test_przelew_wych_zero_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(0.0)
        assert account.balance == 50.0

    def test_przelew_wych_zero_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("0.0")
        assert account.balance == 50.0

    def test_przelew_wych_wiecej_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(51.0)
        assert account.balance == 50.0

    def test_przelew_wych_troche_wiecej_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(50.1)
        assert account.balance == 50.0

    def test_przelew_wych_wiecej_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("51.0")
        assert account.balance == 50.0

    def test_przelew_wych_wiecej_sposrod_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(100.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(51.0)
        assert account.balance == 50.0

    def test_przelew_wych_wiecej_sposrod_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("100.0")
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("51.0")
        assert account.balance == 50.0
    
    def test_przelew_wych_kilka_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(1.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(51.0)
        account.przelew_wychodzacy(37.0)
        assert account.balance == 11.0

    def test_przelew_wych_kilka_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("1.0")
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy("51.0")
        account.przelew_wychodzacy("37.0")
        assert account.balance == 11.0

    def test_przelew_wych_kilka_mieszana(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        account.przelew_wychodzacy(1.0)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy("51.0")
        account.przelew_wychodzacy(37.0)
        assert account.balance == 11.0

    def test_przelew_wych_nieprawidlowy_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(30.0)
        account.przelew_wychodzacy("hej")
        assert account.balance == 30.0

    def test_przelew_wych_nieprawidlowy_koniec_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(10.0)
        account.przelew_wychodzacy("10.k")
        assert account.balance == 10.0

    def test_przelew_wych_nieprawidlowy_string_znak(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(10.0)
        account.przelew_wychodzacy("!)-")
        assert account.balance == 10.0

    def test_przelew_wych_promo_dobry(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_wychodzacy("50.0")
        assert account.balance == 0.0

    def test_przelew_wych_zero_start(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(10.0)
        account.przelew_wychodzacy("05.0")
        assert account.balance == 5.0

    def test_przelew_wych_spacje(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(10.0)
        account.przelew_wychodzacy(" 05.0 ")
        assert account.balance == 10.0

    def test_przelew_wych_naukowy_widok_exponenta(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(10.0)
        account.przelew_wychodzacy("1e2")
        assert account.balance == 10.0

## przelewy ekspresowe

    def test_przelew_ekspresowy_z_prom(self):
        account = Account("Vera", "Kibin", 81020311161, "PROM_hej")
        account.przelew_ekspresowy(45.0)
        assert account.kwota_express == 1.0
        assert account.balance == 4.0

    def test_przelew_ekspresowy(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(45.0)
        assert account.kwota_express == 1.0
        assert account.balance == 4.0
        
    def test_przelew_ekspresowy_full(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(50.0)
        assert account.balance == -1.0

    def test_przelew_ekspresowy_less(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(51.0)
        assert account.balance == 50.0

    def test_przelew_ekspresowy_kilka(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy(10.0)
        account.przelew_ekspresowy(10.0)
        account.przelew_ekspresowy(10.0)
        account.przelew_ekspresowy(10.0)
        assert account.balance == 6.0

    def test_przelew_ekspresowy_string(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy("51.0")
        assert account.balance == 50.0

    def test_przelew_ekspresowy_kilka_string(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy("10.0")
        account.przelew_ekspresowy("10.0")
        account.przelew_ekspresowy("10.0")
        account.przelew_ekspresowy("10.0")
        assert account.balance == 6.0

    def test_przelew_ekspresowy_string_bledny(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(50.0)
        account.przelew_ekspresowy("51.0k")
        assert account.balance == 50.0

    def test_chain_of_operations_mixed(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy("100.00")
        account.przelew_wychodzacy(25)
        account.przelew_przychodzacy(12.34)
        account.przelew_ekspresowy(50.0)  
        assert round(account.balance, 4) == round(36.34, 4)

## history

    def test_history_pusty(self):
        account = Account("Vera", "Kibin", 81020311161,)
        assert account.history == []

    def test_history_przelew_niepoprawny_typ(self):
        account = Account("Vera", "Kibin", 81020311161,)
        account.przelew_przychodzacy("money")
        assert account.history == []

    def test_history_jeden_przelew_prz_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        assert account.history == [50.0]

    def test_history_jeden_przelew_prz_str(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50.0")
        assert account.history == [50.0]

    def test_history_przelew_prz_int_i_str_kilka(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_przychodzacy("50.0")
        account.przelew_przychodzacy(50.0)
        assert account.history == [50.0, 50.0, 50.0]

    def test_history_przelew_wych_jeden_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50.0)
        account.przelew_wychodzacy(45.0)
        assert account.history == [50.0,-45.0]

    def test_history_przelew_wych_jeden_int_z_balance(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.balance = 50.0
        account.przelew_wychodzacy(45.0)
        assert account.history == [-45.0]

    def test_history_przelew_wych_kilka_int_z_balance(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.balance = 50.0
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        account.przelew_wychodzacy(5.0)
        assert account.history == [-5.0,-5.0,-5.0,-5.0]

    def test_history_przelew_wych_kilka_int_z_balance_z_przelew_prz(self):
        account = Account("Vera", "Kibin", 12345678910)
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

    def test_history_no_entry_when_outgoing_insufficient(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(10.0)
        assert account.przelew_wychodzacy(11.0) is False
        assert account.history == [10.0] 
        assert account.balance == 10.0

    def test_history_no_entry_when_outgoing_zero_or_negative(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(10.0)
        assert account.przelew_wychodzacy(0.0) is False
        assert account.przelew_wychodzacy(-5.0) is False
        assert account.history == [10.0]
        assert account.balance == 10.0

    def test_history_express_no_entry_when_amount_gt_balance(self):
        account = Account("Vera", "Kibin", 81020311161)
        account.przelew_przychodzacy(10.0)
        assert account.przelew_ekspresowy(11.0) is False
        assert account.history == [10.0]
        assert account.balance == 10.0

## kredyt

    def test_loan_rule1_three_last_deposits_grants(self):
        a = Account("Vera", "Kibin", 81020311161)
        a.przelew_przychodzacy(10.0)
        a.przelew_wychodzacy(5.0)
        a.przelew_przychodzacy(20.0)
        a.przelew_przychodzacy(30.0)
        a.przelew_przychodzacy(40.0) 
        start = a.balance
        ok = a.submit_for_loan(100.0)
        assert ok is True
        assert a.history[-1] == 100.0
        assert a.balance == start + 100.0

    def test_loan_rule1_fails_when_last_three_not_all_positive(self):
        a = Account("Vera", "Kibin", 81020311161)
        a.przelew_przychodzacy(50.0)
        a.przelew_przychodzacy(30.0)
        a.przelew_wychodzacy(1.0) 
        before_len = len(a.history)
        start = a.balance
        ok = a.submit_for_loan(10.0)
        assert ok is False
        assert len(a.history) == before_len
        assert a.balance == start

    def test_loan_rule2_sum5_greater_grants(self):
        a = Account("Vera", "Kibin", 81020311161)
        a.przelew_przychodzacy(100.0)
        a.przelew_wychodzacy(50.0)
        a.przelew_przychodzacy(60.0)
        a.przelew_wychodzacy(10.0)
        a.przelew_przychodzacy(5.0)
        before_len = len(a.history)
        start = a.balance
        ok = a.submit_for_loan(100.0) 
        assert ok is True
        assert len(a.history) == before_len + 1
        assert a.history[-1] == 100.0
        assert a.balance == start + 100.0

    def test_loan_rule2_equal_sum_fails(self):
        a = Account("Vera", "Kibin", 81020311161)
        a.przelew_przychodzacy(100.0)
        a.przelew_wychodzacy(50.0)
        a.przelew_przychodzacy(60.0)
        a.przelew_wychodzacy(10.0)
        a.przelew_przychodzacy(5.0)
        before_len = len(a.history)
        start = a.balance
        ok = a.submit_for_loan(105.0) 
        assert ok is False
        assert len(a.history) == before_len
        assert a.balance == start

    def test_loan_rule2_requires_at_least_five_transactions(self):
        a = Account("Vera", "Kibin", 81020311161)
        a.przelew_przychodzacy(40.0)
        a.przelew_przychodzacy(30.0)
        a.przelew_wychodzacy(10.0)
        a.przelew_przychodzacy(5.0)
        before_len = len(a.history)
        start = a.balance
        ok = a.submit_for_loan(50.0)
        assert ok is False
        assert len(a.history) == before_len
        assert a.balance == start

    def test_loan_invalid_amounts_rejected(self):
        a = Account("Vera", "Kibin", 81020311161)
        before = (a.balance, list(a.history))
        for bad in [0, -10, "abc", None]:
            assert a.submit_for_loan(bad) is False
        assert a.balance == before[0]
        assert a.history == before[1]

    def test_loan_string_amount_ok_with_rule1(self):
        a = Account("Vera", "Kibin", 81020311161)
        a.przelew_przychodzacy(1.0)
        a.przelew_przychodzacy(2.0)
        a.przelew_przychodzacy(3.0) 
        start = a.balance
        ok = a.submit_for_loan("100.0")
        assert ok is True
        assert a.history[-1] == 100.0
        assert a.balance == start + 100.0

    def test_loan_after_express_last_three_positive_still_grants(self):
        a = Account("Vera", "Kibin", 81020311161)
        a.przelew_przychodzacy(100.0)
        a.przelew_ekspresowy(10.0)
        a.przelew_przychodzacy(2.0)
        a.przelew_przychodzacy(3.0)
        a.przelew_przychodzacy(4.0)   
        start = a.balance
        ok = a.submit_for_loan(50.0)
        assert ok is True
        assert a.history[-1] == 50.0
        assert a.balance == start + 50.0