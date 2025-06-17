from flask import Flask, request
from telegram import Bot, Update
import os
import asyncio
import logging
from functools import partial

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

# Initialize bot
bot = Bot(token=TOKEN)

# Create a new event loop for the application
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def send_telegram_message(chat_id: int, text: str) -> None:
    """Send a message to Telegram with proper error handling"""
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise

def run_async(coro):
    """Run an async function in the event loop"""
    return asyncio.run_coroutine_threadsafe(coro, loop)

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running! This free instance may take ~30s to wake up after inactivity.'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Basic validation
            if not data:
                return 'No data received', 400

            chat_id = data.get('message', {}).get('chat', {}).get('id')
            text = data.get('message', {}).get('text')

            if not chat_id:
                return 'No chat ID found', 400

            # Handle /start command
            if text == '/start':
                response_text = (
                    "Hello! I'm BertCoin Bot. 👋\n\n"
                    "I'm running on a free service that may take a few seconds to wake up if I've been inactive.\n"
                    "Once I'm awake, I'll respond instantly! 🚀"
                )
            else:
                response_text = f"You said: {text}"

            # Send response
            future = run_async(send_telegram_message(chat_id, response_text))
            future.result(timeout=10)  # Wait for the response with a timeout
            
            return 'OK'
        except Exception as e:
            logger.error(f"Error in webhook: {e}")
            return 'Error processing message', 500
    
    return 'Only POST requests are accepted'

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 8080))
        app.run(host='0.0.0.0', port=port)
    finally:
        loop.close() 