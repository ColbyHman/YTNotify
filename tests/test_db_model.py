import pytest
import sys
sys.path.append('application/database')
import db_model as db
import db_wrapper as wrapper

test_channel = {"name":"testChannel",
            "video_id":"video",
            "title":"title",
            "date":"date",
            "link":"channel_link",
            "last_updated":"now"
            }

test_channel_updated = {"name":"testChannelUpdated",
            "video_id":"video",
            "title":"title",
            "date":"date",
            "link":"channel_link",
            "last_updated":"now"
            }

test_server = {"server_id": "123456789",
                "subs" : ["testChannel"]}

test_server_updated = {"server_id": "123456789",
                "subs" : ["testChannel","testChannel2"]}

@pytest.fixture()
def setup():
    wrapper.remove_all_entries_from_collection("discord_servers")
    wrapper.remove_all_entries_from_collection("channels")

def test_add_channel():
    try:
        db.add_channel(test_channel)
        db.remove_channel(test_channel)
    except Exception as exec:
        assert False, exec

def test_update_channel():
    db.add_channel(test_channel)
    try:
        db.update_channel({"name":"testChannel"},test_channel_updated)
        query = db.list_channel_info({"name":"testChannelUpdated"})
        db.remove_channel({"name":"testChannelUpdated"})
        assert query is not None
    except Exception as exec:
        assert False, exec

def test_remove_channel():
    db.add_channel(test_channel)
    try:
        db.remove_channel(test_channel)
        search = db.list_channels()
        search = [_ for _ in search]
        assert search == []
    except Exception as exec:
        assert False, exec

def test_list_channel_info():
    db.add_channel(test_channel)
    query = db.list_channel_info({"name": "testChannel"})
    db.remove_channel({"name": "testChannel"})
    assert query["name"] == "testChannel"
    pass

def test_list_channels():
    db.add_channel(test_channel)
    db.remove_channel(test_channel)
    pass

def test_add_discord_server():
    try:
        db.add_discord_server(test_server)
        query = db.list_server_info({"server_id": "123456789"})
        db.remove_discord_server({"server_id": "123456789"})
        assert query["server_id"] == "123456789"
    except Exception as exec:
        assert False, exec

def test_remove_discord_server():
    try:
        db.add_discord_server(test_server)
        db.remove_discord_server({"server_id": "123456789"})
        search = db.list_servers()
        search = [x for x in search]
        assert len(search) == 0
    except Exception as exec:
        assert False, exec

def test_update_discord_server():
    try:
        db.add_discord_server(test_server)
        db.update_discord_server({"server_id": "123456789"}, test_server_updated)
        query = db.list_server_info({"server_id": "123456789"})
        db.remove_discord_server({"server_id": "123456789"})
        assert query is not None
    except Exception as exec:
        assert False, exec

def test_list_server_info():
    db.add_discord_server(test_server)
    query = db.list_server_info({"server_id": "123456789"})
    db.remove_discord_server({"server_id": "123456789"})
    assert query["server_id"] == "123456789"

def test_list_servers():
    db.add_discord_server(test_server)
    db.add_discord_server(test_server_updated)
    list = db.list_servers()
    search = [x for x in list]
    db.remove_discord_server({"subs": ["testChannel"]})
    db.remove_discord_server({"subs": ["testChannel","testChannel2"]})
    assert search[0]['subs'] == ["testChannel"] and search[1]['subs'] == ["testChannel","testChannel2"]