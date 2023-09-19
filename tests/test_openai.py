from myapp.models import users, notebooks, notes
from unittest.mock import Mock, patch
import os
import shutil

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

def test_create_chroma_no_data(client, app):
    client.post("/register-user", json={"uid":"1"})
    client.post("/create-chroma", json={"uid":"1"})

    path_to_check = os.environ["CHROMA_STORE"] + "1" + "/chromadb"
        
    with app.app_context():
        assert not os.path.exists(path_to_check)


def test_create_chroma_with_data(client, app):
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/create-chroma", json={"uid":"1"})
    
    path_to_check = os.environ["CHROMA_STORE"] + "1" + "/chromadb"
        
    with app.app_context():
        assert os.path.exists(path_to_check)

    try:
        shutil.rmtree(path_to_check)
    except Exception as e:
        print(f"Error removing directory: {e}")


def test_create_chroma_multiple_notebooks(client, app):
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook2"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook3"})
    client.post("/post", json={"uid":"2", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/create-chroma", json={"uid":"2"})
    
    path_to_check = os.environ["CHROMA_STORE"] + "2" + "/chromadb"
        
    with app.app_context():
        assert os.path.exists(path_to_check)

    try:
        shutil.rmtree(path_to_check)
    except Exception as e:
        print(f"Error removing directory: {e}")


def test_create_chroma_multiple_notes(client, app):
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook"})
    client.post("/post", json={"uid":"2", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"2", "title":"title2", "content":"content2", 
                                          "notebook":"notebook", "base64String":"base64String2"})
    client.post("/post", json={"uid":"2", "title":"title3", "content":"content3", 
                                          "notebook":"notebook", "base64String":"base64String3"})
    client.post("/create-chroma", json={"uid":"2"})
    
    path_to_check = os.environ["CHROMA_STORE"] + "2" + "/chromadb"
        
    with app.app_context():
        assert os.path.exists(path_to_check)

    try:
        shutil.rmtree(path_to_check)
    except Exception as e:
        print(f"Error removing directory: {e}")


def test_create_chroma_multiple_users(client, app):
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/register-user", json={"uid":"3"})

    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"3", "notebook":"notebook"})


    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"2", "title":"title2", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"3", "title":"title3", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/create-chroma", json={"uid":"1"})
    client.post("/create-chroma", json={"uid":"2"})
    client.post("/create-chroma", json={"uid":"3"})
    
    path_to_check_1 = os.environ["CHROMA_STORE"] + "1" + "/chromadb"
    path_to_check_2 = os.environ["CHROMA_STORE"] + "2" + "/chromadb"
    path_to_check_3 = os.environ["CHROMA_STORE"] + "3" + "/chromadb"
        
    with app.app_context():
        assert os.path.exists(path_to_check_1)
        assert os.path.exists(path_to_check_2)
        assert os.path.exists(path_to_check_3)

    try:
        shutil.rmtree(path_to_check_1)
        shutil.rmtree(path_to_check_2)
        shutil.rmtree(path_to_check_3)
    except Exception as e:
        print(f"Error removing directory: {e}")


# OPENAI endpoint

def test_get_openai(client, app):
    #first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    content = "My name is Michael and my favourite sport is basketball"
    client.post("/post", json={"uid":"1", "title":"title", "content":content, 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/create-chroma", json={"uid":"1"})
    

    response = client.post("/query", json={"uid":"1", "query_string":"What is Michael's favourite sport?", "notebook":"notebook"})
    
    path_to_check = os.environ["CHROMA_STORE"] + "1" + "/chromadb"
    print(response)

    with app.app_context():
        notebook_id = notebooks.query.filter_by(user_id=1, name="notebook").first()._id

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id=notebook_id, title="title", 
                                     content=content, base64_string="base64String").first() != None

        assert len(response.json["result"].split()) <= 50

        assert os.path.exists(path_to_check)

    
    try:
        shutil.rmtree(path_to_check)
    except Exception as e:
        print(f"Error removing directory: {e}")


def test_get_openai_multiple_users(client, app):
    pass


# Summarize endpoint

def test_summarize(client, app):
    #first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    content = "My name is Michael and my favourite sport is basketball"
    client.post("/post", json={"uid":"1", "title":"title", "content":content, 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/create-chroma", json={"uid":"1"})
    

    response = client.post("/summarize", json={"uid":"1", "notebook_id":"1", "note":"title", "note_id":"1"})
    
    path_to_check = os.environ["CHROMA_STORE"] + "1" + "/chromadb"


    with app.app_context():
        notebook_id = notebooks.query.filter_by(user_id=1, name="notebook").first()._id

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id=notebook_id, title="title", 
                                     content=content, base64_string="base64String").first() != None

        assert len(response.json["result"].split()) <= 200

        assert os.path.exists(path_to_check)

    
    try:
        shutil.rmtree(path_to_check)
    except Exception as e:
        print(f"Error removing directory: {e}")


def test_summarize_multiple_users(client, app):
    #first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/register-user", json={"uid":"3"})

    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"3", "notebook":"notebook"})

    content1 = "My name is Michael1 and my favourite sport is basketball"
    content2 = "My name is Michael2 and my favourite sport is basketball"
    content3 = "My name is Michael3 and my favourite sport is basketball"

    client.post("/post", json={"uid":"1", "title":"title", "content":content1, 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"2", "title":"title", "content":content2, 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"3", "title":"title", "content":content3, 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/create-chroma", json={"uid":"1"})
    client.post("/create-chroma", json={"uid":"2"})
    client.post("/create-chroma", json={"uid":"3"})
    

    response1 = client.post("/summarize", json={"uid":"1", "notebook_id":"1", "note":"title", "note_id":"1"})
    response2 = client.post("/summarize", json={"uid":"2", "notebook_id":"2", "note":"title", "note_id":"2"})
    response3 = client.post("/summarize", json={"uid":"3", "notebook_id":"3", "note":"title", "note_id":"3"})
    
    path_to_check_1 = os.environ["CHROMA_STORE"] + "1" + "/chromadb"
    path_to_check_2 = os.environ["CHROMA_STORE"] + "2" + "/chromadb"
    path_to_check_3 = os.environ["CHROMA_STORE"] + "3" + "/chromadb"


    with app.app_context():

        assert users.query.count() == 3
        assert notebooks.query.count() == 3
        assert notes.query.count() == 3

        assert len(response1.json["result"].split()) <= 200
        assert len(response1.json["result"].split()) <= 200
        assert len(response1.json["result"].split()) <= 200

        assert os.path.exists(path_to_check_1)
        assert os.path.exists(path_to_check_2)
        assert os.path.exists(path_to_check_3)

    
    try:
        shutil.rmtree(path_to_check_1)
        shutil.rmtree(path_to_check_2)
        shutil.rmtree(path_to_check_3)
    except Exception as e:
        print(f"Error removing directory: {e}")

