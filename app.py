# Standard library imports
import json
import logging
import os
import time

# Third-party imports
from dotenv import load_dotenv
from flask import Flask, request, Response
import requests
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

"""TriageFlow Medical Information System.

A voice-based medical triage system that helps users describe their symptoms
and receive preliminary medical information.
"""

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize Twilio client
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Try to initialize Google Cloud Speech client
GOOGLE_SPEECH_AVAILABLE = False
try:
    from google.cloud import speech_v1 as speech
    GOOGLE_SPEECH_AVAILABLE = True
except Exception:
    logger.warning("Google Cloud Speech client not available")

def get_informedica_response(question):
    """Query the Infermedica API with the given question.
    
    Args:
        question (str): The user's medical question or symptom description
    Returns:
        str: A formatted response containing medical information or an error message
    """
    load_dotenv(override=True)
    
    api_url = os.getenv('INFORMEDICA_API_URL')
    api_key = os.getenv('INFORMEDICA_API_KEY')
    app_id = os.getenv('INFORMEDICA_APP_ID')
    
    logger.info("Using API URL: %s", api_url)
    logger.info("Using App ID: %s", app_id)
    logger.info("API Key present: %s", 'Yes' if api_key else 'No')
    
    if not all([api_url, api_key, app_id]):
        logger.error("Infermedica URL, API key, or App ID not set")
        return "Sorry, I'm having trouble connecting to the medical service."
    
    headers = {
        'App-Id': app_id,
        'App-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    data = {
        'text': question,
        'age': {'value': 30},
        'sex': 'male',
        'type': 'symptoms'
    }
    
    try:
        logger.info("Sending request to Infermedica API with data: %s", data)
        full_url = f"{api_url}/parse"
        logger.info("Full URL being called: %s", full_url)
        
        response = requests.post(full_url, headers=headers, json=data, timeout=30)
        
        logger.info("Infermedica API response status: %s", response.status_code)
        logger.info("Infermedica API response headers: %s", dict(response.headers))
        logger.info("Infermedica API response content: %s", response.text)
        
        if response.status_code == 403:
            logger.error("Authentication failed with Infermedica API")
            return "Sorry, I'm having trouble authenticating with the service."
        
        if response.status_code != 200:
            logger.error("Unexpected status code: %s", response.status_code)
            return "Sorry, I'm having trouble getting an answer. Please try again."
        
        result = response.json()
        logger.info("Infermedica API parsed response: %s", result)
        
        if not result.get('mentions'):
            return "I couldn't find relevant medical information. Please try again."
        
        symptoms = []
        for mention in result['mentions']:
            if mention['type'] == 'symptom':
                name = mention.get('common_name', mention.get('name', ''))
                if name:
                    symptoms.append(name)
        
        if not symptoms:
            return "I couldn't identify specific symptoms. Could you rephrase that?"
        
        response_text = (
            f"I found these symptoms in your description: {', '.join(symptoms)}.\n\n"
            "These symptoms could be related to various conditions. "
            "Please consult a healthcare provider for proper diagnosis."
        )
        
        symptom_info = {
            "headache": (
                "Headaches can be caused by stress, dehydration, "
                "or lack of sleep. Seek medical attention if severe."
            ),
            "fever": (
                "Fever often indicates infection. "
                "Consult a doctor if it persists or is high."
            ),
            "cough": (
                "Coughing can be from infections or allergies. "
                "See a doctor if breathing is difficult."
            ),
            "fatigue": (
                "Fatigue has many causes including stress and illness. "
                "Consult a doctor if persistent."
            )
        }
        
        for symptom in symptoms:
            info = symptom_info.get(
                symptom.lower(),
                f"{symptom} should be evaluated by a doctor if it persists."
            )
            response_text += f"\n\n{info}"
        
        response_text += "\n\nWould you like more details about any of these symptoms?"
        logger.info("Final response text: %s", response_text)
        return response_text
            
    except requests.exceptions.RequestException as e:
        logger.error("Error querying Infermedica API: %s", str(e))
        return "Sorry, I'm having trouble connecting. Please try again later."

@app.route("/voice", methods=['POST'])
def voice():
    """Handle incoming phone calls and provide initial greeting."""
    logger.info("New Call Received on /voice endpoint")
    logger.info("Request headers: %s", dict(request.headers))
    logger.info("Request form data: %s", dict(request.form))
    
    response = VoiceResponse()
    voice_params = {
        'voice': "Polly.Amy-Neural",
        'prosody': {'rate': '0.9', 'pitch': '+2Hz', 'volume': 'loud'}
    }
    
    # Add initial greeting with a pause between "Triage" and "Flow"
    response.say("Welcome to", **voice_params)
    response.say("Triage", **voice_params)
    response.pause(length=0.3)
    response.say(
        "Flow Medical Information. Please describe your symptoms.",
        **voice_params
    )
    
    gather = Gather(
        input='speech',
        action='/handle-input',
        method='POST',
        language='en-US',
        speechTimeout='auto'
    )
    
    gather.say("Please speak now.", **voice_params)
    response.append(gather)
    response.say("I didn't hear anything. Please try again.", **voice_params)
    response.redirect('/voice')
    
    logger.info("Sending TwiML Response: %s", str(response))
    return Response(str(response), mimetype='text/xml')

@app.route("/handle-input", methods=['POST'])
def handle_input():
    """Handle the user's speech input."""
    logger.info("=== Handling Speech Input ===")
    logger.info(f"Request form data: {dict(request.form)}")
    
    # Create a new response
    response = VoiceResponse()
    
    # Get the speech input
    if 'SpeechResult' in request.form:
        # Get what the user said
        user_input = request.form['SpeechResult']
        logger.info(f"Received speech: {user_input}")
        
        try:
            # Get medical information from Infermedica
            answer = get_informedica_response(user_input)
            logger.info(f"=== Full Infermedica Response Text ===")
            logger.info(answer)
            logger.info("=== End of Response Text ===")
            
            # Echo back what the user said first
            response.say(
                f"You said: {user_input}",
                voice="Polly.Amy-Neural",
                prosody={
                    'rate': '0.9',
                    'pitch': '+2Hz',
                    'volume': 'loud'
                }
            )
            
            # Add a pause
            response.pause(length=1)
            
            # Split the answer into parts and speak each part
            parts = answer.split('\n\n')
            logger.info(f"=== Split Response Parts ===")
            for i, part in enumerate(parts):
                logger.info(f"Part {i + 1}: {part.strip()}")
                if part.strip():  # Only speak non-empty parts
                    response.say(
                        part.strip(),
                        voice="Polly.Amy-Neural",
                        prosody={
                            'rate': '0.9',
                            'pitch': '+2Hz',
                            'volume': 'loud'
                        }
                    )
                    # Add a small pause between parts
                    response.pause(length=0.5)
            logger.info("=== End of Split Parts ===")
            
            # Add a pause before asking for another question
            response.pause(length=1)
            
            # Ask if they have another question
            gather = Gather(
                input='speech',
                action='/handle-input',
                method='POST',
                language='en-US',
                speechTimeout='auto'
            )
            gather.say(
                "Do you have another question? If yes, please speak now.",
                voice="Polly.Amy-Neural",
                prosody={
                    'rate': '0.9',
                    'pitch': '+2Hz',
                    'volume': 'loud'
                }
            )
            response.append(gather)
            
            # If no response, end the call
            response.say(
                "Thank you for using Triageflow Medical Information. Goodbye!",
                voice="Polly.Amy-Neural",
                prosody={
                    'rate': '0.9',
                    'pitch': '+2Hz',
                    'volume': 'loud'
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            response.say("I apologize, but I'm having trouble processing your request. Please try again.", voice="Polly.Amy-Neural")
            response.redirect('/voice')
        
    else:
        logger.warning("No speech input received")
        response.say("I'm sorry, I didn't catch that. Could you please try again?", voice="Polly.Amy-Neural")
        response.redirect('/voice')
    
    logger.info(f"=== Final TwiML Response ===")
    logger.info(str(response))
    
    return Response(str(response), mimetype='text/xml')

@app.route("/health", methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return json.dumps({"status": "ok", "timestamp": time.time()}), 200, {'Content-Type': 'application/json'}

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(host='0.0.0.0', debug=True, port=5000) 