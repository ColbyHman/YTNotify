"""Module to interact with a database"""
import db_wrapper as db

def add_channel(channel_info):
    """Adds a channel"""
    try:
        db.add_entry_to_collection("channels", channel_info)
    except:
        raise Exception("Database Unavailable")

def update_channel(search, channel_info):
    """Updates a channel"""
    try:
        db.update_entry_in_collection("channels", search, channel_info)
    except:
        raise Exception("Database Unavailable")

def remove_channel(channel_info):
    """Removes a channel"""
    try:
        db.remove_entry_from_collection("channels", channel_info)
    except:
        raise Exception("Database Unavailable")

def list_channel_info(channel_info):
    """Lists the info for a channel"""
    try:
        return db.search_collection("channels", channel_info)
    except:
        raise Exception("Database Unavailable")

def list_channels():
    """Lists out all channels"""
    try:
        return db.search_collection("channels", {})
    except:
        raise Exception("Database Unavailable")

def add_discord_server(server_info):
    """Adds a discord server"""
    try:
        db.add_entry_to_collection("discord_servers", server_info)
    except:
        raise Exception("Database Unavailable")

def remove_discord_server(server_info):
    """Removes a discord server"""
    try:
        db.remove_entry_from_collection("discord_servers", server_info)
    except:
        raise Exception("Database Unavailable")

def update_discord_server(query, server_info):
    """Updates a discord server"""
    try:
        db.update_entry_in_collection("discord_servers", query, server_info)
    except:
        raise Exception("Database Unavailable")

def list_server_info(server_info):
    """Lists discord server info"""
    try:
        return db.search_collection("discord_servers", server_info)
    except:
        raise Exception("Database Unavailable")

def list_servers():
    """Lists all discord servers"""
    try:
        return db.search_collection("discord_servers", {})
    except:
        raise Exception("Database Unavailable")
        