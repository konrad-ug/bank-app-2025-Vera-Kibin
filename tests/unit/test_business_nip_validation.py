import pytest
from src.business_account import BusinessAccount

class TestBusinessNipValidation:
    @staticmethod
    def _resp(json_obj, status=200):
        class R:
            status_code = status
            headers = {"Content-Type": "application/json"}
            def json(self): return json_obj
            @property
            def text(self): return str(json_obj)
        return R()

    def test_verify_true_when_status_czynny(self, mocker, monkeypatch, capsys):
        monkeypatch.setenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        mocker.patch(
            "src.business_account.requests.get",
            return_value=self._resp({"result": {"subject": {"statusVat": "Czynny"}}})
        )

        dummy = BusinessAccount.__new__(BusinessAccount)
        ok = BusinessAccount.verify_nip_with_mf(dummy, "8461627563")
        assert ok is True

        out = capsys.readouterr().out
        assert "[MF] GET" in out
        assert "Czynny" in out

    def test_verify_false_when_not_czynny(self, mocker):
        mocker.patch(
            "src.business_account.requests.get",
            return_value=self._resp({"result": {"subject": {"statusVat": "Brak"}}})
        )
        dummy = BusinessAccount.__new__(BusinessAccount)
        assert BusinessAccount.verify_nip_with_mf(dummy, "8461627563") is False

    def test_verify_false_on_non_200(self, mocker):
        mocker.patch(
            "src.business_account.requests.get",
            return_value=self._resp({"error": "not found"}, status=404)
        )
        dummy = BusinessAccount.__new__(BusinessAccount)
        assert BusinessAccount.verify_nip_with_mf(dummy, "8461627563") is False

    def test_verify_handles_exception_and_returns_false(self, mocker):
        mocker.patch(
            "src.business_account.requests.get",
            side_effect=Exception("boom")
        )
        dummy = BusinessAccount.__new__(BusinessAccount)
        assert BusinessAccount.verify_nip_with_mf(dummy, "8461627563") is False

    def test_ctor_raises_when_mf_denies(self, mocker):
        mocker.patch.object(BusinessAccount, "verify_nip_with_mf", return_value=False)
        with pytest.raises(ValueError, match="Company not registered!!"):
            BusinessAccount("ACME", "1234567890") 

    def test_ctor_skips_mf_when_bad_length(self, mocker):
        spy = mocker.spy(BusinessAccount, "verify_nip_with_mf")
        acc = BusinessAccount("ACME", "123")
        assert acc.nip == "Invalid"
        assert spy.call_count == 0

    def test_ctor_accepts_when_mf_ok(self, mocker):
        mocker.patch.object(BusinessAccount, "verify_nip_with_mf", return_value=True)
        acc = BusinessAccount("ACME", "8461627563")
        assert acc.nip == "8461627563"

    def test_verify_handles_bad_json_and_returns_false(self, mocker, monkeypatch, capsys):
        class FakeResp:
            status_code = 200
            headers = {"Content-Type": "text/html"}
            def json(self): 
                raise ValueError("bad json")
            @property
            def text(self):
                return "<html>oops</html>"

        monkeypatch.setenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        mocker.patch("src.business_account.requests.get", return_value=FakeResp())

        dummy = BusinessAccount.__new__(BusinessAccount)
        assert BusinessAccount.verify_nip_with_mf(dummy, "8461627563") is False

        out = capsys.readouterr().out
        assert "[MF] GET" in out