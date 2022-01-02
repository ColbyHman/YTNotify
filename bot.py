"""Discord Bot Module"""
import os
import discord
from dotenv import load_dotenv
import controller

load_dotenv()

client = discord.Client()
discord_secret = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    """Prints to console that Bot has connected to Discord"""
    print('We have logged in as {client}')

@client.event
async def on_guild_join(guild):
    """Prints to console that Bot has joined a server and adds server to DB"""
    print('I have logged into {guild.id}')
    controller.add_server(guild.id)

@client.event
async def on_guild_remove(guild):
    """Prints to console that Bot has been removed from a server and removes it from DB"""
    print('I have been removed from {guild.id}')
    controller.remove_server(guild.id)

@client.event
async def on_message(message):
    """Handles bot commands"""
    guild_id = message.guild.id
    msg = message.content
    if message.content.startswith('&list'):
        await message.channel.send(controller.list_server_info(guild_id))
    if message.content.startswith('&add'):
        await message.channel.send(controller.add_channel(guild_id, msg.split(" ")[1]))
    if message.content.startswith('&remove'):
        await message.channel.send(controller.remove_channel(guild_id, msg.split(" ")[1]))
    if message.content.startswith('&latest'):
        await message.channel.send(controller.display_channel_info(guild_id, msg.split(" ")[1]))
    if message.content.startswith('&update'):
        await message.channel.send(controller.update_channels())
    if message.content.startswith('&ping'):
        await message.channel.send("Pong")
    if message.content.startswith('&help'):
        await message.channel.send("""```
        \n1. Add a YouTube Channel to your server's list:\n
            \t&add <YouTube Channel Videos Page Link> i.e. &add https://www.youtube.com/c/YTNotify/videos\n
        2. List your server's YouTube Channel subs: &list\n
        3. Remove a channel from your server's YouTube Channel list:\n
            \t&remove <numbered index or channel shortname> i.e. &remove 1 OR &remove YTNotify\n
        4. Update channel list manually: &update\n
        5. View latest video from a YouTube Channel:\n
            \t&latest i.e. &latest <numbered index or channel shortname> i.e. &latest 1 OR &latest YTNotify
        ```""")

client.run(discord_secret)
