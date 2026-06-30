<p align="center">
  <img src="assets/kokoclip-logo.png" width="148" alt="Kokos logo">
</p>

<h1 align="center">Kokos</h1>

<p align="center">
  <strong>Production-ready Telegram bot for turning TikTok and YouTube Shorts links into native video replies.</strong>
</p>

<p align="center">
  <a href="https://github.com/Oleksii1221/Kokos/releases/tag/v0.1.0"><img alt="version" src="https://img.shields.io/badge/version-0.1.0-21d6c3?style=for-the-badge&labelColor=4a4a4a"></a>
  <img alt="platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Docker-b9f24b?style=for-the-badge&labelColor=4a4a4a">
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-MIT-101820?style=for-the-badge&labelColor=4a4a4a"></a>
</p>

<p align="center">
  <a href="https://github.com/Oleksii1221/Kokos/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Oleksii1221/Kokos/ci.yml?branch=dev&label=CI&style=flat-square&labelColor=101820"></a>
  <a href="https://github.com/Oleksii1221/Kokos/actions/workflows/codeql.yml"><img alt="CodeQL" src="https://img.shields.io/github/actions/workflow/status/Oleksii1221/Kokos/codeql.yml?branch=dev&label=CodeQL&style=flat-square&labelColor=101820"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white&labelColor=101820">
  <img alt="aiogram" src="https://img.shields.io/badge/aiogram-3.13.1-2CA5E0?style=flat-square&labelColor=101820">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white&labelColor=101820">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white&labelColor=101820">
  <img alt="Redis" src="https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white&labelColor=101820">
</p>

<p align="center">
  <a href="https://oleksii1221.github.io/Kokos/">Website</a>
  ·
  <a href="docs/deployment.md">Deploy</a>
  ·
  <a href="docs/operations.md">Operate</a>
  ·
  <a href="docs/production-checklist.md">Production checklist</a>
  ·
  <a href="ROADMAP.md">Roadmap</a>
</p>

---

## What Kokos Does

Kokos watches Telegram chats for supported short-video links and replies to the
original message with the actual video file. It is built for self-hosted
community use: simple to run, visible in logs, backed by statistics, and safe to
operate without manually managing user IDs.

```text
Telegram message -> URL detection -> cache lookup -> yt-dlp download -> video reply -> statistics
```

## Core Capabilities

| Capability | Included |
| --- | --- |
| TikTok links | `tiktok.com`, `vm.tiktok.com`, `vt.tiktok.com` |
| YouTube Shorts | `youtube.com/shorts/...`, `youtu.be/...` |
| Group chats | Works after BotFather privacy mode is disabled |
| Direct messages | Works out of the box |
| Statistics | Users, chats, active users, link events, successful videos |
| Video cache | Telegram `file_id` reuse for repeated links |
| Maintenance mode | Bot stays online while processing is paused |
| Server runtime | Docker Compose with PostgreSQL and Redis |
| Windows controls | Start, stop, and maintenance `.bat` files |

## Quick Start

```bat
copy .env.example .env
```

Fill in the production values:

```text
BOT_TOKEN=your_telegram_bot_token
OWNER_ID=your_telegram_user_id
POSTGRES_PASSWORD=change_this_password
DATABASE_URL=postgresql://kokos:change_this_password@postgres:5432/kokos
```

Start the stack:

```bat
start_bot.bat
```

Follow the live console:

```bash
docker compose logs -f bot
```

## BotFather Setup

Kokos needs to see normal group messages to detect links. Disable privacy mode:

```text
/setprivacy -> choose bot -> Disable
```

Suggested command list:

```text
start - Activate the bot
stats - Show public bot statistics
health - Show bot status
admin_stats - Owner statistics
```

## Commands

| Command | Access | Description |
| --- | --- | --- |
| `/start` | Everyone | Activates the bot and shows the intro message. |
| `/stats` | Everyone or owner-only | Shows public usage statistics. |
| `/admin_stats` | Owner | Shows raw owner statistics. |
| `/health` | Everyone | Shows active or maintenance runtime mode. |

## Runtime Architecture

```mermaid
flowchart LR
    A["Telegram chat"] --> B["aiogram bot"]
    B --> C["URL parser"]
    C --> D{"Cached?"}
    D -- yes --> E["Reply with Telegram file_id"]
    D -- no --> F["yt-dlp + ffmpeg"]
    F --> G["Upload video"]
    G --> H["Save file_id cache"]
    B --> I["PostgreSQL statistics"]
    B --> J["Docker logs"]
```

## Repository Quality

| Area | Status |
| --- | --- |
| CI | Python compile, pytest, Docker build |
| Security | CodeQL workflow and Dependabot |
| Docs | GitHub Pages-ready website and operator guides |
| Governance | Code of conduct, security policy, contribution guide |
| Release process | SemVer, changelog, GitHub Release workflow |
| Branch model | `dev` for work, `master` for stable releases |

## Project Layout

```text
app/
  bot.py          Telegram handlers and runtime flow
  config.py       Environment configuration
  db.py           PostgreSQL schema and queries
  downloader.py   yt-dlp download pipeline
  url_parser.py   Supported URL detection
assets/           Repository and bot logo assets
docs/             Public website and operator documentation
tests/            Unit tests
```

## Documentation

| Guide | Purpose |
| --- | --- |
| [Deployment](docs/deployment.md) | Start Kokos locally or on a server. |
| [Operations](docs/operations.md) | Logs, health, common issues, backups. |
| [Configuration](docs/configuration.md) | Environment variables and defaults. |
| [BotFather](docs/botfather.md) | Telegram-side setup. |
| [Architecture](docs/architecture.md) | Runtime flow and scaling notes. |
| [Production checklist](docs/production-checklist.md) | Pre-flight list before real users. |
| [Roadmap](ROADMAP.md) | Planned improvements. |
| [Release process](RELEASE.md) | How stable releases are promoted. |

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m compileall app
python -m pytest
docker build -t kokos-bot:dev .
```

## Operations Shortcuts

| Action | Command |
| --- | --- |
| Start | `start_bot.bat` |
| Stop | `stop_bot.bat` |
| Maintenance | `maintenance_bot.bat` |
| Logs | `docker compose logs -f bot` |
| Status | `docker compose ps` |

## Security Notes

Never commit `.env`, Telegram bot tokens, database passwords, session files, or
production logs. If a token was pasted into chat, screenshots, terminals, or CI
logs, rotate it in BotFather immediately.

See [SECURITY.md](SECURITY.md) and [NOTICE](NOTICE).

## Legal

Kokos is not affiliated with Telegram, TikTok, YouTube, Google, ByteDance, or
related brands. Operators are responsible for using Kokos in compliance with
applicable laws, platform terms, chat rules, and copyright requirements.

Released under the [MIT License](LICENSE).

