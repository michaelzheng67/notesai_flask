from flask import Flask

from .extensions import db
from .models import users, notebooks, notes

from flask import Flask, request, jsonify
import json
import os
import shutil
from flask_sqlalchemy import SQLAlchemy

# import
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain import PromptTemplate

app = Flask(__name__)

# Centralized endpoints that allow for storage as well as calls to langchain / openAI

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# POST endpoint when user logs in, makes sure that they have an existing account
@app.route("/register-user", methods=["POST"])
def register_user():
    uid = request.json["uid"]

    user = users.query.filter_by(user_id=uid).first()
    # create user if doesn't exist
    if user is None:
        new_user = users(uid, 0.2, 1, 50)
        db.session.add(new_user)
        db.session.commit()
        return "User is new. Created new profile"
    
    return "Existing user"

# GET endpoint for all documents of a notebook. Specify notebook
@app.route("/get", methods=["GET"])
def get_documents():
    uid = request.args.get('uid')
    notebook_name = request.args.get('notebook')

    user = users.query.filter_by(user_id=uid).first()

    notebook_obj = notebooks.query.filter_by(user_id=user._id, name=notebook_name).first()

    # If notebook is not found, return an error message
    if notebook_obj is None:
        return jsonify({'error': 'Notebook not found'})

    # Extract notes and convert them to dictionaries
    notes_list = []
    for note in notebook_obj.notes:
        notes_list.append({
            'title': note.title,
            'content': note.content,
            'base64String' : note.base64_string
        })


    # Return the notes as a JSON object
    return json.dumps(notes_list)


# UPDATE endpoint for new documents. Specify notebook and note title / content
@app.route("/update", methods=["POST"])
def update_document():
    uid = request.json["uid"]
    title = request.json["title"]
    content = request.json["content"]
    notebook = request.json["notebook"]
    base64String = request.json["base64String"]

    user = users.query.filter_by(user_id=uid).first()

    # create notebook if it doesn't exist
    notebook_obj = notebooks.query.filter_by(user_id=user._id, name=notebook).first()

    # chromaDB variables
    docs = None
    documents = None
    text_splitter = CharacterTextSplitter()
    ids = None

    if not notebook_obj:
        notebook_obj = notebooks(user_id=user._id, name=notebook)
        db.session.add(notebook_obj)


    # check if note with the given title already exists in the notebook
    existing_note = notes.query.filter_by(notebook_id=notebook_obj._id, title=title).first()

    # UPDATE
    if existing_note:
        # update in ChromaDB

        # get old data in Document form
        curr_doc = Document(page_content=existing_note.content)
        documents = [curr_doc]
        docs = text_splitter.split_documents(documents)
        old_ids = [existing_note.title + str(i) for i in range(1, len(docs) + 1)]


        # update the existing note's content
        existing_note.content = content
        existing_note.base64_string = base64String

        # insert into ChromaDB
        # turn text content into Document form
        curr_doc = Document(page_content=existing_note.content)
        documents = [curr_doc]
        docs = text_splitter.split_documents(documents)
        new_ids = [title + str(i) for i in range(1, len(docs) + 1)]

        # delete old data then add new data to ChromaDB
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        chroma_db = Chroma(embedding_function= embedding_function, persist_directory="./chromadb")
        chroma_db._collection.delete(ids=old_ids)
        chroma_db = Chroma.from_documents(docs, embedding_function, persist_directory="./chromadb", ids=new_ids)
        chroma_db.persist()

        existing_note.chroma_parts = len(docs)

        db.session.add(existing_note)
        db.session.commit()

        return "Success!"

    
# POST endpoint for new documents. Specify notebook and note title / content
@app.route("/post", methods=["POST"])
def post_document():
    uid = request.json["uid"]
    title = request.json["title"]
    content = request.json["content"]
    notebook = request.json["notebook"]
    base64String = request.json["base64String"]

    user = users.query.filter_by(user_id=uid).first()

    # create notebook if it doesn't exist
    notebook_obj = notebooks.query.filter_by(user_id=user._id, name=notebook).first()

    # chromaDB variables
    docs = None
    documents = None
    text_splitter = CharacterTextSplitter()
    ids = None

    if not notebook_obj:
        notebook_obj = notebooks(user_id=user._id, name=notebook)
        db.session.add(notebook_obj)


    # check if note with the given title already exists in the notebook
    existing_note = notes.query.filter_by(notebook_id=notebook_obj._id, title=title).first()


    # POST
    # create note and insert into notebook
    note = notes(notebook_id=notebook_obj._id, title=title, content=content, base64_string=base64String)

    # add to ChromaDB

    # turn text content into Document form
    curr_doc = Document(page_content=note.content)
    documents = [curr_doc]
    docs = text_splitter.split_documents(documents)
    ids = [title + str(i) for i in range(1, len(docs) + 1)]

    # actually add to ChromaDB instance
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    chroma_db = Chroma.from_documents(docs, embedding_function, persist_directory="./chromadb", ids=ids)
    chroma_db.persist()

    # update variable in note object
    note.chroma_parts = len(docs)

    db.session.add(note)
    
    db.session.commit()

    return "success!"


# DELETE endpoint for existing documents. Specify notebook and note title
@app.route('/delete', methods=['DELETE'])
def delete_document():
    uid = request.args.get('uid')
    notebook = request.args.get('notebook')  # Get notebook from query string
    title = request.args.get('title')   

    user = users.query.filter_by(user_id=uid).first()

    notebook_obj = notebooks.query.filter_by(user_id=user._id, name=notebook).first()

    if notebook_obj is None:
        return jsonify({'error': 'Notebook not found'})

    # Retrieve the note by title within the notebook
    note_obj = notes.query.filter_by(notebook_id=notebook_obj._id, title=title).first()

    if note_obj is None:
        print("Note not found")
        print(notebook_obj._id)
        print(title)
        return jsonify({'error': 'Note not found'})

    # Delete the note
    # get old data in Document form
    curr_doc = Document(page_content=note_obj.content)
    documents = [curr_doc]
    text_splitter = CharacterTextSplitter()
    docs = text_splitter.split_documents(documents)
    old_ids = [note_obj.title + str(i) for i in range(1, len(docs) + 1)]

    # delete from chroma
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    chroma_db = Chroma(embedding_function= embedding_function, persist_directory="./chromadb")
    chroma_db._collection.delete(ids=old_ids)
    chroma_db.persist()

    db.session.delete(note_obj)
    db.session.commit()

    return jsonify({'message': 'Note and notebook deleted successfully'})


# GET endpoint for notebooks
@app.route("/get-notebooks/<uid>")
def get_notebooks(uid):
    
    # REPLACE WITH AUTH ID
    # createTestDummy()
    # user = users.query.get(1)
    user = users.query.filter_by(user_id=uid).first()
        

    notebooks_list = []
    if user.notebook:
        for notebook in user.notebook:
            notebooks_list.append({
                'label' : notebook.name
            })

    return json.dumps(notebooks_list)
    


# POST endpoint for a given notebook
@app.route("/post-notebook", methods=["POST"])
def post_notebook():
    uid = request.json["uid"]
    notebook = request.json["notebook"]

    user = users.query.filter_by(user_id=uid).first()

    if user is None:
        print('User not found')  # Or handle this situation differently, e.g., return an error response
    
    else:
        new_notebook = notebooks(name=notebook)
        new_notebook.user = user
    
        db.session.add(new_notebook)
        db.session.commit()

    return "success!"


# DELETE endpoint for a given notebook
@app.route('/delete-notebook', methods=['DELETE'])
def delete_notebook():
    uid = request.args.get('uid')
    notebook = request.args.get('notebook') 
    
    user = users.query.filter_by(user_id=uid).first()

    # Check if the user is found
    if user is None:
        print("User not found") # Handle this as needed
    else:
        # Get the notebook by title and user
        notebook_to_delete = notebooks.query.filter_by(user_id=user._id, name=notebook).first()

        # Check if the notebook is found
        if notebook_to_delete is None:
            print("Notebook not found") # Handle this as needed
        else:
            # Delete the notebook
            db.session.delete(notebook_to_delete)
            db.session.commit()

    return jsonify({'message': 'Note and notebook deleted successfully'})


# GET endpoint for OpenAI query (Making this a post request so we can send a long string in the body if necessary)
# FOR FUTURE: separate the chromadb from this request. This may involve storing it in a database
@app.route('/query', methods=['POST'])
def query():
    uid = request.json["uid"]
    query_string = request.json["query_string"]
    notebook = request.json["notebook"]

    user = users.query.filter_by(user_id=uid).first()


    # query on it
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./chromadb", embedding_function=embedding_function)
    docs = db.similarity_search(query_string, k=int(user.similarity))

    temp_str = "summarize the following in " + str(user.wordcount) + " words or less: "
    PROMPT = PromptTemplate.from_template(template=temp_str + "{text}")

    
    llm = OpenAI(temperature=float(user.temperature)) # PLACE THIS SOMEWHERE ELSE
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
    return_output = chain.run(docs)


    return jsonify(result=return_output)



# GET endpoint for Langchain advanced settings (customize how the backend works)
@app.route('/get-settings/<uid>', methods=['GET'])
def get_settings(uid):

    # REPLACE WITH AUTH ID
    user = users.query.filter_by(user_id=uid).first()


    return jsonify({'temperature' : round(float(user.temperature), 2),
                    'similarity' : int(user.similarity),
                    'wordcount' : int(user.wordcount)
                    })


# POST endpoint for Langchain advanced settings (customize how the backend works)
@app.route('/post-settings', methods=['POST'])
def post_settings():
    uid = request.json["uid"]
    temperature = round(float(request.json["temperature"]), 2)
    similarity = int(request.json["similarity"])
    wordcount = int(request.json["wordcount"])

    user = users.query.filter_by(user_id=uid).first()
    
    user.temperature = temperature
    user.similarity = similarity
    user.wordcount = wordcount

    db.session.commit()

    return "Success"