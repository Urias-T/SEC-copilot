def create_react_agent_memory(chat_history: list) -> str:

    history = ""

    for tuple in chat_history:
        history += "Human: " + tuple[0]
        history += "\nAI: " + tuple[1]

    return history

