import pickle
from pathlib import Path
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Set page configuration
st.set_page_config(page_title="Streaming bot", page_icon="🤖")

# ---- SIDEBAR ----
st.title("StarShadow Chat Bot")
st.sidebar.title("StarShadow Chat Bot")

# Define channels with icons and hint prompts
channels = [
    {"name": "Travel Channel", "icon": "✈️", "hints": [{"text": "Tell some places for dream destination?", "style": "box"}, {"text": "Share me the best sunset tarvel place in the world", "style": "box"},{"text": "What is the best season to visit New York?", "style": "box"},{"text": "What are some tips for budget travel?", "style": "box"}]},
    {"name": "Business Channel", "icon": "💬", "hints": [{"text": "What's the latest business trend?", "style": "box"}, {"text": "Discuss a successful business strategy.", "style": "box"},{"text": "What are some effective communication skills in business?", "style": "box"},{"text": "What are some tips for negotiating a better deal?", "style": "box"}]},
    {"name": "Gaming Channel", "icon": "🎮", "hints": [{"text": "Tell me something about PUBG", "style": "box"}, {"text": "Share some tips and tricks for PUBG", "style": "box"},{"text": "What are some popular multiplayer games?", "style": "box"},{"text": "What are some upcoming video game releases?", "style": "box"}]},
    {"name": "Tech Channel", "icon": "🌐", "hints": [{"text": "What's the most exciting tech news?", "style": "box"}, {"text": "Can you explain AI?", "style": "box"},{"text": "What are some emerging technologies in software development?", "style": "box"},{"text": "What are some tips for securing my personal data online?", "style": "box"}]},
    {"name": "Food Channel", "icon": "🍜", "hints": [{"text": "How can I make Pasta?", "style": "box"}, {"text": "I'm getting bored, tell me what food I should eat to make myself feel good.", "style": "box"},{"text": "What are some healthy meal options for breakfast?", "style": "box"},{"text": "What are some popular food trends?", "style": "box"}]}
]

# Display channels in the sidebar with borders, border radius, and gap between channels
selected_channel = st.sidebar.selectbox("Select Channel", [channel["name"] for channel in channels])
for channel in channels:
    if channel["name"] == selected_channel:
        st.sidebar.markdown(
            f"""
            <div class="animated-channel" style="border: 2px solid white; border-radius: 10px; padding: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px grey; background-color: black; color: white;">
                <span style="font-size: large;">{channel["icon"]} {channel["name"]}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Display hint prompts above the chat box
        st.markdown(f"**Hints:**", unsafe_allow_html=True)
        for hint in channel['hints']:
            if hint['style'] == 'box':
                st.markdown(f"<div class='hint-box'>{hint['text']}</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown(
            f"""
            <div class="animated-channel" style="border: 2px solid white; border-radius: 10px; padding: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px grey;">
                <span style="font-size: large;">{channel["icon"]} {channel["name"]}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# Add animation CSS
st.markdown("""
<style>
@keyframes slideIn {
from {
    transform: translateY(-20px);
    opacity: 0;
}
to {
    transform: translateY(0);
    opacity: 1;
}
}

.animated-channel {
animation: slideIn 0.5s forwards;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.hint-box {
    border: 2px solid white;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 2px 2px 5px grey;
    background-color: black;
    color: white;
    text-shadow: 2px 2px 5px grey;
}
</style>
""", unsafe_allow_html=True)


def get_response(user_query, chat_history):
    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# Session state initialization
if "channel_chat_history" not in st.session_state:
    st.session_state.channel_chat_history = {channel["name"]: [AIMessage(content="Hello, I am a bot. How can I help you?")] for channel in channels}

# Get or initialize chat history for the selected channel
chat_history = st.session_state.channel_chat_history.get(selected_channel, [])

# Conversation history
for message in chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# User input 
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.channel_chat_history[selected_channel].append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, chat_history))

    st.session_state.channel_chat_history[selected_channel].append(AIMessage(content=response))
