# 🚀 Chatbot MVP: Entra ID + Azure Cosmos DB Integration

This repository is part of a **larger chatbot project** that we are actively developing. The code here serves as a **Minimum Viable Product (MVP)** prototype designed to **test authentication capabilities** and **evaluate different options for storing chat history** within the Azure ecosystem.

---

## **💡 Why Azure?**
As we are building our chatbot using **Azure**, we decided to stay within its ecosystem and utilize **Azure-native solutions** for authentication and data storage. This prototype was specifically designed to explore **how well Microsoft Entra ID and Azure Cosmos DB integrate with our chatbot architecture**.

---

## **🌟 Why Cosmos DB?**
We chose **Azure Cosmos DB** for its **flexibility, scalability, and performance**. Key advantages include:
- **Globally distributed, low-latency database** with multi-region replication.
- **Schema-agnostic design**, allowing us to store and query structured chat logs efficiently.
- **Automatic indexing** for fast retrieval of conversation history.
- **Seamless integration with other Azure services**, making it a natural fit for our project.

---

## **🔐 Why Microsoft Entra ID?**
For authentication, we opted for **Microsoft Entra ID** due to:
- **Secure, enterprise-grade identity management**.
- **Seamless Single Sign-On (SSO) experience** for authenticated users.
- **Granular access control and user identity verification**.
- **Support for both guest users and Microsoft-authenticated users**, allowing flexibility in user interaction.

This MVP provides a **basic framework** that will be expanded as the chatbot evolves, ensuring a robust and scalable authentication and data storage solution.

---
## **🔹 Key Features**
✅ **Microsoft Entra ID Integration**  
- Supports **guest users** and **authenticated Microsoft users**  
- Entra ID handles **secure authentication**  

✅ **Azure Cosmos DB for Persistent Storage**  
- Stores **user sessions** (session ID, user ID, login type)  
- Saves **chat history** (messages sent by the user and bot responses)  
- Maintains **user name** for authenticated users  

✅ **Web-Based Chat UI (No React)**  
- Simple **HTML + Bootstrap** for a lightweight interface  
- **Message input field** with real-time chat display  

✅ **Secure Environment Configuration**  
- Uses a **`.env` file** to store credentials  
- **GitHub-safe** (credentials are not pushed)  

---

## **⚡ Quick Setup Guide**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/datadex-chatbot.git
cd datadex-chatbot
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Configure Environment Variables**
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

### **4️⃣ Run the Flask App**
```bash
python app.py
```
Visit http://localhost:5000 in your browser.
