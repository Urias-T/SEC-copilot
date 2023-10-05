import os
import streamlit as st


st.set_page_config(page_title="SEC Copilot 🤖")

with st.sidebar:
    st.title("SEC Copilot 🤖")
    if ("OPENAI_API_KEY" in st.secrets) and ("KAY_API_KEY" in st.secrets):
        st.success("All API keys have been provided!", icon="✅")
    else:
        openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")
        kay_api_key = st.text_input("Enter your Kay API key:", type="password")

        if not (openai_api_key.startswith("sk-") and len(openai_api_key)==51):
            st.warning("The OpenAI API key you've entered is invalid!", icon="⚠️")
        else:
            st.success("Proceed to enter your query!", icon="👉")

    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["KAY_API_KEY"] = kay_api_key

    

