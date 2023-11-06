from typing import List, TypedDict

"""
Defines the structs of the documents in each collection in our MongoDB

There are two collections in our DB
    - IdToDocStruct: a collection for storing documents with a unique id
    - WordToIdStruct: A ReverseIndex collection for storing words to id
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
    

class InfoStruct(TypedDict):
    question: str
    answer: str