"""MongoDB Wrapper"""
from mongo import Connect

client = Connect.get_connection()
db = client.ytnotify

def list_collections():
    """Returns a list of collections in a database"""
    return db.list_collection_names()

def get_collection(collection_name):
    """Retrieve a collection if it exists. Returns None if non-existent"""
    if collection_name in list_collections():
        return db[collection_name]
    return None

def add_entry_to_collection(collection_name, entry):
    """Adds entry to an existing collection """
    collection = get_collection(collection_name)
    if collection != None:
        collection.insert_one(entry)
    else:
        print("Collection does not exist!")

def search_collection(collection_name, query):
    """Searches an existing collection"""
    collection = get_collection(collection_name)
    if collection != None:
        return collection.find(query)
    return None

def remove_entry_from_collection(collection_name, query):
    """Removes an entry from an existing collection"""
    collection = get_collection(collection_name)
    if collection != None:
        collection.delete_one(query)

def update_entry_in_collection(collection_name, search, query):
    """Updates an entry in an existing collection"""
    collection = get_collection(collection_name)
    if collection != None:
        collection.update_one(search, {"$set":query})
