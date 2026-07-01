"""
FarmMateAI - AI-Powered Agricultural Assistant
Professional Agricultural Consultant for Farmers
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
    page_title="FarmMateAI 🌾",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="expanded"
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

# --- PROFESSIONAL CSS ---
st.markdown("""
<style>
    /* ===== RESET & BASE ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: #f5f8f5;
    }
    
    /* ===== MAIN HEADER ===== */
    .main-header {
        background: linear-gradient(135deg, #0f2b1a 0%, #1a4d0e 50%, #2a7a1a 100%);
        padding: 32px 40px;
        border-radius: 18px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 40px rgba(15, 43, 26, 0.3);
        border: 1px solid rgba(255, 213, 79, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 70% 30%, rgba(255,213,79,0.06) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .main-header .logo {
        font-size: 2.8rem;
        font-weight: 800;
        font-family: 'Inter', 'Segoe UI', 'Arial', sans-serif;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    
    .main-header .logo span {
        color: #ffd54f;
    }
    
    .main-header .sub-title {
        font-size: 0.9rem;
        font-weight: 300;
        opacity: 0.85;
        margin-top: 6px;
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    .main-header .badge-container {
        margin-top: 12px;
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    
    .main-header .badge-container .badge {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(8px);
        padding: 5px 18px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        border: 1px solid rgba(255,255,255,0.06);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* ===== SIDEBAR ===== */
    .sidebar-box {
        background: linear-gradient(145deg, #0f2b1a 0%, #1a4d0e 100%);
        padding: 22px 20px;
        border-radius: 16px;
        color: white;
        margin-bottom: 16px;
        box-shadow: 0 8px 32px rgba(15, 43, 26, 0.25);
        border: 1px solid rgba(255, 213, 79, 0.06);
    }
    
    .sidebar-box h3 {
        color: #ffd54f;
        font-size: 1rem;
        font-weight: 700;
        border-bottom: 2px solid rgba(255, 213, 79, 0.15);
        padding-bottom: 12px;
        margin-bottom: 14px;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        letter-spacing: 0.3px;
    }
    
    .sidebar-box ul {
        padding-left: 0;
        list-style: none;
        margin: 0;
    }
    
    .sidebar-box li {
        padding: 10px 14px;
        margin: 6px 0;
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
        font-size: 0.85rem;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        border-left: 3px solid transparent;
        transition: all 0.25s ease;
        color: rgba(255,255,255,0.85);
    }
    
    .sidebar-box li:hover {
        background: rgba(255,255,255,0.08);
        border-left-color: #ffd54f;
        transform: translateX(4px);
    }
    
    .sidebar-box .stats {
        background: rgba(255,255,255,0.05);
        padding: 12px 16px;
        border-radius: 10px;
        margin-top: 14px;
        text-align: center;
        font-size: 0.75rem;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        border: 1px dashed rgba(255,213,79,0.1);
        color: rgba(255,255,255,0.6);
    }
    
    .sidebar-box .stats strong {
        color: #ffd54f;
    }
    
    /* ===== SIDEBAR SECTION TITLE ===== */
    .sidebar-section-title {
        color: rgba(255,255,255,0.3);
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        margin: 18px 0 12px 0;
        font-weight: 700;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #2a7a1a 0%, #1a4d0e 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 0.85rem;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        cursor: pointer;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 16px rgba(26, 77, 14, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(26, 77, 14, 0.35);
        background: linear-gradient(135deg, #3a9a27 0%, #1a4d0e 100%);
    }
    
    .stButton > button:active {
        transform: scale(0.97);
    }
    
    /* Quick Question Buttons */
    .quick-btn .stButton > button {
        background: rgba(255,255,255,0.06);
        color: #e8f0e8;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: none;
        padding: 8px 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .quick-btn .stButton > button:hover {
        background: rgba(255,255,255,0.12);
        border-color: rgba(255,213,79,0.15);
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    /* Reset Button */
    .reset-btn .stButton > button {
        background: rgba(255,255,255,0.04);
        color: rgba(255,255,255,0.6);
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: none;
    }
    
    .reset-btn .stButton > button:hover {
        background: rgba(255,255,255,0.08);
        color: white;
        border-color: rgba(255,255,255,0.08);
    }
    
    /* ===== CHAT MESSAGES ===== */
    .chat-message {
        padding: 16px 20px;
        border-radius: 14px;
        margin: 10px 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.03);
        animation: fadeIn 0.4s ease;
        line-height: 1.7;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 0.95rem;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: #e8f0e8;
        border-left: 4px solid #2a7a1a;
        margin-left: 20px;
        border-radius: 14px 14px 4px 14px;
        color: #1a3a1a;
    }
    
    .assistant-message {
        background: #ffffff;
        border-left: 4px solid #1a4d0e;
        margin-right: 20px;
        border-radius: 14px 14px 14px 4px;
        border: 1px solid #e8ede8;
        color: #1a2a1a;
        box-shadow: 0 2px 16px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    .assistant-message:hover {
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    }
    
    /* ===== INPUT BOX ===== */
    .stChatInputContainer {
        border-radius: 14px !important;
        border: 2px solid #d5e0d5 !important;
        background: white !important;
        box-shadow: 0 2px 16px rgba(0,0,0,0.02) !important;
        transition: border-color 0.3s ease !important;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #2a7a1a !important;
        box-shadow: 0 0 0 4px rgba(42, 122, 26, 0.06) !important;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 14px 20px;
        background: linear-gradient(135deg, #0f2b1a 0%, #1a4d0e 100%);
        color: rgba(255, 213, 79, 0.4);
        border-top: 1px solid rgba(255, 213, 79, 0.04);
        font-size: 0.7rem;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        letter-spacing: 1.5px;
        z-index: 1000;
        backdrop-filter: blur(10px);
    }
    
    .footer span {
        color: #ffd54f;
        opacity: 0.5;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    
    ::-webkit-scrollbar-track {
        background: #e8efe8;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2a7a1a, #1a4d0e);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1a4d0e;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .main-header .logo {
            font-size: 1.8rem;
        }
        
        .main-header {
            padding: 20px;
        }
        
        .chat-message {
            padding: 12px 16px;
            margin: 8px 0;
        }
        
        .user-message {
            margin-left: 8px;
        }
        
        .assistant-message {
            margin-right: 8px;
        }
        
        .sidebar-box li {
            font-size: 0.8rem;
            padding: 8px 12px;
        }
    }
    
    /* ===== UTILITY ===== */
    .text-center { text-align: center; }
    .mt-1 { margin-top: 10px; }
    .mb-1 { margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
<div class="main-header">
    <div class="logo">🌾 Farm<span>Mate</span>AI</div>
    <div class="sub-title">Professional Agricultural Consultant • AI-Powered Guidance</div>
    <div class="badge-container">
        <span class="badge">{season_emoji} {current_season}</span>
        <span class="badge">🌱 30+ Crops</span>
        <span class="badge">📋 Expert Advice</span>
        <span class="badge">🤖 AI Assistant</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-box">
        <h3>🌱 About FarmMateAI</h3>
        <ul>
            <li>🌾 <b>Seasonal Crops</b> — What to plant now</li>
            <li>📋 <b>Crop Guides</b> — Soil, water, fertilizer</li>
            <li>🐛 <b>Pest Control</b> — Natural & chemical</li>
            <li>🌧️ <b>Weather Tips</b> — Season-wise advice</li>
            <li>🧑‍🌾 <b>Pro Tips</b> — For maximum yield</li>
        </ul>
        <div class="stats">
            {season_emoji} <strong>Current Season:</strong> {current_season} • {season_month}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Reset Button
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.quick_question = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button("🌾 Seasonal", use_container_width=True):
            st.session_state.quick_question = "Which crops should I plant this season?"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button("📋 Crop Guide", use_container_width=True):
            st.session_state.quick_question = "Give me complete guide for Wheat"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button("🐛 Pest Control", use_container_width=True):
            st.session_state.quick_question = "How to control pests naturally?"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button("🧑‍🌾 Pro Tips", use_container_width=True):
            st.session_state.quick_question = "Give me pro farming tips"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- SYSTEM PROMPT ---
def get_system_prompt():
    current_season, season_month, emoji = get_current_season()
    return f"""
You are FarmMateAI, a professional agricultural consultant with 20+ years of farming expertise.

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
- If user asks anything non-farming, politely say: "I'm only an agricultural consultant. Please ask me about crops, pests, seasons, fertilizers, and farming."

CURRENT SEASON: {current_season} ({season_month}) {emoji}
"""

# --- CROP DATABASE ---
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
🌾 **FarmMateAI - Complete Farming Guide**

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
    
    # Default - Short & Professional
    return """
🌾 **FarmMateAI - Agricultural Assistant**

✅ **I can help with:**
• Crop recommendations
• Complete crop guides (soil, water, fertilizer)
• Pest control solutions
• Seasonal farming tips

❌ **I don't know about:**
• Non-farming topics
• Weather forecasts
• Personal advice

📌 **Just ask me about farming!** 🌾
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
🌾 **Welcome to FarmMateAI!** 🌾

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
        with st.spinner("🌾 FarmMateAI is thinking..."):
            response = get_ai_response(st.session_state.messages)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# --- DISPLAY CHAT ---
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# --- USER INPUT ---
user_input = st.chat_input("💬 Type your farming question here...")

if user_input:
    if user_input.strip() == "":
        st.warning("🙏 Please type a question!")
    else:
        # ✅ ADD USER MESSAGE
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # ✅ DISPLAY USER MESSAGE
        with st.chat_message("user"):
            st.write(user_input)
        
        # ✅ GET AND DISPLAY BOT RESPONSE
        with st.chat_message("assistant"):
            with st.spinner("🌾 FarmMateAI is thinking..."):
                response = get_ai_response(st.session_state.messages)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- FOOTER ---
st.markdown("""
<div class="footer">
    🌾 FarmMateAI • <span>Professional Agricultural AI</span> • 30+ Crops • All Seasons
</div>
""", unsafe_allow_html=True)