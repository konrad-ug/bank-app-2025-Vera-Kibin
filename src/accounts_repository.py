from abc import ABC, abstractmethod

class AccountsRepository(ABC):
    @abstractmethod
    def save_all(self, accounts):
        raise NotImplementedError

    @abstractmethod
    def load_all(self):
        raise NotImplementedError

    def close(self):
        pass