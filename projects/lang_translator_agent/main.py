from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,Runner  # Assuming this handles translation logic
# from dotenv import load_dotenv
import streamlit as st
import json
import os

st.set_page_config(page_title="TransBot", layout="centered")

import asyncio

def run_async(func, *args, **kwargs):
    try:
        return asyncio.run(func(*args, **kwargs))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(func(*args, **kwargs))



# load_dotenv()
gemini_api_key = st.secrets["GEMINI_API_KEY"]
# gemini_api_key = os.getenv('GEMINI_API_KEY')
if not gemini_api_key:
    st.write("Unable to access LLM")



external_client = AsyncOpenAI( 
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model = model,
    model_provider=external_client,
    tracing_disabled=True
)



#Title
st.markdown("## 🗣️ Language Translator (Chatbot Version)")
st.markdown("#### Translate 600+ languages")



# Load language list
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
lang_path = os.path.join(BASE_DIR, 'languages.json')

with open(lang_path, 'r', encoding='utf-8') as f:
    data = json.load(f)




# Convert JSON to language list
languages = [data[k] for k in data]



# Layout for language selection
# Store selected language in session state to detect changes
if "selected_language" not in st.session_state:
    st.session_state.selected_language = None

# Language selection
language = st.selectbox(
    label="From which language you want to translate",
    options=languages,
    index=languages.index(st.session_state.selected_language)
    if st.session_state.selected_language in languages else 0
)

# Check for language change
if language != st.session_state.selected_language:
    st.session_state.selected_language = language
    st.session_state.messages = []  # Clear previous chat
    st.rerun()  # Rerun the app to refresh the UI


translator_agent = Agent(
    name = "language translator",
    instructions=f"""
    You are a professional language translator. 
Translate the user's prompt from the detected input language into '{language}' in two ways:
Native language: In the translatd native script.
Roman Version(if possible oterwise skip): In the Romanized version.
Respond only with the translations, no extra commentary.
    """
)
with st.chat_message('assistant'):
    st.markdown(f"Hey there! 👋 I'm your translation assistant. I'll translate your text into **{language}**, Type below to begin! ")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []
# st.write(st.session_state.messages)
# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Translate your text here...")
if user_input:
    # Save user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = run_async(
    Runner.run,
    translator_agent,
    input=user_input,
    run_config=config
)
    # Dummy translation logic (replace with your actual Agent logic)
    translated_text = response.final_output
    # Example if using Agent:
    # translated_text = Agent.translate(user_input, from_language, to_language)

    # Save assistant's response
    st.session_state.messages.append({"role": "assistant", "content": translated_text})
    with st.chat_message("assistant"):
        st.markdown(translated_text)
