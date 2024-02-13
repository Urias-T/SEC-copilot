import os
import streamlit as st

import langchain
langchain.debug=True

from crewai import Agent

from crew.tools import (
    retrieval_tool, search_tool, 
    get_current_stock_price
)

from langchain_openai import ChatOpenAI

# from dotenv import load_dotenv
# load_dotenv()

# openai_api_key = os.environ.get("OPENAI_API_KEY")
# kay_api_key = os.environ.get("KAY_API_KEY")

ss = st.session_state

model = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=ss.configurations["openai_api_key"])

class InvestmentAgents():

    def fillings_researcher(self):
        return Agent(
            role="Fillings Research Expert",
            goal="Find the spending patterns in the company's spend over the past three quarters.",
            backstory="""An expert financial analyst, capable of reading through company's SEC fillings
            to understand patterns in spend over the past three quarters.""",
            tools=[retrieval_tool],
            llm=model,
            allow_delegation=False,
            verbose=True
        )
    
    def market_trader(self):
        return Agent(
            role="Stock Price Seeker",
            goal="Find the current stock price of a company.",
            backstory="An expert stock market trader able to find out the current stock price of a company.",
            tools=[get_current_stock_price],
            llm=model,
            allow_delegation=False,
            verbose=True
        )

    def news_researcher(self):
        return Agent(
            role="News Research Expert",
            goal="Find most recent news headlines that can affect investment decisions.",
            backstory="""An expert news analyst. Your expertise lies in getting relevant 
            news articles from the internet on a specific company.""",
            tools=[search_tool],
            llm=model,
            verbose=True
        )
    
    def report_writer(self):
        return Agent(
            role="Report Writing Expert",
            goal="""Impress your customers with a robust company analysis.""",
            backstory="""An expert report writer, capable of writing financial articles for investors to highlights 
            key pieces of information to facilitate informed, data-driven investment decisions.""",
            llm=model,
            verbose=True
        )
