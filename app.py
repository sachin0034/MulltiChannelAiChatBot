import pickle
from pathlib import Path
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

load_dotenv()

# Set page configuration
st.set_page_config(page_title="Streaming bot", page_icon="🤖")

# --- USER AUTHENTICATION ---
names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

icator = stauth.Authenticate(names, usernames, hashed_passwords,
        'starshadow ai bot', 'abcd', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.title("StarShadow Chat Bot")
    st.sidebar.title("StarShadow Chat Bot")

    # Define channels with icons
    channels = [
        {"name": "News Channel", "icon": "📺"},
        {"name": "Discussion Channel", "icon": "💬"},
        {"name": "Gaming Channel", "icon": "🎮"},
        {"name": "Tech Channel", "icon": "🌐"},
        {"name": "Cooking Channel", "icon": "🍜"}
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
