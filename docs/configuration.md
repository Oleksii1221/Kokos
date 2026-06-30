# Configuration

Kokos is configured through environment variables.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `BOT_TOKEN` | Yes | none | Telegram bot token from BotFather. |
| `OWNER_ID` | Recommended | `0` | Telegram user ID allowed to use owner-only commands. |
| `POSTGRES_DB` | Yes | `kokos` | PostgreSQL database name. |
| `POSTGRES_USER` | Yes | `kokos` | PostgreSQL user. |
| `POSTGRES_PASSWORD` | Yes | `change_me` | PostgreSQL password. Change this in production. |
| `DATABASE_URL` | Yes | none | SQL connection string used by the bot. |
| `REDIS_URL` | No | `redis://redis:6379/0` | Reserved for queue and rate-limit features. |
| `BOT_MAINTENANCE` | No | `false` | Keeps bot online but disables video processing. |
| `MAX_PARALLEL_DOWNLOADS` | No | `3` | Maximum concurrent downloads per bot process. |
| `MAX_VIDEO_MB` | No | `48` | Maximum accepted video size. |
| `DOWNLOAD_TIMEOUT_SECONDS` | No | `120` | Download timeout for one link. |
| `PUBLIC_STATS` | No | `true` | Allows non-owner users to call `/stats`. |

