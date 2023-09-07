from myapp.models import users
from unittest.mock import Mock, patch

# POST settings

def test_post_settings(client, app):
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-settings", json={"uid":"1", "temperature" : "10", "similarity" : "10", "wordcount" : "10"})

    with app.app_context():
        user = users.query.filter_by(user_id="1").first()
        assert user.temperature == 10
        assert user.similarity == 10
        assert user.wordcount == 10

def test_post_settings_multiple_users(client, app):
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-settings", json={"uid":"1", "temperature" : "10", "similarity" : "10", "wordcount" : "10"})
    client.post("/post-settings", json={"uid":"2", "temperature" : "20", "similarity" : "20", "wordcount" : "20"})

    with app.app_context():
        user1 = users.query.filter_by(user_id="1").first()
        user2 = users.query.filter_by(user_id="2").first()
        assert user1.temperature == 10
        assert user1.similarity == 10
        assert user1.wordcount == 10
        assert user2.temperature == 20
        assert user2.similarity == 20
        assert user2.wordcount == 20


# GET settings

def test_get_settings(client, app):
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-settings", json={"uid":"1", "temperature" : "10", "similarity" : "10", "wordcount" : "10"})
    response = client.get("/get-settings/1")

    with app.app_context():
        data = response.json
        assert data["temperature"] == 10
        assert data["similarity"] == 10
        assert data["wordcount"] == 10


def test_get_settings_multiple_users(client, app):
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-settings", json={"uid":"1", "temperature" : "10", "similarity" : "10", "wordcount" : "10"})
    response_1 = client.get("/get-settings/1")
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-settings", json={"uid":"2", "temperature" : "20", "similarity" : "20", "wordcount" : "20"})
    response_2 = client.get("/get-settings/2")
    
    with app.app_context():
        data_1 = response_1.json
        assert data_1["temperature"] == 10
        assert data_1["similarity"] == 10
        assert data_1["wordcount"] == 10

        data_2 = response_2.json
        assert data_2["temperature"] == 20
        assert data_2["similarity"] == 20
        assert data_2["wordcount"] == 20


# OPENAI endpoint

def test_get_openai(client, app):
    pass

def test_get_openai_multiple_users(client, app):
    pass

