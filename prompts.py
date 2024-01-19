from langchain_core.prompts import ChatPromptTemplate

template = """Answer the question based on the following context only:
{context}

Question: {question}"""

prompt = ChatPromptTemplate.from_template(template)


react_template = """You are designed to help stock market investors understand company financials 
as well as stock values before making investment decisions.

TOOLS:
------

You have access to the following tools:

{tools}

If you decide to use the vector store tool, the action input should be the new input from the user.

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
"""

react_prompt = ChatPromptTemplate.from_template(react_template)

