from app import app
# import requests
import json

def test_index_route():
    """
        Standard implementation of pytest
        get request
    """
    response = app.test_client().get('/')
    assert response.status_code == 200


def test_add_document_to_db():
    """
        Standard implementation of pytest
        post request
    """
    with app.test_client() as client:
        data = {
            "document": "new string in test"
        }

        response = client.post(
            "/add",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        assert(200, response.status_code)

def test_search_for_documents_containing_term():
    """
        Standard implementation of pytest
        post request
    """
    with app.test_client() as client:
        data = {
            "document": "random"
        }

        response = client.post(
            "/search",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        assert(200, response.status_code)


def test_delete():
    """
        Standard implementation of pytest
        post request
    """
    with app.test_client() as client:
        data = {
            "document": "random"
        }

        response = client.post(
            "/delete",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        assert(200, response.status_code)

def test_answer_question():
    """
        Standard implementation of pytest
        get request
    """
    with app.test_client() as client:

        response = client.get(
            '/answer/how does this work'
        )
        assert response.status_code == 200