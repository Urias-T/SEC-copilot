import streamlit as st

from app import login
from crew.main import CopilotCrew
from streamlit.errors import StreamlitAPIException

ss = st.session_state


st.markdown("This is the Crew Page.")

try:
    info_placeholder = login()

except StreamlitAPIException:
    pass

if "configurations" in ss:
    info_placeholder.empty()
    # st.markdown()
    company = st.text_input("What company do you want to research?")
    if company:
        crew = CopilotCrew(company)
        result = crew.run()
        st.markdown(result)
