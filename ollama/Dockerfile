# Используем официальный базовый образ Ollama
FROM ollama/ollama:latest

# Установка рабочего каталога
WORKDIR /ollama

# Копируем entrypoint.sh в контейнер
COPY ./entrypoint.sh ./entrypoint.sh

# Преобразуем файл в формат Unix и делаем его исполняемым
RUN sed -i 's/\r$//' ./entrypoint.sh && chmod +x ./entrypoint.sh

# Экспонируем порт Ollama API
EXPOSE 11434

# Указываем скрипт для запуска
ENTRYPOINT ["./entrypoint.sh"]
