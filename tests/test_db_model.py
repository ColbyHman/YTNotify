import sys
sys.path.append('application/database')
import db_model as db

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
        db.remove_channel(test_channel_updated)
        assert query is not None
    except Exception as exec:
        assert False, exec

def test_remove_channel():
    db.add_channel(test_channel)
    try:
        db.remove_channel(test_channel)
        assert db.list_channels() is None
    except Exception as exec:
        assert False, exec

def test_list_channel_info():
    db.add_channel(test_channel)
    db.remove_channel(test_channel)
    pass

def test_list_channels():
    db.add_channel(test_channel)
    db.remove_channel(test_channel)
    pass

def test_add_discord_server():
    try:
        db.add_discord_server(test_server)
    except Exception as exec:
        assert False, exec

def test_remove_discord_server():
    try:
        db.add_discord_server(test_server)
    except Exception as exec:
        assert False, exec

def test_update_discord_server():
    try:
        db.add_discord_server(test_server)
    except Exception as exec:
        assert False, exec

def test_list_server_info():
    db.add_discord_server(test_server)
    pass

def test_list_servers():
    db.add_discord_server(test_server)
    pass