import requests
import json

# Set the backend URL
BASE_URL = "http://localhost:5000"

def start_session():
    """Starts a new guest session and returns session details"""
    response = requests.get(f"{BASE_URL}/start_session")
    if response.status_code == 200:
        data = response.json()
        print("✅ Session started successfully!")
        print(json.dumps(data, indent=2))
        return data["sessionId"], data["userId"]
    else:
        print(f"❌ Failed to start session: {response.text}")
        return None, None

def send_message(session_id, user_id, message):
    """Sends a message to the chatbot and returns the response"""
    payload = {
        "sessionId": session_id,
        "userId": user_id,
        "message": message
    }
    response = requests.post(f"{BASE_URL}/store_message", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✅ Message sent successfully!")
        print(f"You: {data['userMessage']['text']}")
        print(f"Bot: {data['botResponse']['text']}")
    else:
        print(f"❌ Failed to send message: {response.text}")

if __name__ == "__main__":
    print("🔄 Testing connection to backend...\n")

    # Start a guest session
    session_id, user_id = start_session()

    if session_id and user_id:
        # Send a test message
        send_message(session_id, user_id, "Hello Chatbot!")

    print("\n🔄 Connection test complete.")
