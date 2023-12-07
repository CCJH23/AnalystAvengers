from flask_pymongo import pymongo

CONNECTION_STRING = "mongodb+srv://clovischowjh:analystavengersforever@cluster0.qx0lb1j.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('testdb')
user_collection = pymongo.collection.Collection(db, 'test_collection')

