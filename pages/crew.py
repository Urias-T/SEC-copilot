import streamlit as st

from app import login
from streamlit.errors import StreamlitAPIException

ss = st.session_state


st.title("SEC Copilot Crew 🧑‍💻")


github_url = "https://github.com/Urias-T/SEC-copilot"
twitter_url = "https://twitter.com/mista_triumph"
linkedin_url = "https://www.linkedin.com/in/triumph-urias/"


# info_placeholder = None

if "configurations" not in ss:
    try:
        info_placeholder = login()

    except StreamlitAPIException:
        pass

else:

    from crew.main import CopilotCrew

    company = st.text_input("What company do you want to research?")
    if company:
        with st.spinner("Researching..."):
            crew = CopilotCrew(company)
            result = crew.run()

            if (result is None) and ("error_message" in ss):
                st.error(ss.error_message)

            st.markdown(result)

with st.sidebar:
    with st.sidebar.expander("📬 Contact"):

        st.write("**Website:**", "[triumphurias.com](https://triumphurias.com)")
        st.write("**GitHub:**", f"[Urias-T/SEC-copilot]({github_url})")
        st.write("**Twitter:**", f"[@mista_triumph]({twitter_url})")
        st.write("**LinkedIn:**", f"{linkedin_url}")
        st.write("**Mail:**", "triumph@triumphurias.com")
        st.write("**Created by Triumph Urias**")

    st.markdown("*SEC Copilot might display inaccurate information. It is therefore important to verify its responses.*")
