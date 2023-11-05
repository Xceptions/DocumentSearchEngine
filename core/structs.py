from typing import List, TypedDict

"""
Defines the structs of the documents in each collection in our MongoDB

There are three collections in our DB
    - save_document: a collection for storing documents with a unique id
    - word_to_id: A ReverseIndex collection for storing words to id
    - deleted_documents: a collection that holds the ids of deleted documents. \
        It will be used to filter responses to the client
"""

class IdToDocStruct(TypedDict):
    document_type: str = "id_to_doc"
    _id: str
    document: str


class WordToIdStruct(TypedDict):
    document_type: str = "word_to_id"
    _id: str
    word: str
    ids: List[str]
    

# structs_deleted_documents = {
#     "type":string = "deleted_documents",
#     "values":List = []
# }