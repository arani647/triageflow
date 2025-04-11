import requests
import json

def test_voice_endpoint():
    """Test the voice endpoint directly."""
    # The ngrok URL
    ngrok_url = "https://e913-24-7-4-71.ngrok-free.app"
    
    # Test the voice endpoint
    print(f"Testing voice endpoint at {ngrok_url}/voice...")
    
    try:
        # Send a POST request to the voice endpoint
        response = requests.post(f"{ngrok_url}/voice")
        
        # Print the response status code
        print(f"Status code: {response.status_code}")
        
        # Print the response content
        print(f"Response content: {response.text[:500]}...")
        
        # Check if the response contains TwiML
        if "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" in response.text:
            print("✅ Response contains TwiML")
        else:
            print("❌ Response does not contain TwiML")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_voice_endpoint() 