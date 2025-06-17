from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, filters
import os
import asyncio

app = Flask(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN environment variable set!")

# Initialize bot
bot = Bot(token=TOKEN)

async def start_command(update: Update):
    """Handle /start command"""
    await update.message.reply_text(
        "Hello! I'm BertCoin Bot. 👋\n\n"
        "I'm running on a free service that may take a few seconds to wake up if I've been inactive.\n"
        "Once I'm awake, I'll respond instantly! 🚀"
    )

async def handle_message(update: Update):
    """Handle regular messages"""
    message = update.message.text
    # Add your existing message handling logic here
    response = f"You said: {message}"
    await update.message.reply_text(response)

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running! This free instance may take ~30s to wake up after inactivity.'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            update = Update.de_json(request.get_json(), bot)
            
            async def process_update():
                if update.message is None:
                    return
                
                if update.message.text:
                    if update.message.text.startswith('/start'):
                        await start_command(update)
                    else:
                        await handle_message(update)
            
            asyncio.run(process_update())
            return 'OK'
        except Exception as e:
            print(f"Error processing update: {e}")
            return 'Error processing update', 500
            
    return 'Only POST requests are accepted'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 