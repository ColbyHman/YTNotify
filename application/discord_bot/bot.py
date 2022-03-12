"""Discord Bot Module"""
import os
import discord
from dotenv import load_dotenv
import controller

client = discord.Client()

@client.event
async def on_ready():
    """Prints to console that Bot has connected to Discord"""
    print('I have logged in!')

@client.event
async def on_guild_join(guild):
    """Prints to console that Bot has joined a server and adds server to DB"""
    print(f'I have logged into {guild.id}')
    first_channel = guild.text_channels[0]
    print(first_channel.name)
    await a_send_message(first_channel,
f'Hello! Thank you for using YTNotify. By default, I will be sending messages in **{first_channel.name}**')
    await a_send_message(first_channel,
'If you would like to change this, please use the command: &channel *channel_name*')

    controller.add_server(guild.id, first_channel)

@client.event
async def on_guild_remove(guild):
    """Prints to console that Bot has been removed from a server and removes it from DB"""
    print(f'I have been removed from {guild.id}')
    controller.remove_server(guild.id)

async def send_message(channel, message):
    """Sends message to specific channel in a guild"""
    await channel.send(message)

def get_guild_channel(guild_id, channel_name):
    """Returns the channel object of a guild"""
    guild = client.get_guild(guild_id)
    if guild is None:
        return guild
    for channel in guild.text_channels:
        if channel.name == channel_name:
            return channel
    return None
async def a_send_message(channel, message):
    """Sends message to specific channel in a guild"""
    await channel.send(message)

async def a_get_guild_channel(guild_id, channel_id):
    """Returns the channel object of a guild"""
    guild = client.get_guild(guild_id)
    guild_channel = guild.get_channel(channel_id)
    return guild_channel

@client.event
async def on_message(message):
    """Handles bot commands"""
    guild_id = message.guild.id
    msg = message.content
    channel = message.channel
    if message.content.startswith('&list'):
        await a_send_message(channel, controller.list_server_info(guild_id))
    if message.content.startswith('&add'):
        if msg.split(" ")[1] is not None:
            await a_send_message(channel, controller.add_channel(guild_id, msg.split(" ")[1]))
        else:
            await a_send_message(channel, "Invalid Command")
    if message.content.startswith('&remove'):
        if msg.split(" ")[1] is not None:
            await a_send_message(channel, controller.remove_channel(guild_id, msg.split(" ")[1]))
        else:
            await a_send_message(channel, "Invalid Command")
    if message.content.startswith('&latest'):
        if msg.split(" ")[1] is not None:
            await a_send_message(channel, controller.display_channel_info(guild_id, msg.split(" ")[1]))
        else:
            await a_send_message(channel, "Invalid Command")
    if message.content.startswith('&update'):
        await a_send_message(channel, controller.update_channels())
    if message.content.startswith('&channel'):
        if msg.split(" ")[1] is not None:
            await a_send_message(channel, controller.update_discord_channel(guild_id, msg.split(" ")[1]))
        else:
            await a_send_message(channel, "Invalid Command")
    if message.content.startswith('&ping'):
        await a_send_message(channel, "Pong")
    if message.content.startswith('&help'):
        await a_send_message(channel, """```
1. Add a YouTube Channel to your server's list:
    &add <YouTube Channel Videos Page Link> i.e. &add https://www.youtube.com/c/YTNotify/videos
2. List your server's YouTube Channel subs: &list
3. Remove a channel from your server's YouTube Channel list:
    &remove <numbered index or channel shortname> i.e. &remove 1 OR &remove YTNotify
4. Update channel list manually: &update
5. View latest video from a YouTube Channel:
    &latest i.e. &latest <numbered index or channel shortname> i.e. &latest 1 OR &latest YTNotify
```""")

def main():
    """Main Function"""
    load_dotenv('/app/aplication/config/.env')
    discord_secret = os.getenv('DISCORD_TOKEN')
    client.run(discord_secret)

if __name__ == '__main__':
    main()
