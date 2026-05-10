from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    data: str

@app.get("/")
def read_root():
    return {"message": "EvenUp"}

@app.post("/")
def PingPong(payload: Data):
    if payload.data == "ping":
        return {"ping": "pong"}