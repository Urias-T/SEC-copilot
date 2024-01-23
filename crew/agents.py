import os

from crewai import Agent

from tools import retrieval_tool, search_tool

from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
kay_api_key = os.environ.get("KAY_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=openai_api_key)

class InvestmentAgents():

    def news_researcher(self):
        return Agent(
            role="News Research Expert",
            goal="Find most recent news headlines that can affect investment decisions.",
            backstory="""An expert news analyst. Your expertise lies in getting relevant 
            news articles from the internet on a specific company. Also get the current stock price.""",
            tools=[search_tool],
            llm=model,
            verbose=True
        )
    
    def fillings_researcher(self):
        return Agent(
            role="Fillings Research Expert",
            goal="Find the spending patterns in the company's spend over the past three quarters.",
            backstory="""An expert financial analyst, capable of reading through company's SEC fillings
            to understand patterns in spend over the past three quarters.""",
            tools=[retrieval_tool],
            llm=model,
            verbose=True
        )
    
    def report_writer(self):
        return Agent(
            role="Report Writing Expert",
            goal="""Write a report, summarizing the findings on a given company as regards the spending patterns
            and most recent news headlines.""",
            backstory="""An expert report writer, capable of writing financial articles for investors to highlights 
            key pieces of information to facilitate informed, data-driven investment decisions.""",
            llm=model,
            verbose=True
        )
