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
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    # client.post("/post", json={"uid":"1", "title":"title1", "content":"content3", 
    #                                       "notebook":"notebook1", "base64String":"base64Stringasdfgh"})

    # response = client.delete("/delete?uid=1&notebook=notebook1&id=1")
        
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notes.query.count() == 0

# test delete same note multiple times

# test delete multiple notes

# test delete same note from diff users

# test delete diff note from diff users


# UDPATE endpoint

# update note with same name multiple times

# update note with different names

# update note of one person with multiple ppl

# update multiple notes of multiple ppl


# GET endpoint

# get notes from multiple users
