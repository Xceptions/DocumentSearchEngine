import pymongo
from pymongo import MongoClient, UpdateOne, InsertOne
from core.structs import IdToDocStruct, WordToIdStruct


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
        return (
            str(result.inserted_id),
            self.db
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
                - receives a document(str), document_id, and db_conn input from
                    the add_document_to_db in the `app.py`
                - converts the document(str) to a list of lowercase words called `words`
                - uses the db_conn to retrieve the documents(MongoDB) that
                    contains any word in `words`
                - creates a set (word_set) of the words in `words` to be used for O(1)
                    comparison
                - loops through the documents(MongoDB) and appends the document_id
                    to the ids field of any word present in `words` and prepares it for
                    an update while removing the word from word_set
                - at the end of the loop, all words left in `words` will be the new words 
                    that are not present in the document(MongoDB)
                - loop through the word_set again and prepare these words for an insert
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
            document[ids].append(document_id)
            data_to_insert: WordToIdStruct = {
                "document_type": "word_to_id",
                "word": document[word],
                "ids": document[ids]
            }
            bulk_write_operations.append(
                updateOne({
                    "filter": { "word": data_to_insert.word },
                    "update": { "$set": {"ids": [ data_to_insert.ids ]} },
                    "upsert": True
                })
            )
            word_set.remove(document[word])

        for word in word_set:
            bulk_write_operations.append(
                InsertOne({
                    "document": {
                        "document_type": 'word_to_id',
                        "word": word,
                        "ids": [document_id]
                    }
                })
            )
        result = db_conn.WordToId.bulk_write(bulk_write_operations)
        return result.acknowledged

    def search(self, search_string):
        all_occurrences = []
        search_string = search_string.split(" ")

        for string in search_string:
            if string in self.document_search_graph:
                all_occurrences.append(self.document_search_graph[string])
        print(f'all_occurrences is {all_occurrences}')
        
        result_id = set().union(*all_occurrences)
        print(f'result_id is {result_id}')
        
        return result_id or []

    def delete(self, word):
        # this is not the add to filter function. This is the
        # main delete that gets called once in a month
        pass