import requests
import sys

def test_ngrok():
    """Test the ngrok URL to ensure it's working correctly."""
    ngrok_url = "https://5852-24-7-4-71.ngrok-free.app/voice"
    print(f"Testing ngrok URL: {ngrok_url}")
    
    try:
        response = requests.post(ngrok_url)
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Ngrok URL is working correctly!")
        else:
            print(f"❌ Ngrok URL returned status code {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing ngrok URL: {str(e)}")

if __name__ == "__main__":
    test_ngrok() 