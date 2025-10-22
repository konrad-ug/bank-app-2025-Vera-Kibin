from src.account import Account

class TestAccount_Transfers:

## przelew przychodzacy

    def test_jeden_przelew_prz_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        assert account.balance == 50

    def test_jeden_przelew_prz_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50)
        assert account.balance == 50

    def test_przelew_prz_string_kilka(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy("50")
        assert account.balance == 150

    def test_przelew_prz_int_kilka(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        assert account.balance == 150

    def test_przelew_prz_zero_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(0)
        assert account.balance == 0

    def test_przelew_prz_zero_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("0")
        assert account.balance == 0

    def test_przelew_prz_zero_na_koniec(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(0)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        assert account.balance == 200

    def test_przelew_prz_mniej_niz_zero_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(-5)
        assert account.balance == 0

    def test_przelew_prz_mniej_niz_zero_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("-5")
        assert account.balance == 0

    def test_przelew_prz_z_mniej_niz_zero(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(-5)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(-5)
        account.przelew_przychodzacy(50)
        assert account.balance == 100

    def test_przelew_prz_nieprawidlowy_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("Hello")
        assert account.balance == 0

    def test_przelew_prz_nieprawidlowy_string_sposrod(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy("Hello")
        account.przelew_przychodzacy("50")
        assert account.balance == 100

    def test_przelew_prz_nieprawidlowy_string_koniec(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("10-")
        assert account.balance == 0

## przelew wychodzacy

    def test_przelew_wych_pusty_balance(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_wychodzacy(10)
        assert account.balance == 0


    def test_przelew_wych_jeden_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(45)
        assert account.balance == 5

    def test_przelew_wych_jeden_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("45")
        assert account.balance == 5

    def test_przelew_wych_zero_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(0)
        assert account.balance == 50

    def test_przelew_wych_zero_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("0")
        assert account.balance == 50

    def test_przelew_wych_wiecej_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(51)
        assert account.balance == 50

    def test_przelew_wych_wiecej_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("51")
        assert account.balance == 50

    def test_przelew_wych_wiecej_sposrod_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(100)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(51)
        assert account.balance == 50

    def test_przelew_wych_wiecej_sposrod_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("100")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("51")
        assert account.balance == 50
    
    def test_przelew_wych_kilka_int(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(1)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(51)
        account.przelew_wychodzacy(37)
        assert account.balance == 11

    def test_przelew_wych_kilka_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("1")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("51")
        account.przelew_wychodzacy("37")
        assert account.balance == 11

    def test_przelew_wych_kilka_mieszana(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy(1)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy("51")
        account.przelew_wychodzacy(37)
        assert account.balance == 11

    def test_przelew_wych_nieprawidlowy_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(30)
        account.przelew_wychodzacy("hej")
        assert account.balance == 30

    def test_przelew_wych_nieprawidlowy_koniec_string(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(10)
        account.przelew_wychodzacy("10k")
        assert account.balance == 10

    def test_przelew_wych_nieprawidlowy_string_znak(self):
        account = Account("Vera", "Kibin", 12345678910)
        account.przelew_przychodzacy(10)
        account.przelew_wychodzacy("!)-")
        assert account.balance == 10