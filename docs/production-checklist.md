# Production Checklist

Before running Kokos for real users:

- Rotate any token that was pasted into chat, screenshots, logs, or terminals.
- Set a strong `POSTGRES_PASSWORD`.
- Set `OWNER_ID` to the operator Telegram user ID.
- Disable BotFather privacy mode for group operation.
- Confirm `.env` is not committed.
- Run `docker compose up -d --build`.
- Send `/health` to the bot.
- Send `/stats` to verify database writes.
- Test one TikTok link and one YouTube Shorts link.
- Configure server backups for PostgreSQL.
- Decide log retention policy.
- Enable GitHub Pages from the repository settings if the public site is needed.

