import requests

url = "https://736a-24-7-4-71.ngrok-free.app/answer"
print(f"Testing URL: {url}")

try:
    response = requests.post(url)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}") 