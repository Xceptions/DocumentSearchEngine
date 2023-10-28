from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_index_html_template():
    """standard implenetation of Flask render template"""
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_document_to_document_search():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({'document': data['document']})


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