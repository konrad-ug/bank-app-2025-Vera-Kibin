from flask import Flask, request, jsonify, abort
from src.accounts_registry import AccountsRegistry
from src.account import Account

app = Flask(__name__)
registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print("Create account request received")
    print(f"Create account request: {data}")
    if registry.find_by_pesel(data["pesel"]):
        return jsonify({"message": "Account with this PESEL already exists"}), 409
    account = Account(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    return jsonify({"count": registry.count()}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)
    return jsonify(
        {"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance}
    ), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)
    data = request.get_json(force=True) or {}
    if "name" in data:    acc.first_name = data["name"]
    if "surname" in data: acc.last_name  = data["surname"]    
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    if not registry.remove_by_pesel(pesel):
        abort(404)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def execute_transfer(pesel):
    data = request.get_json(force=True) or {}
    if "amount" not in data or "type" not in data:
        return jsonify({"message": "Request body must contain 'amount' and 'type'."}), 400

    acc = registry.find_by_pesel(pesel)
    if not acc:
        return jsonify({"message": "Account not found"}), 404

    amount = data["amount"]
    transfer_type = data["type"]

    transfers_types_mapping = {
        "incoming": acc.przelew_przychodzacy,
        "outgoing": acc.przelew_wychodzacy,
        "express":  acc.przelew_ekspresowy,
    }
    if transfer_type not in transfers_types_mapping:
        return jsonify({"message": "Unknown transfer type"}), 400

    ok = transfers_types_mapping[transfer_type](amount)

    if transfer_type in {"outgoing", "express"} and ok is False:
        return jsonify({"message": "Transfer rejected"}), 422
    if transfer_type == "incoming" and ok is False:
        return jsonify({"message": "Invalid amount"}), 400

    return jsonify({"message": "Transfer successful", "balance": acc.balance}), 200