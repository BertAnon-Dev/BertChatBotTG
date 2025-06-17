#!/bin/bash

# TheBertCoin Telegram Bot Deployment Script
echo "🤖 TheBertCoin Bot Deployment Script"
echo "====================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check if TELEGRAM_BOT_TOKEN is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️  TELEGRAM_BOT_TOKEN environment variable is not set."
    echo "Please set it with: export TELEGRAM_BOT_TOKEN='your_bot_token_here'"
    echo ""
    echo "To get a bot token:"
    echo "1. Message @BotFather on Telegram"
    echo "2. Send /newbot"
    echo "3. Follow the instructions"
    echo "4. Copy the token and set it as an environment variable"
    exit 1
fi

echo "✅ Bot token found"
echo "🚀 Starting TheBertCoin bot..."
echo "Press Ctrl+C to stop the bot"
echo ""

# Run the bot
python3 thebertcoin_bot.py 