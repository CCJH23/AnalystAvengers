from flask_pymongo import pymongo
import os

CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('testdb')
user_collection = pymongo.collection.Collection(db, 'test_collection')
