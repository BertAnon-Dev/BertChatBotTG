#!/usr/bin/env python3
"""
Setup Telegram Webhook for Railway Deployment
"""

import requests
import os

def setup_webhook(railway_url):
    """Set up Telegram webhook with Railway URL."""
    
    token = os.getenv('TELEGRAM_BOT_TOKEN', '7892756309:AAGxdSbwPc6jhNU65srmldWGQe2gR58izSg')
    
    # Set webhook URL
    webhook_url = f"https://api.telegram.org/bot{token}/setWebhook"
    webhook_data = {
        'url': f"{railway_url}/webhook"
    }
    
    print(f"🔗 Setting webhook to: {railway_url}/webhook")
    
    try:
        response = requests.post(webhook_url, json=webhook_data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Webhook set successfully!")
                print(f"📱 Your bot is now live at: {railway_url}")
                return True
            else:
                print(f"❌ Webhook setup failed: {result.get('description')}")
                return False
        else:
            print(f"❌ Webhook setup failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook setup error: {e}")
        return False

def check_webhook_status():
    """Check current webhook status."""
    
    token = os.getenv('TELEGRAM_BOT_TOKEN', '7892756309:AAGxdSbwPc6jhNU65srmldWGQe2gR58izSg')
    
    webhook_info_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    try:
        response = requests.get(webhook_info_url)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                webhook_info = result.get('result', {})
                if webhook_info.get('url'):
                    print(f"✅ Webhook is set to: {webhook_info['url']}")
                    return webhook_info['url']
                else:
                    print("❌ No webhook is currently set")
                    return None
        else:
            print(f"❌ Failed to get webhook info: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error checking webhook: {e}")
        return None

if __name__ == '__main__':
    print("🤖 TheBertCoin Bot - Webhook Setup")
    print("=" * 40)
    
    # Check current status
    current_webhook = check_webhook_status()
    
    if current_webhook:
        print(f"Current webhook: {current_webhook}")
        response = input("Do you want to change it? (y/n): ")
        if response.lower() != 'y':
            print("Keeping current webhook.")
            exit()
    
    # Get Railway URL
    railway_url = input("Enter your Railway URL (e.g., https://your-project.railway.app): ").strip()
    
    if not railway_url:
        print("❌ No URL provided!")
        exit()
    
    # Set up webhook
    if setup_webhook(railway_url):
        print("\n🎉 Your TheBertCoin bot is now live and secure!")
        print("🔒 Running 24/7 on Railway with encrypted environment variables")
        print("💰 Free tier covers your usage")
    else:
        print("\n❌ Webhook setup failed. Please check your Railway URL and try again.") 