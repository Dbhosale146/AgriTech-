import streamlit as st
import time
from app.chat_utils import get_chat_model, ask_chat_model
from app.config import EURI_API_KEY

# Page config
st.set_page_config(
    page_title="🌱 AgroBot - Farmer Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2e7d32;
        color: white;
    }
    .chat-message.assistant {
        background-color: #f1f8e9;
        color: black;
    }
    .stButton > button {
        background-color: #388e3c;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_model" not in st.session_state:
    st.session_state.chat_model = get_chat_model(EURI_API_KEY)

# Header
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #2e7d32; font-size: 3rem; margin-bottom: 0.5rem;">🌱 AgroBot</h1>
    <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
        Your Intelligent Farming Assistant 🌾<br>
        Ask me about crops, fertilizers, pests, and best practices!
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar (extras)
with st.sidebar:
    st.markdown("### 🌿 Quick Options")
    crop_choice = st.selectbox("Select a crop", ["🌾 Wheat", "🌽 Maize", "🥔 Potato", "🍅 Tomato", "🍚 Rice", "Other"])
    st.markdown("You can ask me about diseases, fertilizers, or weather tips for your crop.")

# Display chat history
st.markdown("### 💬 Chat with AgroBot")
for message in st.session_state.messages:
    role = message["role"]
    with st.chat_message(role):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Chat input
if prompt := st.chat_input("Ask AgroBot anything about farming..."):
    # Add user message
    timestamp = time.strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt, 
        "timestamp": timestamp
    })
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🌾 Thinking..."):
            system_prompt = f"""
            You are AgroBot, a friendly farming assistant. 
            Provide accurate, simple, and practical advice for farmers in India.
            Be conversational and supportive. 
            Crop selected by user: {crop_choice}
            
            User Question: {prompt}
            
            Answer:
            """
            response = ask_chat_model(st.session_state.chat_model, system_prompt)
        
        st.markdown(response)
        st.caption(timestamp)
        
        # Save assistant reply
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response, 
            "timestamp": timestamp
        })

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🤖 Powered by Euri AI | 🌱 Helping Farmers Grow Better</p>
</div>
""", unsafe_allow_html=True)
