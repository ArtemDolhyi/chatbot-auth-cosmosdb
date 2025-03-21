# Chatbot MVP

This is an **MVP prototype** for a chatbot with **Microsoft Entra ID authentication** and **Azure Cosmos DB storage**. It serves as a proof of concept for authentication flows and session management within the Azure ecosystem.

---

## **Key Components**
- **Microsoft Entra ID** → Authenticates users (Guest & Microsoft Accounts).
- **Azure Cosmos DB** → Stores session data, user info, and chat history.
- **Flask Backend** → Manages authentication and data storage.
- **Web-Based UI** → Simple HTML & Bootstrap interface for chat interaction.

---

## **Quick Setup**
### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Configure Environment Variables**
Create a .env file and add:
```bash
COSMOS_DB_URL=your-cosmos-db-url
COSMOS_DB_KEY=your-cosmos-db-key
DATABASE_NAME=ChatBotDB
CONTAINER_NAME=UserSessions

TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
```

### **3. Run the Flask App**
```bash
python app.py
```
Visit http://localhost:5000 in your browser.

