from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
from transformers import MarianMTModel, MarianTokenizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно указать домены сайта
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загрузка модели и токенизатора
model_name = "./models/opus-mt-en-ru"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)



class Query(BaseModel):
    prompt: str

@app.post("/translate/")
async def translate_text(query: Query):
    inputs = tokenizer.encode(query.prompt, return_tensors="pt")
    outputs = model.generate(inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    for output in outputs:
        print(tokenizer.decode(output, skip_special_tokens=True))
    return {"response": response}

# Запускается с помощью uvicorn
# uvicorn test:app --host 0.0.0.0 --port 8000