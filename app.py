from flask import Flask, request
import requests
import os
import logging
import random
import re
from threading import Lock
import secrets

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def apply_bert_capitalization(text):
    """Apply Bert's chaotic capitalization style"""
    roll = random.random()
    if roll < 0.4:  # 40% lowercase
        return text.lower()
    elif roll < 0.7:  # 30% UPPERCASE
        return text.upper()
    elif roll < 0.9:  # 20% Mixed case
        words = text.split()
        return ' '.join(w.upper() if random.random() < 0.5 else w.lower() for w in words)
    return text  # 10% unchanged

def add_bert_punctuation_and_emojis(text):
    """Add Bert's excessive punctuation and emojis"""
    # Add exclamation marks (90% chance)
    if random.random() < 0.9 and not text.endswith('!'):
        text += '!' * random.randint(1, 3)
    
    # Core emoji sets
    CHICKEN_EMOJIS = ['🐔', '🐓', '🥚', '🍗']
    CRYPTO_EMOJIS = ['🚀', '🌕', '💎', '📈']
    PARANOID_EMOJIS = ['😵‍💫', '👁️', '🤪', '💫']
    
    # 40% chance to add emojis
    if random.random() < 0.4:
        emoji_count = random.randint(1, 3)
        emojis = random.sample(
            CHICKEN_EMOJIS + CRYPTO_EMOJIS + PARANOID_EMOJIS,
            k=emoji_count
        )
        text += ' ' + ''.join(emojis)
    
    return text

def insert_bert_misspellings_and_clucks(text):
    """Add Bert's characteristic misspellings and clucks"""
    MISSPELLINGS = {
        'friend': 'fren',
        'friends': 'frens',
        'more': 'moar',
        'eggs': 'egggs',
        'hold': 'hodl',
        'holding': 'hodling',
        'going': 'goin',
        'what': 'wut',
        'the': 'da',
    }
    
    # Apply misspellings (30% chance per word)
    words = text.split()
    for i, word in enumerate(words):
        if random.random() < 0.3:
            words[i] = MISSPELLINGS.get(word.lower(), word)
    
    # Insert CLUCK or SQUAWK (20% chance)
    if random.random() < 0.2:
        cluck = random.choice(['CLUCK!', 'SQUAWK!', '*clucks nervously*', '*squawks intensely*'])
        insert_pos = random.randint(0, len(words))
        words.insert(insert_pos, cluck)
    
    return ' '.join(words)

def add_paranoid_tangent(text):
    """Add a random paranoid tangent (15% chance)"""
    if random.random() < 0.15:
        PARANOID_TANGENTS = [
            "...the pigeons are watching...",
            "ERNIE'S A FED!",
            "...whales lurking in the shadows...",
            "*whispers* foxes everywhere...",
            "they don't want you to know about the eggs...",
            "the coop has eyes...",
            "...binary code in the chicken feed...",
            "*adjusts tinfoil hat*",
        ]
        text += f" {random.choice(PARANOID_TANGENTS)}"
    return text

def insert_random_code_string(text):
    """Add a random binary or hex string (5% chance)"""
    if random.random() < 0.05:
        if random.random() < 0.5:
            # Binary string
            code = ''.join(random.choice('01') for _ in range(8))
            text += f" [BINARY:{code}]"
        else:
            # Hex string
            code = secrets.token_hex(4).upper()
            text += f" [HEX:{code}]"
    return text

def transform_bert_response(text):
    """Apply all Bert transformations in sequence"""
    text = apply_bert_capitalization(text)
    text = insert_bert_misspellings_and_clucks(text)
    text = add_paranoid_tangent(text)
    text = insert_random_code_string(text)
    text = add_bert_punctuation_and_emojis(text)
    return text

app = Flask(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN environment variable set!")

# Thread lock for sending messages
send_lock = Lock()

# Bert's personality responses
GREETINGS = [
    "CLUCK CLUCK frens! The coop is BULLISH today!",
    "ayoo coop fam! ready to lay some golden eggs?",
    "SQUAWK! another day of gains in the chicken feed!",
    "GM GM GM! *flaps wings excitedly* The charts are EGGSCELENT!",
    "sup my feathered frens! Bert's here with that ALPHA FEED!",
    "BAWK! The coop is PUMPING! Time to feast on gains!",
    "*nervous chicken noises* THE EGGS ARE HATCHING FRENS!",
    "GOOD MORNING EGGSPLORATION TEAM! Ready for moon mission?",
    "henlo crypto chickens! Bert's got that morning ALPHA!",
    "RISE AND GRIND COOP FAM! The foxes can't stop us!"
]

GENERIC_RESPONSES = [
    "my chicken senses are tingling... BULLISH ON THIS!",
    "BAWK BAWK! have you considered buying moar $BERT?",
    "that's the kind of alpha that makes my feathers tingle!",
    "SQUAWK! this is the most based thing since chicken feed!",
    "*pecks chart frantically* THESE GAINS ARE JUST THE START!",
    "sir, this is a chicken coop... but I LOVE YOUR ENERGY!",
    "instructions unclear, laid another golden egg!",
    "few understand the chicken wisdom... BUT YOU GET IT!",
    "big if true! *adjusts tinfoil feathers*",
    "sounds like something a pigeon spy would say... BUT BULLISH!",
    "the coop committee approves this message! WAGMI!",
    "this is the kind of hopium that feeds the whole coop!",
    "certified fresh alpha from the chicken oracle!",
    "my third eye feather sees MASSIVE GAINS!",
    "the sacred chicken bones have spoken... MOON SOON!"
]

# Community promotion responses (10% chance to use)
COMMUNITY_SHILLS = [
    "join the coop fam in our Telegram! We got the juiciest chicken feed!",
    "SQUAWK THE WORD! Tell your frens about the most bullish bird!",
    "the coop needs more chickens! Bring your flock to telegram!",
    "spread your wings and share the alpha! Telegram coop is waiting!",
    "you think this is alpha? Wait till you see our telegram nest!"
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
    ],

    r"wen.*lambo|lambo.*wen": [
        "Lambo? Think bigger fren... we're getting a fleet! 🏎️",
        "Forget Lambo, we're getting a golden chicken-mobile! 🐔",
        "Already ordered mine in $BERT green! Just trust the process! 💚"
    ],

    r"cope|copium": [
        "It's not cope if you're right! *taps head* 🧠",
        "The only thing I'm coping with is all these gains! 📈",
        "Cope? More like hope! And hope is all we need! 🙏"
    ],

    r"fud|fuder": [
        "FUD = Fear, Uncertainty, and Delusion about not buying more $BERT! 🎯",
        "The only FUD I know is Fully Undervalued Deal! 💰",
        "Imagine FUDing the comfiest hold in crypto! NGMl! 😤"
    ],

    r"wen.*listing|listing.*wen": [
        "Soon™ fren! The exchanges are literally begging us! 📱",
        "Binance CEO is in my DMs right now! Trust! 💫",
        "We're too based for CEX... but maybe just one 😏"
    ],

    r"hodl|hold": [
        "HODL? More like BODL (Buy Only Don't Leave)! 💎🙌",
        "My grip stronger than my morning coffee! ☕",
        "Been hodling since the egg days! 🥚"
    ],

    r"dip|buying": [
        "What dip? I only see discount opportunities! 🛍️",
        "Buy the dip, then buy the rip! This is financial advice! (jk) 📈",
        "Imagine not buying this gift from the crypto gods! 🎁"
    ],

    r"gas|fees": [
        "Gas fees too high? Just be rich! 🤑",
        "Think of it as a VIP entry fee to the gains club! 💫",
        "Gas is temporary, gains are forever! ⛽"
    ],

    r"wen.*binance|binance.*wen": [
        "CZ just needs to stop being ngmi and list us already! 📊",
        "Binance? You mean that small CEX that hasn't listed $BERT yet? 😏",
        "Forget Binance, we're getting listed on NASA! 🚀"
    ],

    r"bear.*market|market.*bear": [
        "Bears are just bulls in denial! 🐻➡️🐂",
        "The only bear I know is Build, Evolve, Accumulate, Rise! 📈",
        "Bear market is just a social construct! Stay bullish! 💪"
    ],

    r"wagmi|we.*gonna.*make.*it": [
        "WAGMI? More like WEGMI (We're Extremely Gonna Make It)! 🚀",
        "The WAGMIest of WAGMIs! Few understand! 💫",
        "WAGMI but some more than others (hint: $BERT holders)! 😉"
    ],

    r"ser|sir": [
        "Yes ser! 🫡",
        "Ser, this is a Bertcoin! 🐦",
        "The seriest ser that ever ser'd! 🎩"
    ],

    r"ath|all.*time.*high": [
        "You mean all time low? Because we're just getting started! 📈",
        "Every second is ATH in my heart! 💚",
        "ATH? Oh, you mean that thing we break daily? 💪"
    ],

    r"roadmap|plans": [
        "Step 1: Buy $BERT\nStep 2: ???\nStep 3: Yacht! 🛥️",
        "The roadmap is simple: up only! 📈",
        "We're going wherever the alpha takes us fren! 🗺️"
    ],

    r"whitepaper|white.*paper": [
        "Whitepaper? More like rightpaper! It's just '$BERT = number go up'! 📄",
        "We wrote it in green ink because we're eco-friendly! 💚",
        "The real whitepaper is the friends we made along the way! 🤝"
    ],

    r"dev|developer": [
        "Devs doing dev things! Very busy! Much wow! 👨‍💻",
        "The code is poetry, and we're Shakespeare! ✍️",
        "Dev team = Best team! Trust the process! 💻"
    ],

    r"airdrop|drop": [
        "The only thing dropping is your chance to buy this low! 📉",
        "Airdrop? You mean the $BERT falling from heaven? 🪂",
        "Imagine needing airdrops when you have $BERT! 🎯"
    ],

    r"nft|jpeg": [
        "Right click save that! But you can't right click save these gains! 🖼️",
        "NFTs are cool, but have you tried $BERT? 🎨",
        "Every $BERT holder is an NFT - Non Fungible Trader! 😎"
    ],

    r"pump.*it|dump.*it": [
        "He bought? Pamp it! 📞",
        "Bogdanoff would be proud! 🪦",
        "The pump is eternal, the dump is internal! 📈"
    ],

    r"based": [
        "Based? More like BERT-pilled! 💊",
        "The basedest of based takes! 🎯",
        "So based even the pH scale can't measure it! 🧪"
    ],

    r"alpha": [
        "The alpha is in the air... and it smells like chicken tendies! 🍗",
        "Alpha so good you can taste it! 😋",
        "Real alpha is buying whatever I buy! (NFA) 📈"
    ],

    r"bot|robot": [
        "Beep boop... I mean, chirp chirp! 🤖🐦",
        "I'm not a bot, I'm just bullish 24/7! 💫",
        "The only bot here is your trading strategy! 😎"
    ],

    r"wife|girlfriend": [
        "Relationships are temporary, $BERT is forever! 💕",
        "Show her the charts, that'll fix everything! 📊",
        "My girlfriend? Yeah she goes to another blockchain... 👀"
    ],

    r"rich|wealth": [
        "Being rich is a state of mind... and also a state of $BERT! 💰",
        "Wealth is measured in $BERT, few understand! 🧠",
        "Why be rich when you can be $BERT rich? 🤑"
    ]
}

# Compile regex patterns once
PATTERNS = {key: re.compile(key, re.IGNORECASE) for key in BERT_QA.keys()}

def send_message(chat_id, text, retry_count=1):
    """Send message using Telegram's HTTP API directly with retries"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    with send_lock:
        for attempt in range(retry_count + 1):
            try:
                response = requests.post(url, json=data, timeout=5)  # Reduced timeout
                response.raise_for_status()
                return True
            except requests.exceptions.Timeout:
                if attempt == retry_count:
                    logger.error("Final timeout attempt failed")
                    return False
                logger.warning(f"Timeout attempt {attempt + 1}/{retry_count + 1}")
            except Exception as e:
                logger.error(f"Failed to send message: {e}")
                return False
    return False

def get_bert_response(text):
    """Generate a contextual Bert-like response with schizophrenic chicken personality"""
    text_lower = text.lower()
    base_response = None
    
    # Quick checks first
    if any(word in text_lower for word in ['hi', 'hello', 'hey', 'sup']):
        base_response = random.choice(GREETINGS)
    
    elif 'gm' in text_lower:
        base_response = "GM GM GM! *flaps wings frantically* Another day of EGGSCELENT gains ahead! The charts are CLUCKING BEAUTIFUL!"
    
    elif 'bert' in text_lower:
        base_response = "BAWK! That's me! Your favorite schizophrenic crypto chicken! Always here with that ALPHA FEED!"
    
    # Check patterns
    if not base_response:
        for pattern, responses in BERT_QA.items():
            if PATTERNS[pattern].search(text_lower):
                base_response = random.choice(responses)
                break
    
    # Question mark check
    if not base_response and '?' in text:
        base_response = "SQUAWK! Great question fren! The answer is always buy moar $BERT! Not financial eggvice though!"
    
    # Default response if nothing else matched
    if not base_response:
        base_response = random.choice(GENERIC_RESPONSES)
    
    # 10% chance to append a community shill
    if random.random() < 0.1:
        base_response = f"{base_response}\n\n{random.choice(COMMUNITY_SHILLS)}"
    
    # Apply all our chaotic transformations
    return transform_bert_response(base_response)

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running! This free instance may take ~30s to wake up after inactivity.'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        # Basic validation
        if not data or 'message' not in data:
            return 'No message in update', 400

        chat_id = data['message'].get('chat', {}).get('id')
        text = data['message'].get('text', '')

        if not chat_id:
            return 'No chat ID in message', 400

        # Handle /start command
        if text == '/start':
            response_text = (
                "*EXCITED CHICKEN NOISES* BAWK BAWK FRENS! 🐔\n\n"
                "I'm Bert, your favorite schizophrenic crypto chicken! Ready to share some EGGSCLUSIVE alpha from the coop! 🥚\n\n"
                "The pigeons might be watching... but I'll still tell you about the MASSIVE GAINS ahead! 👁️\n\n"
                "What's clucking, fren? Let's talk crypto, gains, and why Ernie is definitely a FED! 💫"
            )
            response_text = transform_bert_response(response_text)
        else:
            response_text = get_bert_response(text)

        # Send response with retry
        if send_message(chat_id, response_text, retry_count=2):
            return 'OK', 200
        else:
            return 'Failed to send message', 500

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return 'Error processing message', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 