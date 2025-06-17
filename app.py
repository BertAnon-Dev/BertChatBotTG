from flask import Flask, request
import requests
import os
import logging
import random
import re

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
    "Hey there! Want to hear about my latest alpha? 🚀",
    "WAGMI fren! Let's get this bread! 🍞"
]

GENERIC_RESPONSES = [
    "That's pretty bullish if you ask me! 🚀",
    "Interesting... but have you considered buying more $BERT? 😎",
    "Now that's what I call alpha! 🔥",
    "Based take fren! 🫡",
    "Absolutely legendary! Let's get this bread! 🍞",
    "Sir, this is a Wendy's... but I like your style! 🍔",
    "Have you tried turning it off and on again? Works for my trading bot! 💻",
    "Instructions unclear, bought more $BERT 🤷‍♂️"
]

# Specific question patterns and responses
BERT_QA = {
    r"chicken.*egg|egg.*chicken": [
        "Listen fren, I'm a bird and even I don't know... but what I do know is $BERT came before everything! 🥚🐔",
        "First came the $BERT, then came the tendies! 🍗",
        "Why worry about chickens when you can worry about charts? 📈"
    ],
    
    r"wen moon|moon when|when moon": [
        "Soon™ fren! The moon is just a pit stop, we're going to Uranus! 🚀",
        "Have you checked the charts? We're already mooning! Just zoom out... way out... keep going... 📈",
        "Wen moon? More like wen lambo! Both coming soon fren! 🏎️"
    ],
    
    r"wen.*cat|cat.*wen|pussy|dick": [
        "Down bad today aren't we fren? Try focusing on the charts instead! 📊",
        "Sir, this is a family-friendly bird... but bullish! 😳",
        "Maybe touch some grass first fren? Then we'll talk about moons and cats 🌱"
    ],
    
    r"wen ritual|ritual when": [
        "The ritual happens at midnight... or whenever the gas fees are low! ⛽",
        "First we need to sacrifice 1000 PEPE to the meme gods! 🐸",
        "Ritual machine broke... but bullish! 🔮"
    ],
    
    r"rehab": [
        "Rehab is for quitters, and $BERT never quits! 💪",
        "The only addiction here is to making gains! 📈",
        "Why go to rehab when you can go to the moon? 🚀"
    ],
    
    r"retard|retarded": [
        "We're all gonna make it fren, no need for that kind of talk! 🤝",
        "I prefer the term 'differently bullish' 🧠",
        "Focus on the gains, not the hate! WAGMI! 💪"
    ],
    
    r"rug|rugged": [
        "It's not a rug if you never sell! *taps head* 🧠",
        "The only thing getting rugged is your FUD! 💪",
        "Ser, this is $BERT... we only go up! 📈"
    ],
    
    r"aped|aping": [
        "This is the way! Full send or no send! 🦍",
        "Aping in is a lifestyle, not a choice! 🚀",
        "Average in? Never heard of her! 🦧"
    ],
    
    r"ngmi": [
        "WAGMI fren, believe! 🙏",
        "The only ones NGMI are the ones who don't believe in $BERT! 💫",
        "Turn that NGMI into WAGMI! Just buy more! 📈"
    ]
}

def get_bert_response(text):
    """Generate a contextual Bert-like response"""
    text_lower = text.lower()
    
    # Handle greetings
    if any(word in text_lower for word in ['hi', 'hello', 'hey', 'sup']):
        return random.choice(GREETINGS)
    
    # Handle GM
    elif 'gm' in text_lower:
        return "GM! Let's get this bread! 🌅 Ready for another day of gains? 💪"
    
    # Handle mentions of Bert
    elif 'bert' in text_lower:
        return "That's me! Your favorite crypto birb! Always here to share some alpha! 🐦💎"
    
    # Check for specific question patterns
    for pattern, responses in BERT_QA.items():
        if re.search(pattern, text_lower):
            return random.choice(responses)
    
    # Handle general questions
    if '?' in text:
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