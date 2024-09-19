@echo off

echo Starting Telegram Echo Bot...

cd %~dp0

call venv/Scripts/Activate.bat

@REM set TOKEN=

python telegrambot/StartBot.py

echo Telegram Echo Bot stopped.

pause
