import sys
sys.path.append('application/database')
import db_wrapper as db

test_entry = {"name":"testChannel",
            "video_id":"video",
            "title":"title",
            "date":"date",
            "link":"channel_link",
            "last_updated":"now"
            }

test_entry_updated = {"name":"testChannelUpdated",
                    "video_id":"video",
                    "title":"title",
                    "date":"date",
                    "link":"channel_link",
                    "last_updated":"now"
                    }

def test_list_collections():
    collections = db.list_collections()
    assert "discord_servers" in collections and "channels" in collections

def test_get_collections():
    ds_collection = db.get_collection("discord_servers")
    c_collection = db.get_collection("channels")
    assert ds_collection.name == "discord_servers" and c_collection.name == "channels"

def test_add_entry_to_collection():
    try:
        db.add_entry_to_collection("channels",test_entry)
        query = db.search_collection_for_one("channels",{"name":"testChannel"})
        assert query["name"] == "testChannel"
    except Exception as exec:
        assert False, exec
    db.remove_entry_from_collection("channels",test_entry)

def test_remove_entry_from_collection():
    db.add_entry_to_collection("channels",test_entry)
    try:
        db.remove_entry_from_collection("channels",test_entry)
        query = db.search_collection_for_one("channels",{"name":"testChannel"})
        assert query is None
    except Exception as exec:
        assert False, exec

def test_search_collection():
    db.add_entry_to_collection("channels",test_entry)
    try:
        query = db.search_collection("channels", {"name":"testChannel"})
        db.remove_entry_from_collection("channels",test_entry)
        assert query is not None
    except Exception as exec:
        assert False, exec

def test_search_collection_for_one():
    db.add_entry_to_collection("channels",test_entry)
    try:
        query = db.search_collection_for_one("channels", {"name":"testChannel"})
        db.remove_entry_from_collection("channels",test_entry)
        assert query["name"] == "testChannel"
    except Exception as exec:
        assert False, exec

def test_update_entry_in_collection():
    db.add_entry_to_collection("channels",test_entry)
    try:
        db.update_entry_in_collection("channels", {"name":"testChannel"}, test_entry_updated)
        query = db.search_collection_for_one("channels", {"name":"testChannelUpdated"})
        db.remove_entry_from_collection("channels",test_entry)
        assert query["name"] == "testChannelUpdated"
    except Exception as exec:
        assert False, exec