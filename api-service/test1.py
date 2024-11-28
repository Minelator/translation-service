from fastapi import FastAPI, HTTPException
import ollama

app = FastAPI()
model_name="llama2"

@app.post("/generate/")
async def generate_text(prompt: str, model: str = model_name):
    try:
        response = ollama.generate(model=model, prompt=prompt)
        generated_text = ''.join(chunk["text"] for chunk in response)  # Собираем текст из частей
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
