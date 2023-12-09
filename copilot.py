import os

# For debugging and local experimentation

# import langchain
# langchain.debug=True

import yfinance as yf

from pydantic.v1 import BaseModel, Field

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.retrievers import KayAiRetriever

from langchain.tools import tool
from langchain.agents import Tool, initialize_agent

from memory import create_memory


class CurrentStockPriceInput(BaseModel):
    symbol: str = Field(..., description="The ticker symbol for the company whose stock price is to be checked.")


@tool(args_schema=CurrentStockPriceInput)
def get_current_stock_price(symbol: str) -> str:
    """Call this function to get the current stock price of a company."""
    stock_info = yf.Ticker(symbol)
    current_price = stock_info.info["currentPrice"]

    return f"The current price is USD {current_price}"


def get_response(query, configurations, chat_history):

    os.environ["KAY_API_KEY"] = configurations["kay_api_key"]

    model = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=configurations["openai_api_key"])
    retriever = KayAiRetriever.create(dataset_id="company", data_types=["10-K", "10-Q"], num_contexts=6)
    qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=retriever)

    memory = create_memory(chat_history=chat_history)

    retrieval_tool = Tool(
        name="Kay AI Vector Store",
        func=qa.run,
        description=("Use this tool when answering questions that relate to a company's SEC filings.")
    )

    tools = [get_current_stock_price, retrieval_tool]

    agent = initialize_agent(
        agent="chat-conversational-react-description",
        tools=tools,
        llm=model,
        max_iterations=3,
        early_stopping_method="generate",
        memory=memory
    )

    result = agent(query)

    chat_history.append((query, result["output"]))

    return result["output"], chat_history
