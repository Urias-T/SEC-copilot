import streamlit as st

from copilot import get_response


st.set_page_config(page_title="SEC Copilot 🤖")

ss = st.session_state

with st.sidebar:
    with st.form("config"):
        st.header("Configuration")

        openai_api_key = st.text_input("Enter your OpenAI API key:", placeholder="sk-xxx", type="password")
        kay_api_key = st.text_input("Enter your Kay API key:", type="password")

        if st.form_submit_button("Submit"):
            if not (openai_api_key.startswith("sk-") and len(openai_api_key)==51):
                st.warning("The OpenAI API key you've entered is invalid!", icon="⚠️")
            else:
                st.success("Proceed to enter your query!", icon="👉")


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
        ss.messages = [{"role": "co-pilot", "message": "Hi, ask me any question about a company's SEC fillings."}]

    
    for message in ss.messages:
        with st.chat_message(message["role"]):
            st.write(message["message"])

    if query := st.chat_input(disabled=False):
        ss.messages.append({"role": "user", "message": query})

        with st.chat_message("user"):
            st.write(query)

    if ss.messages[-1]["role"] != "co-pilot":
        with st.chat_message("Co-pilot"):
            with st.spinner("Thinking..."):
                answer, chat_history = get_response(query, ss.configurations, ss.chat_history)

                placeholder = st.empty()
                full_answer = ''
                for item in answer:
                    full_answer += item
                    placeholder.markdown(full_answer)
                placeholder.markdown(full_answer)

                ss.chat_history = chat_history
                ss.messages.append({"role": "co-pilot", "message": full_answer})

