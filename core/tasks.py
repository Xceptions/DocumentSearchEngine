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
    return DocumentSearch( mongo_uri ).save_document(
                                            document,
                                            document_id['$oid']
                                        )

@celery.task
def call_save_words(mongo_uri, document, document_id):
    return DocumentSearch( mongo_uri ).save_words(
                                            document,
                                            document_id['$oid']
                                        )
# @celery.task()
# def call_save_word():
#     return DocumentSearch( app.config["MONGO_URI"] ).save_words( document )

# def call_search_for_word():
#     passed

# def call_delete():
#     passed

# def call_