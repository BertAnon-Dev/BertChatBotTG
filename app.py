from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

app = Flask(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN environment variable set!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm BertCoin Bot. 👋\n\n"
        "I'm running on a free service that may take a few seconds to wake up if I've been inactive.\n"
        "Once I'm awake, I'll respond instantly! 🚀"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    # Add your existing message handling logic here
    response = f"You said: {message}"
    await update.message.reply_text(response)

async def process_update(update_dict):
    """Process the update using the bot's dispatcher."""
    async_app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    async_app.add_handler(CommandHandler("start", start))
    async_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Create an Update object
    update = Update.de_json(update_dict, async_app.bot)
    
    # Process the update
    await async_app.process_update(update)

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running! This free instance may take ~30s to wake up after inactivity.'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        import asyncio
        update = request.get_json()
        
        # If this is the first message after spin-up, send a quick acknowledgment
        try:
            if update.get('message', {}).get('text') and not update.get('edited_message'):
                asyncio.run(process_update({
                    'message': {
                        'message_id': update['message']['message_id'],
                        'chat': update['message']['chat'],
                        'text': '⚡ Waking up... I'll respond in a moment!',
                        'date': update['message']['date']
                    }
                }))
        except Exception:
            pass  # Don't let the acknowledgment interfere with main processing
        
        # Process the actual message
        asyncio.run(process_update(update))
        return 'OK'
    return 'Only POST requests are accepted'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 