import pymongo
from pymongo import MongoClient, UpdateOne, InsertOne
from bson.objectid import ObjectId
from core.structs import IdToDocStruct, WordToIdStruct

from typing import List


class DocumentSearch:

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

    def save_document(self, document:str) -> str:
        """ 
            Returns the document id of the inserted document.
            The function receives a document (a string) from the
            add_document_to_db method in the app.py.
            It then saves the document in our MongoDB collection (idToDoc),
            and returns the inserted id.
            The function performs the following steps:
                - receives a document (str) input from the 
                    add_document_to_db in the `app.py`
                - activates a connection to the idToDoc collection where the
                    document will be saved
                - creates a document_data by type matching the idToDocStruct
                    imported from the core.structs
                - inserts the document in the collection
                - returns the inserted id
            Args:
                document(str) - a string sent from the add_document_to_db
                    with the intention of adding to our search system / corpus.
            Returns
                Str: the document id (inserted id) returned as a string
        """
        conn = self.db.IdToDoc
        document_data: IdToDocStruct = {
            "document_type": "id_to_doc",
            "document": document
        }
        result = conn.insert_one(document_data)
        all_documents = conn.find()
        documents_list = [doc['document'] for doc in all_documents]
        return (
            str(result.inserted_id),
            self.db,
            documents_list
        )


    def save_words(
                self,
                document: str,
                document_id: str,
                db_conn: MongoClient
            ) -> bool:
        """ 
            Returns the status of the inserted/updated document.

            document(str) -> input received from user to store in db
            document(MongoDB) ->  the standard mongodb document

            The function receives a document(str), a document_id(str),
            and a db_conn(MongoDB) from the add_document_to_db
            method in the app.py. It then saves the document(str) in our
            MongoDB collection (WordToId), and returns the operation status.
            The function performs the following steps:
                - receives a document(str), document_id, and db_conn input
                    from the add_document_to_db in the `app.py`
                - converts the document(str) to a list of lowercase words
                    called `words`
                - uses the db_conn to retrieve the documents(MongoDB) that
                    contains any word in `words`
                - creates a set (word_set) of the words in `words` to be used
                    for O(1) comparison
                - loops through the documents(MongoDB) and appends the document_id
                    to the ids field of any word present in `words` and prepares
                    it for an update while removing the word from word_set
                - at the end of the loop, all words left in `words` will be the
                    new words that are not present in the document(MongoDB)
                - loop through the word_set again and prepare these words for
                    an insert
                - bulkWrite the insert and update operations.
                - Return the bulkWrite status
            Args:
                document : str - a string sent from the client
                    with the intention of adding to our search system / corpus.
                document_id : str - the id of the document gotten from insertion
                    of the document(str) into the idToDoc collection
                db_conn: MongoDB.db - the database connection to a collection
            Returns
                Bool: the status of the insert/update bulkWrite operation
        """

        bulk_write_operations = []
        words = document.lower().split(" ")
        word_set = set(words)
        collection = db_conn.WordToId.find(
            { "word": { "$in": words } }
        )
        for document in collection:
            document["ids"].append(document_id)
            data_to_update: WordToIdStruct = {
                "document_type": "word_to_id",
                "word": document["word"],
                "ids": document["ids"]
            }
            bulk_write_operations.append(
                UpdateOne(
                    { "word": data_to_update["word"] },
                    { "$set": {
                        "ids": data_to_update["ids"] + [document_id]
                        }
                    }
                )
            )
            word_set.remove(document["word"])

        for word in word_set:
            data_to_insert: WordToIdStruct = {
                "document_type": "word_to_id",
                "word": word,
                "ids": document_id
            }
            bulk_write_operations.append(
                InsertOne({
                    "document_type": 'word_to_id',
                    "word": word,
                    "ids": [document_id]
                })
            )
        result = db_conn.WordToId.bulk_write(bulk_write_operations)
        return result.acknowledged

    def search_for_word(self, user_input: str) -> List[str]:
        """ 
            Returns a list of the strings that contain the searched word.
            The function receives a user_input (a string) from the
            add_document_to_db method in the app.py.
            It then retrieves the documents in our DB collection (WordToId),
            containing that word, gets their corresponding ids and returns
            the document (from IdToDoc) using the ids.
            The function performs the following steps:
                - receives a user input (str) from the 
                    add_document_to_db in the `app.py`
                - creates an all_occurrence list to hold a list of the ids
                    that contain the words in user_input
                - splits the user_input into a list of lowercase words called
                    `words` for searching the db
                - retrieves a collection of documents containing words in `words`
                    from the WordToId collection
                - for all the documents in the collection above, it extends their
                    `ids` field into the all_occurrence. This `ids` field is a
                    a list containing the _id of the documents that contain these
                    words
                - creates an `all_occurrence_id` to convert the all_occurrence
                    List[str] to List[ObjectId(str)]. This is needed because that
                    is the datatype stored in the MongoDB collection
                - retrieves a collection of documents containing ObjectId(ids) in
                    `all_occurrence_ids`
                - returns a list of document(str) contained in documents(MongoDB)
                    above or empty list
            Args:
                user_input(str) - a string sent from the add_document_to_db
                    with the intention of searching our DB for it.
            Returns
                List[str]: a list of the documents that contain the words in user_input
        """

        all_occurrences = []
        words = user_input.lower().split(" ")

        collection = self.db.WordToId.find(
            { "word": { "$in": words } }
        )
        for doc in collection:
            all_occurrences.extend(doc['ids'])

        all_occurrences_id = [ObjectId(id) for id in set(all_occurrences)]

        collection = self.db.IdToDoc.find(
            { "_id": { "$in": all_occurrences_id } }
        )
        result = [doc['document'] for doc in collection]

        return result or []


    def delete(self, user_input: str):
        result = self.db.IdToDoc.delete_many({"document": user_input})
        print(result)
        conn = self.db.IdToDoc
        all_documents = conn.find()
        documents_list = [doc['document'] for doc in all_documents]
        return (
            str(result),
            documents_list
        )

    def clear_db(self):
        """
        Returns the status of dropping both collections in the db
        Args:
            None
        Returns
            Dict[str, str]: the status of dropping the collections
        """
        drop_IdToDoc = self.db.drop_collection("IdToDoc")
        drop_WordToId = self.db.drop_collection("WordToId")
        return drop_IdToDoc and drop_WordToId
        