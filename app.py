from flask import Flask, render_template, request, jsonify
import uuid
import os
import json
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def get_blob_name(session_id):
    return f"sessions/{session_id}.json"

def save_session_data(session_id, session_data):
    """Save session data to Azure Blob Storage."""
    blob_name = get_blob_name(session_id)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(session_data), overwrite=True)

def load_session_data(session_id):
    """Load session data from Azure Blob Storage."""
    blob_name = get_blob_name(session_id)
    blob_client = container_client.get_blob_client(blob_name)

    if blob_client.exists():
        return json.loads(blob_client.download_blob().readall())
    return None

@app.route("/")
def home():
    """Serve the frontend chat UI."""
    return render_template("index.html")

@app.route("/start_session")
def start_session():
    """Start a new chat session and store it in Azure Blob Storage."""
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())

    session_data = {"sessionId": session_id, "userId": user_id, "messages": []}
    save_session_data(session_id, session_data)

    response = jsonify({"message": "Session started", "userId": user_id, "sessionId": session_id})
    response.set_cookie("userId", user_id)
    return response

@app.route("/store_message", methods=["POST"])
def store_message():
    """Store user messages and return a chatbot reply."""
    data = request.json
    session_id, user_id, message = data.get("sessionId"), data.get("userId"), data.get("message")

    if not session_id or not user_id or not message:
        return jsonify({"error": "Invalid request"}), 400

    session_data = load_session_data(session_id) or {"sessionId": session_id, "userId": user_id, "messages": []}
    session_data["messages"].append({"sender": "User", "text": message})

    bot_reply = "Hello! I'm DataDex Chatbot. How can I help you today?" if len(session_data["messages"]) == 1 else "Interesting! Can you tell me more about that?"
    session_data["messages"].append({"sender": "Bot", "text": bot_reply})

    save_session_data(session_id, session_data)

    return jsonify({"userMessage": {"sender": "User", "text": message}, "botResponse": {"sender": "Bot", "text": bot_reply}})

@app.route("/get_session", methods=["GET"])
def get_session():
    """Retrieve the full session history."""
    session_id = request.args.get("sessionId")
    user_id = request.args.get("userId")

    if not session_id or not user_id:
        return jsonify({"error": "Missing sessionId or userId"}), 400

    session_data = load_session_data(session_id)
    if not session_data:
        return jsonify({"error": "Session not found"}), 404

    return jsonify(session_data)

if __name__ == "__main__":
    app.run(debug=True)
