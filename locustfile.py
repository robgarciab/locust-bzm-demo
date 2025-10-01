from locust import HttpUser, SequentialTaskSet, task, between
import os
import json

class DbBankFlow(SequentialTaskSet):
    def on_start(self):
        # storage for variables extracted during the flow
        self.vars = {}

    @task
    def login(self):
        # POST http://dbankdemo.com/bank/api/v1/auth?username=...&password=...
        url = "/bank/api/v1/auth"
        params = {
            "username": "rgarcia@perforce.com",
            "password": os.getenv("BZM_SECRET_dbank_rgarcia_password", "default_password")
        }
        headers = {"Content-Type": "application/json"}

        with self.client.post(url, params=params, headers=headers, catch_response=True) as res:
            if res.status_code == 200:
                try:
                    data = res.json()
                    token = data.get("authToken", "")
                    if token:
                        self.vars["token"] = token
                    else:
                        res.failure("No authToken in response JSON")
                except json.JSONDecodeError:
                    res.failure("Login response is not JSON")
            else:
                res.failure(f"Login failed: {res.status_code}")

    @task
    def get_transactions(self):
        # Skip if we don’t have token yet
        token = self.vars.get("token")
        if not token:
            return

        # GET http://dbankdemo.com/bank/api/v1/account/161739/transaction
        url = "/bank/api/v1/account/161739/transaction"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        with self.client.get(url, headers=headers, catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"Transaction fetch failed: {res.status_code}")

class WebsiteUser(HttpUser):
    tasks = [DbBankFlow]
    wait_time = between(1, 3)
    # Do NOT hardcode host; Taurus will pass --host via "default-address" in YAML
    # host = "http://dbankdemo.com"
