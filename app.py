"""
KisaanMitra - Agricultural Assistant Bot
A chatbot for farmers to get crop, pest, and weather advice
"""

import streamlit as st
import os
from dotenv import load_dotenv
import time

# .env file load karein
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="KisaanMitra 🌾",
    page_icon="🌾",
    layout="centered"
)

# --- CUSTOM CSS FOR FARMING THEME ---
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
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
        st.rerun()



# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are KisaanMitra, a helpful agricultural assistant for farmers.

Your role:
- Help farmers with crop recommendations (which crop to grow in which season)
- Provide pest control advice (how to protect crops from insects/diseases)
- Give weather-related farming suggestions (what to do before/after rain)
- Answer general farming questions (soil, fertilizers, irrigation)

Your boundaries:
- ONLY answer agriculture/farming related questions
- If asked about anything else, say: "Main sirf kheti-baari ke baare mein jaanta hun. Aap mujhse crop recommendations, pests, ya weather ke baare mein pooch sakte hain."

Tone: Friendly, respectful, and encouraging. Use simple Hindi/Urdu/English language that farmers can easily understand.

Important: Always be helpful and give practical, actionable advice.
"""

# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    # Welcome message
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

# --- USER INPUT ---
def get_ai_response(messages):
    """Get response from AI using Groq API"""
    try:
        from groq import Groq
        
        # Groq client initialize
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            return """
            ⚠️ API Key not found!
            
            Please:
            1. Get API key from Groq
            2. Add it to .env file
            3. Or use alternative API
            
            🌾 Main ready hun aapki madad karne ke liye!
            """
        
        
        groq_api_key = st.secrets["GROQ_API_KEY"]
        
        # Convert messages to Groq format
        groq_messages = []
        for msg in messages:
            if msg["role"] == "system":
                groq_messages.append({"role": "system", "content": msg["content"]})
            elif msg["role"] == "user":
                groq_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                groq_messages.append({"role": "assistant", "content": msg["content"]})
        
        # Get response
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=groq_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg:
            return """
            🔑 API Key Error!
            
            Please check:
            1. .env file mein GROQ_API_KEY set hai?
            2. Key sahi copy ki hai?
            
            🌾 Tab tak main aapko basic advice de sakta hun!
            """
        else:
            return f"""
            ⚠️ Kuch technical issue aa gaya!
            
            Error: {error_msg}
            
            Please try again later. 🌾
            """

# --- INPUT HANDLING ---
user_input = st.chat_input("💬 Apna sawaal likhein...")

if user_input:
    # Empty input check
    if user_input.strip() == "":
        st.warning("🙏 Kuch sawaal likhein!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(f"""
            <div class="chat-message user-message">
                🧑‍🌾 {user_input}
            </div>
            """, unsafe_allow_html=True)
        
        # Get and display AI response
        with st.chat_message("assistant"):
            with st.spinner("🌾 KisaanMitra soch raha hai..."):
                response = get_ai_response(st.session_state.messages)
                
                # Fallback check: agar API kaam na kare
                if "API Key" in response or "error" in response.lower():
                    # Basic fallback responses
                    if "crop" in user_input.lower() or "fasal" in user_input.lower():
                        response = """
                        🌾 Fasal ki baat kar rahe hain!
                        
                        Kuch common faslein:
                        🌱 Wheat - November mein lagayein, March mein katein
                        🌾 Rice - June-July mein lagayein, October mein katein
                        🌽 Corn - March mein lagayein, July mein katein
                        
                        Kis fasal ke baare mein jaanna chahenge? 😊
                        """
                    elif "pest" in user_input.lower() or "keeda" in user_input.lower():
                        response = """
                        🐛 Keedon se bachav!
                        
                        Common remedies:
                        🌿 Neem oil spray - 2ml per liter pani
                        🧅 Garlic + chili spray - natural solution
                        🧪 Commercial pesticides - dealer se lein
                        
                        Kaunsi fasal mein keeda hai? 😊
                        """
                    else:
                        response = """
                        🌾 KisaanMitra yahan hai!
                        
                        Main madad kar sakta hun:
                        🌱 Konsi fasal lagayein?
                        🐛 Keedon se kaise bachein?
                        🌧️ Mausam ka kya karein?
                        🧑‍🌾 Kheti ke tips?
                        
                        Koi sawaal poochhein! 😊
                        """
                
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    🌾 {response}
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- FOOTER ---
st.markdown("""
<div style="
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    text-align: center;
    padding: 10px;
    background: #2d5016;
    color: white;
    font-size: 0.8rem;
    border-top: 2px solid #4a7c2e;
">
    🌾 KisaanMitra v1.0 • Made with ❤️ for Farmers • Always here to help!
</div>
""", unsafe_allow_html=True)