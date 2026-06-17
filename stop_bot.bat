@echo off
setlocal
cd /d "%~dp0"
echo Stopping Kokos bot...
docker compose down
echo Bot stopped.

