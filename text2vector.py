from tp_cohere import text2embeeding
from tp_qdrant import textToPoint, insert_vectors
from langchain.text_splitter import CharacterTextSplitter

texts = [
    'Hola',
    'Hi'
]

character_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=512,
    chunk_overlap=200,
    length_function=len,
)

docs = character_splitter.create_documents(texts=texts)

split_texts = [i.page_content for i in docs]

vectors = text2embeeding(split_texts)

points = [textToPoint(text, vector) for text, vector in zip(texts, vectors)]

insert_vectors(points)
