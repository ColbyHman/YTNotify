"""MongoDB Wrapper"""
import os
from mongo import Connect
from dotenv import load_dotenv

env = os.getenv("ENVIRONMENT")
DB = None

if not env:
    load_dotenv("../application/config/.env")
    env = os.getenv("ENVIRONMENT")
if env:
    DB = Connect.get_connection(env)
else:
    raise Exception("Database Not Connected - Environment Variable is not set")

def list_collections():
    """Returns a list of collections in a database"""
    return DB.list_collection_names()

def get_collection(collection_name):
    """Retrieve a collection if it exists. Returns None if non-existent"""
    if collection_name in list_collections():
        return DB[collection_name]
    return None

def add_entry_to_collection(collection_name, entry):
    """Adds entry to an existing collection """
    collection = get_collection(collection_name)
    if collection is not None:
        try:
            collection.insert_one(entry)
        except:
            raise Exception("Unable to add entry to collection")
    else:
        raise Exception("Collection does not exist!")

def search_collection(collection_name, query):
    """Searches an existing collection"""
    collection = get_collection(collection_name)
    if collection is not None:
        try:
            return collection.find(query)
        except:
            raise Exception("Item not found")
    return None

def search_collection_for_one(collection_name, query):
    """Searches an existing collection"""
    collection = get_collection(collection_name)
    if collection is not None:
        return collection.find_one(query)
    return None

def remove_entry_from_collection(collection_name, query):
    """Removes an entry from an existing collection"""
    collection = get_collection(collection_name)
    if collection is not None:
        try:
            collection.delete_one(query)
        except:
            raise Exception("Unable to remove entry from collection")
    else:
        raise Exception("Collection does not exist!")

def update_entry_in_collection(collection_name, search, query):
    """Updates an entry in an existing collection"""
    collection = get_collection(collection_name)
    if collection is not None:
        try:
            collection.update_one(search, {"$set":query})
        except:
            raise Exception("Unable to update entry")
    else:
        raise Exception("Collection does not exist!")

def remove_all_entries_from_collection(collection_name):
    collection = get_collection(collection_name)
    if collection is not None:
        try:
            collection.delete_many({})
            print(f"Cleared the {collection_name} collection!")
        except:
            raise Exception(f"Could not clear the {collection_name} collection!")
    else:
        raise Exception("Collection does not exist!")