Feature: Wykonywanie przelewów
@transfer
Scenario: Udany przelew przychodzący
    Given Użytkownik posiada konto bankowe o numerze PESEL 98765432109
    And Saldo użytkownika na koncie wynosi 1000 zł
    When Użytkownik otrzymuje przelew przychodzący w wysokości 500 zł
    Then Saldo użytkownika na koncie powinno wynosić 1500 zł

@transfer
Scenario: Udany przelew wychodzący
    Given Użytkownik posiada konto bankowe o numerze PESEL 98765432109
    And Saldo użytkownika na koncie wynosi 1000 zł
    When Użytkownik zleca przelew wychodzący w wysokości 300 zł
    Then System powinien zwrócić komunikat: Zlecenie przyjeto do realizacji
    And Saldo użytkownika na koncie powinno wynosić 700 zł

@transfer
Scenario: Udany przelew ekspresowy
    Given Użytkownik posiada konto bankowe o numerze PESEL 98765432109
    And Saldo użytkownika na koncie wynosi 2000 zł
    When Użytkownik zleca przelew ekspresowy w wysokości 1000 zł
    Then System powinien zwrócić komunikat: Zlecenie przyjeto do realizacji
    And Saldo użytkownika na koncie powinno wynosić 999 zł

@transfer
Scenario: Nieudany przelew wychodzący – niewystarczające środki
    Given Użytkownik posiada konto bankowe o numerze PESEL 98765432109
    And Saldo użytkownika na koncie wynosi 200 zł
    When Użytkownik zleca przelew wychodzący w wysokości 500 zł
    Then System powinien zwrócić komunikat: Niewystarczające srodki na koncie
    And Saldo użytkownika na koncie powinno wynosić 200 zł

@transfer
Scenario: Nieudany przelew ekspresowy – niewystarczające środki
    Given Użytkownik posiada konto bankowe o numerze PESEL 98765432109
    And Saldo użytkownika na koncie wynosi 300 zł
    When Użytkownik zleca przelew ekspresowy w wysokości 1000 zł
    Then System powinien zwrócić komunikat: Niewystarczające srodki na koncie
    And Saldo użytkownika na koncie powinno wynosić 300 zł

@transfer
Scenario: Niepoprawny typ przelewu
    Given Użytkownik posiada konto bankowe o numerze PESEL 98765432109
    And Saldo użytkownika na koncie wynosi 1000 zł
    When Użytkownik zleca przelew o niepoprawnym typie superfast
    Then System powinien zwrócić komunikat: Nieznany typ transferu: superfast
    And Saldo użytkownika na koncie powinno wynosić 1000 zł