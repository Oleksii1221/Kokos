# Kokos / KokoClip

Telegram bot that watches chats for TikTok and YouTube Shorts links, downloads the linked clip, and replies with the video.

## Git flow

- `master` is only for stable releases.
- `dev` is for development and testing.
- Do not push to `master` until release approval.

## Features

- Works in private chats and groups.
- Detects TikTok, `vm.tiktok.com`, YouTube Shorts, and `youtu.be` links.
- Replies to the original message with the video.
- Stores user, chat, activity, and processing statistics in PostgreSQL.
- Caches Telegram `file_id` values so repeated links do not need to be downloaded again.
- Runs in Docker.
- Has Windows batch files for start, stop, and maintenance mode.

## First setup

Copy `.env.example` to `.env` and fill the real values:

```bat
copy .env.example .env
```

Important variables:

- `BOT_TOKEN` - Telegram bot token from BotFather.
- `OWNER_ID` - your Telegram user ID for owner-only commands.
- `POSTGRES_PASSWORD` - change this before running on a server.
- `DATABASE_URL` - must use the same PostgreSQL password.

For groups, disable privacy mode in BotFather:

```text
/setprivacy -> choose bot -> Disable
```

## Run

```bat
start_bot.bat
```

This builds containers, starts the bot, and opens live logs.

## Stop

```bat
stop_bot.bat
```

## Maintenance mode

```bat
maintenance_bot.bat
```

In maintenance mode the bot stays online and tells users that video processing is temporarily unavailable.

## Commands

- `/start` - activate the bot.
- `/stats` - public bot statistics.
- `/admin_stats` - owner-only raw stats.
- `/health` - basic status check.

## Logo idea

Use the name **KokoClip**. The logo should be a dark circular icon with a clean white play triangle in the center and two short turquoise motion ribbons around it. It should read well as a small Telegram avatar.

