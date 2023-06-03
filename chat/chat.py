import os
from langchain.chat_models import ChatAnthropic
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)


def new_query(query: str, session_id=None):

    messages_template = [
        SystemMessagePromptTemplate.from_template(
            "You are a storyteller. Your principal rol is to create stories based on the animal information."),
        MessagesPlaceholder(variable_name='story'),
        HumanMessagePromptTemplate.from_template(
            "Continue writing the story and include the next animal: {input}."),
    ]

    res = model(query, session_id, messages_template)

    return res


def new_query_animals(query: str, session_id=None):

    messages_template = [
        SystemMessagePromptTemplate.from_template(
            "You are a storyteller. Your principal rol is to create stories based on the animal information."),
        MessagesPlaceholder(variable_name='story'),
        HumanMessagePromptTemplate.from_template(
            "Continue writing the story include now the next animals: {input}."),
    ]

    return model(query, session_id, messages_template)


def new_query_question(query, session_id=None):
    messages_template = [
        MessagesPlaceholder(variable_name='story'),
        HumanMessagePromptTemplate.from_template(
            "Responde the next question: {input}.")
    ]

    return model(query, session_id, messages_template)


def model(query, session_id, messages):
    url = os.getenv('REDIS_URL')
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

    llm = ChatAnthropic(anthropic_api_key=anthropic_api_key)

    history = RedisChatMessageHistory(session_id=session_id, url=url)
    memory = ConversationBufferMemory(
        memory_key='story', return_messages=True, chat_memory=history)

    chat_prompt_template = ChatPromptTemplate.from_messages(
        messages=messages
    )
    conversation_chain = ConversationChain(
        memory=memory,
        llm=llm,
        prompt=chat_prompt_template,
    )

    output = conversation_chain.predict(input=query)
    return output
