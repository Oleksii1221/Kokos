# Deployment Guide

## Requirements

- Docker Desktop or Docker Engine
- Docker Compose
- Telegram bot token from BotFather
- A server with enough disk space for temporary downloads

## Environment

Copy the sample environment file:

```bash
cp .env.example .env
```

Set:

- `BOT_TOKEN`
- `OWNER_ID`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`

`DATABASE_URL` must use the same database password as `POSTGRES_PASSWORD`.

## Start

Windows:

```bat
start_bot.bat
```

Linux:

```bash
docker compose up -d --build
docker compose logs -f bot
```

## Stop

Windows:

```bat
stop_bot.bat
```

Linux:

```bash
docker compose down
```

## Maintenance Mode

Windows:

```bat
maintenance_bot.bat
```

Linux:

```bash
BOT_MAINTENANCE=true docker compose up -d --build
```

Maintenance mode keeps the bot online but disables video processing.

