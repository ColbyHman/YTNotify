import discord
from dotenv import load_dotenv
import os
import controller
import schedule

load_dotenv()

client = discord.Client()
discord_secret = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
    print('I have logged into {0.id}'.format(guild))
    controller.add_server(guild.id)

@client.event
async def on_guild_remove(guild):
    print('I have been removed from {0.id}'.format(guild))
    controller.remove_server(guild.id)

@client.event
async def on_message(message):
    if message.content.startswith('&list'):
        await message.channel.send(controller.list_server_info(message.guild.id))
    if message.content.startswith('&add'):
        await message.channel.send(controller.add_channel(message.guild.id, message.content.split(" ")[1]))
    if message.content.startswith('&remove'):
        await message.channel.send(controller.remove_channel(message.guild.id, message.content.split(" ")[1]))
    if message.content.startswith('&latest'):
        await message.channel.send(controller.display_channel_info(message.guild.id, message.content.split(" ")[1]))
    if message.content.startswith('&update'):
        await message.channel.send(controller.update_channels())
    if message.content.startswith('&ping'):
        await message.channel.send("Pong")
    if message.content.startswith('&help'):
        await message.channel.send("```\n1. Add a YouTube Channel to your server's list:\n\t&add <YouTube Channel Videos Page Link> i.e. &add https://www.youtube.com/c/YTNotify/videos\n2. List your server's YouTube Channel subs: &list\n3. Remove a channel from your server's YouTube Channel list:\n\t&remove <numbered index or channel shortname> i.e. &remove 1 OR &remove YTNotify\n4. Update channel list manually: &update\n5. View latest video from a YouTube Channel:\n\t&latest i.e. &latest <numbered index or channel shortname> i.e. &latest 1 OR &latest YTNotify```")

client.run(discord_secret)
