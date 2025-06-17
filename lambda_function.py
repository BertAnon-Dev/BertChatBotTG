#!/usr/bin/env python3
"""
TheBertCoin Telegram Bot - AWS Lambda Version
Secure, serverless deployment with encrypted environment variables.
"""

import json
import logging
import os
import random
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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
    if random.random() < 0.1:
        text = text.upper()
    
    if random.random() < 0.15:
        append_phrases = ["You too?", "Berthrens know dis", "//END TRANSMISSION", "BERT out"]
        text += f" {random.choice(append_phrases)}"
    
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
    
    await update.effective_message.reply_text(response)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages with 'thebertcoin' persona logic."""
    user_message = update.message.text.lower()
    
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
    
    else:
        response = random.choice(GENERIC_PHRASES)
    
    response = apply_bertcoin_style(response)
    
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors gracefully with logging."""
    logger.error(f"Exception while handling an update: {context.error}")
    
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
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")
    
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_error_handler(error_handler)

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    global application
    
    try:
        # Initialize bot if not already done
        if application is None:
            initialize_bot()
        
        # Process the webhook update
        update = Update.de_json(json.loads(event['body']), application.bot)
        application.process_update(update)
        
        return {
            'statusCode': 200,
            'body': json.dumps('OK')
        }
        
    except Exception as e:
        logger.error(f"Lambda handler error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        } 