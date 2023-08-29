from myapp.models import users, notebooks, notes

# POST endpoint

def test_post_notes(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    response = client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    with app.app_context():
        notebook_id = notebooks.query.filter_by(user_id=1, name="notebook").first()._id

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id=notebook_id, title="title", 
                                     content="content", base64_string="base64String").first() != None


# test multiple notes with same name
def test_post_notes_multiple_same_name(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    response = client.post("/post", json={"uid":"1", "title":"title", "content":"content1", 
                                          "notebook":"notebook", "base64String":"base64Stringasdf"})
    response = client.post("/post", json={"uid":"1", "title":"title", "content":"content2", 
                                          "notebook":"notebook", "base64String":"base64Stringasdfg"})
    response = client.post("/post", json={"uid":"1", "title":"title", "content":"content3", 
                                          "notebook":"notebook", "base64String":"base64Stringasdfgh"})
    
    with app.app_context():
        notebook_id = notebooks.query.filter_by(user_id=1, name="notebook").first()._id

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id=notebook_id, title="title").first() != None


# test multiple notes with different names
def test_post_notes_multiple_different_name(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})

    response = client.post("/post", json={"uid":"1", "title":"title1", "content":"content3", 
                                          "notebook":"notebook1", "base64String":"base64Stringasdfgh"})
    response = client.post("/post", json={"uid":"1", "title":"title2", "content":"content3", 
                                          "notebook":"notebook1", "base64String":"base64Stringasdfgh"})
    response = client.post("/post", json={"uid":"1", "title":"title3", "content":"content3", 
                                          "notebook":"notebook1", "base64String":"base64Stringasdfgh"})

    with app.app_context():
        notebook_id = notebooks.query.filter_by(user_id=1, name="notebook1").first()._id

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 3
        assert notes.query.filter_by(notebook_id=notebook_id, title="title1").first() != None
        assert notes.query.filter_by(notebook_id=notebook_id, title="title2").first() != None
        assert notes.query.filter_by(notebook_id=notebook_id, title="title3").first() != None


# test notes with same name that belong to diff people
def test_post_notes_same_name_different_people(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook"})

    response = client.post("/post", json={"uid":"1", "title":"title", "content":"content3", 
                                          "notebook":"notebook", "base64String":"base64Stringasdfgh"})
    
    response = client.post("/post", json={"uid":"2", "title":"title", "content":"content3", 
                                          "notebook":"notebook", "base64String":"base64Stringasdfgh"})
    
    with app.app_context():
        notebook_id_1 = notebooks.query.filter_by(user_id=1, name="notebook").first()._id
        notebook_id_2 = notebooks.query.filter_by(user_id=2, name="notebook").first()._id

        assert users.query.count() == 2
        assert notebooks.query.count() == 2
        assert notes.query.count() == 2
        assert notes.query.filter_by(notebook_id=notebook_id_1, title="title").first() != None
        assert notes.query.filter_by(notebook_id=notebook_id_2, title="title").first() != None


# test notes with diff name that belong to diff people
def test_post_notes_different_name_different_people(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook2"})

    response = client.post("/post", json={"uid":"1", "title":"title1", "content":"content3", 
                                          "notebook":"notebook1", "base64String":"base64Stringasdfgh"})
    
    response = client.post("/post", json={"uid":"2", "title":"title2", "content":"content3", 
                                          "notebook":"notebook2", "base64String":"base64Stringasdfgh"})
    
    with app.app_context():
        notebook_id_1 = notebooks.query.filter_by(user_id=1, name="notebook1").first()._id
        notebook_id_2 = notebooks.query.filter_by(user_id=2, name="notebook2").first()._id

        assert users.query.count() == 2
        assert notebooks.query.count() == 2
        assert notes.query.count() == 2
        assert notes.query.filter_by(notebook_id=notebook_id_1, title="title1").first() != None
        assert notes.query.filter_by(notebook_id=notebook_id_2, title="title2").first() != None


# DELETE endpoint

def test_delete_notes(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    response = client.delete("/delete", query_string={"uid":"1", "notebook":"notebook", "id":"1"})
    
    with app.app_context():

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 0

# test delete same note multiple times

def test_delete_notes_multiple_times(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook", "id":"1"})
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook", "id":"1"})
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook", "id":"1"})
    
    with app.app_context():

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 0


# test delete multiple notes

def test_delete_notes_multiple_notes(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"1", "title":"title2", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"1", "title":"title3", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook", "id":"1"})
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook", "id":"2"})
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook", "id":"3"})
    
    with app.app_context():

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 0


# test delete same notes in diff notebooks

def test_delete_notes_same_note_diff_notebooks(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook3"})

    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook1", "base64String":"base64String"})
    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook2", "base64String":"base64String"})
    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook3", "base64String":"base64String"})
    
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook1", "id":"1"})
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook2", "id":"2"})
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook3", "id":"3"})
    
    with app.app_context():

        assert users.query.count() == 1
        assert notebooks.query.count() == 3
        assert notes.query.count() == 0


# test delete diff notes in diff notebooks

def test_delete_notes_diff_notes_diff_notebooks(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook3"})

    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook1", "base64String":"base64String"})
    client.post("/post", json={"uid":"1", "title":"title2", "content":"content", 
                                          "notebook":"notebook2", "base64String":"base64String"})
    client.post("/post", json={"uid":"1", "title":"title3", "content":"content", 
                                          "notebook":"notebook3", "base64String":"base64String"})
    
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook1", "id":"1"})
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook2", "id":"2"})
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook3", "id":"3"})
    
    with app.app_context():

        assert users.query.count() == 1
        assert notebooks.query.count() == 3
        assert notes.query.count() == 0


# test delete same note from diff users

def test_delete_notes_same_note_diff_users(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/register-user", json={"uid":"3"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook2"})
    client.post("/post-notebook", json={"uid":"3", "notebook":"notebook3"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook1", "base64String":"base64String"})
    client.post("/post", json={"uid":"2", "title":"title", "content":"content", 
                                          "notebook":"notebook2", "base64String":"base64String"})
    client.post("/post", json={"uid":"3", "title":"title", "content":"content", 
                                          "notebook":"notebook3", "base64String":"base64String"})
    
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook1", "id":"1"})
    client.delete("/delete", query_string={"uid":"2", "notebook":"notebook2", "id":"2"})
    client.delete("/delete", query_string={"uid":"3", "notebook":"notebook3", "id":"3"})
    
    with app.app_context():

        assert users.query.count() == 3
        assert notebooks.query.count() == 3
        assert notes.query.count() == 0


# test delete diff note from diff users

def test_delete_notes_diff_note_diff_users(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/register-user", json={"uid":"3"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook2"})
    client.post("/post-notebook", json={"uid":"3", "notebook":"notebook3"})

    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook1", "base64String":"base64String"})
    client.post("/post", json={"uid":"2", "title":"title2", "content":"content", 
                                          "notebook":"notebook2", "base64String":"base64String"})
    client.post("/post", json={"uid":"3", "title":"title3", "content":"content", 
                                          "notebook":"notebook3", "base64String":"base64String"})
    
    client.delete("/delete", query_string={"uid":"1", "notebook":"notebook1", "id":"1"})
    client.delete("/delete", query_string={"uid":"2", "notebook":"notebook2", "id":"2"})
    client.delete("/delete", query_string={"uid":"3", "notebook":"notebook3", "id":"3"})
    
    with app.app_context():

        assert users.query.count() == 3
        assert notebooks.query.count() == 3
        assert notes.query.count() == 0


# UDPATE endpoint

def test_update_notes(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/update", json={"uid":"1", "id":"1", "title":"title1", "content":"content1", 
                                          "notebook":"notebook", "base64String":"base64String1"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id="1", title="title1", 
                                     content="content1", base64_string="base64String1").first() != None
        
# update note's title

def test_update_notes_title(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/update", json={"uid":"1", "id":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id="1", title="title1", 
                                     content="content", base64_string="base64String").first() != None


# update note's content

def test_update_notes_content(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/update", json={"uid":"1", "id":"1", "title":"title", "content":"content1", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id="1", title="title", 
                                     content="content1", base64_string="base64String").first() != None


# update note's base64String

def test_update_notes_base64string(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/update", json={"uid":"1", "id":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String1"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id="1", title="title", 
                                     content="content", base64_string="base64String1").first() != None
        

# update note with same name multiple times

def test_update_notes_multiple_times(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/update", json={"uid":"1", "id":"1", "title":"title1", "content":"content1", 
                                          "notebook":"notebook", "base64String":"base64String1"})
    client.post("/update", json={"uid":"1", "id":"1", "title":"title2", "content":"content2", 
                                          "notebook":"notebook", "base64String":"base64String2"})
    client.post("/update", json={"uid":"1", "id":"1", "title":"title3", "content":"content3", 
                                          "notebook":"notebook", "base64String":"base64String3"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert notes.query.filter_by(notebook_id="1", title="title3", 
                                     content="content3", base64_string="base64String3").first() != None


# update note with different names

def test_update_notes_multiple_names_multiple_times(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"1", "title":"title2", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"1", "title":"title3", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/update", json={"uid":"1", "id":"1", "title":"title4", "content":"content1", 
                                          "notebook":"notebook", "base64String":"base64String1"})
    client.post("/update", json={"uid":"1", "id":"2", "title":"title5", "content":"content2", 
                                          "notebook":"notebook", "base64String":"base64String2"})
    client.post("/update", json={"uid":"1", "id":"3", "title":"title6", "content":"content3", 
                                          "notebook":"notebook", "base64String":"base64String3"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 3
        assert notes.query.filter_by(notebook_id="1", title="title4", 
                                     content="content1", base64_string="base64String1").first() != None
        assert notes.query.filter_by(notebook_id="1", title="title5", 
                                     content="content2", base64_string="base64String2").first() != None
        assert notes.query.filter_by(notebook_id="1", title="title6", 
                                     content="content3", base64_string="base64String3").first() != None
        

# update note of one person with multiple ppl

def test_update_notes_multiple_people_same_person_updates(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/register-user", json={"uid":"3"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"3", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"2", "title":"title2", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"3", "title":"title3", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/update", json={"uid":"1", "id":"1", "title":"title1", "content":"content1", 
                                          "notebook":"notebook", "base64String":"base64String1"})
    
    with app.app_context():
        assert users.query.count() == 3
        assert notebooks.query.count() == 3
        assert notes.query.count() == 3
        assert notes.query.filter_by(notebook_id="1", title="title1", 
                                     content="content1", base64_string="base64String1").first() != None
        assert notes.query.filter_by(notebook_id="2", title="title2", 
                                     content="content", base64_string="base64String").first() != None
        assert notes.query.filter_by(notebook_id="3", title="title3", 
                                     content="content", base64_string="base64String").first() != None


# update multiple notes of multiple ppl

def test_update_notes_multiple_people_multiple_person_updates(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/register-user", json={"uid":"3"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook"})
    client.post("/post-notebook", json={"uid":"3", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"2", "title":"title2", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    client.post("/post", json={"uid":"3", "title":"title3", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    client.post("/update", json={"uid":"1", "id":"1", "title":"title1", "content":"content1", 
                                          "notebook":"notebook", "base64String":"base64String1"})
    client.post("/update", json={"uid":"2", "id":"2", "title":"title1", "content":"content2", 
                                          "notebook":"notebook", "base64String":"base64String2"})
    client.post("/update", json={"uid":"3", "id":"3", "title":"title1", "content":"content3", 
                                          "notebook":"notebook", "base64String":"base64String3"})
    
    with app.app_context():
        assert users.query.count() == 3
        assert notebooks.query.count() == 3
        assert notes.query.count() == 3
        assert notes.query.filter_by(notebook_id="1", title="title1", 
                                     content="content1", base64_string="base64String1").first() != None
        assert notes.query.filter_by(notebook_id="2", title="title1", 
                                     content="content2", base64_string="base64String2").first() != None
        assert notes.query.filter_by(notebook_id="3", title="title1", 
                                     content="content3", base64_string="base64String3").first() != None
        

# GET endpoint

def test_get_notes(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})

    client.post("/post", json={"uid":"1", "title":"title", "content":"content", 
                                          "notebook":"notebook", "base64String":"base64String"})
    
    response = client.get("/get?uid=1&notebook=notebook")

    with app.app_context():

        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 1
        assert b'[{"id": 1, "title": "title", "content": "content", "base64String": "base64String"}]' in response.data


# get notes from multiple users

def test_get_notes_multiple_users(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/register-user", json={"uid":"3"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook2"})
    client.post("/post-notebook", json={"uid":"3", "notebook":"notebook3"})

    client.post("/post", json={"uid":"1", "title":"title1", "content":"content", 
                                          "notebook":"notebook1", "base64String":"base64String"})
    client.post("/post", json={"uid":"2", "title":"title2", "content":"content", 
                                          "notebook":"notebook2", "base64String":"base64String"})
    client.post("/post", json={"uid":"3", "title":"title3", "content":"content", 
                                          "notebook":"notebook3", "base64String":"base64String"})
    
    response_1 = client.get("/get?uid=1&notebook=notebook1")
    response_2 = client.get("/get?uid=2&notebook=notebook2")
    response_3 = client.get("/get?uid=3&notebook=notebook3")

    with app.app_context():

        assert users.query.count() == 3
        assert notebooks.query.count() == 3
        assert notes.query.count() == 3
        assert b'[{"id": 1, "title": "title1", "content": "content", "base64String": "base64String"}]' in response_1.data
        assert b'[{"id": 2, "title": "title2", "content": "content", "base64String": "base64String"}]' in response_2.data
        assert b'[{"id": 3, "title": "title3", "content": "content", "base64String": "base64String"}]' in response_3.data