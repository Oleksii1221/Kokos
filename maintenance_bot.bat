@echo off
setlocal
cd /d "%~dp0"
echo Starting Kokos bot in maintenance mode...
docker compose --env-file .env --env-file .env.maintenance up -d --build
echo.
echo Maintenance mode is active. Live console:
docker compose logs -f bot

