import pytest
import sys
sys.path.append('application/database')
import db_wrapper as wrapper


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

@pytest.fixture(scope="function")
def setup():
    wrapper.remove_all_entries_from_collection("discord_servers")
    wrapper.remove_all_entries_from_collection("channels")

def test_list_collections(setup):
    collections = wrapper.list_collections()
    assert "discord_servers" in collections and "channels" in collections

def test_get_collections(setup):
    ds_collection = wrapper.get_collection("discord_servers")
    c_collection = wrapper.get_collection("channels")
    assert ds_collection.name == "discord_servers" and c_collection.name == "channels"

def test_add_entry_to_collection(setup):
    try:
        wrapper.add_entry_to_collection("channels",test_entry)
        query = wrapper.search_collection_for_one("channels",{"name":"testChannel"})
        assert query["name"] == "testChannel"
    except Exception as exec:
        assert False, exec
    wrapper.remove_entry_from_collection("channels",test_entry)

def test_remove_entry_from_collection(setup):
    wrapper.add_entry_to_collection("channels",test_entry)
    try:
        wrapper.remove_entry_from_collection("channels",test_entry)
        query = wrapper.search_collection_for_one("channels",{"name":"testChannel"})
        assert query is None
    except Exception as exec:
        assert False, exec

def test_search_collection(setup):
    wrapper.add_entry_to_collection("channels",test_entry)
    try:
        query = wrapper.search_collection("channels", {"name":"testChannel"})
        wrapper.remove_entry_from_collection("channels",test_entry)
        assert query is not None
    except Exception as exec:
        assert False, exec

def test_search_collection_for_one(setup):
    wrapper.add_entry_to_collection("channels",test_entry)
    try:
        query = wrapper.search_collection_for_one("channels", {"name":"testChannel"})
        wrapper.remove_entry_from_collection("channels",{"name":"testChannel"})
        assert query["name"] == "testChannel"
    except Exception as exec:
        assert False, exec

def test_update_entry_in_collection(setup):
    wrapper.add_entry_to_collection("channels",test_entry)
    try:
        wrapper.update_entry_in_collection("channels", {"name":"testChannel"}, test_entry_updated)
        query = wrapper.search_collection_for_one("channels", {"name":"testChannelUpdated"})
        wrapper.remove_entry_from_collection("channels",{"name":"testChannelUpdated"})
        assert query["name"] == "testChannelUpdated"
    except Exception as exec:
        assert False, exec