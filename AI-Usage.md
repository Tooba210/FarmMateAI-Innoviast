# AI Usage Documentation - FarmMateAI

## Project Overview

FarmMateAI is an agricultural chatbot that helps farmers with crop planning, pest control, fertilizer management, and seasonal farming advice. It uses AI to provide practical, real-world guidance in simple language.

This document explains how AI is used in the project — the tools, prompts, improvements I made manually, limitations, and how user data is handled.

---

## AI Tools Used

### Groq API

I used Groq API as the primary AI engine for this project. Groq provides fast, free access to large language models, which made it ideal for this prototype.

- **Model:** Mixtral-8x7b-32768
- **Purpose:** Generate responses for crop-related queries
- **Why I chose it:** Free tier available, quick response time, no data retention

### Why Not OpenAI?

I considered OpenAI's GPT models, but Groq offered a free tier with good performance, which was more practical for this internship project.

---

## How the Bot Works

The bot follows a simple flow:

1. **User asks a question** through the chat interface.
2. **System prompt defines the bot's personality** — an agricultural consultant with 20+ years of experience.
3. **The AI processes the question** and generates a response.
4. **If the AI fails** (API error, network issue), a fallback system takes over.

### The Fallback System

I built a keyword-based fallback system to ensure the bot still responds even when the API is down. It checks for keywords like:

- **"crop" or "season"** → gives seasonal crop recommendations
- **"pest" or "insect"** → provides pest control advice
- **"fertilizer" or "soil"** → offers fertilizer guidance
- **"help" or "guide"** → shows general farming tips

If none of these match, the bot responds with a short, professional message explaining what it can and cannot do.

---

## System Prompt Design

The system prompt is the most important part of the bot. It tells the AI:

- **Who it is** — a professional agricultural consultant
- **What it knows** — crops, soil, water, fertilizers, pests, seasons
- **What it doesn't know** — non-farming topics, weather forecasts, personal advice
- **How to respond** — in a structured format with complete crop details

I refined this prompt over several testing rounds to make sure responses were helpful and consistent.

### Sample Prompt Snippet

You are FarmMateAI, a professional agricultural consultant with 20+ years of farming expertise.

Your role is to:

Recommend crops based on current season

Provide complete crop guides: soil, water, fertilizer, temperature, harvest, pests

Give pro tips for maximum yield

Use simple, friendly English


---

## Manual Improvements I Made

Beyond the basic AI setup, I made several manual improvements to make the bot more useful:

### 1. Crop Database

I built a custom JSON database with 14 crops, each containing details like:

- Best season to plant
- Soil type and pH range
- Water requirements
- Fertilizer recommendations
- Optimal temperature
- Harvest timeline
- Common pests and solutions
- Pro tips for better yield

This database is used both by the AI and the fallback system.

### 2. Season Detection

The bot automatically detects the current season (Winter, Spring, Monsoon, Autumn) and uses this to give context-aware recommendations.

### 3. Quick Questions

I added quick action buttons in the sidebar for common queries:
- Seasonal Crops
- Crop Guide
- Pest Control
- Pro Tips

This makes the bot easier to use for non-technical users.

### 4. Professional UI

I designed a clean, green-themed interface using custom CSS. It's responsive and works on both desktop and mobile.

### 5. Error Handling

I added error handling for:
- Empty input (user types nothing)
- API failures (Groq goes down)
- Out-of-scope questions (user asks about non-farming topics)

---

## What the Bot Can and Cannot Do

### ✅ What It Can Do

- Recommend crops for the current season
- Provide detailed crop guides (soil, water, fertilizer, temperature, harvest, pests)
- Suggest organic and chemical pest control methods
- Offer fertilizer and soil management tips
- Respond in English with clear, structured information

### ❌ What It Cannot Do

- Answer non-farming questions
- Provide weather forecasts (only seasonal guidance)
- Give personal or financial advice
- Process images or voice
- Remember conversations across sessions

---

## Limitations

- **No memory between sessions** — each conversation starts fresh
- **Text-only** — no image or voice support
- **Fixed crop database** — not connected to real-time data
- **English only** — no multi-language support yet
- **API dependency** — requires internet access to work

---

## Data Privacy & Ethics

I took privacy seriously while building this project:

### What I Don't Do

- Store user conversations
- Track user behavior or location
- Use user data for training
- Share data with third parties
- Collect any personal information

### What I Do

- Process user queries in real time
- Handle data securely (HTTPS)
- Keep API keys in environment variables (never hardcoded)
- Provide clear information about what the bot can and cannot do

---

## Security Practices

### API Key Management

I stored the API key in two places:
- `.env` file for local development (gitignored)
- `st.secrets` for deployment on Streamlit Cloud

### No Hardcoded Keys

At no point is the API key written directly in the code. This prevents accidental exposure on GitHub.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | June 2025 | Basic chatbot with Groq API and 30+ crops |
| v1.1 | July 2025 | Added professional UI, rebranded to FarmMateAI |
| v1.2 | July 2025 | Improved fallback system, quick questions, responsive design |

---

## What I Learned

Building this project taught me:

- How to integrate LLM APIs into a real application
- The importance of prompt engineering for consistent responses
- How to build fallback systems for reliability
- The value of clean UI/UX for user adoption
- How to deploy and maintain a live web app

---

## Next Steps

If I had more time, I would:

- Add support for Urdu and Hindi (regional farmers)
- Integrate a real-time weather API
- Add image upload for crop disease detection
- Save conversation history
- Build a mobile app version

---

## References

- Groq API Documentation: console.groq.com
- Streamlit Documentation: docs.streamlit.io
- Python Documentation: docs.python.org

---

## About This Document

This document is part of my internship submission at Innoviast. It reflects the actual work I did — the tools I used, the decisions I made, and the limitations I faced. No AI was used to write this document; it's based on my real experience building FarmMateAI.

---

## Author

**Tooba Rehman**  
AI Chatbot Developer Intern  
Innoviast

GitHub: Tooba210  
Project URL: farmmateai.streamlit.app

---

*Last updated: July 2025*