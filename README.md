# YTNotify

YTNotify is a Discord Bot that allows users to stay up to date with their favorite YouTube Content Creators in the comfort of their own Discord Servers.

## Purpose

With Discord communities on the rise, friends will often share videos of their favorite online content creators when they are released. The purpose of this bot is to allow users to be automatically updated when new videos are released. 

## Requirements

- Discord Account
- Docker

## Installation

1. Create an Application at [Discord Developer Portal](https://discord.com/developers)(DDP)
2. Copy the Bot's Token into a .env file in the project's root directory
3. From your CLI (Command Line Interface) of choice, execute the following command:

```
docker-compose up -d
```
4. Once the containers are up and running, navigate back to the DDP and copy the Bot's Client ID. Use that ID to create your invite link with this format

```
https://discord.com/oauth2/authorize?client_id=<YOUR CLIENT ID HERE>&permissions=149504&scope=bot
```
5. This URL will give the Bot permission to "Send Messages", "Embed Links", and "Mention @everyone, @here, and All Roles"
6. Once YTNotify has joined the server, have fun! Use ``&help`` to view the list of commands

## Usage

1. Add a YouTube Channel to your server's list:<br />
    &add <YouTube Channel Videos Page Link> i.e. &add https://www.youtube.com/c/YTNotify/videos
2. List your server's YouTube Channel subs: &list<br />
3. Remove a channel from your server's YouTube Channel list:
    &remove <numbered index or channel shortname> i.e. &remove 1 OR &remove YTNotify
4. Update channel list manually: &update
5. View latest video from a YouTube Channel:<br />
    `&latest` i.e. `&latest <numbered index or channel shortname>` i.e. `&latest 1` OR `&latest LinusTechTips`

## Contributing

Pull requests are welcome. For any major changes to the codebase, please open up an issue for discussion on the desired changes.

Testing will be developed soon.

All contributors will be credited, and any and all contributions are appreciated!