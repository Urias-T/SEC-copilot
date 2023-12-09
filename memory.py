from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema.messages import HumanMessage, AIMessage


def create_memory(chat_history: list) -> ConversationBufferMemory:
    """Creates a langchain ConversationBufferMemory object from a list of tuples in query-answer pairs.

    Args:
        chat_history (list): a list of tuples to be used in creating the memory object

    Returns:
        ConversationBufferMemory: the conversation buffer memory object
    """

    messages = []

    for tuple in chat_history:
        messages.append(HumanMessage(content=tuple[0]))
        messages.append(AIMessage(content=tuple[1]))

    chat_history = ChatMessageHistory(messages=messages)

    memory = ConversationBufferMemory(chat_memory=chat_history,
                                        return_messages=True,
                                        memory_key="chat_history")
    
    return memory

