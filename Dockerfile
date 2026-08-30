FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram_kino_bot.py .
COPY admin_add_movies.py .
COPY statistika.py .
COPY kinolar.csv .
COPY README.md .

CMD ["python", "telegram_kino_bot.py"]
