from behave import given, when, then, step
import requests
URL = "http://127.0.0.1:5000"

@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = { "name": f"{name}",
    "surname": f"{last_name}",
    "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json = json_body)
    assert create_resp.status_code == 201

@step('Account registry is empty')
@step('Acoount registry is empty')
def clear_account_registry_typo(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()

    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")

@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    assert len(accounts) == int(count)

@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    json_body = { "name": None, "surname": None, f"{field}": f"{value}" }
    response = requests.patch(URL + f"/api/accounts/{pesel}", json = json_body)
    assert response.status_code == 200

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account = response.json()
    assert account[field] == value

@when('I make "{transfer_type}" transfer of "{amount}" to account with pesel: "{pesel}"')
@step('I make "{transfer_type}" transfer of "{amount}" to account with pesel: "{pesel}"')
def make_transfer(context, transfer_type, amount, pesel):
    json_body = {
        "type": transfer_type,
        "amount": float(amount)
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    context.transfer_response = response

@then('Transfer is accepted')
def transfer_accepted(context):
    assert context.transfer_response.status_code == 200

@then('Transfer is rejected')
def transfer_rejected(context):
    assert context.transfer_response.status_code == 422

@then('Account with pesel "{pesel}" has balance of "{balance}"')
def check_balance(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account = response.json()
    assert account["balance"] == float(balance)