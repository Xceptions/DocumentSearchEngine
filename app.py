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
        A more sophisticated template should be built to go
        with the software, but feel free to test with this
    """
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_document_to_document_search():
    """ Returns a map (dict) of 'document_id':document_id entry.
        The function receives a document (a string) from the client.
        It then passes it to the save method of the DocumentSearch
        class, with the expectation of the document (our term) being
        saved as a document (mongodb term) to our MongoDB collection,
        with an expected return value of a document id.
        The function performs the following steps:
            - aggregates the text elements in the batch_item_texts
            - produces an offset map for each word in the aggregated text, where
                each word begins and ends
            - uses the tokenizer to produce tokens, token attension masks, and
                token offsets (where each token begins and and ends in the
                corresponding aggregated item text)
            - prepares the input tensor for the respective tokenizer output
            - applies the model (calling forwad funciton) and produces the
                model's output tensor
            - extracts the aspect name:value from the model's output tensor using
                the private function _extract_aspects
        Args:
            document (str): a string sent from the user with the intention of
                adding to our search system / corpus. This argument is gotten
                from the request object itself, via the request.get_json() method
                of the flask api. This document string is what is passed to the
                DocumentSearch class, expecting a string as return value
        Returns
            Dict: a map/dict[str,str] with 'document_id' as key and document_id as value.
                This document_id value is the string gotten from the save_document
                method of the DocumentSearch class
    """
    if request.method == 'POST':
        document = request.get_json()['document']
        document_id = DocumentSearch( app.config["MONGO_URI"] ).save_document( document )
        print(document_id)
        return jsonify({'document_id': str(document_id)})


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