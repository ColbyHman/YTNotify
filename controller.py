import re
import requests
import json
import db_model as db

def validate_channel(channel_link):
    if ("/c/" in channel_link or "/user/" in channel_link) and "videos" in channel_link :
        channel_name = re.search("c/(.+)/videos", channel_link)
        if not channel_name:
            channel_name = re.search("user/(.+)/videos", channel_link)
        return channel_name.group(1)

def build_video_url(video_id):
    return "https://www.youtube.com/watch?v={0}".format(video_id)

def download_webpage(channel_name, channel_link):
    filename = channel_name + ".html"
    r = requests.get(channel_link, allow_redirects=True)
    open(filename, "wb").write(r.content)
    return filename

def parse_html_file(filename):
    infile = open(filename, "rt", encoding="utf8")
    page = ""
    for line in infile:
        page += line
    infile.close()
    return page

def find_video_titles(page):
    titles = []  
    video_page = re.finditer('{"text":".{0,100}"}\],', page)
    if(video_page):
        for video in video_page:
            vidtitle = re.search(':".{0,100}"', video[0])
            titles += [vidtitle[0][2:-1]]
    return titles

def find_video_ids(page):
    ids = []  
    video_page = re.finditer('"videoId":"(.{0,20})","', page)
    if(video_page):
        for video_id in video_page:
            ids += [video_id.group(1)]
    return ids

def find_video_dates(page):
    dates = []  
    video_page = re.finditer('"publishedTimeText":{"simpleText":"(.{0,20})"},"', page)
    if(video_page):
        for video_date in video_page:
            dates += [video_date.group(1)]
    return dates

def build_channel_json(video_id, title, date, link):
    channel_info = {"video_id":video_id,
                    "title":title,
                    "date":date,
                    "link":link
                    }
    return json.dumps(channel_info)


def json_to_dict(json_str):
    if json_str != None:
        return json.loads(json_str)
    else:
        return {}

def add_channel_to_server_json(server_id, channel_to_add):
    server_subs = json_to_dict(db.list_server_subs(server_id))
    num_subs = len(server_subs.keys())
    if channel_to_add not in server_subs.values():
        server_subs[num_subs] = channel_to_add
        return json.dumps(server_subs)
    else:
        return None

def add_channel(server_id, channel_link):
    channel_name, video, title, date = get_channel_info(channel_link)
    channel_info = build_channel_json(video, title, date, channel_link)
    channels = list_channels()

    if(channel_name == None):
        return "Invalid Link"
    if(channel_name not in channels.keys()):
        db.add_channel(channel_name, channel_info)

    server_subs = add_channel_to_server_json(server_id, channel_name)
    if server_subs is None:
        return "Channel already exists!"

    db.add_channel_to_server_subs(server_id, server_subs)
    return "{0} has been added!".format(channel_name)

def add_server(server_id):
    db.add_discord_server(server_id, json.dumps({}))

def remove_channel(server_id, channel_name):
    if channel_name.isdigit():
        channel_name = str(int(channel_name)-1)
    subs = json_to_dict(db.list_server_subs(server_id))
    new_subs = {}
    for sub in subs:
        if channel_name == sub:
            channel_name = subs.get(sub)
        elif channel_name == subs.get(sub):
            continue
        else:
            new_subs[sub] = subs.get(sub)
    new_subs = json.dumps(new_subs)
    db.add_discord_server(server_id, new_subs)
    return "{0} has been removed from your server's subscriptions".format(channel_name)

def remove_server(server_id):
    db.remove_discord_server(server_id)

def update_channels():
    channels = list_channels()
    for channel in channels.keys():
        channel_link = json_to_dict(channels.get(channel).decode("utf-8")).get("link")
        name, video_id, title, date = get_channel_info(channel_link)
        channel_json = build_channel_json(video_id, title, date, channel_link)
        db.add_channel(channel, channel_json)
    return "Channels have been updated!"

def list_channels():
    return db.list_channels()

def display_channel_info(server_id, channel_name):
    if channel_name.isdigit():
        channel_name = str(int(channel_name) - 1)
        channels = json_to_dict(db.list_server_subs(server_id))
        channel_name = channels.get(channel_name)
    if not channel_name:
        return "That channel does not exist. Check `&list` to see what channels you are subscribed to..."
    channel = json_to_dict(db.list_channel_info(channel_name))
    return "> ***{0}***\n> {1}\n> `{2}`".format(channel['title'], build_video_url(channel['video_id']), channel['date'])

def list_server_info(server_id):
    subs = json_to_dict(db.list_server_subs(server_id))
    if len(subs.keys()) == 0:
        return "You have no server subscriptions!"
    else:
        output = "**Here are your server subscriptions:**\n"
        for sub in subs.keys():
            output += "> ``{1}. {0} ``\n".format(subs.get(sub), int(sub)+1)
        return output 

def get_channel_info(channel_link):
    channel_name = validate_channel(channel_link)
    if channel_name:    
        filename = download_webpage(channel_name, channel_link)
        page = parse_html_file(filename)
        videos = find_video_titles(page)
        video_ids = find_video_ids(page)
        dates = find_video_dates(page)
        return channel_name, video_ids[0], videos[0], dates[0]
    else:
        return None, None, None, None

