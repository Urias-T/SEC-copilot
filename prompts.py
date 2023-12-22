from langchain.prompts import ChatPromptTemplate

template = """Answer the question based on the following context only:
{context}

Question: {question}"""

prompt = ChatPromptTemplate.from_template(template)

