from django.conf import settings
import pymongo

class WeatherRepository:
    
    collection = ''
    
    def __init__(self, collection_name) -> None:
        self.collection = collection_name
        
    def get_connection(self):
        client = pymongo.MongoClient(
            getattr(settings, "MONGO_CONNECTION_STRING"))
        connection = client[
            getattr(settings, "MONGO_DATABASE_NAME")]
        return connection
        
        
    def get_collection(self):
        conn = self.get()
        collection = conn[self.collection]
        return collection
    
    def get_all(self):
        document = self.getCollection().find({}).sort("date", -1)
        return document
    
    def insert(self, document):
        self.getCollection().insert_one(document)
        
    def drop_all(self):
        self.getCollection().drop()