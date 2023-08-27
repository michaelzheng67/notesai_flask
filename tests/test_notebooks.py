from myapp.models import users, notebooks

# POST endpoints

def test_post_notebooks(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})

    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notebooks.query.first().user_id == 1
        assert notebooks.query.first().name == "notebook"


def test_post_notebooks_multiple_same_name(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})

    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notebooks.query.first().user_id == 1
        assert notebooks.query.first().name == "notebook"


def test_post_notebooks_multiple_different_name(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})

    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook2"})
    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook3"})
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 3
        assert notebooks.query.filter_by(user_id=1, name="notebook1").first() != None
        assert notebooks.query.filter_by(user_id=1, name="notebook2").first() != None
        assert notebooks.query.filter_by(user_id=1, name="notebook3").first() != None


def test_post_notebooks_same_name_different_people(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})

    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook"})
    response = client.post("/post-notebook", json={"uid":"2", "notebook":"notebook"})
    
    with app.app_context():
        assert users.query.count() == 2
        assert notebooks.query.count() == 2

        assert notebooks.query.filter_by(user_id=1).first().user_id == 1
        assert notebooks.query.filter_by(user_id=1).first().name == "notebook"

        assert notebooks.query.filter_by(user_id=2).first().user_id == 2
        assert notebooks.query.filter_by(user_id=2).first().name == "notebook"
        

def test_post_notebooks_different_name_different_people(client, app):
    # first create user
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})

    response = client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    response = client.post("/post-notebook", json={"uid":"2", "notebook":"notebook2"})
    
    with app.app_context():
        assert users.query.count() == 2
        assert notebooks.query.count() == 2

        assert notebooks.query.filter_by(user_id=1).first().user_id == 1
        assert notebooks.query.filter_by(user_id=1).first().name == "notebook1"

        assert notebooks.query.filter_by(user_id=2).first().user_id == 2
        assert notebooks.query.filter_by(user_id=2).first().name == "notebook2"


# DELETE endpoint

def test_delete_notebooks(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})


    response = client.delete("/delete-notebook?uid=1&notebook=notebook1")
        
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 0



def test_delete_notebooks_delete_multiple_same(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})


    response = client.delete("/delete-notebook?uid=1&notebook=notebook1")
    response = client.delete("/delete-notebook?uid=1&notebook=notebook1")
    response = client.delete("/delete-notebook?uid=1&notebook=notebook1")
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 0


def test_delete_notebooks_delete_multiple_multiple(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook3"})


    response = client.delete("/delete-notebook?uid=1&notebook=notebook1")
    response = client.delete("/delete-notebook?uid=1&notebook=notebook2")
    response = client.delete("/delete-notebook?uid=1&notebook=notebook3")
    
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 0


def test_delete_notebooks_delete_same_user(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook2"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook3"})

    response = client.delete("/delete-notebook?uid=1&notebook=notebook1")
    response = client.delete("/delete-notebook?uid=2&notebook=notebook1")
    response = client.delete("/delete-notebook?uid=1&notebook=notebook2")
    response = client.delete("/delete-notebook?uid=2&notebook=notebook3")

    with app.app_context():
        assert users.query.count() == 2
        assert notebooks.query.count() == 0


def test_delete_notebooks_delete_different_user(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook2"})

    response = client.delete("/delete-notebook?uid=1&notebook=notebook2")
    response = client.delete("/delete-notebook?uid=2&notebook=notebook1")

    with app.app_context():
        assert users.query.count() == 2
        assert notebooks.query.count() == 2


# UPDATE endpoints

def test_update_notebooks(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})


    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook2","notebook_id":"1"})
        
    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notebooks.query.filter_by(user_id=1, name="notebook2").first() != None


def test_update_notebooks_same_name(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})

    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook2","notebook_id":"1"})
    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook2","notebook_id":"1"})
    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook2","notebook_id":"1"})

    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notebooks.query.filter_by(user_id=1, name="notebook2").first() != None


def test_update_notebooks_different_names(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})

    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook2","notebook_id":"1"})
    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook3","notebook_id":"1"})
    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook4","notebook_id":"1"})

    with app.app_context():
        assert users.query.count() == 1
        assert notebooks.query.count() == 1
        assert notebooks.query.filter_by(user_id=1, name="notebook2").first() == None
        assert notebooks.query.filter_by(user_id=1, name="notebook2").first() == None
        assert notebooks.query.filter_by(user_id=1, name="notebook4").first() != None


def test_update_notebooks_multiple_people_same_person(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook1"})

    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook2","notebook_id":"1"})
    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook3","notebook_id":"1"})
    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook4","notebook_id":"1"})

    with app.app_context():
        assert users.query.count() == 2
        assert notebooks.query.count() == 2
        assert notebooks.query.filter_by(user_id=1, name="notebook2").first() == None
        assert notebooks.query.filter_by(user_id=1, name="notebook3").first() == None
        assert notebooks.query.filter_by(user_id=1, name="notebook4").first() != None


def test_update_notebooks_multiple_people_multiple_persons(client, app):
    # first create user and create notebook(s)
    client.post("/register-user", json={"uid":"1"})
    client.post("/register-user", json={"uid":"2"})
    client.post("/post-notebook", json={"uid":"1", "notebook":"notebook1"})
    client.post("/post-notebook", json={"uid":"2", "notebook":"notebook1"})

    response = client.post("/update-notebook", json={"uid":"1", "notebook":"notebook2","notebook_id":"1"})
    response = client.post("/update-notebook", json={"uid":"2", "notebook":"notebook3","notebook_id":"2"})

    with app.app_context():
        assert users.query.count() == 2
        assert users.query.filter_by(user_id=1).first()._id == 1
        assert users.query.filter_by(user_id=2).first()._id == 2
        assert notebooks.query.count() == 2
        assert notebooks.query.filter_by(user_id=1, name="notebook3").first() == None
        assert notebooks.query.filter_by(user_id=2, name="notebook2").first() == None
        assert notebooks.query.filter_by(user_id=1, name="notebook1").first() == None
        assert notebooks.query.filter_by(user_id=2, name="notebook1").first() == None
        assert notebooks.query.filter_by(user_id=1, name="notebook2").first() != None
        assert notebooks.query.filter_by(user_id=2, name="notebook3").first() != None
