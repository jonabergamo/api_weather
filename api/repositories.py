from django.conf import settings
import pymongo

class WeatherRepository:
    
    collection = ''
    
    def __init__(self, collectionName):
        self.collection = collectionName
        
    def getConnection(self):
        client = pymongo.MongoClient(
            getattr(settings, "MONGO_CONNECTION_STRING")
        )
        connection = client[getattr(settings, "MONGO_DATABASE_NAME")]
        return connection
        
        
    def getCollection(self):
        conn = self.getCollection()
        collection = conn[self.collection]
        return collection
    
    def getAll(self):
        data = self.getCollection().find({})
        return data
    
    def insert(self, document):
        self.getCollection().insert_one(document)