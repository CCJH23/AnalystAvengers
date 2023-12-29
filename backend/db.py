from flask_pymongo import pymongo
import os
import certifi

CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
db = client.get_database('testdb')
user_collection = pymongo.collection.Collection(db, 'test_collection')
