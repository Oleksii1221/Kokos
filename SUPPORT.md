# Support

For setup questions, open a GitHub issue with:

- your operating system;
- Docker and Docker Compose versions;
- the command you ran;
- relevant `docker compose logs --tail=100 bot` output with tokens removed.

For production incidents:

```bash
docker compose ps
docker compose logs --tail=200 bot
docker compose logs --tail=100 postgres
```

If the bot does not see group messages, disable privacy mode in BotFather:

```text
/setprivacy -> choose bot -> Disable
```

