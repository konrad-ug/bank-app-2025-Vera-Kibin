from src.account import Account
from src.mongo_account_repository import MongoAccountsRepository
import pytest

class TestMongoAccountsRegistry:
    acc1 = Account("Alice", "Smith", "12345678901")
    acc2 = Account("Bob", "Johnson", "10987654321")

    @pytest.fixture(autouse=True)
    def mongo_repo(self):
        self.acc1.przelew_przychodzacy(100.0)

    def test_save_and_load_accounts(self, mocker):
        mock_collection = mocker.Mock()
        mock_collection.find.return_value = [
            self.acc1.to_dict(),
            self.acc2.to_dict()
        ]
        mongo_repo = MongoAccountsRepository(collection=mock_collection)
        mongo_repo.save_all([self.acc1, self.acc2])

        loaded_accounts = mongo_repo.load_all()

        assert len(loaded_accounts) == 2
        assert any(acc.pesel == "12345678901" and acc.first_name == "Alice" for acc in loaded_accounts)
        assert any(acc.pesel == "10987654321" and acc.first_name == "Bob" for acc in loaded_accounts)