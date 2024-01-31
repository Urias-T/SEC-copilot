import os
import streamlit as st
import requests

import logging
copilot_logger = logging.getLogger("copilot")
copilot_logger.setLevel(logging.ERROR)

from langchain.agents import Tool
from langchain.tools import tool

from langchain_openai import ChatOpenAI

from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser

from langchain_community.tools import DuckDuckGoSearchRun

from pydantic.v1 import BaseModel, Field

import yfinance as yf

from prompts import prompt

# from dotenv import load_dotenv
# load_dotenv()

# openai_api_key = os.environ.get("OPENAI_API_KEY")
# kay_api_key = os.environ.get("KAY_API_KEY")

ss = st.session_state


model = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=ss.configurations["openai_api_key"])


class CurrentStockPriceInput(BaseModel):
    symbol: str = Field(..., description="The ticker symbol for the company whose stock price is to be checked.")


@tool(args_schema=CurrentStockPriceInput)
def get_current_stock_price(ticker: str) -> str:
    """Call this function with only a company's ticker symbol, to get the current stock price for the company."""
    stock_info = yf.Ticker(ticker)
    current_price = stock_info.info["currentPrice"]

    return f"The current price is USD {current_price}"


def handle_kay_errors(status_code: str):
    """Handles errors that occur during call to KAY AI endpoint."""
    copilot_logger.error(f"Kay AI API returned status code {status_code}")
    # ss.error_message = "An error occured."


def retriever(query):
        dataset_config = {
            "dataset_id": "company",
            "data_types": ["10-K", "10-Q"]
        }

        retrieval_config = {
            "num_context": 6
        }

        url = "https://api.kay.ai/retrieve"

        headers = {"API-KEY": ss.configurations["kay_api_key"]}

        payload = {
            "query": query,
            "dataset_config": dataset_config,
            "retrieval_config": retrieval_config
        }

        response = requests.post(url, headers=headers, json=payload)

        status_code = response.status_code 

        if status_code == 200:
            context_list = response.json()["contexts"]

            texts = []

            for i in range(0, len(context_list)):
                text = context_list[i]["chunk_embed_text"]
                texts.append(text)


            chain = RunnableParallel({
                "question": lambda x: x["question"],
                "context": lambda x: x["context"]
            }) | prompt | model | StrOutputParser()

            answer = chain.invoke({"question": query,
                                    "context": texts})
            
            return answer
        else:
            handle_kay_errors(status_code)


retrieval_tool = Tool(
        name="Kay AI Vector Store",
        func=retriever,
        description=("Use this tool when answering questions that relate to a company's SEC filings, financials and/ or spending patterns."),
        return_direct=True
    )


search_tool = DuckDuckGoSearchRun()

