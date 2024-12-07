from typing import Dict
import ollama
import io
import zipfile
import yaml
import toml
import json
from configparser import ConfigParser
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse, StreamingResponse

from fastapi import FastAPI, HTTPException


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model_name = "llama2"

class Query(BaseModel):
    prompt: str
    model: str

class FileQuery(BaseModel):
    file: str
    fileType: str

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


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Чтение содержимого файла
        file_content = await file.read()
        file_extension = file.filename.split('.')[-1].lower()

        if file_extension == "txt":
            # Обработка TXT файлов
            try:
                processed_content = file_content.upper()  # Пример: конвертация текста в верхний регистр
                print("Обработанное содержимое TXT файла:", processed_content.decode("utf-8"))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Ошибка обработки TXT: {str(e)}")

        elif file_extension == "json":
            # Обработка JSON файлов
            try:
                parsed_content = json.loads(file_content)
                print("Содержимое JSON файла:", parsed_content)
                processed_content = json.dumps(parsed_content, indent=4).encode("utf-8")  # Форматируем JSON
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=400, detail=f"Ошибка обработки JSON: {str(e)}")

        elif file_extension in ["yaml", "yml"]:
            # Обработка YAML файлов
            try:
                parsed_content = yaml.safe_load(file_content)
                print("Содержимое YAML файла:", parsed_content)
                processed_content = json.dumps(parsed_content, indent=4).encode("utf-8")  # Конвертируем в JSON
            except yaml.YAMLError as e:
                raise HTTPException(status_code=400, detail=f"Ошибка обработки YAML: {str(e)}")

        elif file_extension == "toml":
            # Обработка TOML файлов
            try:
                parsed_content = toml.loads(file_content.decode("utf-8"))
                print("Содержимое TOML файла:", parsed_content)
                processed_content = toml.dumps(parsed_content).encode("utf-8")  # Возвращаем отформатированный TOML
            except toml.TomlDecodeError as e:
                raise HTTPException(status_code=400, detail=f"Ошибка обработки TOML: {str(e)}")



        elif file_extension == "properties":
            # Обработка PROPERTIES файлов
            try:
                properties = {}
                file_content_decoded = file_content.decode("utf-8")
                for line in file_content_decoded.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):  # Пропускаем пустые строки и комментарии
                        continue
                    key_value = line.split("=", 1) if "=" in line else line.split(":", 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        properties[key.strip()] = value.strip()
                print("Содержимое PROPERTIES файла:", properties)

                # Возвращаем обработанный файл, преобразовав его обратно в формат .properties
                processed_content = "\n".join(f"{k}={v}" for k, v in properties.items()).encode("utf-8")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Ошибка обработки PROPERTIES: {str(e)}")


        elif file_extension == "zip":
            # Обработка ZIP файлов
            try:
                with zipfile.ZipFile(io.BytesIO(file_content)) as zip_file:
                    file_list = zip_file.namelist()
                    print("Файлы в ZIP архиве:", file_list)

                    # Логируем содержимое каждого файла
                    for file_name in file_list:
                        with zip_file.open(file_name) as zip_entry:
                            content = zip_entry.read()
                            print(f"Содержимое файла {file_name}: {content[:100]}")  # Первые 100 байт

                processed_content = file_content  # Возвращаем архив без изменений
            except zipfile.BadZipFile:
                raise HTTPException(status_code=400, detail="Некорректный ZIP файл")


        elif file_extension == "jar":
            # Обработка JAR файлов (как ZIP)
            try:
                with zipfile.ZipFile(io.BytesIO(file_content)) as jar_file:
                    file_list = jar_file.namelist()
                    print("Файлы в JAR архиве:", file_list)

                    # Логируем содержимое каждого файла
                    for file_name in file_list:
                        with jar_file.open(file_name) as jar_entry:
                            content = jar_entry.read()
                            print(f"Содержимое файла {file_name}: {content[:100]}")  # Первые 100 байт

                processed_content = file_content  # Возвращаем JAR без изменений
            except zipfile.BadZipFile:
                raise HTTPException(status_code=400, detail="Некорректный JAR файл")

        else:
            # Для неподдерживаемых типов файлов
            raise HTTPException(status_code=415, detail="Тип файла не поддерживается.")

        # Подготовка ответа
        response = io.BytesIO(processed_content)
        response.seek(0)
        return StreamingResponse(
            response,
            media_type=file.content_type,
            headers={
                "Content-Disposition": f"attachment; filename={file.filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке файла: {str(e)}")
