#!/usr/bin/env python3
"""
AWS Lambda Deployment Script for TheBertCoin Bot
Automates secure deployment with encrypted environment variables.
"""

import boto3
import json
import os
import zipfile
import tempfile
import shutil
from botocore.exceptions import ClientError

def create_deployment_package():
    """Create a ZIP file for Lambda deployment."""
    print("📦 Creating deployment package...")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy required files
        files_to_include = [
            'lambda_function.py',
            'requirements.txt'
        ]
        
        for file in files_to_include:
            if os.path.exists(file):
                shutil.copy2(file, temp_dir)
        
        # Install dependencies
        os.system(f"pip3 install -r requirements.txt -t {temp_dir}")
        
        # Create ZIP file
        zip_path = 'thebertcoin_lambda.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Deployment package created: {zip_path}")
        return zip_path

def deploy_to_lambda(function_name, zip_path, token):
    """Deploy the bot to AWS Lambda."""
    print("🚀 Deploying to AWS Lambda...")
    
    lambda_client = boto3.client('lambda')
    
    try:
        # Check if function exists
        try:
            lambda_client.get_function(FunctionName=function_name)
            print(f"📝 Updating existing function: {function_name}")
            update_existing = True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"🆕 Creating new function: {function_name}")
                update_existing = False
            else:
                raise
        
        # Read ZIP file
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
        
        # Environment variables (encrypted by AWS)
        environment_vars = {
            'Variables': {
                'TELEGRAM_BOT_TOKEN': token
            }
        }
        
        if update_existing:
            # Update existing function
            lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            
            lambda_client.update_function_configuration(
                FunctionName=function_name,
                Environment=environment_vars,
                Timeout=30,
                MemorySize=256
            )
        else:
            # Create new function
            lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role='arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role',  # You'll need to create this
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_content},
                Environment=environment_vars,
                Timeout=30,
                MemorySize=256,
                Description='TheBertCoin Telegram Bot - Secure Serverless Deployment'
            )
        
        print("✅ Lambda function deployed successfully!")
        
        # Get function URL for webhook
        try:
            url_response = lambda_client.create_function_url_config(
                FunctionName=function_name,
                AuthType='NONE'
            )
            webhook_url = url_response['FunctionUrl']
            print(f"🌐 Function URL: {webhook_url}")
            print(f"🔗 Webhook URL: {webhook_url}")
            
        except ClientError as e:
            if 'ResourceConflictException' in str(e):
                print("ℹ️  Function URL already exists")
            else:
                print(f"⚠️  Could not create function URL: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def setup_webhook(token, webhook_url):
    """Set up Telegram webhook."""
    print("🔗 Setting up Telegram webhook...")
    
    import requests
    
    webhook_set_url = f"https://api.telegram.org/bot{token}/setWebhook"
    data = {'url': webhook_url}
    
    try:
        response = requests.post(webhook_set_url, json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Webhook set successfully!")
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

def main():
    """Main deployment function."""
    print("🤖 TheBertCoin Bot - AWS Lambda Deployment")
    print("=" * 50)
    
    # Get bot token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set it with: export TELEGRAM_BOT_TOKEN='your_token'")
        return
    
    # Configuration
    function_name = 'thebertcoin-bot'
    
    # Create deployment package
    zip_path = create_deployment_package()
    
    # Deploy to Lambda
    if deploy_to_lambda(function_name, zip_path, token):
        print("\n🎉 Deployment completed successfully!")
        print("\n📋 Next steps:")
        print("1. Create an IAM role for Lambda execution")
        print("2. Set up the webhook URL with Telegram")
        print("3. Your bot will be running 24/7 securely!")
        
        # Clean up
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print(f"🧹 Cleaned up: {zip_path}")
    else:
        print("❌ Deployment failed!")

if __name__ == '__main__':
    main() 