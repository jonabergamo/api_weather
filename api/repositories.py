from django.conf import settings
import pymongo
import uuid

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
        conn = self.get_connection()
        collection = conn[self.collection]
        return collection
    
    def get_all(self):
        document = self.get_collection().find({}).sort("date", -1)
        return document
    
    def insert(self, document):
        data = {
            "id": str(uuid.uuid4()),
            "temperature": document['temperature'],
            "date": document['date'],
            "atmospheric_pressure": document['atmospheric_pressure'],
            "humidity": document['humidity'],
            "city": document['city'],
            "weather": document['weather']
        }
        self.get_collection().insert_one(data)
        
    def drop_all(self):
        self.get_collection().drop()
        
    def update(self, query, data):
        self.get_collection().update_one({"id": query}, {"$set": data})

    def delete(self, query):
        self.get_collection().delete_one({"id": query})
    
    def get_by_id(self, id):
        document = self.get_collection().find_one({"id": id})
        return document

    def drop_by_id(self, id):
        self.get_collection().delete_one({"id": id})
        
        
    def get(self, filter):
        documents = []
        for document in self.get_collection().find(filter):
            id = document.pop('_id')
            document['id'] = str(id)
            documents.append(document)
        return documents