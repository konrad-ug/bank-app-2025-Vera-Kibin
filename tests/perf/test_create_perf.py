import random
import pytest
import requests
from faker import Faker

BASE_URL = "http://127.0.0.1:5000" 
TIMEOUT = 0.5
fake = Faker()

def _new_pesel():
    return ''.join(str(random.randint(0, 9)) for _ in range(11))

def _assert_fast(resp, limit=TIMEOUT, label="request"):
    assert resp.elapsed.total_seconds() < limit, (
        f"{label} took {resp.elapsed.total_seconds():.3f}s >= {limit}s"
    )

@pytest.fixture(scope="module")
def s():
    with requests.Session() as sess:
        yield sess

def test_performance_create_and_delete_100_accounts(s):
    for i in range(100):
        pesel = _new_pesel()
        payload = {"name": fake.first_name(), "surname": fake.last_name(), "pesel": pesel}

        r_create = s.post(f"{BASE_URL}/api/accounts", json=payload, timeout=TIMEOUT)
        assert r_create.status_code in (200, 201), f"create #{i} -> {r_create.status_code}"
        _assert_fast(r_create, label=f"create #{i}")

        r_delete = s.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)
        assert r_delete.status_code == 200, f"delete #{i} -> {r_delete.status_code}"
        _assert_fast(r_delete, label=f"delete #{i}")

def test_performance_create_and_make_100_incoming_transfers(s):
    pesel = _new_pesel()
    payload = {"name": fake.first_name(), "surname": fake.last_name(), "pesel": pesel}

    r_create = s.post(f"{BASE_URL}/api/accounts", json=payload, timeout=TIMEOUT)
    assert r_create.status_code in (200, 201)
    _assert_fast(r_create, label="create")

    total = 0
    for i in range(100):
        amount = random.randint(1, 1000)
        total += amount
        r = s.post(
            f"{BASE_URL}/api/accounts/{pesel}/transfer",
            json={"type": "incoming", "amount": amount},
            timeout=TIMEOUT,
        )
        assert r.status_code == 200, f"transfer #{i} -> {r.status_code}"
        _assert_fast(r, label=f"transfer #{i}")

    r_get = s.get(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)
    assert r_get.status_code == 200
    _assert_fast(r_get, label="get account")

    actual_balance = r_get.json()["balance"]
    assert actual_balance == pytest.approx(float(total), abs=1e-9), (
        f"Balance mismatch. Expected: {total}, Actual: {actual_balance}"
    )

    r_delete = s.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)
    assert r_delete.status_code == 200
    _assert_fast(r_delete, label="cleanup delete")