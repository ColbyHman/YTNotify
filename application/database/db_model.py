"""Module to interact with a database"""
import db_wrapper as db

def add_channel(channel_info):
    """Adds a channel"""
    db.add_entry_to_collection("channels", channel_info)

def update_channel(search, channel_info):
    """Updates a channel"""
    db.update_entry_in_collection("channels", search, channel_info)

def remove_channel(channel_info):
    """Removes a channel"""
    db.remove_entry_from_collection("channels", channel_info)

def list_channel_info(channel_info):
    """Lists the info for a channel"""
    return db.search_collection("channels", channel_info)[0]

def list_channels():
    """Lists out all channels"""
    return db.search_collection("channels", {})

def add_discord_server(server_info):
    """Adds a discord server"""
    db.add_entry_to_collection("discord_servers", server_info)

def remove_discord_server(server_info):
    """Removes a discord server"""
    db.remove_entry_from_collection("discord_servers", server_info)

def update_discord_server(query, server_info):
    """Updates a discord server"""
    db.update_entry_in_collection("discord_servers", query, server_info)

def list_server_info(server_info):
    """Lists discord server info"""
    return db.search_collection("discord_servers", server_info)[0]

def list_servers():
    """Lists all discord servers"""
    return db.search_collection("discord_servers", {})
