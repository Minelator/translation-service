# Используем Python-образ
FROM python:3.10-slim

# Установка необходимых системных библиотек
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Убедимся, что pip обновлен
RUN python -m pip install --upgrade pip setuptools wheel

# Установка зависимостей
WORKDIR /api-service
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app.py .

# Экспонируем порт приложения
EXPOSE 8000


# Команда для запуска приложения через uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]