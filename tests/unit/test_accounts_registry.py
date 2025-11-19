import pytest
from src.account import Account
from src.business_account import BusinessAccount
from src.accounts_registry import AccountsRegistry

class TestAccountRegistry:
    @pytest.fixture
    def registry(self):
        return AccountsRegistry()

    @pytest.fixture
    def alice(self):
        return Account("Alice", "A", "01234567890")

    @pytest.fixture
    def bob(self):
        return Account("Bob", "B", "12345678901")

    def test_empty_registry(self, registry):
        assert registry.count() == 0
        assert registry.all_accounts() == []

    def test_add_and_list(self, registry, alice, bob):
        registry.add_account(alice)
        registry.add_account(bob)
        accs = registry.all_accounts()
        assert registry.count() == 2
        assert accs[0] is alice and accs[1] is bob

    def test_find_by_pesel_hit_and_miss(self, registry, alice, bob):
        registry.add_account(alice)
        registry.add_account(bob)
        assert registry.find_by_pesel("01234567890") is alice
        assert registry.find_by_pesel("no-such") is None

    def test_all_returns_copy_not_reference(self, registry, alice):
        registry.add_account(alice)
        snapshot = registry.all_accounts()
        snapshot.append(object())
        assert registry.count() == 1

    def test_rejects_non_personal_accounts(self, registry):
        ba = BusinessAccount("KIBINGUITARS", "1234567890")
        with pytest.raises(TypeError):
            registry.add_account(ba)

    @pytest.mark.parametrize(
        "pesel_lookup, expected",
        [("01234567890", True), ("12345678901", True), ("99999999999", False)]
    )
    def test_param_find(self, registry, alice, bob, pesel_lookup, expected):
        registry.add_account(alice)
        registry.add_account(bob)
        found = registry.find_by_pesel(pesel_lookup)
        assert (found is not None) is expected

    @pytest.mark.parametrize("lookup, ok", [("01234567890", True), (1234567890, False)])
    def test_lookup_requires_string_11_digits(self, registry, alice, lookup, ok):
        registry.add_account(alice)
        found = registry.find_by_pesel(lookup)
        assert (found is not None) is ok

    def test_all_returns_new_list_each_time(self, registry, alice):
        registry.add_account(alice)
        a = registry.all_accounts()
        b = registry.all_accounts()
        assert a is not b
