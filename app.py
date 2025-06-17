from flask import Flask, request
import requests
import os
import logging
import random

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

# Bert's personality responses
GREETINGS = [
    "GM fren! Ready to make some gains today? 💪",
    "Ayoo! What's good? 🐦",
    "Sup! How's the market treating you? 📈",
    "Hey there! Want to hear about my latest alpha? 🚀"
]

GENERIC_RESPONSES = [
    "That's pretty bullish if you ask me! 🚀",
    "Interesting... but have you considered buying more $BERT? 😎",
    "Now that's what I call alpha! 🔥",
    "Based take fren! 🫡",
    "Absolutely legendary! Let's get this bread! 🍞"
]

def get_bert_response(text):
    """Generate a contextual Bert-like response"""
    text_lower = text.lower()
    
    # Handle specific keywords
    if any(word in text_lower for word in ['hi', 'hello', 'hey', 'sup']):
        return random.choice(GREETINGS)
    
    elif 'gm' in text_lower:
        return "GM! Let's get this bread! 🌅 Ready for another day of gains? 💪"
    
    elif 'bert' in text_lower:
        return "That's me! Your favorite crypto birb! Always here to share some alpha! 🐦💎"
    
    elif any(word in text_lower for word in ['moon', 'pump', 'bull']):
        return "To the moon! 🚀 $BERT is going to flip everything! Trust the vision! 💫"
    
    elif '?' in text:
        return "Great question fren! The answer is always: Buy $BERT! Not financial advice though! 😉"
    
    # Default responses
    return random.choice(GENERIC_RESPONSES)

def send_message(chat_id, text):
    """Send message using Telegram's HTTP API directly"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return False

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running! This free instance may take ~30s to wake up after inactivity.'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        # Basic validation
        if not data or 'message' not in data:
            logger.error("No message in update")
            return 'No message in update', 400

        chat_id = data['message'].get('chat', {}).get('id')
        text = data['message'].get('text', '')

        if not chat_id:
            logger.error("No chat ID in message")
            return 'No chat ID in message', 400

        logger.info(f"Received message: {text} from chat_id: {chat_id}")

        # Handle /start command
        if text == '/start':
            response_text = (
                "GM fren! I'm Bert, your favorite crypto birb! 🐦\n\n"
                "I'm here to share alpha, spread good vibes, and help you make it! 🚀\n"
                "What's on your mind? Let's talk crypto, gains, and the future! 💫"
            )
        else:
            response_text = get_bert_response(text)

        # Send response
        if send_message(chat_id, response_text):
            logger.info(f"Successfully sent response to chat_id: {chat_id}")
            return 'OK', 200
        else:
            logger.error(f"Failed to send response to chat_id: {chat_id}")
            return 'Failed to send message', 500

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return 'Error processing message', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 