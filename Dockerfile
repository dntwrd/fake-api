# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Открываем нужный порт
EXPOSE 5555

# Запускаем приложение на порту 5555
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]
