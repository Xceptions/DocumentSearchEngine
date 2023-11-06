import pymongo
from pymongo import MongoClient
from core.structs import InfoStruct

from typing import List, Tuple


class Info:

    def __init__(self, conn:str):
        """
            Establishes a connection to the database using the
            connection string that is received from the client
            Args:
                conn : str - connection string to the mongodb
                        instance
            Attributes
                connection: MongoClient(str) - connection to the
                        mongodb instance
                db: MongoClient.DB - the connection to the database
        """
        self.connection = MongoClient(conn)
        self.db = self.connection.DocumentSearchDB
        self._initializedb_()


    def _initializedb_(self):
        """
            Checks if the collection already exists,
            creates one if it doesn't, and inserts the
            questions and their corresponding answers
        """
        # self.db.drop_collection("Info")
        if not self.db.Info.count_documents({}):
            self.db.Info.insert_many([
                {
                    "question": "how does this work?",
                    "answer": "It works on by assigning a document id to each document"
                },
                {
                    "question": "what languages and technologies rest in the backend?",
                    "answer": "Python, Flask, Celery, Javascript, HTML, CSS, MongoDB"
                },
                {
                    "question": "does it cache any request?",
                    "answer": "yes it does, like this one for example. Redis is our cache"
                },
                {
                    "question": "what are additional ways to go about this?",
                    "answer": "use react as the frontend"
                }
            ])

    def get_answer(self, question:str) -> str:
        """
            Returns the answer to the input `question`
            The function performs the following steps:
                - receives a user input (str) from the answer_question in
                    the `app.py`
                - searches the Info collection in the db for the document(MongoDB)
                    that contains the user input in its question field
                - during the query, it uses the self.db as the connection to the
                    db, and it takes a lower of the `question` to ensure consistency
                    irrespective of letter casing
                - retrieves the collection of the query
                - returns the answer field of the first document in the collection
                    This is because the document comes as a dict in a list
            Args:
                question : str - connection string to the mongodb
                        instance
            returns
                str: the `answer` key of the `question` in the 
                    document(MongoDB) that is the same as the input
                    question
        """
        document = self.db.Info.find({
            "question": question.lower()
        })
        result = document[0]["answer"]
        return result
