"""Connection class for MongoDB instance"""

from urllib.parse import quote
import os
from pymongo import MongoClient

class Connect():
    """Connection class for MongoDB instance"""
    @staticmethod
    def get_connection(environment):
        """Returns connection string for MongoDB instance"""
        user = os.getenv("MONGODB_USER")
        db_pw = os.getenv("MONGODB_PW")
        database = None
        try:
            db_pw = quote(db_pw)
        except TypeError:
            print("MONGODB_PW Environment Variable not set")
        server = os.getenv("MONGO_INSTANCE_NAME")
        client = MongoClient(f"mongodb://{user}:{db_pw}@{server}/?authSource=ytnotify")

        if environment == "test":
            database = client.test
        if environment == "dev":
            database = client.ytnotify
        if environment == "prod":
            database = client.ytnotify
        return database
