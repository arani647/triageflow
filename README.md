# TriageFlow Medical Information System

A voice-based medical triage system that helps users describe their symptoms and receive preliminary medical information. The system uses Twilio for voice interaction and the Infermedica API for medical symptom analysis.

## Features

- Voice-based interaction using Twilio
- Natural language symptom analysis using Infermedica API
- Real-time medical information and recommendations
- Support for common symptoms like headache, fever, cough, and fatigue
- Clear separation between words "Triage" and "Flow" in voice prompts

## Requirements

- Python 3.x
- Flask
- Twilio
- Requests
- python-dotenv

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=your_phone_number
   INFORMEDICA_API_URL=https://api.infermedica.com/v3
   INFORMEDICA_API_KEY=your_api_key
   INFORMEDICA_APP_ID=your_app_id
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Call the Twilio phone number associated with the application
2. When prompted, describe your symptoms
3. Listen to the medical information and recommendations
4. Ask follow-up questions as needed

## Note

This system is for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. 