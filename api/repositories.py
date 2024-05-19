from django.conf import settings
import pymongo
import uuid
from django.contrib.auth.hashers import make_password, check_password

class WeatherRepository:
    def __init__(self, collection_name) -> None:
        self.collection = collection_name

    def get_connection(self):
        client = pymongo.MongoClient(getattr(settings, "MONGO_CONNECTION_STRING"))
        connection = client[getattr(settings, "MONGO_DATABASE_NAME")]
        return connection

    def get_collection(self):
        conn = self.get_connection()
        collection = conn[self.collection]
        return collection

    def get_all(self):
        documents = self.get_collection().find({}).sort("date", -1)
        return documents

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
            _id = document.pop('_id')
            document['id'] = str(_id)
            documents.append(document)
        return documents

class AuthRepository:
    collection = 'users'

    def __init__(self):
        # Ensure unique index on email
        self.get_collection().create_index("email", unique=True)

    def get_connection(self):
        client = pymongo.MongoClient(getattr(settings, "MONGO_CONNECTION_STRING"))
        connection = client[getattr(settings, "MONGO_DATABASE_NAME")]
        return connection

    def get_collection(self):
        conn = self.get_connection()
        collection = conn[self.collection]
        return collection

    def create_user(self, username, email, password):
        hashed_password = make_password(password)
        data = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "password": hashed_password
        }
        self.get_collection().insert_one(data)
        return data

    def get_user(self, email):
        user = self.get_collection().find_one({"email": email})
        return user

    def verify_credentials(self, email, password):
        user = self.get_user(email)
        if user and check_password(password, user['password']):
            return user
        return None
