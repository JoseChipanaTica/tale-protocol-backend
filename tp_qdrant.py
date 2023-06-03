import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models

qdrant_url = os.getenv('QDRANT_URL')
qdrant_port = os.getenv('QDRANT_PORT')
qdrant_cname = os.getenv('QDRANT_CNAME')

client = QdrantClient(qdrant_url, port=qdrant_port)


def create_collection():
    client.recreate_collection(
        collection_name=qdrant_cname,
        vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE))


def get_collection():
    client.get_collection(collection_name=qdrant_cname)


def insert_vectors(points: list):
    client.upsert(collection_name=qdrant_cname, points=points)


def textToPoint(text: str, emb: list):
    return models.PointStruct(
        id=str(uuid()),
        payload={"text": text},
        vector=emb
    )
