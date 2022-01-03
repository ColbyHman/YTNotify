"""Module to interact with a database"""
import db_wrapper as db

def add_channel(channel_name, video_info):
    """Adds a channel to the "channels" hash """
    db.add("channels", channel_name, video_info)

def remove_channel(channel_name):
    """Removes a channel from the "channels" hash"""
    db.remove("channels", channel_name)

def list_channel_info(channel_name):
    """Lists the info for a channel"""
    return db.list_field("channels", channel_name)

def list_channels():
    """Lists out all channels in the "channels" hash"""
    return db.list_hash("channels")

def add_discord_server(server_id, subs):
    """Adds a discord server to the "discord_servers" hash"""
    db.add("discord_servers", server_id, subs)

def remove_discord_server(server_id):
    """Removes a discord server from the "discord_servers" hash"""
    db.remove("discord_servers", server_id)

def add_channel_to_server_subs(server_id, channel_id):
    """Adds a channel to a discord server"""
    db.add("discord_servers", server_id, channel_id)

def remove_channel_from_server_subs(server_id, channel_id):
    """Removes a channel from a discord server"""
    db.remove_field("discord_servers", server_id, channel_id)

def list_server_subs(server_id):
    """Lists all the channels within a discord server"""
    return db.list_field("discord_servers", server_id)
