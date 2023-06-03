from typing import Union
import os
from fastapi import Body, FastAPI
from chat import chat
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", 'https://tale-protocol.vercel.app'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"API": "Tale Protocol API"}


@app.post("/")
async def read_root(payload: dict = Body(...)):
    animal = payload['animal']
    session = payload['sessionId']
    res = chat.new_query(animal, session)
    return {"story": res}


@app.post("/animals")
async def read_root(payload: dict = Body(...)):
    animals = payload['animals']
    session = payload['sessionId']
    res = chat.new_query_animals(animals, session)
    return {"story": res}


@app.post("/question")
async def read_root(payload: dict = Body(...)):
    question = payload['question']
    session = payload['sessionId']
    res = chat.new_query_question(question, session)
    return {"story": res}
