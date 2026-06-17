@echo off
setlocal
cd /d "%~dp0"
echo Starting Kokos bot...
docker compose --env-file .env up -d --build
echo.
echo Bot started. Live console:
docker compose logs -f bot

