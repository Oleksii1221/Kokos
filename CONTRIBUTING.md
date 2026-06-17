# Contributing

Thanks for helping improve Kokos.

## Branching

- `master` is for stable releases only.
- `dev` is for development and testing.
- Feature branches should branch from `dev`.

## Local Setup

1. Copy `.env.example` to `.env`.
2. Fill in `BOT_TOKEN`, `OWNER_ID`, and database credentials.
3. Start the stack:

```bat
start_bot.bat
```

## Development Checks

Run the lightweight checks before opening a change:

```bash
python -m compileall app
python -m pytest
```

## Pull Requests

Pull requests should include:

- a clear summary of the change;
- test notes or manual verification steps;
- screenshots for visible UI or documentation changes;
- migration notes when database behavior changes.

## Security

Never commit `.env`, Telegram bot tokens, database passwords, session files, or
production logs.

