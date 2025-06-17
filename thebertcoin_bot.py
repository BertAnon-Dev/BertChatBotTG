#!/usr/bin/env python3
"""
TheBertCoin Telegram Bot
A cost-effective, stateless Telegram bot embodying the 'thebertcoin' persona
from X (Twitter) samples with characteristic misspellings and tone.
Supports both polling (local) and webhook (Railway) modes.
"""

import logging
import os
import random
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app for webhook support
app = Flask(__name__)

# Pre-defined phrase lists for cost-effective responses
GREETINGS = [
    "GM Berthrens",
    "GM. BERT is here",
    "Good morning. Only BERT business today",
    "GM. No munkey business",
    "GM. BERT is the chosen one",
    "GM. Chase dregens, not sherk"
]

FAREWELLS = [
    "Goodbye Berthrens",
    "BERT out. No more business",
    "See you later. Only BERT knows",
    "Bye. BERT is the chosen one",
    "End transmission. You too?",
    "BERT signing off. Berthrens know dis"
]

CRYPTO_PHRASES = [
    "BERT is the chosen one. No cesh needed",
    "Only BERT business. No munkey business",
    "Chase dregens, not sherk. You too?",
    "BERT has all the cesh. Berthrens know dis",
    "No warning needed. BERT is here",
    "BERT business only. No other business",
    "Cesh is temporary. BERT is forever",
    "Dregens bring cesh. BERT brings truth"
]

IDENTITY_PHRASES = [
    "BERT is the chosen one",
    "Donald Bert is here",
    "BERT no chase. BERT lead",
    "Berthrens know BERT",
    "BERT is special. No other like BERT",
    "BERT business only. No munkey business",
    "BERT is the one. You too?",
    "BERT has power. Berthrens see dis"
]

BUSINESS_PHRASES = [
    "No munkey business. Only BERT business",
    "BERT business is good business",
    "No other business. Only BERT",
    "BERT make business. You follow",
    "Business is BERT. BERT is business",
    "No warning needed. BERT handle business",
    "BERT business bring cesh. You too?",
    "Only BERT know business. Berthrens trust"
]

GENERIC_PHRASES = [
    "BERT is here",
    "No munkey business",
    "Only BERT business",
    "BERT is the chosen one",
    "Berthrens know dis",
    "You too?",
    "BERT no chase",
    "Chase dregens, not sherk",
    "BERT has power",
    "No warning needed",
    "BERT make cesh",
    "Only BERT know",
    "BERT is special",
    "No other like BERT",
    "BERT lead. You follow"
]

# Binary and hex strings for robotic flavor
BINARY_STRINGS = [
    "01010010",
    "10101100",
    "11001010",
    "00110101",
    "11100011"
]

HEX_STRINGS = [
    "0x1A2B3C",
    "0xDEADBEEF",
    "0xCAFEBABE",
    "0xF00DBAR",
    "0xBERT123"
]

def get_random_binary_or_hex():
    """Generate a random binary or hex string for robotic flavor."""
    if random.random() < 0.5:
        return random.choice(BINARY_STRINGS)
    else:
        return random.choice(HEX_STRINGS)

def apply_bertcoin_style(text):
    """Apply 'thebertcoin' style transformations to text."""
    # 10% chance to capitalize entire message for emphasis
    if random.random() < 0.1:
        text = text.upper()
    
    # 15% chance to append signature phrases
    if random.random() < 0.15:
        append_phrases = ["You too?", "Berthrens know dis", "//END TRANSMISSION", "BERT out"]
        text += f" {random.choice(append_phrases)}"
    
    # 8% chance to add binary/hex string
    if random.random() < 0.08:
        text += f" {get_random_binary_or_hex()}"
    
    return text

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with 'thebertcoin' welcome message."""
    welcome_messages = [
        "GM Berthrens. BERT is here. No munkey business. Only BERT business.",
        "GM. BERT is the chosen one. You too?",
        "GM. BERT welcome you. No warning needed. Berthrens know dis.",
        "GM. BERT is special. No other like BERT. Chase dregens, not sherk."
    ]
    
    response = random.choice(welcome_messages)
    response = apply_bertcoin_style(response)
    
    await update.message.reply_text(response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command with 'thebertcoin' style help message."""
    help_messages = [
        "BERT is simple. BERT is here. No complex business. Only BERT business.",
        "BERT help you. BERT is the chosen one. No munkey business needed.",
        "BERT guide you. BERT know all. Berthrens trust BERT. You too?",
        "BERT is here to help. No warning needed. BERT make everything simple."
    ]
    
    response = random.choice(help_messages)
    response = apply_bertcoin_style(response)
    
    await update.message.reply_text(response)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages with 'thebertcoin' persona logic."""
    user_message = update.message.text.lower()
    
    # Keyword detection for specific response categories
    if any(word in user_message for word in ['hello', 'hi', 'hey', 'gm', 'good morning', 'morning']):
        response = random.choice(GREETINGS)
    
    elif any(word in user_message for word in ['bye', 'goodbye', 'see you', 'later', 'gn', 'good night']):
        response = random.choice(FAREWELLS)
    
    elif any(word in user_message for word in ['crypto', 'bitcoin', 'money', 'cash', 'cesh', 'coin', 'token', 'trade', 'invest']):
        response = random.choice(CRYPTO_PHRASES)
    
    elif any(word in user_message for word in ['who', 'what', 'bert', 'you', 'your', 'identity', 'name']):
        response = random.choice(IDENTITY_PHRASES)
    
    elif any(word in user_message for word in ['business', 'work', 'job', 'project', 'plan', 'goal']):
        response = random.choice(BUSINESS_PHRASES)
    
    # Fallback for messages that don't trigger specific keywords
    else:
        response = random.choice(GENERIC_PHRASES)
    
    # Apply 'thebertcoin' style transformations
    response = apply_bertcoin_style(response)
    
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors gracefully with logging."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Send a simple error message in 'thebertcoin' style
    error_messages = [
        "BERT error. BERT fix. No warning needed.",
        "BERT problem. BERT handle. Berthrens know dis.",
        "Error happen. BERT no worry. BERT continue.",
        "BERT error. No munkey business. Only BERT business."
    ]
    
    if update and update.effective_message:
        response = random.choice(error_messages)
        response = apply_bertcoin_style(response)
        await update.effective_message.reply_text(response)

# Global application instance
application = None

def initialize_bot():
    """Initialize the bot application."""
    global application
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        return None
    
    application = Application.builder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handler for all text messages (excluding commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    return application

# Flask routes for webhook support
@app.route('/')
def home():
    """Health check endpoint."""
    return jsonify({"status": "BERT is running", "message": "No munkey business. Only BERT business."})

@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram webhook endpoint."""
    global application
    
    if application is None:
        application = initialize_bot()
        if application is None:
            return jsonify({"error": "Bot not initialized"}), 500
    
    try:
        # Process the webhook update
        update = Update.de_json(request.get_json(), application.bot)
        application.process_update(update)
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

def main():
    """Main function to initialize and run the bot."""
    # Check if running in webhook mode (Railway) or polling mode (local)
    port = int(os.getenv('PORT', 0))
    
    if port > 0:
        # Webhook mode (Railway)
        logger.info("Starting TheBertCoin bot in webhook mode...")
        initialize_bot()
        app.run(host='0.0.0.0', port=port)
    else:
        # Polling mode (local development)
        logger.info("Starting TheBertCoin bot in polling mode...")
        application = initialize_bot()
        if application:
            application.run_polling()

if __name__ == '__main__':
    main() 