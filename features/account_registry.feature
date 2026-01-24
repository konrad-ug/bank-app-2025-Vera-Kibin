Feature: Account registry

Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry
Scenario: User is able to update surname of already created account
    Given Acoount registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "name" of account with pesel: "95092909876" to "nsdjnvbvsdsvhdsh"
    Then Account with pesel "95092909876" has "name" equal to "nsdjnvbvsdsvhdsh"

Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "james", last name: "hetfield", pesel: "63080509876"
    Then Account with pesel "63080509876" exists in registry
    And Account with pesel "63080509876" has "name" equal to "james"
    And Account with pesel "63080509876" has "surname" equal to "hetfield"
    And Number of accounts in registry equals: "1"

Scenario: User is able to delete created account
    Given Acoount registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

Scenario: User can make incoming transfer
    Given Account registry is empty
    And I create an account using name: "dsaf", last name: "fdsafasfdj", pesel: "40100909876"
    When I make "incoming" transfer of "100" to account with pesel: "40100909876"
    Then Transfer is accepted
    And Account with pesel "40100909876" has balance of "100"

Scenario: User can make outgoing transfer with sufficient balance
    Given Account registry is empty
    And I create an account using name: "paul", last name: "mccartney", pesel: "42061809876"
    And I make "incoming" transfer of "200" to account with pesel: "42061809876"
    When I make "outgoing" transfer of "50" to account with pesel: "42061809876"
    Then Transfer is accepted
    And Account with pesel "42061809876" has balance of "150"

Scenario: User cannot make outgoing transfer with insufficient balance
    Given Account registry is empty
    And I create an account using name: "george", last name: "harrison", pesel: "43022509876"
    When I make "outgoing" transfer of "100" to account with pesel: "43022509876"
    Then Transfer is rejected
    And Account with pesel "43022509876" has balance of "0"

Scenario: User can make express transfer with fee
    Given Account registry is empty
    And I create an account using name: "ringo", last name: "starr", pesel: "40070709876"
    And I make "incoming" transfer of "100" to account with pesel: "40070709876"
    When I make "express" transfer of "50" to account with pesel: "40070709876"
    Then Transfer is accepted
    And Account with pesel "40070709876" has balance of "49"