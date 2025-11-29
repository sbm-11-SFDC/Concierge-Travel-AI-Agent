
# 🌍 Concierge Travel AI Agent

<p align="center">
  <img src="images/logo.png"
  width="800"
  height="300"
  style="object-fit: cover;
  border-radius:8px;"  
  alt="Concierge Travel AI Agent Banner"/>
</p>

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
# 1. User → Web UI

    User enters a query like:
    “Plan a 3-day trip to Goa from Mumbai, budget 30,000 INR.”

# 2. Web UI → Travel Agent API

    app.js sends a POST request to http://localhost:8005/agent/task.

# 3. Travel Agent (Core Engine)

    The Travel Agent processes the user’s trip request, extracts destination, dates, preferences, and

    budget, and sends a structured query to Gemini. It gathers location insights, attractions, and hotel

    suggestions, then formats everything into a complete itinerary. The final response includes day-wise

    plans, budget details, and citations.
    
# 4. (Optional) Coordinator Agent

    The Coordinator Agent manages multi-turn conversations by tracking the session and clarifying

    incomplete user inputs. It decides when refinement is needed and when the Travel Agent should

    generate the final plan. This ensures smoother, more natural travel planning interactions.

# 5. Response → UI

    After processing, the Travel Agent returns a structured travel plan to the UI, including itinerary,

    hotels, places to visit, and budget. The browser displays this result in a user-friendly format so

    users instantly see their personalized trip plan. The overall flow remains simple:

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

    COORD_PORT=8000

    TRAVEL_PORT=8005

    MCP_PORT=8001

    GENAI_MODEL=models/gemini-2.5-pro

    GENAI_TIMEOUT_SEC=120

    GENAI_RETRIES=1


## 🚀 Running the Project 

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

     Invoke-RestMethod -Method Post `

     -Uri "http://localhost:8005/agent/task" `

     -Body $body `

     -ContentType "application/json"

Test Coordinator Agent

     Invoke-RestMethod -Method Post ` 

     -Uri "http://localhost:8000/start_convo" `


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


## 📄 License
This project is licensed under the MIT License.

See the [LICENSE] file for details

## 👤 Author
Suraj Mahale

AI & Salesforce Developer

GitHub: https://github.com/sbm-11-SFDC