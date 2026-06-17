# Security Policy

## Supported Versions

The latest `master` release receives security fixes. Active development happens
on `dev`.

## Reporting a Vulnerability

Do not open a public issue for leaked tokens, authentication bypasses, private
data exposure, or infrastructure credentials.

Send a private report to the repository owner with:

- affected version or commit;
- exact impact;
- reproduction steps;
- logs with secrets removed;
- suggested fix, if available.

## Secret Handling

Kokos reads secrets from `.env`. The file is ignored by git and excluded from
Docker build context. If a Telegram token is exposed, rotate it in BotFather
immediately.

## Data Handling

Kokos stores Telegram user IDs, chat IDs, usernames, names, language code,
activity timestamps, and link processing metadata. Operators are responsible
for protecting database backups and production logs.

