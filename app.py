from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

app = Flask(__name__)

# Your existing bot token
TOKEN = "7892756309:AAGxdSbwPc6jhNU65srmldWGQe2gR58izSg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm BertCoin Bot. How can I help you today?")

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
    return 'Bot is running'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        import asyncio
        update = request.get_json()
        asyncio.run(process_update(update))
        return 'OK'
    return 'Only POST requests are accepted'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 