import requests
import random
import string

BASE_URL = "http://localhost:8000/api/v1"


def random_email():
    return "".join(random.choices(string.ascii_lowercase, k=10)) + "@test.com"


def test_auth_flow():
    email = random_email()
    password = "testpassword123"

    print(f"Testing registration with {email}...")
    try:
        # 1. Register
        reg_resp = requests.post(
            f"{BASE_URL}/register",
            json={"email": email, "password": password, "full_name": "Test User"},
        )
        print(f"Register status: {reg_resp.status_code}")
        if reg_resp.status_code != 200:
            print(f"Register error: {reg_resp.text}")
            return

        # 2. Login
        print("Testing login...")
        login_resp = requests.post(
            f"{BASE_URL}/login", data={"username": email, "password": password}
        )
        print(f"Login status: {login_resp.status_code}")
        if login_resp.status_code != 200:
            print(f"Login error: {login_resp.text}")
            return

        token = login_resp.json().get("access_token")
        auth_header = {"Authorization": f"Bearer {token}"}

        # 3. Scan (Private)
        print("Testing private scan...")
        scan_resp = requests.post(
            f"{BASE_URL}/scan", headers=auth_header, json={"url": "http://example.com"}
        )
        print(f"Scan status: {scan_resp.status_code}")

        # 4. History
        print("Testing history...")
        history_resp = requests.get(f"{BASE_URL}/history", headers=auth_header)
        print(f"History status: {history_resp.status_code}")
        print(f"History count: {len(history_resp.json())}")

    except Exception as e:
        print(f"API Connection error: {e}")


if __name__ == "__main__":
    test_auth_flow()
