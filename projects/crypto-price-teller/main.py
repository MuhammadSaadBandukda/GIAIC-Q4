import streamlit as st
from agents import Agent, Runner
from agents.tool import function_tool
from connection import config
import asyncio, requests

st.header("Crypto Price Teller")
st.write("Enter the symbol to check the price")
def run_async(func, *args, **kwargs):
    try:
        return asyncio.run(func(*args, **kwargs))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(func(*args, **kwargs))

@function_tool
def crypto_price_teller(symbol: str):
    """Get the symbol of crypto currency and return the price"""
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    response = requests.get(url)
    if response.status_code != 200:
        return "❌ Error: Invalid or unsupported cryptocurrency symbol."
    try:
        result: dict = response.json()
        return result.get('price', "❌ Price not found")
    except Exception as e:
        return f"❌ An error occurred: {e}"

crypto_agent = Agent(
    name="Crypto Price Teller",
    instructions="""
    You are a cryptocurrency assistant. When the user asks for a crypto price, use the 'crypto_price_teller' tool.
    Keep your responses short and to the point. Use symbols like BTCUSDT, ETHUSDT, etc.
    """,
    tools=[crypto_price_teller]
)

# Maintain prompt state if needed
if "prompt" not in st.session_state:
    st.session_state.prompt = ""

prompt = st.text_input(
    label="Your Prompt",
    placeholder="Ask cryptocurrency related questions here",
    value=st.session_state.prompt
)
st.session_state.prompt = prompt

if st.button(label="Submit"):
    result = run_async(
        Runner.run,
        crypto_agent,
        input=prompt,
        run_config=config
    )
    st.success(result.final_output)

if st.button("Refresh"):
    st.rerun()
