from flask import Flask, request
from telegram import Bot, Update
import os
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN environment variable set!")

# Initialize bot with a larger connection pool
bot = Bot(token=TOKEN)
executor = ThreadPoolExecutor(max_workers=4)

async def send_message(chat_id: int, text: str):
    """Helper function to send messages with proper error handling"""
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Error sending message: {e}")

async def handle_update(update: Update):
    """Process a single update"""
    if not update.message:
        return
    
    chat_id = update.message.chat_id
    
    if update.message.text:
        if update.message.text.startswith('/start'):
            await send_message(
                chat_id,
                "Hello! I'm BertCoin Bot. 👋\n\n"
                "I'm running on a free service that may take a few seconds to wake up if I've been inactive.\n"
                "Once I'm awake, I'll respond instantly! 🚀"
            )
        else:
            # Echo the message back
            await send_message(chat_id, f"You said: {update.message.text}")

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running! This free instance may take ~30s to wake up after inactivity.'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            # Parse the update
            update = Update.de_json(request.get_json(), bot)
            
            # Create a new event loop for this request
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Process the update
            loop.run_until_complete(handle_update(update))
            
            # Clean up
            loop.close()
            
            return 'OK'
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            return 'Error processing update', 500
    
    return 'Only POST requests are accepted'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 