from dotenv import load_dotenv
import os
from pymongo import MongoClient
from urllib.parse import quote

class Connect(object):
    @staticmethod    
    def get_connection():
        load_dotenv()
        user = os.getenv("MONGODB_USER")
        pw = quote(os.getenv("MONGODB_PW"))
        return MongoClient(f"mongodb://{user}:{pw}@localhost:27017/?authSource=ytnotify")