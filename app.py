import os
import logging
import streamlit as st

app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)


st.set_page_config(page_title="SEC Copilot 🤖")

st.title("SEC Copilot 🤖")

ss = st.session_state

app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)

github_url = "https://github.com/Urias-T/SEC-copilot"
twitter_url = "https://twitter.com/mista_triumph"
linkedin_url = "https://www.linkedin.com/in/triumph-urias/"


def login():

    openai_api_key = os.environ.get("OPENAI_API_KEY")
    kay_api_key = os.environ.get("KAY_API_KEY")

    if not openai_api_key or not kay_api_key:
        app_logger.info("Did not find OpenAI and KayAI API keys in environment variables.")
        # with st.sidebar:
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
                    st.success("Proceed to use either the chat or crew options", icon="👈")
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

    return info_placeholder

if "configurations" not in ss:
    login()

else:
    st.markdown("You're already logged in. Use one of either chat or crew in the options.")


with st.sidebar:
    with st.sidebar.expander("📬 Contact"):

        st.write("**Website:**", "[triumphurias.com](https://triumphurias.com)")
        st.write("**GitHub:**", f"[Urias-T/SEC-copilot]({github_url})")
        st.write("**Twitter:**", f"[@mista_triumph]({twitter_url})")
        st.write("**LinkedIn:**", f"{linkedin_url}")
        st.write("**Mail:**", "triumph@triumphurias.com")
        st.write("**Created by Triumph Urias**")

