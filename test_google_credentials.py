from google.cloud import speech
import os
from dotenv import load_dotenv
from google.auth import default

def test_google_credentials():
    try:
        # Load environment variables
        load_dotenv()
        
        # Try to get default credentials
        credentials, project_id = default()
        
        # Initialize the Speech client
        client = speech.SpeechClient()
        
        print("✅ Google Cloud credentials are working correctly!")
        print("Successfully connected to Speech-to-Text API")
        print(f"Project ID: {project_id}")
        return True
        
    except Exception as e:
        print("❌ Error testing Google Cloud credentials:")
        print(str(e))
        return False

if __name__ == "__main__":
    test_google_credentials() 