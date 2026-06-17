# Kokos

Kokos is a production-oriented Telegram bot that watches chats for TikTok and
YouTube Shorts links, downloads the linked media on the server, and replies to
the original message with the video.

It is designed for group chats, self-hosted Docker deployments, and operators
who want clear logs, statistics, and maintenance controls.

![Kokos logo](assets/kokoclip-logo.png)

## Highlights

- Detects TikTok, `vm.tiktok.com`, `vt.tiktok.com`, YouTube Shorts, and `youtu.be` links.
- Replies directly to the message that contains the link.
- Runs as a Docker Compose stack with PostgreSQL and Redis.
- Stores statistics for users, chats, active users, processed links, and successful videos.
- Caches Telegram `file_id` values to avoid downloading the same video repeatedly.
- Supports maintenance mode while keeping the bot online.
- Includes Windows batch files for start, stop, and maintenance operations.
- Ships with documentation, legal pages, GitHub templates, CI, and logo assets.

## Quick Start

Copy the environment file:

```bat
copy .env.example .env
```

Fill in:

```text
BOT_TOKEN=your_telegram_bot_token
OWNER_ID=your_telegram_user_id
POSTGRES_PASSWORD=change_this_password
DATABASE_URL=postgresql://kokos:change_this_password@postgres:5432/kokos
```

Start the bot:

```bat
start_bot.bat
```

Stop the bot:

```bat
stop_bot.bat
```

Start maintenance mode:

```bat
maintenance_bot.bat
```

## BotFather Setup

For group chats, disable privacy mode so Kokos can see normal messages:

```text
/setprivacy -> choose bot -> Disable
```

Suggested commands:

```text
start - Activate the bot
stats - Show public bot statistics
health - Show bot status
admin_stats - Owner statistics
```

## Commands

- `/start` - activate the bot and show a short introduction.
- `/stats` - show public usage statistics.
- `/admin_stats` - show owner-only raw statistics.
- `/health` - show runtime mode and basic health.

## Project Structure

```text
app/
  bot.py          Telegram handlers and runtime flow
  config.py       Environment configuration
  db.py           PostgreSQL schema and queries
  downloader.py   yt-dlp download pipeline
  url_parser.py   Supported URL detection
assets/           Logo files
docs/             GitHub Pages site and operator documentation
tests/            Unit tests
```

## Documentation

- [Deployment guide](docs/deployment.md)
- [Operations guide](docs/operations.md)
- [BotFather setup](docs/botfather.md)
- [Architecture](docs/architecture.md)
- [Privacy policy](docs/privacy.html)
- [Terms of use](docs/terms.html)

## Development

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run checks:

```bash
python -m compileall app
python -m pytest
```

## Git Flow

- `master` is for stable releases only.
- `dev` is for development and testing.
- Release changes are promoted from `dev` to `master` only after approval.

## Security

Never commit `.env`, Telegram bot tokens, session files, database passwords, or
production logs. If a token is exposed, rotate it in BotFather immediately.

See [Security Policy](SECURITY.md).

## Legal

Kokos is not affiliated with Telegram, TikTok, YouTube, Google, ByteDance, or
related brands. Operators are responsible for using Kokos in compliance with
applicable laws, platform terms, chat rules, and copyright requirements.

This project is licensed under the [MIT License](LICENSE).

