# BotFather Setup

## Create the bot

1. Open BotFather in Telegram.
2. Run `/newbot`.
3. Choose the display name and username.
4. Copy the token into `.env` as `BOT_TOKEN`.

## Disable group privacy

Kokos needs to read normal group messages to detect video links.

```text
/setprivacy -> choose bot -> Disable
```

## Suggested commands

```text
start - Activate the bot
stats - Show public bot statistics
health - Show bot status
admin_stats - Owner statistics
```

## Suggested description

```text
Kokos watches chats for TikTok and YouTube Shorts links and replies with the video.
```

## Suggested about text

```text
Send a TikTok or YouTube Shorts link. Kokos will answer with the video.
```

## Suggested profile photo

Use `assets/kokoclip-logo.png`.

