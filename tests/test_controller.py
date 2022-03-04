from calendar import c
import os
import sys
import pytest
from tests import mock_discord
from mock_discord import MockDiscord

sys.path.append('application/discord_bot')
sys.path.append('application/database')
import controller
import db_model as db
import db_wrapper as wrapper

@pytest.fixture(scope="function")
def setup():
    wrapper.remove_all_entries_from_collection("discord_servers")
    wrapper.remove_all_entries_from_collection("channels")

def test_validate_channel():
    channel_channel = controller.validate_channel("https://www.youtube.com/channel/test/videos")
    channel_user = controller.validate_channel("https://www.youtube.com/user/test/videos")
    channel_c = controller.validate_channel("https://www.youtube.com/c/test/videos")
    assert channel_channel == "test" and channel_user == "test" and channel_c == "test"

def test_build_video_url():
    url = controller.build_video_url("test")
    assert url == "https://www.youtube.com/watch?v=test"

def test_download_webpage():
    filename = controller.download_webpage("test","https://www.youtube.com/c/LinusTechTips/videos")
    page = ""
    with open(filename, "rt",encoding="utf8") as infile:
        for line in infile:
            page += line
    infile.close()
    os.remove(filename)
    assert page != ""

def test_find_video_titles():
    filename = controller.download_webpage("test","https://www.youtube.com/c/LinusTechTips/videos")
    page = ""
    with open(filename, "rt",encoding="utf8") as infile:
        for line in infile:
            page += line
        titles = controller.find_video_titles(page)
    infile.close()
    os.remove(filename)
    assert len(titles) != 0

def test_find_video_ids():
    filename = controller.download_webpage("test","https://www.youtube.com/c/LinusTechTips/videos")
    page = ""
    with open(filename, "rt",encoding="utf8") as infile:
        for line in infile:
            page += line
        ids = controller.find_video_ids(page)
    infile.close()
    os.remove(filename)
    assert len(ids) != 0

def test_find_video_dates():
    filename = controller.download_webpage("test","https://www.youtube.com/c/LinusTechTips/videos")
    page = ""
    with open(filename, "rt",encoding="utf8") as infile:
        for line in infile:
            page += line
        dates = controller.find_video_dates(page)
    infile.close()
    os.remove(filename)
    assert len(dates) != 0

def test_build_channel_json():
    json = controller.build_channel_json("name","id","title","today","link","updated")
    assert json == '{"name": "name", "video_id": "id", "title": "title", "date": "today", "link": "link", "last_updated": "updated"}'

def test_json_to_dict():
    json = '{"name": "name", "video_id": "id", "title": "title", "date": "today", "link": "link", "last_updated": "updated"}'
    json = controller.json_to_dict(json)
    assert json["name"] == "name"

def test_add_channel_to_server():
    mock_server = MockDiscord("test","channel")
    controller.add_server("test",mock_server)
    query, server_info = controller.add_channel_to_server("test","testChannel")
    db.remove_discord_server({"server_id":"test"})
    assert query is not None and server_info is not None

def test_add_channel():
    mock_server = MockDiscord("test","channel")
    controller.add_server("test",mock_server)
    response = controller.add_channel("test","https://www.youtube.com/c/LinusTechTips/videos")
    db.remove_discord_server({"server_id":"test"})
    db.remove_channel({"name":"LinusTechTips"})
    assert response == "LinusTechTips has been added!"

def test_add_server():
    try:
        mock_server = MockDiscord("test", "channel")
        controller.add_server("test", mock_server)
        db.remove_discord_server({"server_id":"test"})
    except Exception as exec:
        assert False, exec

def test_remove_channel():
    mock_server = MockDiscord("test", "channel")
    controller.add_server("test", mock_server)
    controller.add_channel("test", "https://www.youtube.com/c/LinusTechTips/videos")
    try:
        controller.remove_channel("test", "LinusTechTips")
        list_subs = db.list_server_info({"server_id":"test"})['subs']
        subs = [x for x in list_subs]
        db.remove_channel({"name":"LinusTechTips"})
        db.remove_discord_server({"server_id":"test"})
        assert len(subs) == 0
    except Exception as exec:
        assert False, exec
