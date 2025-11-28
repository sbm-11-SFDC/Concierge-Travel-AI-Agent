
<p align="center">
  <img src="images/logo.png"
  width="800"
  height="180"
  style="object-fit: cover;
  border-radius:8px;"  
  alt="Concierge Travel AI Agent Banner"/>
</p>

# 🌍 Concierge Travel AI Agent

An AI-powered multi-agent travel planner built with Google Gemini, FastAPI, and a clean browser UI.
Users can request personalized trip plans (destination, dates, budget, preferences), and the system generates a complete itinerary including attractions, hotels, budget details, and citations.

## 🧭 Overview

This project demonstrates a practical implementation of a multi-agent architecture where:

A Travel Agent LLM handles trip planning, itinerary generation, and cost estimates.

A Coordinator Agent manages the conversation flow and user intent across sessions.

A Custom Gemini WebSearch Tool retrieves summarized information using the Gemini API.

A Front-end Web UI allows users to interact with the system in real time.

The project was developed as a submission to the Kaggle Agents Intensive Capstone Competition (Concierge Agents Track).

## ✨ Key Features
🔹 Multi-Agent System

Coordinator Agent → Handles conversation sessions, intent tracking, routing.

Travel Agent → Generates structured trip plans, budgets, attractions, hotels, and source citations.

🔹 Custom Tools

gemini_websearch.py performs search-like summarization using Gemini API (no external APIs).

🔹 End-to-End Full Stack App

Backend: FastAPI + Uvicorn

Frontend: HTML + CSS + JavaScript

LLM: Google Gemini (2.5 Pro / Flash)

🔹 Real-Time Travel Planning

Itinerary generation

Budget breakdown

Hotel suggestions

Attraction list

Sources (Holidify, Tripoto, MakeMyTrip, Thrillophilia, etc.)

🔹 Local Web UI

A clean, lightweight interface:

Submit a travel query

Receive structured result

Handle timeouts, errors, and agent responses

## 🧱 Project Architecture Overview
1. User → Web UI

User enters a query like:
“Plan a 3-day trip to Goa from Mumbai, budget 30,000 INR.”

2. Web UI → Travel Agent API

app.js sends a POST request to http://localhost:8005/agent/task.

3. Travel Agent

Processes query

Calls Gemini for:

Location summaries

Attraction suggestions

Hotel recommendations

Budget estimation

Structures response

4. (Optional) Coordinator Agent

Manages session

Handles follow-up queries

Decides when to invoke travel agent tool

5. Response → UI

Returned with:

Itinerary

Budget

Places to visit

Hotels

Citations

User → Web UI → Travel Agent → Gemini Search Tool → Travel Agent → UI Output

## 📁 Project Structure

![alt text](<Screenshot 2025-11-27 204731.png>)

## ⚙️ Setup & Installation
1️⃣ Clone the repository
git clone https://github.com/<your-username>/ai-capstone-gemini.git
cd ai-capstone-gemini

2️⃣ Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your Gemini API Key

Create .env in project root:

GEMINI_API_KEY=YOUR_API_KEY_HERE
GENAI_MODEL=models/gemini-2.5-pro
GENAI_TIMEOUT_SEC=60
GENAI_RETRIES=1

🚀 Running the Project
1️⃣ Start Travel Agent (Port 8005)
.venv\Scripts\activate
python -m agents.travel_agent

2️⃣ Start Coordinator Agent (Port 8000)

(optional)

.venv\Scripts\activate
python -m agents.coordinator_agent

3️⃣ Start Web UI
cd web
python -m http.server 8080

4️⃣ Open browser
http://localhost:8080

🧪 Testing the System
Test Travel Agent directly
$body = @{
  task_id = "T-test"
  payload = @{ query = "Plan a 2 day trip to Nashik from Pune in December, budget 20000 INR" }
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8005/agent/task" -Body $body -ContentType "application/json"

Test Coordinator Agent
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/start_convo"

## 📱 Example Prompt (UI)
Plan a 3-day trip to Goa from Mumbai in December, budget 30,000 INR.


✔ You will receive:

Day-wise itinerary

Travel options

Hotels

Attractions

Budget calculation

Source citations

## 🛠️ Future Enhancements

✔ Image fetching for attractions (Unsplash API)

✔ Hotel booking links (MakeMyTrip / Booking.com affiliate)

✔ Google Maps embed for routes

✔ User profile + history

✔ PDF itinerary export

✔ Chat-like interface


## 🪪 License

MIT License 

## 💙 Credits

Built with ❤️ using:

Google Gemini

FastAPI

Vanilla JS

Kaggle AI Intensive Capstone

## 👤 Author
Suraj Mahale

AI & Salesforce Developer

GitHub: https://github.com/sbm-11-SFDC