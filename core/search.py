import pymongo
from pymongo import MongoClient
from core.structs import IdToDocTrait


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
            add_document_to_document_search method in the app.py.
            It then saves the document in our MongoDB collection (idToDoc),
            and returns the inserted id.
            The function performs the following steps:
                - receives a document (str) input from the 
                    add_document_to_document_search in the `app.py`
                - activates a connection to the idToDoc collection where the
                    document will be saved
                - creates a document_data by type matching the idToDocTrait
                    imported from the core.structs
                - inserts the document in the collection
                - returns the inserted id
            Args:
                document : str - a string sent from the add_document_to_document_search
                    with the intention of adding to our search system / corpus.
            Returns
                Str: the document id (inserted id) returned as a string
        """
        conn = self.db.IdToDoc
        # collection_count = conn.count_documents(filter={})
        document_data: IdToDocTrait = {
            "document": document
        }
        result = conn.insert_one(document_data)
        return str(result.inserted_id)


    def add_word_to_id(self, document_search_graph, word, id):
        self.document_search_graph = document_search_graph

        document_id = document['id']
        words = document.lower().split(" ")
        
        for word in words:
            self.document_search_graph[word].append(document_id)

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