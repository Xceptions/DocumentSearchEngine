import pymongo
from pymongo import MongoClient
from core.traits import IdToDocTrait


class DocumentSearch:

    def __init__(self, conn:str):
        """
        Establishes a connection to the database using the
        connection string that is received from the client
        """
        self.connection = MongoClient(conn)
        self.db = self.connection.DocumentSearchDB

    def save_document(self, document:str) -> int:
        """
        Establishes a connection to the collection IdToDoc
        - Counts the number of items in the collection. This will be useful for adding \
            new documents in the collection and new words in the word_to_id collection
        - Insert the document in the collection using the trait trait_id_to_doc
        - Return the count
        """
        conn = self.db.IdToDoc
        # collection_count = conn.count_documents(filter={})
        document_data: IdToDocTrait = {
            "document": document
        }
        result = conn.insert_one(document_data)
        return result.inserted_id


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