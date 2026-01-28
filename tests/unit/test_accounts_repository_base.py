import pytest
from src.accounts_repository import AccountsRepository

class DummyRepo(AccountsRepository):
    def save_all(self, accounts):
        return super().save_all(accounts)
    def load_all(self):
        return super().load_all()

def test_base_repo_abstract_methods_raise():
    repo = DummyRepo()
    with pytest.raises(NotImplementedError):
        repo.save_all([])
    with pytest.raises(NotImplementedError):
        repo.load_all()

def test_base_repo_close_noop():
    repo = DummyRepo()
    assert repo.close() is None