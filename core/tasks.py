from core.search import DocumentSearch
import time
from celery import Celery
from celery.utils.log import get_task_logger
from bson import ObjectId

logger = get_task_logger(__name__)

celery = Celery('tasks',
                broker='amqp://admin:mypass@rabbit:5672',
                backend='rpc://'
            )

@celery.task
def call_save_document(mongo_uri, document, document_id):
    """
        Returns as DocumentSearch instance
        This method simply asynchronously receives a request
        from the flask entry point and returns a DocumentSearch
        instance. It is the link between Flask, and search
        The function performs the following steps:
            - receives the mongo_uri string, document string, and
                document_id
            - returns a DocumentSearch instance using these three
                arguments
        Args:
            mongo_uri: str - connection string to the MongoDB instance
            document : str - a string sent from the flask app with the
                intention of saving to our DB.
            document_id:str - a string sent from the flask app with the
                intention of saving to our DB.
        Returns
            instance: DocumentSearch - a DocumentSearch instance that
                calls the save_document method.
    """
    return DocumentSearch( mongo_uri ).save_document(
                                            document,
                                            document_id['$oid']
                                        )

@celery.task
def call_save_words(mongo_uri, document, document_id):
    """
        Returns as DocumentSearch instance
        This method simply asynchronously receives a request
        from the flask entry point and returns a DocumentSearch
        instance. It is the link between Flask, and search
        The function performs the following steps:
            - receives the mongo_uri string, document string, and
                document_id
            - returns a DocumentSearch instance using these three
                arguments
        Args:
            mongo_uri: str - connection string to the MongoDB instance
            document : str - a string sent from the flask app with the
                intention of saving to our DB.
            document_id:str - a string sent from the flask app with the
                intention of saving to our DB.
        Returns
            instance: DocumentSearch - a DocumentSearch instance that
                calls the save_words method.
    """
    return DocumentSearch( mongo_uri ).save_words(
                                            document,
                                            document_id['$oid']
                                        )