# 🏡 Fact-Checking API for PolitiFact Data

## 🚀 Step 1: Installing and Running the Project from Scratch

### **1️⃣ Clone the Repository**
To install and run this project, first **clone the GitHub repository**:

```sh
git clone https://github.com/hlee014e/031224.git
cd 031224/api_deployment
```

---

## 🫠 **Step 2: Installing Dependencies (if not using Docker)**
If you want to run the API **without Docker**, install the required dependencies:

```sh
pip install -r requirements.txt
```

### **3️⃣ Running the API Locally**
Start the FastAPI server with:

```sh
uvicorn main:app --reload
```

Once started, access:
- **API Base URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Swagger API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🛣️ **Step 3: Running the API in Docker**
This repository includes a **Dockerfile**, allowing you to **build and run** the API inside a Docker container.

### **4️⃣ Build the Docker Image**
```sh
docker build -t fact-check-api .
```

### **5️⃣ Run the API in a Docker Container**
```sh
docker run -p 8000:8000 fact-check-api
```

Once running, the API will be available at:
- **Base URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## ☁️ **Step 4: Deploying to a Cloud Server (AWS, Google Cloud, etc.)**
To deploy the API on a cloud server (e.g., AWS EC2, Google Cloud Run, Azure):

### **6️⃣ SSH into Your Cloud Server**
```sh
ssh user@your-server-ip
```

### **7️⃣ Clone the Repository on the Server**
```sh
git clone https://github.com/hlee014e/031224.git
cd 031224/api_deployment
```

### **8️⃣ Run the API in a Docker Container on the Server**
```sh
docker build -t fact-check-api .
docker run -p 80:8000 fact-check-api
```

Now, the API will be accessible at:

```
http://YOUR_SERVER_IP/
```

---

## 📊 How the Model Works
1. The model was **trained on labeled statements** from **PolitiFact.com**, where each statement has been reviewed by fact-checkers.
2. Given a new statement, the model **analyzes its content** and predicts one of the following truthfulness categories:
   - `"True"` ✅ (Completely true statement)
   - `"False"` ❌ (Completely false statement)
   - `"Half True"` ⚖️ (Partially true but misleading)
   - `"Mostly False"` 🚨 (Mostly false with some truth)
   - `"Barely True"` ⚠️ (Contains some truth but mostly misleading)
   - `"Pants on Fire"` 🔥 (Completely fabricated)

---

## 📅 Example API Request & Response

### **1️⃣ Input Format**
This API accepts a **JSON object** containing:
- `"text"` → The statement to fact-check.
- `"date_source_text"` → The source and date of the statement.
- `"name_text"` → The source platform (e.g., "Facebook posts", "Twitter", "News article").

**Example Request:**
```json
{
  "text": "The Department of Government Efficiency found a $6 million grant awarded to Whoopi Goldberg to promote diversity on The View.",
  "date_source_text": "stated on March 7, 2025 in a post on Facebook",
  "name_text": "Facebook posts"
}
```

### **2️⃣ Expected Output**
The API will return a **prediction** indicating the truthfulness of the statement.

**Example Response:**
```json
{
  "prediction": "False"
}
```

**Another Example Response:**
```json
{
  "prediction": "Half True"
}
```

**Possible Values for `"prediction"`:**
- `"True"` ✅ (Completely true statement)
- `"False"` ❌ (Completely false statement)
- `"Half True"` ⚖️ (Partially true but misleading)
- `"Mostly False"` 🚨 (Mostly false with some truth)
- `"Barely True"` ⚠️ (Contains some truth but mostly misleading)
- `"Pants on Fire"` 🔥 (Completely fabricated)

---

## 📚 Where the Data Comes From
This API processes **fact-checking data** from **PolitiFact.com**, which includes:
- **Statements made by public figures, media sources, and social media posts**
- **Fact-check ratings** provided by PolitiFact’s expert reviewers
- **Historical truthfulness data** for similar statements

📌 **Note:** The API **does not perform real-time fact-checking** but rather predicts truthfulness **based on past PolitiFact data and trained model features**.

---

## 📃 **License**
This project is licensed under the MIT License.


