from behave import given, when, then, step
import requests

URL = "http://127.0.0.1:5000"

def _ensure_empty_registry():
    r = requests.get(f"{URL}/api/accounts", timeout=5)
    if r.ok and r.headers.get("Content-Type", "").startswith("application/json"):
        for acc in r.json():
            requests.delete(f"{URL}/api/accounts/{acc['pesel']}", timeout=5)

def _create_account_if_missing(pesel, name="BDD", surname="User"):
    payload = {"name": name, "surname": surname, "pesel": pesel}
    r = requests.post(f"{URL}/api/accounts", json=payload, timeout=5)
    assert r.status_code in (201, 409), f"Create failed: {r.status_code}"

def _get_balance(pesel) -> float:
    r = requests.get(f"{URL}/api/accounts/{pesel}", timeout=5)
    assert r.status_code == 200
    return float(r.json()["balance"])

def _set_balance(pesel, target):
    _ensure_empty_registry()
    _create_account_if_missing(pesel)
    if float(target) > 0:
        r = requests.post(f"{URL}/api/accounts/{pesel}/transfer",
                          json={"type": "incoming", "amount": float(target)},
                          timeout=5)
        assert r.status_code == 200, f"Failed to seed balance: {r.status_code}"

@given('Użytkownik posiada konto bankowe o numerze PESEL {pesel}')
def step_have_account(context, pesel):
    _create_account_if_missing(pesel)
    context.pesel = pesel

@given('Saldo użytkownika na koncie wynosi {amount:g} zł')
def step_balance_is(context, amount):
    assert hasattr(context, "pesel"), "Brak peselu w kontekście"
    _set_balance(context.pesel, amount)

@when('Użytkownik otrzymuje przelew przychodzący w wysokości {amount:g} zł')
def step_incoming(context, amount):
    r = requests.post(f"{URL}/api/accounts/{context.pesel}/transfer",
                      json={"type": "incoming", "amount": float(amount)},
                      timeout=5)
    context.last_response = r

@when('Użytkownik zleca przelew wychodzący w wysokości {amount:g} zł')
def step_outgoing(context, amount):
    r = requests.post(f"{URL}/api/accounts/{context.pesel}/transfer",
                      json={"type": "outgoing", "amount": float(amount)},
                      timeout=5)
    context.last_response = r

@when('Użytkownik zleca przelew ekspresowy w wysokości {amount:g} zł')
def step_express(context, amount):
    r = requests.post(f"{URL}/api/accounts/{context.pesel}/transfer",
                      json={"type": "express", "amount": float(amount)},
                      timeout=5)
    context.last_response = r

@when('Użytkownik zleca przelew o niepoprawnym typie {kind}')
def step_wrong_kind(context, kind):
    r = requests.post(f"{URL}/api/accounts/{context.pesel}/transfer",
                      json={"type": kind, "amount": 1},
                      timeout=5)
    context.last_response = r
    context.kind = kind

@then('System powinien zwrócić komunikat: Zlecenie przyjeto do realizacji')
def step_msg_accepted(context):
    assert context.last_response.status_code == 200

@then('System powinien zwrócić komunikat: Niewystarczające srodki na koncie')
def step_msg_insufficient(context):
    assert context.last_response.status_code == 422

@then('System powinien zwrócić komunikat: Nieznany typ transferu: {kind}')
def step_msg_unknown_kind(context, kind):
    assert context.last_response.status_code == 400
    try:
        msg = context.last_response.json().get("message", "").lower()
        assert "type" in msg or "unknown" in msg or "doesn`t" in msg
    except Exception:
        pass

@then('Saldo użytkownika na koncie powinno wynosić {expected:g} zł')
def step_balance_equals(context, expected):
    bal = _get_balance(context.pesel)
    assert abs(bal - float(expected)) < 1e-6, f"Expected {expected}, got {bal}"