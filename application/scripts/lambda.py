"""Module to automatically update channels in DB"""
import sys
import os
from datetime import datetime, timedelta
import discord
from dotenv import load_dotenv
from discord.ext import tasks

sys.path.append('/app/application/database')
sys.path.append('/app/application/discord_bot')

import db_model as db
import controller
import bot

load_dotenv('../config/.env')
discord_secret = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@tasks.loop(minutes=30)
async def auto_notify_guilds():
    """Notifies guilds of new videos"""
    refresh()
    channels = db.list_channels()
    servers = db.list_servers()
    updated_channels = []
    for channel in channels:
        name = channel["name"]
        last_updated = datetime.strptime(channel["last_updated"],"%Y-%m-%dT%H:%M")
        if datetime.now() - last_updated < timedelta(minutes=30):
            updated_channels.append(name)
    for server in servers:
        subs = server["subs"]
        server_id = server["server_id"]
        guild = client.get_guild(server_id)
        channel_name = server['channel']
        for channel in guild.text_channels:
            if channel.name == channel_name:
                channel_obj = channel
                break
        for sub in subs:
            if sub in updated_channels:
                await bot.send_message(channel_obj,
                controller.display_channel_info(server_id, sub))

def refresh():
    """Calls update_channels in DB"""
    controller.update_channels()
    print(f"Channels have been updated at {datetime.now()}")

@client.event
async def on_ready():
    """Runs when bot is logged in and ready"""
    auto_notify_guilds.start()
    print("Logged in and connected...")

client.run(discord_secret)
