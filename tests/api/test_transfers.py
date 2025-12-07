import requests
import pytest


class TestTransfersApi:
    url = "http://127.0.0.1:5000"
    acc = {"name": "Vera", "surname": "Kibin", "pesel": "33333333333"}

    @pytest.fixture(autouse=True, scope="function")
    def setup(self):
        r = requests.post(f"{self.url}/api/accounts", json=self.acc, timeout=5)
        assert r.status_code in (201, 409)
        yield
        r_list = requests.get(f"{self.url}/api/accounts", timeout=5)
        if r_list.ok:
            for a in r_list.json():
                requests.delete(f"{self.url}/api/accounts/{a['pesel']}", timeout=5)

    def _transfer(self, pesel, amount, kind):
        return requests.post(
            f"{self.url}/api/accounts/{pesel}/transfer",
            json={"amount": amount, "type": kind},
            timeout=5,
        )

    def _get_balance(self, pesel):
        r = requests.get(f"{self.url}/api/accounts/{pesel}", timeout=5)
        assert r.status_code == 200
        return r.json()["balance"]

    @pytest.mark.parametrize("amt", [150.0, "150.0", 150])
    def test_incoming_success(self, amt):
        r = self._transfer(self.acc["pesel"], amt, "incoming")
        assert r.status_code == 200
        assert "balance" in r.json()
        assert r.json()["balance"] == 150.0

    @pytest.mark.parametrize("bad", [0, -5, "abc", None])
    def test_incoming_invalid_amount_400(self, bad):
        start = self._get_balance(self.acc["pesel"])
        r = self._transfer(self.acc["pesel"], bad, "incoming")
        assert r.status_code == 400
        assert self._get_balance(self.acc["pesel"]) == start

    def test_outgoing_success(self):
        assert self._transfer(self.acc["pesel"], 100.0, "incoming").status_code == 200
        r = self._transfer(self.acc["pesel"], 30.0, "outgoing")
        assert r.status_code == 200
        assert self._get_balance(self.acc["pesel"]) == 70.0

    def test_outgoing_insufficient_422(self):
        assert self._transfer(self.acc["pesel"], 50.0, "incoming").status_code == 200
        start = self._get_balance(self.acc["pesel"])
        r = self._transfer(self.acc["pesel"], 51.0, "outgoing")
        assert r.status_code == 422
        assert self._get_balance(self.acc["pesel"]) == start

    def test_express_equal_to_balance_allowed(self):
        assert self._transfer(self.acc["pesel"], 50.0, "incoming").status_code == 200
        r = self._transfer(self.acc["pesel"], 50.0, "express")
        assert r.status_code == 200
        assert self._get_balance(self.acc["pesel"]) == -1.0

    def test_express_gt_balance_422(self):
        assert self._transfer(self.acc["pesel"], 50.0, "incoming").status_code == 200
        start = self._get_balance(self.acc["pesel"])
        r = self._transfer(self.acc["pesel"], 51.0, "express")
        assert r.status_code == 422
        assert self._get_balance(self.acc["pesel"]) == start

    def test_unknown_type_400(self):
        r = self._transfer(self.acc["pesel"], 10.0, "teleport")
        assert r.status_code == 400

    def test_missing_body_400(self):
        r = requests.post(
            f"{self.url}/api/accounts/{self.acc['pesel']}/transfer",
            json={},
            timeout=5,
        )
        assert r.status_code == 400

    def test_transfer_on_missing_account_404(self):
        r = self._transfer("NOPE", 10.0, "incoming")
        assert r.status_code == 404

    def test_outgoing_string_amount_ok(self):
        assert self._transfer(self.acc["pesel"], 50.0, "incoming").status_code == 200
        r = self._transfer(self.acc["pesel"], "45.0", "outgoing")
        assert r.status_code == 200
        assert self._get_balance(self.acc["pesel"]) == 5.0