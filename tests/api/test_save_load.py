import pytest
import requests

class TestSaveLoadApi:
    url = "http://127.0.0.1:5000"
    acc_data = {"name": "Anna", "surname": "Nowak", "pesel": "11223344556"}
    transfer_data = {"amount": 200.0, "type": "incoming"}

    def _wipe(self):
        r = requests.get(f"{self.url}/api/accounts", timeout=5)
        if r.ok:
            for a in r.json():
                requests.delete(f"{self.url}/api/accounts/{a['pesel']}", timeout=5)

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self._wipe()
        r = requests.post(f"{self.url}/api/accounts", json=self.acc_data, timeout=5)
        assert r.status_code in (201, 409)
        r = requests.post(
            f"{self.url}/api/accounts/{self.acc_data['pesel']}/transfer",
            json=self.transfer_data,
            timeout=5,
        )
        assert r.status_code == 200
        yield
        self._wipe()

    def test_save_load_accounts(self):
        r = requests.post(f"{self.url}/api/accounts/save", timeout=5)
        assert r.status_code == 200
        assert r.json()["message"] == "Accounts saved to MongoDB"

        self._wipe()

        r = requests.post(f"{self.url}/api/accounts/load", timeout=5)
        assert r.status_code == 200
        assert r.json()["message"] == "Accounts loaded from MongoDB"

        r = requests.get(f"{self.url}/api/accounts/{self.acc_data['pesel']}", timeout=5)
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == self.acc_data["name"]
        assert body["surname"] == self.acc_data["surname"]
        assert body["pesel"] == self.acc_data["pesel"]
        assert body["balance"] == 200.0