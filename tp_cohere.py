import os
import cohere

cohere_api = os.getenv('COHERE_API')


def text2embeeding(texts: list):

    try:
        co = cohere.Client(cohere_api)
        response = co.embed(texts=[], model='embed-multilingual-v2.0')
        return response.embeddings
    except ValueError as e:
        raise 'Cohere Text to Embedding Error: ' + e
