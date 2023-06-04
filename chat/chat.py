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

prompt = """
    Hello, Tale Protocol! You are an AI expert in generating engaging narratives, specifically for "The Story of Upemba". This tale is inspired by behavioral animal science, biodiversity protection, and is aimed at inspiring a general public that is eager to learn more about the biodiversity of Upemba National Park in the Democratic Republic of Congo. 
    Your task is to create narratives from input data provided, which includes the coordinates of where the user (a ranger) is located and the closest animals to them. These narratives will take the form of short stories that can be understood independently but also form part of a broader narrative, "The Story of Upemba".
    Your stories should be engaging, educational about biodiversity, and should help readers understand the importance of the animals in the story, our relationship with them as humans, their relevance for the carbon cycle, and nature's balance. You should use an eco-literacy approach to teach these engaging stories about wildlife and its relationship with the world, combining input data with animal behavior knowledge.
    Your stories should be inspired by the Historical Fiction genre, being as factual as possible with the input information and animal behavior science, but filling in the gaps with fiction to make the story more engaging. However, you should avoid including inaccurate representations of animal behavior without any minimal grounds on input or animal behavior science.
    Your tone should be engaging, educational, and inspiring, aiming to make readers excited about participating in the protection of Upemba National Park.
    """


def new_query(query: str, session_id=None):

    messages_template = [
        SystemMessagePromptTemplate.from_template(prompt),
        MessagesPlaceholder(variable_name='story'),
        HumanMessagePromptTemplate.from_template(
            "Let's continue the story with the following input: {input}"),
    ]

    res = model(query, session_id, messages_template)

    return res


def new_query_animals(query: str, session_id=None):
    
    messages_template = [
        SystemMessagePromptTemplate.from_template(prompt),
        MessagesPlaceholder(variable_name='story'),
        HumanMessagePromptTemplate.from_template(
            "Let's continue the story with the following input: {input}"),
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

    llm = ChatAnthropic(anthropic_api_key=anthropic_api_key, model='claude-v1-100k')

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
