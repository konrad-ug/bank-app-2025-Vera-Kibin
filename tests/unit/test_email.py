from datetime import date
import pytest
from src.account import Account
from src.business_account import BusinessAccount

class TestEmail:
    @pytest.fixture(autouse=True)
    def _mf_ok(self, mocker):
        mocker.patch.object(BusinessAccount, "verify_nip_with_mf", return_value=True)

    @pytest.fixture
    def personal(self):
        a = Account("Jane", "Smith", "98765432101")
        a.history = [150.0, -50.0]
        return a

    @pytest.fixture
    def business(self):
        b = BusinessAccount("ACME", "8461627563")
        b.history = [5000.0, -1000.0, 500.0]
        return b

    @pytest.fixture
    def today(self):
        return date.today().isoformat()

    def test_personal_success_and_call_args(self, mocker, personal, today):
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=True)

        ok = personal.send_history_via_email("test@email.com")
        assert ok is True

        mock_send.assert_called_once()
        subject, text, to_ = mock_send.call_args[0]
        assert subject == f"Account Transfer History {today}"
        assert text == f"Personal account history: {personal.history}"
        assert to_ == "test@email.com"

    def test_business_success_and_call_args(self, mocker, business, today):
        mock_send = mocker.patch("src.business_account.SMTPClient.send", return_value=True)

        ok = business.send_history_via_email("corp@test.com")
        assert ok is True

        mock_send.assert_called_once()
        subject, text, to_ = mock_send.call_args[0]
        assert subject == f"Account Transfer History {today}"
        assert text == f"Company account history: {business.history}"
        assert to_ == "corp@test.com"

    def test_personal_failure(self, mocker, personal):
        mocker.patch("src.account.SMTPClient.send", return_value=False)
        assert personal.send_history_via_email("x@y.z") is False

    def test_business_failure(self, mocker, business):
        mocker.patch("src.business_account.SMTPClient.send", return_value=False)
        assert business.send_history_via_email("corp@test.com") is False

    @pytest.mark.parametrize("kind", ["personal", "business"])
    def test_empty_history_body(self, mocker, kind, today):
        if kind == "personal":
            acct = Account("A", "B", "98765432101")
            target = "src.account.SMTPClient.send"
            expected_text = "Personal account history: []"
        else:
            acct = BusinessAccount("ACME", "8461627563")
            target = "src.business_account.SMTPClient.send"
            expected_text = "Company account history: []"

        acct.history = []
        mock_send = mocker.patch(target, return_value=True)

        assert acct.send_history_via_email("a@b.c") is True
        subject, text, to_ = mock_send.call_args[0]
        assert subject == f"Account Transfer History {today}"
        assert text == expected_text
        assert to_ == "a@b.c"

    @pytest.mark.parametrize("kind", ["personal", "business"])
    def test_exception_from_smtp_bubbles(self, mocker, kind):
        if kind == "personal":
            acct = Account("A", "B", "98765432101")
            target = "src.account.SMTPClient.send"
        else:
            acct = BusinessAccount("ACME", "8461627563")
            target = "src.business_account.SMTPClient.send"

        acct.history = [1.0]
        mocker.patch(target, side_effect=Exception("smtp down"))

        with pytest.raises(Exception):
            acct.send_history_via_email("a@b.c")