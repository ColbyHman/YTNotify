"""Module to automatically update channels in DB"""
from datetime import datetime, timedelta
import controller

import discord
from bot import a_send_message as send_message
import os
from dotenv import load_dotenv
from discord.ext import tasks
import db_model as db
import controller

load_dotenv()
discord_secret = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@tasks.loop(minutes=30)
async def auto_notify_guilds():
    refresh()
    channels = db.list_channels()
    servers = db.list_servers()
    updated_channels = []
    for channel in channels:
        name = channel["name"]
        last_updated = datetime.strptime(channel["last_updated"],"%Y-%m-%dT%H:%M")
        if (datetime.now() - last_updated < timedelta(minutes=30)):
            updated_channels.append(name)
    
    for server in servers:
        subs = server["subs"]
        server_id = server["server_id"]
        channel = server['channel']
        for sub in subs:
            if sub in updated_channels:
                send_message(controller.display_channel_info(server_id, sub))

def refresh():
    """Calls update_channels in DB"""
    controller.update_channels()
    print(f"Channels have been updated at {datetime.now()}")

@client.event
async def on_ready():
    auto_notify_guilds.start()
    print("Logged in and connected...")

client.run(discord_secret)

