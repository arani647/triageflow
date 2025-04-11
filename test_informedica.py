import os
import requests
import json
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_informedica_api():
    """Test the connection to the Informedica API."""
    # Force reload of environment variables
    load_dotenv(override=True)
    
    api_url = os.getenv('INFORMEDICA_API_URL')
    api_key = os.getenv('INFORMEDICA_API_KEY')
    
    print(f"Testing Informedica API connection...")
    print(f"API URL: {api_url}")
    print(f"API Key: {api_key}")
    
    if not api_url or not api_key:
        print("❌ Error: Informedica URL or API key not set in .env file")
        return
    
    # Try different authentication methods
    auth_methods = [
        # Method 1: App-Id and App-Key headers
        {
            'name': 'App-Id and App-Key',
            'headers': {
                'App-Id': api_key,
                'App-Key': api_key,
                'Content-Type': 'application/json'
            }
        }
    ]
    
    # Test data - a simple medical question
    data = {
        'text': 'What are the symptoms of the flu?',
        'type': 'symptom',
        'max_results': 5
    }
    
    for auth_method in auth_methods:
        print(f"\nTrying {auth_method['name']} authentication...")
        print(f"Headers: {json.dumps(auth_method['headers'], indent=2)}")
        
        try:
            print(f"Sending request to {api_url}/parse...")
            response = requests.post(f"{api_url}/parse", headers=auth_method['headers'], json=data)
            
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ API connection successful!")
                result = response.json()
                print(f"Response data: {json.dumps(result, indent=2)}")
                return  # Exit the function if successful
            else:
                print(f"❌ API request failed")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n❌ Authentication failed. Please check your API key and the API documentation.")

if __name__ == "__main__":
    test_informedica_api() 