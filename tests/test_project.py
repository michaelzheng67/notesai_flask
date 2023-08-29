from myapp.models import users

def test_works(client):
    response = client.get("/")
    assert b"<p>Hello, World!</p>" in response.data


# /register-user

def test_register_user(client, app):
    response = client.post("/register-user", json={"uid" : "1"})

    with app.app_context():
        assert users.query.count() == 1
        assert users.query.first().user_id == "1"

def test_register_user_duplicates(client, app):
    response = client.post("/register-user", json={"uid" : "2"})
    response = client.post("/register-user", json={"uid" : "2"})
    response = client.post("/register-user", json={"uid" : "2"})

    with app.app_context():
        assert users.query.count() == 1
        assert users.query.first().user_id == "2"