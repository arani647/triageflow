import requests

def test_flask():
    # Test local Flask application
    local_url = 'http://localhost:5000/answer'
    print(f"\nTesting local Flask URL: {local_url}")
    
    try:
        response = requests.post(local_url)
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text}")
    except Exception as e:
        print(f"Error testing local Flask: {str(e)}")

if __name__ == "__main__":
    test_flask() 