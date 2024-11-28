# FROM ubuntu:22.04
FROM ollama/ollama:latest

# Установка системных зависимостей
# RUN apt-get update && apt-get install -y \
#     curl \
#     wget \
#     software-properties-common \
#     && rm -rf /var/lib/apt/lists/*

# Установка Ollama CLI
# RUN curl -fsSL https://ollama.com/install.sh | sh && \
#     which ollama

# Проверяем, что Ollama установлена корректно
# RUN which ollama || echo "Ollama CLI не установлена!"

# Добавляем команду для загрузки модели в отдельной стадии
# RUN ollama pull qwen:0.5b || echo "Ошибка при загрузке модели"
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


# Экспонирование порта Ollama API
EXPOSE 11434

# Запуск Ollama сервера
# CMD ["ollama", "serve"]
ENTRYPOINT ["/entrypoint.sh"]



