from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from dotenv import load_dotenv

def test_twilio_credentials():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get Twilio credentials from environment variables
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        print("Checking credentials...")
        print(f"Account SID: {account_sid[:5]}{'*' * (len(account_sid)-5) if account_sid else ''}")
        print(f"Auth Token length: {len(auth_token) if auth_token else 0}")
        print(f"Phone Number: {phone_number}")
        
        if not all([account_sid, auth_token, phone_number]):
            print("❌ Missing Twilio credentials in .env file")
            print("Please ensure you have set:")
            print("- TWILIO_ACCOUNT_SID")
            print("- TWILIO_AUTH_TOKEN")
            print("- TWILIO_PHONE_NUMBER")
            return False
        
        print("\nInitializing Twilio client...")
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        print("Fetching account info...")
        # Try to fetch account info to verify credentials
        account = client.api.accounts(account_sid).fetch()
        
        print("Verifying phone number...")
        # Try to verify phone number
        numbers = client.incoming_phone_numbers.list(phone_number=phone_number)
        if not numbers:
            print("❌ The specified phone number is not found in your Twilio account")
            return False
        
        print("\n✅ Twilio credentials are working correctly!")
        print(f"Account Status: {account.status}")
        print(f"Phone Number: {phone_number}")
        return True
        
    except TwilioRestException as e:
        print("\n❌ Error testing Twilio credentials:")
        print(f"Error Code: {e.code}")
        print(f"Error Message: {e.msg}")
        print("\nPlease verify your credentials at: https://console.twilio.com")
        return False
    except Exception as e:
        print("\n❌ Error testing Twilio credentials:")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        return False

if __name__ == "__main__":
    test_twilio_credentials() 