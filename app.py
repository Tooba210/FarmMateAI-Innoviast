"""
KisaanMitra - Agricultural Assistant Bot
A chatbot for farmers to get crop, pest, and weather advice
"""

import streamlit as st
import os
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="KisaanMitra 🌾",
    page_icon="🌾",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .main-header {
        background: linear-gradient(135deg, #2d5016 0%, #4a7c2e 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 2.5rem;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sub-header {
        text-align: center;
        color: #2d5016;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
    }
    .user-message {
        background: #e8f5e9;
        border-left: 4px solid #2d5016;
    }
    .assistant-message {
        background: #f1f8e9;
        border-left: 4px solid #4a7c2e;
    }
    .sidebar-box {
        background: linear-gradient(135deg, #2d5016 0%, #4a7c2e 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin-bottom: 10px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #4a9e30 0%, #2d7a1a 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(45, 122, 26, 0.4);
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 12px;
        background: linear-gradient(135deg, #2d5016 0%, #4a7c2e 100%);
        color: white;
        font-size: 0.8rem;
        border-top: 3px solid #ffd54f;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="main-header">
    🌾 KisaanMitra
</div>
<div class="sub-header">
    Aapka Agricultural Assistant 🤖
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-box">
        <h3>🌱 About KisaanMitra</h3>
        <p>Main aapki madad kar sakta hun:</p>
        <ul>
            <li>🌾 Crop recommendations</li>
            <li>🐛 Pest control advice</li>
            <li>🌧️ Weather tips</li>
            <li>🧑‍🌾 Farming guidance</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.quick_question = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Questions")
    
    # Quick question buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌾 Wheat", use_container_width=True):
            st.session_state.quick_question = "Wheat ki kheti kab aur kaise karein?"
            st.rerun()
            
    with col2:
        if st.button("🐛 Pest Control", use_container_width=True):
            st.session_state.quick_question = "Fasal mein keedon se kaise bachein?"
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🌧️ Weather Tips", use_container_width=True):
            st.session_state.quick_question = "Barish se pehle kheti mein kya karein?"
            st.rerun()
            
    with col4:
        if st.button("🧑‍🌾 General Tips", use_container_width=True):
            st.session_state.quick_question = "Kheti ke liye kuch general tips dein?"
            st.rerun()

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are KisaanMitra, an expert agricultural assistant for farmers.

You provide specific, practical advice about:
- Crop recommendations (which crop, when, how)
- Pest control (natural and chemical solutions)
- Weather-related farming tips
- Soil management and fertilizers
- General farming guidance

Always give direct, specific answers. Never give generic responses like "How can I help you?".

If asked about non-farming topics, say: "Main sirf kheti-baari ke baare mein jaanta hun. Aap mujhse crops, pests, weather, ya farming ke baare mein pooch sakte hain."

Use simple language that farmers can easily understand. Be encouraging and practical.
"""

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    welcome = """
    🌾 Assalam-o-Alaikum! Main KisaanMitra hun!

    Main aapki madad kar sakta hun:
    🌱 Konsi fasal kab lagayein
    🐛 Keedon se bachav ke upay
    🌧️ Mausam ke mutabiq kheti
    🧑‍🌾 Kheti-baari ke masail

    Kya sawaal hai aapka? 😊
    """
    st.session_state.messages.append({"role": "assistant", "content": welcome})

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None

# --- LOAD CROP DATA ---
def load_crop_data():
    """Load crop data from JSON file"""
    try:
        with open('crops.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"crops": []}
    except Exception as e:
        st.error(f"Error loading crop data: {e}")
        return {"crops": []}

# --- FIND CROP FUNCTION ---
def find_crop(crop_name):
    """Search for crop by name"""
    data = load_crop_data()
    crops = data.get("crops", [])
    
    crop_name = crop_name.lower().strip()
    
    for crop in crops:
        if crop_name in crop["name"].lower():
            return crop
    return None

# --- FALLBACK RESPONSE ---
def fallback_response(user_message):
    """Provide fallback response based on keywords"""
    user_message = user_message.lower()
    
    # Crop related questions
    if any(word in user_message for word in ['crop', 'fasal', 'kheti', 'plant', 'sow', 'lagayein', 'konsi', 'kaunsi']):
        return """
🌾 **Fasal ki baat kar rahe hain!**

Yahan kuch common faslain hain:

| **Fasal** | **Season** | **Soil** | **Temperature** |
|-----------|------------|----------|-----------------|
| 🌾 Wheat | Winter (Nov-Mar) | Loamy soil | 15-20°C |
| 🌾 Rice | Monsoon (Jun-Oct) | Clay soil | 25-30°C |
| 🌽 Corn | Spring (Mar-Jul) | Well-drained loam | 20-30°C |
| 🌿 Cotton | Summer (Apr-Nov) | Black soil | 25-35°C |
| 🥔 Potato | Winter (Oct-Jan) | Sandy loam | 15-20°C |

Kis fasal ke baare mein jaanna chahenge? 😊
"""
    
    # Pest related questions
    elif any(word in user_message for word in ['pest', 'keeda', 'insect', 'bug', 'spray', 'dawa', 'medicine', 'killer']):
        return """
🐛 **Keedon se bachav ke upay:**

🌿 **Natural Remedies:**
• Neem oil spray (2ml per liter pani) - best for most pests
• Garlic + chili solution - natural insecticide
• Soap water spray - kills soft-bodied insects

🧪 **Chemical Methods:**
• Commercial pesticides (dealer se lein)
• Follow instructions carefully
• Use protective gear when applying

🛡️ **Prevention:**
• Regular field inspection
• Crop rotation every season
• Remove infected plants immediately

Kaunsi fasal mein keeda hai? 😊
"""
    
    # Weather related questions
    elif any(word in user_message for word in ['weather', 'mausam', 'rain', 'barish', 'sun', 'dhup', 'temperature']):
        return """
🌧️ **Mausam ke mutabiq kheti:**

☀️ **Garam mausam (Summer):**
• Zyada pani dein (2-3 times a week)
• Morning/evening mein kaam karein
• Crops ko shade dein if possible
• Use mulch to keep soil cool

🌧️ **Barish ka mausam (Monsoon):**
• Drainage system check karein
• Fertilizer barish se pehle na daalein
• Rice (Chawal) ke liye best season

❄️ **Thand ka mausam (Winter):**
• Watering reduce karein (once a week)
• Protect from frost
• Wheat and potato ke liye best season

Kya aap ko specific weather advice chahiye? 😊
"""
    
    # Fertilizer/soil related
    elif any(word in user_message for word in ['fertilizer', 'soil', 'mitti', 'khad', 'compost', 'manure']):
        return """
🧑‍🌾 **Soil aur Fertilizer ka management:**

🌱 **Best Fertilizers:**
• NPK (Nitrogen, Phosphorus, Potassium) - all-purpose
• Organic compost - natural and safe
• Cow manure - improves soil texture

🪴 **Soil Health Tips:**
• Soil test karein every season
• Add organic matter regularly
• Crop rotation - soil nutrients balance rakhein

Kis crop ke liye fertilizer chahiye? 😊
"""
    
    # General farming
    elif any(word in user_message for word in ['help', 'madad', 'guide', 'tips', 'advice', 'suggest']):
        return """
🌾 **KisaanMitra yahan hai!**

Main madad kar sakta hun:
🌱 **Crop:** Konsi fasal, kab, kaise?
🐛 **Pest:** Keedon se kaise bachein?
🌧️ **Weather:** Mausam ka kya karein?
🧑‍🌾 **General:** Soil, fertilizer, irrigation?

Koi specific sawaal poochhein! 😊
"""
    
    # Greeting
    elif any(word in user_message for word in ['hi', 'hello', 'hey', 'salam', 'assalam', 'good morning', 'good evening']):
        return """
🌾 Assalam-o-Alaikum! Main KisaanMitra hun!

Main aapki madad kar sakta hun:
🌱 Konsi fasal kab lagayein
🐛 Keedon se bachav ke upay
🌧️ Mausam ke mutabiq kheti
🧑‍🌾 Kheti-baari ke masail

Kya sawaal hai aapka? 😊
"""
    
    # Default fallback
    else:
        return """
🌾 **KisaanMitra yahan hai!**

Main madad kar sakta hun:
🌱 Crop recommendations
🐛 Pest control tips  
🌧️ Weather advice
🧑‍🌾 General farming guidance

Koi specific sawaal poochhein! 😊

**Example questions:**
• "Wheat ki kheti kab karein?"
• "Keedon se kaise bachein?"
• "Barish se pehle kya karein?"
• "Konsi fasal zyada faida deti hai?"
"""

# --- GET AI RESPONSE ---
def get_ai_response(messages):
    """Get response from AI using Groq API"""
    try:
        from groq import Groq
        
        # API key read karne ka safe tareeqa
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
        
        # Convert messages to Groq format
        groq_messages = []
        for msg in messages:
            if msg["role"] == "system":
                groq_messages.append({"role": "system", "content": msg["content"]})
            elif msg["role"] == "user":
                groq_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                groq_messages.append({"role": "assistant", "content": msg["content"]})
        
        # Get response from Groq
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=groq_messages,
            temperature=0.7,
            max_tokens=600
        )
        
        response = completion.choices[0].message.content
        
        # Agar response empty hai toh fallback
        if not response or len(response.strip()) < 5:
            user_message = messages[-1]["content"] if messages else ""
            return fallback_response(user_message)
        
        return response
        
    except Exception as e:
        user_message = messages[-1]["content"] if messages else ""
        return fallback_response(user_message)

# --- DISPLAY CHAT HISTORY ---
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

# --- QUICK QUESTION HANDLING ---
if st.session_state.quick_question:
    question = st.session_state.quick_question
    st.session_state.quick_question = None
    
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("assistant"):
        with st.spinner("🌾 KisaanMitra soch raha hai..."):
            response = get_ai_response(st.session_state.messages)
            st.markdown(f"""
            <div class="chat-message assistant-message">
                🌾 {response}
            </div>
            """, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# --- USER INPUT ---
user_input = st.chat_input("💬 Apna sawaal likhein...")

if user_input:
    if user_input.strip() == "":
        st.warning("🙏 Kuch sawaal likhein!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(f"""
            <div class="chat-message user-message">
                🧑‍🌾 {user_input}
            </div>
            """, unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            with st.spinner("🌾 KisaanMitra soch raha hai..."):
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
    🌾 KisaanMitra v1.0 • Made with ❤️ for Farmers • Always here to help!
</div>
""", unsafe_allow_html=True)