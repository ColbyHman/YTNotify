"""Connection class for MongoDB instance"""

from urllib.parse import quote
import os
from dotenv import load_dotenv
from pymongo import MongoClient

class Connect():
    """Connection class for MongoDB instance"""
    @staticmethod
    def get_connection(environment):
        """Returns connection string for MongoDB instance"""
        user = os.getenv("MONGODB_USER")
        db_pw = os.getenv("MONGODB_PW")
        db = None
        try:
            db_pw = quote(db_pw)
        except TypeError:
            print("MONGODB_PW Environment Variable not set")
        server = os.getenv("MONGO_INSTANCE_NAME")
        client = MongoClient(f"mongodb://{user}:{db_pw}@{server}:27017/?authSource=ytnotify")

        if environment == "test":
            db = client.test
        if environment == "dev":
            db = client.ytnotify
        if environment == "prod":
            db = client.ytnotify
        return db
