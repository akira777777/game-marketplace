#!/bin/bash
echo "Останавливаю VS Code..."
pkill -f "code" || true
sleep 2

echo "Очищаю кэш VS Code..."
rm -rf ~/.config/Code/Cache/*
rm -rf ~/.config/Code/CachedData/*

echo "Запускаю VS Code с новыми настройками..."
code --no-sleep --disable-extensions-except=saoudrizwan.claude-dev .
