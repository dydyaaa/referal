from locust import HttpUser, task, between
import requests

url = "http://45.143.203.217:5000/auth/login"
data = {"email": "mrt200228@gmail.com", "password": "test_pass"}

class ApiUser(HttpUser):

    wait_time = between(1, 3)
    response = requests.post(url, json=data)
    token = response.json().get('access_token')

    @task(1)
    def test_login(self):
        self.client.post(
            f"/auth/login", 
            json={
                "email": "mrt200228@gmail.com", 
                "password": "test_pass"
                })
        
    @task(1)
    def test_get_ref_email(self):
        self.client.post(f"/referral/code/by-email", json={"email": "mrt200228@gmail.com"})
        
    @task(2)
    def test_get_refs(self):
        self.client.get(
            f'/referral/referrals',
            headers={
                "Authorization": f"Bearer {self.token}", 
                "Content-Type": "application/json"}
        )
