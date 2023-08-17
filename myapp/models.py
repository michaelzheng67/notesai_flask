from .extensions import db 

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Text)
    notebook = db.relationship('notebooks', backref='user')
    temperature = db.Column(db.Float)
    similarity = db.Column(db.Integer)
    wordcount = db.Column(db.Integer)

    def __init__(self, user_id, temperature, similarity, wordcount):
        self.user_id = user_id
        self.temperature = temperature
        self.similarity = similarity
        self.wordcount = wordcount


class notebooks(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Text)
    notes = db.relationship('notes', backref='notebook', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class notes(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.id'), nullable=False)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    base64_string = db.Column(db.String, nullable=False)
    chroma_parts = db.Column(db.Integer)

    def __init__(self, notebook_id, title, content, base64_string):
        self.notebook_id = notebook_id
        self.title = title
        self.content = content
        self.base64_string = base64_string # store freestyle image
