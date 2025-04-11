from app import get_informedica_response
import logging

# Configure logging to see the API responses
logging.basicConfig(level=logging.INFO)

def test_medical_questions():
    """Test the get_informedica_response function with various medical questions."""
    test_questions = [
        "I have a headache and fever",
        "My throat is sore and I have a cough",
        "I'm experiencing chest pain and shortness of breath",
        "I feel dizzy and nauseous"
    ]
    
    print("\nTesting medical questions:\n")
    for question in test_questions:
        print(f"\nQuestion: {question}")
        response = get_informedica_response(question)
        print(f"Response: {response}\n")
        print("-" * 50)

if __name__ == "__main__":
    test_medical_questions() 