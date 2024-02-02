import os
import logging
import streamlit as st

from copilot import get_response

app_logger = logging.getLogger("app")
app_logger.setLevel(logging.ERROR)

console_handler = logging.StreamHandler()
app_logger.addHandler(console_handler)


st.set_page_config(page_title="SEC Copilot 🤖")

st.title("SEC Copilot 🤖")

ss = st.session_state

github_url = "https://github.com/Urias-T/SEC-copilot"
twitter_url = "https://twitter.com/mista_triumph"
linkedin_url = "https://www.linkedin.com/in/triumph-urias/"


openai_api_key = os.environ.get("OPENAI_API_KEY")
kay_api_key = os.environ.get("KAY_API_KEY")


if not openai_api_key or not kay_api_key:
    app_logger.info("Did not find OpenAI and KayAI API keys in environment variables.")
    with st.sidebar:
        with st.form("config"):
            st.header("Configuration")

            openai_api_key = st.text_input("Enter your OpenAI API key:", placeholder="sk-xxx", type="password")
            kay_api_key = st.text_input("Enter your Kay API key:", type="password")

            st.markdown("Get your OpenAI API key [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)")
            st.markdown("Get your KAY API key [here](https://kay.ai/)")

            st.sidebar.markdown(" ")

            st.sidebar.markdown("-------------------")

            st.sidebar.markdown(" ")

            if st.form_submit_button("Submit"):
                if not (openai_api_key.startswith("sk-") and len(openai_api_key)==51):
                    st.warning("The OpenAI API key you've entered is invalid!", icon="⚠️")
                    validated = False
                else:
                    st.success("Proceed to enter your query!", icon="👉")
                    validated = True

                if validated:
                    ss.configurations = {
                        "openai_api_key": openai_api_key,
                        "kay_api_key": kay_api_key
                    }


if ("OPENAI_API_KEY" in os.environ) and ("KAY_API_KEY" in os.environ):
    app_logger.info("Found OpenAI and KAY_API_KEY in environment variables.")

    ss.configurations = {
        "openai_api_key": openai_api_key,
        "kay_api_key": kay_api_key
    }

info_placeholder = st.empty()
info_placeholder.text("Enter valid API keys before you can use the app.")

if "configurations" in ss:
    info_placeholder.empty()

    if "messages" not in ss:
        ss.chat_history = []
        ss.messages = [{"role": "co-pilot", "message": "Hi, ask me any question about a company's SEC fillings or stock prices. \
                            You could also choose from any of these sample questions:"}]

    if "messages" in ss:
        def clear_chat_history():
            ss.chat_history = []
            ss.messages = [{"role": "co-pilot", "message": "Hi, ask me any question about a company's SEC fillings or stock prices. \
                            You could also choose from any of these sample questions:"}]
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    for message in ss.messages:
        with st.chat_message(message["role"]):
            st.write(message["message"])

    if query := st.chat_input(disabled=False):
        ss.messages.append({"role": "user", "message": query})

        with st.chat_message("user"):
            st.write(query)

    buttons = []
    placeholders = []

    button_info = [
        {"label": "What are the patterns in Nvidia's spend over the past three quarters?", "query": "What are the patterns in Nvidia's spend over the past three quarters?"},
        {"label": "Show me the financial statment for Amazon.", "query": "Show me the financial statment for Amazon."},
        {"label": "What is Tesla's current stock price?", "query": "What is Tesla's current stock price?"}
    ]

    for info in button_info:
        button_placeholder = st.empty()
        buttons.append({"placeholder": button_placeholder, "label": info["label"], "query": info["query"]})

    if len(ss.messages) == 1:
        button_clicked = False
        for button in buttons:
            if button["placeholder"].button(button["label"]):
                query = button["query"]
                ss.messages.append({"role": "user", "message": button["query"]})

                with st.chat_message("user"):
                    st.write(query)
                
                button_clicked = True

        if button_clicked:
            for button in buttons:
                button["placeholder"].empty()

    if ss.messages[-1]["role"] != "co-pilot":
        with st.chat_message("Co-pilot"):
            with st.spinner("Thinking..."):
                answer, chat_history = get_response(query, ss.configurations, ss.chat_history)

                if "error_message" in ss:
                    st.error(ss.error_message)

                    if st.button("Retry"):
                        del ss["error_message"]
                        ss.chat_history = ss.chat_history[:-1]
                        query = ss.messages[-1]["message"]
                        answer, chat_history = get_response(query, ss.configurations, ss.chat_history)

                if answer is not None:
                    placeholder = st.empty()
                    full_answer = ''
                    for item in answer:
                        full_answer += item
                        placeholder.markdown(full_answer)
                    placeholder.markdown(full_answer)

                    ss.chat_history = chat_history
                    ss.messages.append({"role": "co-pilot", "message": full_answer})

with st.sidebar:
    with st.sidebar.expander("📬 Contact"):

        st.write("**Website:**", "[triumphurias.com](https://triumphurias.com)")
        st.write("**GitHub:**", f"[Urias-T/SEC-copilot]({github_url})")
        st.write("**Twitter:**", f"[@mista_triumph]({twitter_url})")
        st.write("**LinkedIn:**", f"{linkedin_url}")
        st.write("**Mail:**", "triumph@triumphurias.com")
        st.write("**Created by Triumph Urias**")

