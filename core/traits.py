from typing import List, TypedDict

"""
Defines the traits of the documents in each collection in our MongoDB

There are three collections in our DB
    - save_document: a collection for storing documents with a unique id
    - word_to_id: A ReverseIndex collection for storing words to id
    - deleted_documents: a collection that holds the ids of deleted documents. \
        It will be used to filter responses to the client
"""

class IdToDocTrait(TypedDict):
    document_type: str = "id_to_doc"
    document: str

# trait_id_to_doc: Dict[str, OneOrManyStrings] = {
#     "type":string = "id_to_doc",
#     "id":int,
#     "document":string
# }

# trait_word_to_id = {
#     "type":string = "word_to_id",
#     "word":string,
#     "ids":List = []
# }

# trait_deleted_documents = {
#     "type":string = "deleted_documents",
#     "values":List = []
# }