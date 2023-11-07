## Document Search System

**Optimal Search System for finding all documents containing search term**
![alt text](./images/DSdesign.png)

Tools:

1. Task-Queue distributed saving of documents using celery
2. RabbitMQ message broker
3. Request caching using redis
4. NoSQL for optimal querying of database (MongoDB)
5. Class-Based design
6. Backend Language: Python
7. Frontend Language: Vanilla JS

To run:

1. Clone the repo

```
git clone https://github.com/Xceptions/DocumentSearchEngine.git
```

2. Start the app

```
python3 app.py
```

3. Start celery

```
celery -A app.celery_app worker --loglevel=INFO
```

4. Run tests

```
cd tests

python3 -m pytest
```
