from myapp.models import users, notebooks, notes
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


# Create Chroma endpoint

def test_create_chroma(client, app):
    pass

def test_create_chroma_multiple_users(client, app):
    pass


# OPENAI endpoint

def test_get_openai(client, app):
    # first create user
    # client.post("/register-user", json={"uid":"1"})
    # client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    # content = "My name is Michael and my favourite sport is basketball"
    # client.post("/post", json={"uid":"1", "title":"title", "content":content, 
    #                                       "notebook":"notebook", "base64String":"base64String"})
    # response = client.post("/query", json={"uid":"1", "query_string":"What is Michael's favourite sport?", "notebook":"notebook"})
    
    # with app.app_context():
    #     notebook_id = notebooks.query.filter_by(user_id=1, name="notebook").first()._id

    #     assert users.query.count() == 1
    #     assert notebooks.query.count() == 1
    #     assert notes.query.count() == 1
    #     assert notes.query.filter_by(notebook_id=notebook_id, title="title", 
    #                                  content=content, base64_string="base64String").first() != None
    #     assert len(response.result.split()) <= 50
    #     print(response.result)
    pass

def test_get_openai_multiple_users(client, app):
    pass


# Summarize endpoint

def test_summarize(client, app):
    pass

def test_summarize_multiple_users(client, app):
    pass

