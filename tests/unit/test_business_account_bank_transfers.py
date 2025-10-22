from src.account import BusinessAccount

class TestBusinessAccount_Transfers:

    ## przelew przychodzacy

    def test_jeden_przelew_prz_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        assert account.balance == 50

    def test_jeden_przelew_prz_int(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(50)
        assert account.balance == 50

    def test_przelew_prz_string_kilka(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy("50")
        assert account.balance == 150

    def test_przelew_prz_int_kilka(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        assert account.balance == 150

    def test_przelew_prz_zero_int(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(0)
        assert account.balance == 0

    def test_przelew_prz_zero_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("0")
        assert account.balance == 0

    def test_przelew_prz_zero_na_koniec(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(0)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        assert account.balance == 200

    def test_przelew_prz_mniej_niz_zero_int(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(-5)
        assert account.balance == 0

    def test_przelew_prz_mniej_niz_zero_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("-5")
        assert account.balance == 0

    def test_przelew_prz_z_mniej_niz_zero(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(-5)
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(-5)
        account.przelew_przychodzacy(50)
        assert account.balance == 100

    def test_przelew_prz_nieprawidlowy_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("Hello")
        assert account.balance == 0

    def test_przelew_prz_nieprawidlowy_string_sposrod(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy("Hello")
        account.przelew_przychodzacy("50")
        assert account.balance == 100

    def test_przelew_prz_nieprawidlowy_string_koniec(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("10-")
        assert account.balance == 0

## przelew wychodzacy

    def test_przelew_wych_pusty_balance(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_wychodzacy(10)
        assert account.balance == 0


    def test_przelew_wych_jeden_int(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(45)
        assert account.balance == 5

    def test_przelew_wych_jeden_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("45")
        assert account.balance == 5

    def test_przelew_wych_zero_int(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(0)
        assert account.balance == 50

    def test_przelew_wych_zero_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("0")
        assert account.balance == 50

    def test_przelew_wych_wiecej_int(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(51)
        assert account.balance == 50

    def test_przelew_wych_wiecej_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("51")
        assert account.balance == 50

    def test_przelew_wych_wiecej_sposrod_int(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(50)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(100)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(51)
        assert account.balance == 50

    def test_przelew_wych_wiecej_sposrod_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("100")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("51")
        assert account.balance == 50
    
    def test_przelew_wych_kilka_int(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(1)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy(51)
        account.przelew_wychodzacy(37)
        assert account.balance == 11

    def test_przelew_wych_kilka_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("1")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy("51")
        account.przelew_wychodzacy("37")
        assert account.balance == 11

    def test_przelew_wych_kilka_mieszana(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy("50")
        account.przelew_wychodzacy(1)
        account.przelew_przychodzacy(50)
        account.przelew_wychodzacy("51")
        account.przelew_wychodzacy(37)
        assert account.balance == 11

    def test_przelew_wych_nieprawidlowy_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(30)
        account.przelew_wychodzacy("hej")
        assert account.balance == 30

    def test_przelew_wych_nieprawidlowy_koniec_string(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(10)
        account.przelew_wychodzacy("10k")
        assert account.balance == 10

    def test_przelew_wych_nieprawidlowy_string_znak(self):
        account = BusinessAccount("KIBINGUITARS", "1234567890")
        account.przelew_przychodzacy(10)
        account.przelew_wychodzacy("!)-")
        assert account.balance == 10