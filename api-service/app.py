from typing import Dict
import ollama
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно указать домены сайта
    allow_methods=["*"],
    allow_headers=["*"],
)

model_name = "llama2"

class Query(BaseModel):
    prompt: str
    model: str


@app.get("/")
def read_root():
    return {"message": "Ollama API Server is Running"}

@app.post("/generate/")
async def generate(query: Query):
    try:
      print(query)
      response=ollama.chat(
        query.model,
        messages=[{
            'role':'user',
            'content':query.prompt,
        }],
      )
      
      return {"response": response.message.content}

    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
