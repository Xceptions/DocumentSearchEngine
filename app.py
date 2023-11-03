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
        Returns a map (dict) of 'result':document_id entry.
        The function receives a document (a string) from the client.
        It then passes it to the save method of the DocumentSearch
        class, with the expectation of the document (our term) being
        saved as a document (mongodb term) to our MongoDB collection,
        with an expected return value of a document id.
        The function performs the following steps:
            - checks if the request method is a POST
            - receives the document string from the request object
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
            Dict: a map/dict[str,bool] with 'result' as key and document list as value.
                This document_list value is the response gotten from the save_document
                method of the DocumentSearch class
    """
    if request.method == 'POST':
        document = request.get_json()['document']
        document_id, db_conn, document_list = DocumentSearch(
                                                app.config["MONGO_URI"]
                                            ).save_document(
                                                document
                                            )

        if not document_id:
            return jsonify({'status': "unable to save document"})

        response = DocumentSearch( app.config["MONGO_URI"] ).save_words(
                                                                document, 
                                                                document_id,
                                                                db_conn
                                                            )
        return jsonify({'result': document_list})


@app.route('/search', methods=['POST'])
def search_for_documents_containing_term():
    """ 
        Returns a map (dict) of 'result':document_list.

        document(str) -> input received from user to store in db
        document(MongoDB) ->  the standard mongodb document

        The function receives a document (a string) from the client.
        It then passes it to the search_for_word method of the
        DocumentSearch class, with the expectation of the document(str)
        being saved as a document(MongoDB) to our MongoDB collection,
        with an expected return value of all documents that contain the
        term in our DB as a list.
        The function performs the following steps:
            - checks if the request method is a POST
            - receives the document string from the request object
            - passes it to the search_for_word method of the DocumentSearch
                class of which, if successful, will return a list of the
                documents(MongoDB) that contain the word
            - it returns these documents as a json object to the front end
        Args (retrieved via the POST method):
            document : str - a string sent from the user with the intention of
                adding to our search system / corpus. This argument is gotten
                from the request object itself, via the request.get_json() method
                of the flask api.
        Returns
            Dict: a map/dict[str,bool] with 'result' as key and response as value.
                This response is the document_list gotten from the search_for_words
                method of the DocumentSearch class
    """
    if request.method == 'POST':
        user_input = request.get_json()['document']
        response = DocumentSearch( app.config["MONGO_URI"] ).search_for_word( user_input )
        return jsonify({'result': response})


@app.route('/delete', methods=['POST'])
def delete_document():
    """ 
        Returns a map (dict) of [str, List[str]]

        document(str) -> input received from user to store in db
        document(MongoDB) ->  the standard mongodb document

        The function receives a document (a string) from the client.
        It then passes it to the delete method of the
        DocumentSearch class, with the expectation of the document(MongoDB)
        that contains the document(str) being from our MongoDB collection,
        with an expected return value of all documents in our DB as a
        list.
        The function performs the following steps:
            - checks if the request method is a POST
            - receives the document string from the request object
            - passes it to the delete method of the DocumentSearch
                class of which, if successful, will return a list of all
                the documents(MongoDB) in the DB
            - it returns these documents as a json object to the front end
        Args (retrieved via the POST method):
            document : str - a string sent from the user with the intention of
                deleting from our DB. This argument is gotten
                from the request object itself, via the request.get_json() method
                of the flask api.
        Returns
            Dict: a map/dict[str,List[str]] with 'result' as key and response as value.
                This response is the document_list gotten from the delete
                method of the DocumentSearch class
    """
    if request.method == 'POST':
        data = request.get_json()['document']
        response = DocumentSearch( app.config["MONGO_URI"] ).delete(data)
        return jsonify({'result': response})


@app.route('/dropdb')
def drop_db():
    """ 
        Returns a map (dict) of [str, str]

        This function drops both collections from the db
        The function performs the following steps:
            - receives the request from the client
            - calls the drop method of the DocumentSearch
                class of which, if successful, will drop the WordToId and IdToDoc
                collections, and returns
            - it returns these documents as a json object to the client
        Args:
            None
        Returns
            Dict: a map/dict[str,List[str]] with 'result' as key and response as value.
                This response is the status of dropping the two collections from the db
    """
    response = DocumentSearch( app.config["MONGO_URI"] ).drop_db()
    print(response)
    return jsonify({'result': response})


def answer_question():
    if request.method == 'POST':
        # how does this work
        # what languages and technologies rest in the backend
        # does it cache any request
        # What are additional ways to go about this
        #   - 
        user_input = request.get_json()['document']
        response = DocumentSearch( app.config["MONGO_URI"] ).delete( user_input )
        return jsonify({'result': response})


if __name__ == "__main__":
    app.run()