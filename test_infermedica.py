import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials
api_url = os.getenv('INFORMEDICA_API_URL')
api_key = os.getenv('INFORMEDICA_API_KEY')
app_id = os.getenv('INFORMEDICA_APP_ID')

print(f"Using API URL: {api_url}")
print(f"Using App ID: {app_id}")
print(f"API Key present: {'Yes' if api_key else 'No'}")

if not api_url or not api_key or not app_id:
    print("Error: Infermedica URL, API key, or App ID not set")
    exit(1)

headers = {
    'App-Id': app_id,
    'App-Key': api_key,
    'Content-Type': 'application/json'
}

# Test data
data = {
    'text': 'I have a headache',
    'age': {'value': 30},
    'sex': 'male',
    'type': 'symptoms'
}

try:
    print(f"\nSending request to Infermedica API with data: {data}")
    full_url = f"{api_url}/parse"
    print(f"Full URL being called: {full_url}")
    
    response = requests.post(full_url, headers=headers, json=data)
    
    print(f"\nInfermedica API response status: {response.status_code}")
    print(f"Infermedica API response headers: {dict(response.headers)}")
    print(f"Infermedica API response content: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nInfermedica API parsed response: {result}")
        
        if 'mentions' in result and result['mentions']:
            mentions = result['mentions']
            symptoms = []
            for mention in mentions:
                if mention['type'] == 'symptom':
                    name = mention.get('common_name', mention.get('name', ''))
                    if name:
                        symptoms.append(name)
            
            if symptoms:
                print(f"\nFound symptoms: {', '.join(symptoms)}")
                
                for symptom in symptoms:
                    try:
                        symptom_url = f"{api_url}/info/{symptom}"
                        print(f"\nFetching symptom info from: {symptom_url}")
                        symptom_response = requests.get(symptom_url, headers=headers)
                        
                        if symptom_response.status_code == 200:
                            symptom_info = symptom_response.json()
                            print(f"Symptom info response: {symptom_info}")
                    except Exception as e:
                        print(f"Error getting symptom details: {str(e)}")
            else:
                print("\nNo symptoms found in the response")
        else:
            print("\nNo mentions found in the response")
    else:
        print(f"\nError: Unexpected status code {response.status_code}")
        
except Exception as e:
    print(f"\nError: {str(e)}") 