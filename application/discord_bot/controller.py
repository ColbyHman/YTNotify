"""Controller Module for the Discord Bot"""
import json
import re
import sys
from datetime import datetime
import requests
sys.path.append('/app/application/database')
import db_model as db


def validate_channel(channel_link):
    """Takes in channel link, validates the format, and returns the channel code and 'channel_text' flag"""
    if "videos" in channel_link:
        if "/channel/" in channel_link:
            channel_name = re.search("channel/(.+)/", channel_link)
            if channel_name:
                return channel_name.group(1)
        if "/user/" in channel_link:
            channel_name = re.search("user/(.+)/", channel_link)
            if channel_name:
                return channel_name.group(1)
        if "/c/" in channel_link:
            channel_name = re.search("c/(.+)/", channel_link)
            if channel_name:
                return channel_name.group(1)
        return None
    return None

def build_video_url(video_id):
    """Returns a video URL given the video ID"""
    return f"https://www.youtube.com/watch?v={video_id}"

def download_webpage(channel_name, channel_link):
    """Downloads a webpage and saves it to an HTML file. Returns filename"""
    filename = channel_name + ".html"
    request = requests.get(channel_link, allow_redirects=True)
    with open(filename, "wb") as infile:
        infile.write(request.content)
    return filename

def parse_html_file(filename):
    """Parses a given HTML file"""
    with open(filename, "rt", encoding="utf8") as infile:
        page = ""
        for line in infile:
            page += line
        infile.close()
        return page

def find_video_titles(page):
    """Finds the titles for YouTube videos"""
    titles = []
    video_page = re.finditer('{"text":".{0,100}"}],', page)
    if video_page:
        for video in video_page:
            vidtitle = re.search(':".{0,100}"', video[0])
            titles += [vidtitle[0][2:-1]]
    if len(titles) == 0:
        video_page = re.finditer('{"simpleText":".{0,100}"}{1},"v', page)
        if video_page:
            for video in video_page:
                vidtitle = re.search(':".{0,100}"', video[0]).group(1)
                print(vidtitle)
                titles += [vidtitle[0][2:-1]]
            return titles
        return None
    return titles

def find_video_ids(page):
    """Finds the video IDs for YouTube videos"""
    ids = []
    video_page = re.finditer('"videoId":"(.{0,20})","', page)
    if video_page:
        for video_id in video_page:
            ids += [video_id.group(1)]
    return ids

def find_video_dates(page):
    """Finds the dates for YouTube videos"""
    dates = []
    video_page = re.finditer('"publishedTimeText":{"simpleText":"(.{0,20})"},"', page)
    if video_page:
        for video_date in video_page:
            dates += [video_date.group(1)]
    return dates

def build_channel_json(name,video_id, title, date, link, last_updated):
    """Builds the JSON payload for a YouTube channel"""
    channel_info = {"name":name,
                    "video_id":video_id,
                    "title":title,
                    "date":date,
                    "link":link,
                    "last_updated":last_updated
                    }
    return json.dumps(channel_info)

def json_to_dict(json_str):
    """Converts a JSON payload to a dictionary"""
    if json_str is not None:
        return json.loads(json_str)
    return {}

def add_channel_to_server(server_id, channel_to_add):
    """Adds a channel to the existing server object and returns the new payload"""
    query = {"server_id":server_id}
    server_info = db.list_server_info(query)

    subs = server_info["subs"]
    if channel_to_add not in subs:
        subs.append(channel_to_add)
        server_info['subs'] = subs
        return query, server_info
    return None, None

def add_channel(server_id, channel_link):
    """Adds a YouTube channel to a server's subscriptions"""
    channel_name, video, title, date = get_channel_info(channel_link)
    now = str(datetime.now().isoformat(timespec="minutes"))
    channel_info = {"name":channel_name,
                    "video_id":video,
                    "title":title,
                    "date":date,
                    "link":channel_link,
                    "last_updated":now
                    }
    channels = list_channels()
    channel_exists = False

    if channel_name is None:
        return "Invalid Link"
    for channel in channels:
        if channel_name == channel["name"]:
            channel_exists = True

    if not channel_exists:
        db.add_channel(channel_info)

    query, server_info = add_channel_to_server(server_id, channel_name)
    if server_info is None:
        return "Channel already exists!"

    db.update_discord_server(query, server_info)
    return f"{channel_name} has been added!"

def add_server(server_id, channel):
    """Adds a Discord server to the DB"""
    db.add_discord_server({
        "server_id":server_id,
        "channel":channel.name,
        "subs":[]
    })

def remove_channel(server_id, channel_name):
    """Removes a YouTube channel from a server's subscriptions"""
    query = {"server_id":server_id}
    server_info = db.list_server_info(query)
    subs = server_info["subs"]
    if channel_name.isdigit():
        channel_name = str(int(channel_name)-1)
        subs.pop(channel_name)
    else:
        subs.remove(channel_name)
    server_info["subs"] = subs
    db.update_discord_server(query, server_info)
    return f"{channel_name} has been removed from your server's subscriptions"

def remove_server(server_id):
    """Removes a given server from the DB"""
    db.remove_discord_server({"server_id":server_id})

def update_channels():
    """Updates all channels within the DB"""
    channels = list_channels()
    updated_channels = []
    for channel in channels:
        current_id = channel['video_id']
        channel_link = channel["link"]
        channel_name , video_id, title, date = get_channel_info(channel_link)
        if current_id == video_id:
            break
        now = str(datetime.now().isoformat(timespec="minutes"))
        query = {"name":channel_name}
        channel_info = {"name":channel_name,
                    "video_id":video_id,
                    "title":title,
                    "date":date,
                    "link":channel_link,
                    "last_updated":now
                    }
        db.update_channel(query,channel_info)
        updated_channels.append(channel_name)
    print("Channels updated: ", updated_channels)
    return "Channels have been updated!"

def update_discord_channel(server_id, channel):
    """Updates a discord server's channel preference"""
    query = {"server_id":server_id}
    server_info = db.list_server_info(query)
    server_info['channel'] = channel
    db.update_discord_server(query, server_info)
    return f"I will now send channel updates to **#{channel}**"

def list_channels():
    """Returns a list of all channels in a server"""
    return db.list_channels()

def display_channel_info(server_id, channel_name):
    """Returns a print friendly version of a YouTube channel's info from a discord server"""
    if channel_name.isdigit():
        channel_name = int(channel_name) - 1
        channels = db.list_server_info({"server_id":server_id})["subs"]
        channel_name = channels[channel_name]
        print(channel_name)
    if not channel_name:
        return "That channel does not exist. Check &list for your subscriptions"
    channel = db.list_channel_info({"name":channel_name})
    url = build_video_url(channel['video_id'])
    return f"> ***{channel['title']}***\n> {url}\n> `{channel['date']}`"

def list_server_info(server_id):
    """Returns the list of server subscriptions"""
    server_info = db.list_server_info({"server_id":server_id})
    subs = server_info["subs"]
    count = 1
    if len(subs) == 0:
        return "You have no server subscriptions!"
    output = "**Here are your server subscriptions:**\n"
    for sub in subs:
        output += f"> ``{count}. {sub} ``\n"
        count+=1
    return output

def get_channel_info(channel_link):
    """Returns the information of a channel from a given link"""
    channel_name = validate_channel(channel_link)
    if channel_name:
        filename = download_webpage(channel_name, channel_link)
        page = parse_html_file(filename)
        videos = find_video_titles(page)
        video_ids = find_video_ids(page)
        dates = find_video_dates(page)
        if page is None or len(videos) == 0 or len(video_ids) == 0 or len(dates) == 0:
            return None, None, None, None
        return channel_name, video_ids[0], videos[0], dates[0]
    return None, None, None, None
