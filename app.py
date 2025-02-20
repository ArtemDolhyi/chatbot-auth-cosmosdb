from flask import Flask, request, session, redirect, url_for, render_template, jsonify
import uuid
from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import requests
import os

load_dotenv()
# Azure Configuration
COSMOS_DB_URL = os.getenv("COSMOS_DB_URL")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0"
REDIRECT_URI = "http://localhost:5000/auth/callback"
TOKEN_URL = f"{AUTHORITY}/token"
USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"

# Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Cosmos DB Setup
client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
database = client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/userId"),
)


# Session Handling
@app.route("/")
def home():
    """Home Page with session details for authenticated users"""
    if "user" in session:
        return render_template("index.html", user=session["user"], has_session=True)
    return render_template("index.html", user=None, has_session=False)



@app.route("/login")
def login():
    """Redirects to Microsoft Entra ID for authentication"""
    auth_url = (
        f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
        f"?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&response_mode=query&scope=openid email profile offline_access"
    )
    return redirect(auth_url)


@app.route("/auth/callback")
def auth_callback():
    """Handles authentication callback from Microsoft Entra ID"""
    code = request.args.get("code")
    # print(f"Received authorization code: {code}")

    if not code:
        return "Error: No code received", 400

    # Exchange the authorization code for an access token
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile offline_access User.Read",
    }

    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()

    # print("Token response:", token_json)

    access_token = token_json.get("access_token")
    if not access_token:
        return "Error: No access token received", 400

    # Fetch user details from Microsoft Graph API
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info = requests.get(USER_INFO_URL, headers=headers).json()

    # print("User info response:", user_info)

    user_id = user_info.get("id")
    user_name = user_info.get("displayName")

    if not user_id:
        return "Error: No user ID received", 400

    session["user"] = {"id": user_id, "name": user_name}
    return redirect(url_for("home"))



@app.route("/logout")
def logout():
    """Clears session and logs out"""
    session.clear()
    return redirect(url_for("home"))


@app.route("/start_session")
def start_session():
    """Start a new user session and store login type"""
    if "user" in session:
        user_id = session["user"]["id"]
        login_type = "Authenticated"
        user_name = session["user"]["name"]
    else:
        user_id = request.cookies.get("userId")
        if not user_id:
            user_id = str(uuid.uuid4())  # Generate an anonymous user ID
        login_type = "Guest"
        user_name = "Anonymous"

    session_id = str(uuid.uuid4())

    container.upsert_item({
        "id": session_id,
        "userId": user_id,
        "loginType": login_type,
        "userName": user_name,
        "messages": [],
    })

    response = jsonify({"message": "Session started", "userId": user_id, "sessionId": session_id, "loginType": login_type, "userName": user_name})
    response.set_cookie("userId", user_id)  # Store user ID in cookies for guests
    return response


@app.route("/store_message", methods=["POST"])
def store_message():
    """Store user messages and return a chatbot reply"""
    data = request.json
    session_id = data.get("sessionId")
    user_id = data.get("userId")
    message = data.get("message")

    if not session_id or not user_id or not message:
        return jsonify({"error": "Invalid request"}), 400

    # Retrieve session
    item = container.read_item(item=session_id, partition_key=user_id)

    # Store user message
    user_message = {"sender": "User", "text": message}
    item["messages"].append(user_message)

    # Define the chatbot's response
    if len(item["messages"]) == 1:  # First message in session
        bot_text = "Hello! I'm DataDex Chatbot. How can I help you today?"
    else:
        bot_text = "Interesting! Can you tell me more about that?"

    bot_response = {"sender": "Bot", "text": bot_text}
    item["messages"].append(bot_response)

    # Save conversation history
    container.upsert_item(item)

    return jsonify({"userMessage": user_message, "botResponse": bot_response})


if __name__ == "__main__":
    app.run(debug=True)
