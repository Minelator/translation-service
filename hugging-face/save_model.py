# Локальная установка модели hugging face
from transformers import MarianMTModel, MarianTokenizer

# Загрузка модели и токенизатора
model_name = "Helsinki-NLP/opus-mt-en-ru"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Текст для перевода
text = "Hello, how are you?"

# Токенизация
inputs = tokenizer([text], return_tensors="pt", max_length=512, truncation=True)

# Перевод
translated = model.generate(**inputs)

# Декодирование результата
translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
print(translated_text)

# Сохранение модели и токенизатора
model.save_pretrained("./opus-mt-en-ru")
tokenizer.save_pretrained("./opus-mt-en-ru")

