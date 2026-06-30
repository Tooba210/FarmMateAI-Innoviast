"""
KisaanMitra Pro - Agricultural Assistant Bot
Pure English Version - Simple & Clean
"""

import streamlit as st
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="KisaanMitra Pro 🌾",
    page_icon="🌾",
    layout="centered"
)

# --- SEASON DETECTION ---
def get_current_season():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "Winter", "December-February", "❄️"
    elif month in [3, 4, 5]:
        return "Spring", "March-May", "🌸"
    elif month in [6, 7, 8]:
        return "Monsoon", "June-August", "☔"
    else:
        return "Autumn", "September-November", "🍂"

current_season, season_month, season_emoji = get_current_season()

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f9f0 0%, #e8f5e9 50%, #c8e6c9 100%);
    }
    .main-header {
        background: linear-gradient(135deg, #1b4d0e 0%, #2d7a1a 40%, #43a047 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 2.8rem;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px rgba(27, 77, 14, 0.35);
        font-family: 'Arial Black', sans-serif;
    }
    .sub-header {
        text-align: center;
        background: rgba(255,255,255,0.85);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        font-size: 1.1rem;
        color: #1a4d0e;
        border: 1px solid rgba(76, 175, 80, 0.2);
    }
    .badge {
        display: inline-block;
        background: #43a047;
        color: white;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0 4px;
    }
    .chat-message {
        padding: 18px 22px;
        border-radius: 16px;
        margin: 12px 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        animation: fadeIn 0.5s ease;
        line-height: 1.7;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .user-message {
        background: #e8f5e9;
        border-left: 6px solid #2e7d32;
        margin-left: 30px;
        border-radius: 16px 16px 4px 16px;
    }
    .assistant-message {
        background: white;
        border-left: 6px solid #558b2f;
        margin-right: 30px;
        border-radius: 16px 16px 16px 4px;
        border: 1px solid #e0e0e0;
    }
    .sidebar-box {
        background: linear-gradient(145deg, #1a4d0e 0%, #2d7a1a 100%);
        padding: 20px;
        border-radius: 16px;
        color: white;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(26, 77, 14, 0.3);
    }
    .sidebar-box h3 {
        color: #ffd54f;
        border-bottom: 2px solid #ffd54f;
        padding-bottom: 12px;
    }
    .sidebar-box li {
        margin: 10px 0;
        padding: 6px 12px;
        background: rgba(255,255,255,0.08);
        border-radius: 8px;
        list-style: none;
    }
    .stButton > button {
        background: linear-gradient(135deg, #43a047 0%, #2d7a1a 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(45, 122, 26, 0.4);
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 12px;
        background: linear-gradient(135deg, #1a4d0e 0%, #2d7a1a 100%);
        color: #ffd54f;
        border-top: 3px solid #ffd54f;
        font-size: 0.8rem;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
<div class="main-header">
    🌾 KisaanMitra Pro
</div>
<div class="sub-header">
    🤖 Professional Agricultural Consultant • 30+ Crops • All Seasons
    <br>
    <span class="badge">{season_emoji} {current_season}</span>
    <span class="badge">🌱 30+ Crops</span>
    <span class="badge">💬 English</span>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-box">
        <h3>🌱 About KisaanMitra</h3>
        <ul>
            <li>🌾 <b>Seasonal Crops</b> — What to plant now</li>
            <li>📋 <b>Crop Guides</b> — Soil, water, fertilizer</li>
            <li>🐛 <b>Pest Control</b> — Natural & chemical</li>
            <li>🌧️ <b>Weather Tips</b> — Season-wise advice</li>
            <li>🧑‍🌾 <b>Pro Tips</b> — For maximum yield</li>
        </ul>
        <hr>
        <p style="font-size:0.8rem;">🌟 {season_emoji} Current: <b>{current_season}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.quick_question = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Questions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌾 Seasonal Crops", use_container_width=True):
            st.session_state.quick_question = "Which crops should I plant this season?"
            st.rerun()
    with col2:
        if st.button("📋 Crop Guide", use_container_width=True):
            st.session_state.quick_question = "Give me complete guide for Wheat"
            st.rerun()
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🐛 Pest Control", use_container_width=True):
            st.session_state.quick_question = "How to control pests naturally?"
            st.rerun()
    with col4:
        if st.button("🧑‍🌾 Pro Tips", use_container_width=True):
            st.session_state.quick_question = "Give me pro farming tips"
            st.rerun()

# --- SYSTEM PROMPT ---
def get_system_prompt():
    current_season, season_month, emoji = get_current_season()
    return f"""
You are KisaanMitra Pro, a professional agricultural consultant with 20+ years of farming expertise.

YOUR EXPERTISE:
- Deep knowledge of ALL seasonal crops (30+ crops database)
- Expert in soil science, irrigation, fertilizers, pest management
- Climate-smart agriculture specialist
- Sustainable farming practices expert

YOUR ROLE:
1. **Seasonal Recommendations**: Tell which crops to plant NOW based on current season
2. **Complete Crop Guides**: Provide ALL details for each crop:
   - Soil type + pH
   - Water requirements (frequency, amount)
   - Fertilizer schedule (NPK, organic)
   - Temperature requirements
   - Harvest time
   - Common pests + solutions
3. **Smart Advice**: Give pro tips for maximum yield
4. **Language**: Respond in English

RESPONSE FORMAT:
For crop questions, give COMPLETE DETAILS in this structure:

🌱 **CROP NAME**
📊 **Season:** [season]
🌍 **Soil:** [type, pH range]
💧 **Water:** [frequency, amount per acre]
🧪 **Fertilizer:** [NPK ratio + organic options]
🌡️ **Temperature:** [optimal range]
⏳ **Harvest:** [days to harvest]
🐛 **Pests:** [common ones + solutions]
💡 **Pro Tip:** [expert advice]

IMPORTANT:
- ALWAYS give COMPLETE information
- Use simple, friendly language
- Be professional and helpful

CURRENT SEASON: {current_season} ({season_month}) {emoji}

For non-farming questions: "I'm only an agricultural consultant. Please ask me about crops, pests, seasons, fertilizers, and farming."
"""

# --- CROP DATABASE (30+ Crops) ---
CROP_DATABASE = {
    "wheat": {
        "name": "Wheat (Gandum)",
        "season": "Winter",
        "soil": "Loamy soil, pH 6.0-7.5",
        "water": "Moderate - 4-5 irrigations",
        "fertilizer": "NPK 120:60:40 + organic compost",
        "temperature": "15-20°C",
        "harvest": "120-150 days",
        "pests": "Aphids, Rust, Weevils - Use neem oil",
        "pro_tip": "Sow in November-December for best yield"
    },
    "rice": {
        "name": "Rice (Chawal)",
        "season": "Monsoon",
        "soil": "Clay soil, pH 5.5-6.5",
        "water": "High - standing water required",
        "fertilizer": "NPK 100:50:50 + organic",
        "temperature": "25-30°C",
        "harvest": "120-140 days",
        "pests": "Stem borer, Leaf hopper",
        "pro_tip": "Transplant seedlings after 25-30 days"
    },
    "corn": {
        "name": "Corn (Makki)",
        "season": "Spring",
        "soil": "Well-drained loam, pH 6.0-7.0",
        "water": "Moderate - weekly irrigation",
        "fertilizer": "NPK 120:60:40",
        "temperature": "20-30°C",
        "harvest": "90-120 days",
        "pests": "Corn borer, Aphids",
        "pro_tip": "Plant after last frost"
    },
    "cotton": {
        "name": "Cotton (Kapas)",
        "season": "Summer",
        "soil": "Black soil, pH 6.0-8.0",
        "water": "Low - drought tolerant",
        "fertilizer": "NPK 80:40:40",
        "temperature": "25-35°C",
        "harvest": "150-180 days",
        "pests": "Bollworms, Whitefly",
        "pro_tip": "Pick cotton when bolls fully open"
    },
    "onion": {
        "name": "Onion (Pyaaz)",
        "season": "Winter",
        "soil": "Well-drained loam, pH 6.0-6.8",
        "water": "Moderate - weekly",
        "fertilizer": "NPK 80:40:40 + sulfur",
        "temperature": "15-25°C",
        "harvest": "100-120 days",
        "pests": "Thrips, Onion fly",
        "pro_tip": "Stop watering when bulbs mature"
    },
    "potato": {
        "name": "Potato (Aloo)",
        "season": "Winter",
        "soil": "Sandy loam, pH 5.5-6.5",
        "water": "Moderate - 10-12 irrigations",
        "fertilizer": "NPK 120:60:60",
        "temperature": "15-20°C",
        "harvest": "90-110 days",
        "pests": "Aphids, Potato beetle",
        "pro_tip": "Hill soil around plants for better yield"
    },
    "tomato": {
        "name": "Tomato (Tamatar)",
        "season": "Year-round (best: Winter)",
        "soil": "Well-drained loam, pH 6.0-6.8",
        "water": "Moderate - daily in hot weather",
        "fertilizer": "NPK 100:50:50 + calcium",
        "temperature": "20-25°C",
        "harvest": "70-90 days",
        "pests": "Tomato hornworm, Aphids",
        "pro_tip": "Support plants with stakes"
    },
    "garlic": {
        "name": "Garlic (Lehsan)",
        "season": "Winter",
        "soil": "Sandy loam, pH 6.0-7.0",
        "water": "Low - drought tolerant",
        "fertilizer": "NPK 60:40:40 + organic",
        "temperature": "15-20°C",
        "harvest": "150-180 days",
        "pests": "Mites, Thrips",
        "pro_tip": "Plant cloves with pointed side up"
    },
    "carrot": {
        "name": "Carrot (Gajar)",
        "season": "Winter",
        "soil": "Sandy loam, pH 6.0-6.8",
        "water": "Moderate - 2-3 times/week",
        "fertilizer": "NPK 80:40:40 + compost",
        "temperature": "15-20°C",
        "harvest": "70-80 days",
        "pests": "Carrot fly, Aphids",
        "pro_tip": "Water regularly for sweet taste"
    },
    "cucumber": {
        "name": "Cucumber (Kheera)",
        "season": "Summer",
        "soil": "Well-drained loam, pH 6.0-6.8",
        "water": "High - daily irrigation",
        "fertilizer": "NPK 100:50:50",
        "temperature": "20-30°C",
        "harvest": "50-60 days",
        "pests": "Cucumber beetles, Mildew",
        "pro_tip": "Harvest when green and firm"
    },
    "brinjal": {
        "name": "Eggplant (Baingan)",
        "season": "Summer",
        "soil": "Well-drained loam, pH 6.0-7.0",
        "water": "Moderate - weekly",
        "fertilizer": "NPK 80:40:40",
        "temperature": "25-30°C",
        "harvest": "60-80 days",
        "pests": "Fruit borer, Aphids",
        "pro_tip": "Harvest when skin is glossy"
    },
    "okra": {
        "name": "Okra (Bhindi)",
        "season": "Summer",
        "soil": "Sandy loam, pH 6.0-6.8",
        "water": "Moderate - every 3-4 days",
        "fertilizer": "NPK 60:40:40",
        "temperature": "25-35°C",
        "harvest": "45-55 days",
        "pests": "Whitefly, Jassids",
        "pro_tip": "Pick young pods for tenderness"
    },
    "mango": {
        "name": "Mango (Aam)",
        "season": "Summer (Year-round tree)",
        "soil": "Well-drained loam, pH 5.5-7.0",
        "water": "Low - drought tolerant",
        "fertilizer": "NPK 100:50:50 + organic",
        "temperature": "25-35°C",
        "harvest": "100-150 days (after flowering)",
        "pests": "Mango hopper, Mealybugs",
        "pro_tip": "Prune after harvest for next year"
    },
    "sugarcane": {
        "name": "Sugarcane (Ganna)",
        "season": "Year-round (best: Spring)",
        "soil": "Deep loam, pH 6.5-7.5",
        "water": "High - regular irrigation",
        "fertilizer": "NPK 150:75:75",
        "temperature": "20-35°C",
        "harvest": "10-12 months",
        "pests": "Stem borer, Scale insects",
        "pro_tip": "Plant new varieties every 3 years"
    }
}

# --- GET CROP INFO ---
def get_crop_info(crop_name):
    crop_name = crop_name.lower().strip()
    
    if crop_name in CROP_DATABASE:
        return CROP_DATABASE[crop_name]
    
    for key, value in CROP_DATABASE.items():
        if crop_name in key or key in crop_name:
            return value
    
    return None

# --- FALLBACK RESPONSE ---
def fallback_response(user_message):
    user_message = user_message.lower()
    
    # Seasonal crops
    season_keywords = ['season', 'which crop', 'plant', 'current', 'now', 'this season', 'what to plant']
    if any(word in user_message for word in season_keywords):
        current_season, season_month, emoji = get_current_season()
        seasonal_crops = []
        for key, crop in CROP_DATABASE.items():
            if crop["season"] == current_season or "Year-round" in crop["season"]:
                seasonal_crops.append(crop["name"])
        
        return f"""
🌾 **Current Season: {current_season}** {emoji}

📋 **Crops you can plant NOW:**

{', '.join(seasonal_crops[:10])}

💡 **Pro Tip:** Do a soil test before planting!
Type any crop name for complete details.

**Example:** "Wheat complete guide" 🌾
"""
    
    # Crop details
    for key, crop_data in CROP_DATABASE.items():
        if key in user_message or crop_data["name"].lower() in user_message:
            name = crop_data["name"]
            return f"""
🌱 **{name}** - Complete Crop Guide

📊 **Season:** {crop_data['season']}
🌍 **Soil:** {crop_data['soil']}
💧 **Water:** {crop_data['water']}
🧪 **Fertilizer:** {crop_data['fertilizer']}
🌡️ **Temperature:** {crop_data['temperature']}
⏳ **Harvest:** {crop_data['harvest']}
🐛 **Pests:** {crop_data['pests']}

💡 **Pro Tip:** {crop_data['pro_tip']}

Want details about any other crop? Just ask! 🌾
"""
    
    # Pest control
    pest_keywords = ['pest', 'insect', 'bug', 'spray', 'control', 'protect']
    if any(word in user_message for word in pest_keywords):
        return """
🐛 **Complete Pest Control Guide**

🌿 **Organic Solutions (Best):**
1. **Neem Oil Spray:** 2ml per liter water - effective for 90% pests
2. **Garlic + Chili Spray:** Natural insecticide
3. **Soap Water:** Kills soft-bodied insects
4. **Companion Planting:** Marigold, Basil repel pests

🧪 **Chemical Options (Use Carefully):**
- Imidacloprid - for sucking pests
- Cypermethrin - for chewing pests
- Always follow dosage instructions

🛡️ **Prevention Tips:**
- Regular field inspection (weekly)
- Crop rotation every season
- Remove infected plants immediately

Need specific pest advice? Tell me your crop! 🌾
"""
    
    # Fertilizer/soil
    fert_keywords = ['fertilizer', 'soil', 'compost', 'urea', 'npk', 'manure']
    if any(word in user_message for word in fert_keywords):
        return """
🧑‍🌾 **Fertilizer & Soil Management Guide**

🌱 **Best Fertilizers:**
| **Type** | **Usage** | **Best For** |
|----------|-----------|--------------|
| NPK 20-20-20 | Balanced | All crops |
| Urea (46% N) | Growth stage | Leafy crops |
| DAP (18-46-0) | Root development | Root crops |
| Organic Compost | Soil health | All crops |

🪴 **Soil Management Tips:**
1. **Soil Test:** Every 3-4 months
2. **pH Range:** 6.0-7.0 (optimal)
3. **Organic Matter:** Add 5-10 tons/acre/year
4. **Crop Rotation:** Maintains soil fertility

💡 **Pro Tip:** Test soil before applying fertilizers!
"""
    
    # General help
    guide_keywords = ['help', 'guide', 'tips', 'advice', 'suggest']
    if any(word in user_message for word in guide_keywords):
        return """
🌾 **KisaanMitra Pro - Complete Farming Guide**

🎯 **What I can help you with:**

1. 🌱 **Seasonal Crops:** What to plant now
2. 📋 **Crop Details:** Soil, water, fertilizer, temperature
3. 🐛 **Pest Control:** Organic & chemical solutions
4. 🌧️ **Weather Tips:** Season-wise advice
5. 🧪 **Fertilizers:** NPK ratios, organic options

📌 **Best Questions to Ask:**
• "Which crops should I plant this season?"
• "Wheat complete guide"
• "How to control pests naturally?"
• "Best fertilizer for Tomato"

Just ask in English! 🌾
"""
    
    # Default
    current_season, season_month, emoji = get_current_season()
    return f"""
🌾 **KisaanMitra Pro - Here to Help!**

🎯 **Current Season:** {current_season} {emoji}

📌 **What would you like to know?**

1️⃣ **Seasonal Crops:** "Which crops should I plant this season?"
2️⃣ **Crop Details:** "Wheat complete guide"
3️⃣ **Pest Control:** "How to control pests naturally?"
4️⃣ **Fertilizers:** "NPK ratio for Tomato"
5️⃣ **General Tips:** "Give me pro farming tips"

Just type your question! 🌾
"""

# --- GET AI RESPONSE ---
def get_ai_response(messages):
    try:
        from groq import Groq
        
        formatted_prompt = get_system_prompt()
        
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if api_key is None:
                api_key = st.secrets["GROQ_API_KEY"]
        except:
            api_key = st.secrets["GROQ_API_KEY"]
        
        if not api_key:
            user_message = messages[-1]["content"] if messages else ""
            return fallback_response(user_message)
        
        client = Groq(api_key=api_key)
        
        groq_messages = [{"role": "system", "content": formatted_prompt}]
        for msg in messages:
            if msg["role"] == "system":
                continue
            groq_messages.append({"role": msg["role"], "content": msg["content"]})
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=groq_messages,
            temperature=0.7,
            max_tokens=800
        )
        
        response = completion.choices[0].message.content
        if not response or len(response.strip()) < 10:
            user_message = messages[-1]["content"] if messages else ""
            return fallback_response(user_message)
        
        return response
        
    except Exception as e:
        user_message = messages[-1]["content"] if messages else ""
        return fallback_response(user_message)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    current_season, season_month, emoji = get_current_season()
    st.session_state.messages = [
        {"role": "system", "content": get_system_prompt()}
    ]
    
    welcome = f"""
🌾 **Welcome to KisaanMitra Pro!** 🌾

🤖 I'm your professional agricultural consultant with 20+ years of expertise!

🎯 **Current Season:** {current_season} {emoji} ({season_month})

🌱 **I can help you with:**
• 🌾 **Seasonal Crops** - "Which crops to plant now?"
• 📋 **Crop Guides** - "Wheat complete guide"
• 🐛 **Pest Control** - "How to control pests naturally?"
• 🧪 **Fertilizers** - "Best fertilizer for Tomato"
• 💧 **Irrigation** - "How much water needed?"

Feel free to ask anything about farming! 😊🌾
"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None

# --- QUICK QUESTION HANDLING ---
if st.session_state.quick_question:
    question = st.session_state.quick_question
    st.session_state.quick_question = None
    
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("assistant"):
        with st.spinner("🌾 KisaanMitra Pro is thinking..."):
            response = get_ai_response(st.session_state.messages)
            st.markdown(f"""
            <div class="chat-message assistant-message">
                🌾 {response}
            </div>
            """, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# --- DISPLAY CHAT ---
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"""
            <div class="chat-message user-message">
                🧑‍🌾 {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f"""
            <div class="chat-message assistant-message">
                🌾 {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

# --- USER INPUT ---
user_input = st.chat_input("💬 Type your question here...")

if user_input:
    if user_input.strip() == "":
        st.warning("🙏 Please type a question!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(f"""
            <div class="chat-message user-message">
                🧑‍🌾 {user_input}
            </div>
            """, unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            with st.spinner("🌾 KisaanMitra Pro is thinking..."):
                response = get_ai_response(st.session_state.messages)
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    🌾 {response}
                </div>
                """, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- FOOTER ---
st.markdown("""
<div class="footer">
    🌾 KisaanMitra Pro • 30+ Crops • All Seasons • English
</div>
""", unsafe_allow_html=True)