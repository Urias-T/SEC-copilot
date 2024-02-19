import logging
copilot_logger = logging.getLogger("copilot")
copilot_logger.setLevel(logging.ERROR)

console_handler = logging.StreamHandler()
copilot_logger.addHandler(console_handler)

import streamlit as st
ss = st.session_state

# For debugging and local experimentation

# import langchain
# langchain.debug=True

from utils.prompts import react_prompt

from langchain_openai import ChatOpenAI

from langchain.agents import create_react_agent, AgentExecutor

from openai._exceptions import RateLimitError

from utils.tools import (
    retrieval_tool, get_current_stock_price
)

from chat.memory import create_react_agent_memory


def get_response(query, configurations, chat_history):

    if "error_message" in ss:
        del ss["error_message"]
        query = ss.messages[-1]["message"]


    model = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=configurations["openai_api_key"])

    tools = [get_current_stock_price, retrieval_tool]

    agent = create_react_agent(
        llm=model,
        tools=tools,
        prompt=react_prompt
    )

    memory = create_react_agent_memory(chat_history=chat_history)

    agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True)

    try:
        final_output = agent_executor.invoke(
                                                {
                                                    "input": query,
                                                    "chat_history": memory
                                                }
                                            )
        
        if final_output["output"] is not None:
            chat_history.append((query, final_output["output"]))

        else:
            pass

        return final_output["output"], chat_history

    except RateLimitError as e:
        copilot_logger.error("OpenAI RateLimitError")
        ss.error_message = f"Your Copilot encountered an OpenAI Rate Limit Error. Please check your \
                            OpenAI plan and billing details."
        
        return None, None


