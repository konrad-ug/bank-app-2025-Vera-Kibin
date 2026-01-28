import pytest
import src.mongo_account_repository as mod
from src.account import Account

class FakeCollection:
    def __init__(self):
        self.calls = []
        self._docs = []

    def delete_many(self, q):
        self.calls.append(("delete_many", q))

    def update_one(self, q, update, upsert=False):
        self.calls.append(("update_one", q, update, upsert))

    def find(self, q):
        return list(self._docs)

    def set_docs(self, docs):
        self._docs = list(docs)

class FakeDB:
    def __init__(self):
        self.cols = {}
    def __getitem__(self, name):
        self.cols.setdefault(name, FakeCollection())
        return self.cols[name]

class FakeClient:
    def __init__(self, uri):
        self.uri = uri
        self.dbs = {}
    def __getitem__(self, db_name):
        self.dbs.setdefault(db_name, FakeDB())
        return self.dbs[db_name]

# --- testy ---

def test_init_uses_mongo_client_and_save_all(monkeypatch):
    created = {}

    def fake_mongo_client(uri):
        created["client"] = FakeClient(uri)
        return created["client"]

    monkeypatch.setattr(mod, "MongoClient", fake_mongo_client)

    repo = mod.MongoAccountsRepository(
        uri="mongodb://fake", db_name="db", collection_name="col"
    )

    a = Account("John", "Doe", "123")
    repo.save_all([a])

    coll = created["client"]["db"]["col"]
    assert ("delete_many", {}) in coll.calls
    assert any(c[0] == "update_one" and c[1] == {"pesel": "123"} and c[3] is True for c in coll.calls)

def test_load_all_reads_back(monkeypatch):
    def fake_mongo_client(uri):
        client = FakeClient(uri)
        coll = client["db"]["col"]
        coll.set_docs([Account("A", "B", "111").to_dict()])
        return client

    monkeypatch.setattr(mod, "MongoClient", fake_mongo_client)

    repo = mod.MongoAccountsRepository(
        uri="mongodb://fake", db_name="db", collection_name="col"
    )
    accounts = repo.load_all()
    assert len(accounts) == 1
    assert accounts[0].pesel == "111"