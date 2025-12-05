import requests

class TestCrudApi:
    url = "http://127.0.0.1:5000"
    account_data = {
        "name": "James",
        "surname": "Hetfield",
        "pesel": "89092909825",
    }

    def setup_method(self, _method):
        r = requests.get(f"{self.url}/api/accounts", timeout=5)
        if r.status_code == 200:
            for acc in r.json():
                requests.delete(f"{self.url}/api/accounts/{acc['pesel']}", timeout=5)

        resp = requests.post(f"{self.url}/api/accounts", json=self.account_data, timeout=5)
        assert resp.status_code == 201

    def teardown_method(self, _method):
        r = requests.get(f"{self.url}/api/accounts", timeout=5)
        if r.status_code == 200:
            for acc in r.json():
                requests.delete(f"{self.url}/api/accounts/{acc['pesel']}", timeout=5)

    # -------------------- tetst --------------------

    def test_get_account_count(self):
        r = requests.get(f"{self.url}/api/accounts/count", timeout=5)
        assert r.status_code == 200
        assert r.json()["count"] == 1 

    def test_create_account(self):
        new_acc = {"name": "John", "surname": "Doe", "pesel": "12345678910"}
        r_create = requests.post(f"{self.url}/api/accounts", json=new_acc, timeout=5)
        assert r_create.status_code == 201

        r_cnt = requests.get(f"{self.url}/api/accounts/count", timeout=5)
        assert r_cnt.status_code == 200
        assert r_cnt.json()["count"] == 2

        r_get = requests.get(f"{self.url}/api/accounts/{new_acc['pesel']}", timeout=5)
        assert r_get.status_code == 200
        body = r_get.json()
        assert body["name"] == "John"
        assert body["surname"] == "Doe"
        assert body["pesel"] == "12345678910"
        assert body["balance"] == 0.0

    def test_get_by_pesel_hit(self):
        pesel = self.account_data["pesel"]
        r = requests.get(f"{self.url}/api/accounts/{pesel}", timeout=5)
        assert r.status_code == 200
        j = r.json()
        assert j["name"] == "James"
        assert j["surname"] == "Hetfield"
        assert j["pesel"] == pesel

    def test_get_by_pesel_404(self):
        r = requests.get(f"{self.url}/api/accounts/NOPE", timeout=5)
        assert r.status_code == 404

    def test_list_all(self):
        r0 = requests.get(f"{self.url}/api/accounts", timeout=5)
        assert r0.status_code == 200
        assert len(r0.json()) == 1

        requests.post(f"{self.url}/api/accounts",
                      json={"name": "Alice", "surname": "A", "pesel": "01234567890"},
                      timeout=5)
        requests.post(f"{self.url}/api/accounts",
                      json={"name": "Bob", "surname": "B", "pesel": "12345678901"},
                      timeout=5)

        r = requests.get(f"{self.url}/api/accounts", timeout=5)
        assert r.status_code == 200
        got = {a["pesel"] for a in r.json()}
        assert {"89092909825", "01234567890", "12345678901"}.issubset(got)

    def test_patch_updates_only_provided_fields(self):
        pesel = self.account_data["pesel"]

        r1 = requests.patch(f"{self.url}/api/accounts/{pesel}",
                            json={"name": "Jim"},
                            timeout=5)
        assert r1.status_code == 200
        j1 = requests.get(f"{self.url}/api/accounts/{pesel}", timeout=5).json()
        assert j1["name"] == "Jim"
        assert j1["surname"] == "Hetfield"

        r2 = requests.patch(f"{self.url}/api/accounts/{pesel}",
                            json={"surname": "Roe"},
                            timeout=5)
        assert r2.status_code == 200
        j2 = requests.get(f"{self.url}/api/accounts/{pesel}", timeout=5).json()
        assert j2["name"] == "Jim"
        assert j2["surname"] == "Roe"

    def test_delete_account(self):
        temp = {"name": "X", "surname": "Y", "pesel": "22222222222"}
        requests.post(f"{self.url}/api/accounts", json=temp, timeout=5)

        rdel = requests.delete(f"{self.url}/api/accounts/{temp['pesel']}", timeout=5)
        assert rdel.status_code == 200

        rget = requests.get(f"{self.url}/api/accounts/{temp['pesel']}", timeout=5)
        assert rget.status_code == 404

    def test_delete_missing_returns_404(self):
        r = requests.delete(f"{self.url}/api/accounts/NOPE", timeout=5)
        assert r.status_code == 404