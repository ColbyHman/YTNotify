import db_wrapper as db

## Add channel
def add_channel(channel_name, video_info):
    db.add("channels", channel_name, video_info)

## Remove channel
def remove_channel(channel_name):
    db.remove("channels", channel_name)

def list_channel_info(channel_name):
    return db.list_field("channels", channel_name)

## List channels
def list_channels():
    return db.list_hash("channels")

## Add discord server
def add_discord_server(server_id, subs):
    db.add("discord_servers", server_id, subs)

def remove_discord_server(server_id):
    db.remove("discord_servers", server_id)

## Add channel to server subs
def add_channel_to_server_subs(server_id, channel_id):
    db.add("discord_servers", server_id, channel_id)

## Remove channel from server subs
def remove_channel_from_server_subs(server_id, channel_id):
    db.remove_field("discord_servers", server_id, channel_id)

## List server subs
def list_server_subs(server_id):
    return db.list_field("discord_servers", server_id)
