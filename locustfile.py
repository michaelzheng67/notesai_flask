from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2.5)  # Simulated users will wait 1 to 2.5 seconds between executing tasks

    @task
    def index(self):
        self.client.get("/")