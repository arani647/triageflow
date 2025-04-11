import os
import subprocess
import sys
from dotenv import load_dotenv

def run_ngrok():
    try:
        # Load environment variables
        load_dotenv()
        
        # Check if ngrok is installed
        try:
            subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
        except FileNotFoundError:
            print("❌ ngrok is not installed or not in PATH")
            print("Please download ngrok from https://ngrok.com/download")
            print("Extract it and add it to your PATH or place it in this directory")
            return False
        
        # Check if ngrok is configured
        try:
            subprocess.run(['ngrok', 'config', 'check'], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("❌ ngrok is not configured")
            print("Please sign up at https://dashboard.ngrok.com/signup")
            print("Get your authtoken and run: ngrok config add-authtoken YOUR_TOKEN")
            return False
        
        print("✅ ngrok is installed and configured")
        print("\nStarting ngrok tunnel to Flask application...")
        print("Press Ctrl+C to stop the tunnel")
        
        # Start ngrok tunnel
        subprocess.run(['ngrok', 'http', '5000'])
        
    except KeyboardInterrupt:
        print("\nStopping ngrok tunnel...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    run_ngrok() 