# TheBertCoin Telegram Bot 🤖

A cost-effective, stateless Telegram chatbot that embodies the unique persona of 'thebertcoin' from X (Twitter) samples. The bot features characteristic misspellings, broken grammar, and a distinctive robotic tone.

## Features

- **Cost-Effective**: Uses pre-defined phrase lists instead of expensive LLM APIs
- **Stateless Design**: Perfect for serverless deployment (AWS Lambda, Google Cloud Functions)
- **Secure**: Bot token loaded from environment variables
- **Authentic Persona**: Embodies 'thebertcoin' with characteristic:
  - Misspellings: "cesh" (cash), "lyk" (like), "munkey" (monkey), "dregens" (dragons)
  - Broken grammar: "BERT no chase", "No warning needed"
  - Signature phrases: "No munkey business. Only BERT business"
  - Robotic elements: Binary/hex strings, "//END TRANSMISSION"

## Quick Start

### 1. Get a Telegram Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy your bot token

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

### 4. Run the Bot

```bash
python thebertcoin_bot.py
```

## Bot Commands

- `/start` - Get a 'thebertcoin' welcome message
- `/help` - Receive help in 'thebertcoin' style

## Message Categories

The bot responds to different types of messages with appropriate 'thebertcoin' phrases:

- **Greetings**: "GM Berthrens", "BERT is here"
- **Farewells**: "BERT out. No more business"
- **Crypto**: "BERT has all the cesh. Berthrens know dis"
- **Identity**: "BERT is the chosen one"
- **Business**: "No munkey business. Only BERT business"
- **Generic**: Fallback responses for other messages

## Deployment Options

### Local Development
```bash
python thebertcoin_bot.py
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY thebertcoin_bot.py .
CMD ["python", "thebertcoin_bot.py"]
```

### Serverless Deployment (AWS Lambda)

1. Create a Lambda function with Python runtime
2. Upload the bot code as a ZIP file
3. Set `TELEGRAM_BOT_TOKEN` as an environment variable
4. Configure API Gateway or use Lambda function URLs

### Google Cloud Functions

1. Deploy using Google Cloud CLI:
```bash
gcloud functions deploy thebertcoin-bot \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars TELEGRAM_BOT_TOKEN=your_token
```

## Security Features

- ✅ Bot token loaded from environment variables
- ✅ No hardcoded secrets
- ✅ Comprehensive error handling
- ✅ Logging for debugging and monitoring

## Cost Optimization

- ✅ No external LLM API calls
- ✅ Pre-defined response lists
- ✅ Rule-based message handling
- ✅ Minimal computational overhead

## Customization

### Adding New Phrases

Edit the phrase lists in `thebertcoin_bot.py`:

```python
GREETINGS = [
    "GM Berthrens",
    "GM. BERT is here",
    # Add your custom phrases here
]
```

### Modifying Response Logic

Update the `message_handler` function to add new keyword categories:

```python
elif any(word in user_message for word in ['your_keywords']):
    response = random.choice(YOUR_PHRASE_LIST)
```

## Troubleshooting

### Common Issues

1. **Token not found**: Ensure `TELEGRAM_BOT_TOKEN` environment variable is set
2. **Import errors**: Install dependencies with `pip install -r requirements.txt`
3. **Bot not responding**: Check bot token validity and internet connection

### Logs

The bot logs all activities. Check console output for:
- Bot startup messages
- Error details
- Message handling information

## Contributing

Feel free to add more 'thebertcoin' phrases or improve the bot's logic while maintaining the authentic persona.

## License

This project is open source. Use responsibly and respect Telegram's bot policies.

---

**BERT is the chosen one. No munkey business. Only BERT business. Berthrens know dis.** 