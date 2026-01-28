import os
from pymongo import MongoClient

from src.accounts_repository import AccountsRepository
from src.account import Account


class MongoAccountsRepository(AccountsRepository):
    def __init__(self, collection=None, uri=None, db_name=None, collection_name=None):
        if collection is not None:
            self._collection = collection
            self._client = None
            return

        mongo_uri = uri or os.environ.get("MONGO_URI", "mongodb://localhost:27017")
        mongo_db = db_name or os.environ.get("MONGO_DB", "bank_app")
        mongo_collection = collection_name or os.environ.get("MONGO_COLLECTION", "accounts")

        self._client = MongoClient(mongo_uri)
        self._collection = self._client[mongo_db][mongo_collection]

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True,
            )

    def load_all(self):
        accounts = []
        for data in self._collection.find({}):
            accounts.append(Account.from_dict(data))
        return accounts