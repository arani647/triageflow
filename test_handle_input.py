import requests
import json

def test_handle_input_endpoint():
    """Test the handle-input endpoint with a simulated speech input."""
    # The ngrok URL
    ngrok_url = "https://e913-24-7-4-71.ngrok-free.app"
    
    # Simulated speech input
    speech_input = "I have a fever"
    
    # Test the handle-input endpoint
    print(f"Testing handle-input endpoint at {ngrok_url}/handle-input...")
    print(f"Simulated speech input: '{speech_input}'")
    
    try:
        # Send a POST request to the handle-input endpoint with the speech input
        response = requests.post(
            f"{ngrok_url}/handle-input",
            data={"SpeechResult": speech_input}
        )
        
        # Print the response status code
        print(f"Status code: {response.status_code}")
        
        # Print the response content
        print(f"Response content: {response.text[:500]}...")
        
        # Check if the response contains TwiML
        if "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" in response.text:
            print("✅ Response contains TwiML")
            
            # Check if the response contains the expected answer
            if "fever" in response.text.lower():
                print("✅ Response contains the expected answer about fever")
            else:
                print("❌ Response does not contain the expected answer about fever")
        else:
            print("❌ Response does not contain TwiML")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_handle_input_endpoint() 