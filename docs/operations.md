# Operations Guide

## Live Logs

```bash
docker compose logs -f bot
```

## Health

Send `/health` to the bot.

Expected response:

```text
KokoClip online. Mode: active.
```

## Statistics

Send `/stats` for public statistics.

Send `/admin_stats` from the configured `OWNER_ID` account for owner-only raw
stats.

## Common Issues

### The bot does not see group links

Disable privacy mode in BotFather:

```text
/setprivacy -> choose bot -> Disable
```

### TikTok or YouTube downloads fail

Check:

- `yt-dlp` is current;
- the video is public;
- the video is not larger than `MAX_VIDEO_MB`;
- server networking is healthy;
- platform restrictions have not changed.

### Disk usage grows

Temporary download directories are cleaned after successful or failed jobs. If a
container is killed mid-download, remove old files from `downloads/`.

## Backup

Back up the PostgreSQL volume before production upgrades.

```bash
docker compose exec postgres pg_dump -U kokos kokos > kokos-backup.sql
```

