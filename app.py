from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
# from flask_pymongo import PyMongo
from core.search import DocumentSearch
import json

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
# mongo = PyMongo(app)


@app.route('/')
def get_index_html_template():
    """ Standard implementation of Flask render template

        While the plan of the software is to be decoupled
        and work with any frontend, this is a roughly built
        frontend that helps to test the app.
    """
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_document_to_db():
    """ 
        Returns a map (dict) of 'document_id':document_id entry.
        The function receives a document (a string) from the client.
        It then passes it to the save method of the DocumentSearch
        class, with the expectation of the document (our term) being
        saved as a document (mongodb term) to our MongoDB collection,
        with an expected return value of a document id.
        The function performs the following steps:
            - checks if the request method is a POST
            - receives the document string from the front end
            - passes it to the save_document of the DocumentSearch class of
                which if successful, will return the document id, and the
                db_conn.
            - passes the document_id and db_conn to the save_words method of
                the same class.
            - retrieves the status of the save_words
        Args (retrieved via the POST method):
            document : str - a string sent from the user with the intention of
                adding to our search system / corpus. This argument is gotten
                from the request object itself, via the request.get_json() method
                of the flask api. This document string is what is passed to the
                DocumentSearch class, expecting a string as return value
        Returns
            Dict: a map/dict[str,bool] with 'save_status' as key and save status as value.
                This save status value is the response gotten from the save_words
                method of the DocumentSearch class
    """
    if request.method == 'POST':
        document = request.get_json()['document']
        document_id, db_conn = DocumentSearch( app.config["MONGO_URI"] ).save_document( document )

        if not document_id:
            return jsonify({'document_id': document_id})
        response = DocumentSearch(
                        app.config["MONGO_URI"]
                    ).save_words(
                            document, 
                            document_id,
                            db_conn
                        )

        return jsonify({'document_id': response})


@app.route('/search', methods=['POST'])
def search_for_documents_containing_term():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({'document': data['document']})


@app.route('/delete', methods=['POST'])
def delete_document():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({'document': data['document']})


if __name__ == "__main__":
    app.run()