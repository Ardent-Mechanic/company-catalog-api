FROM python:3.11-slim

# Не пишем .pyc и сразу выводим логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# pip + pipenv
RUN pip install --no-cache-dir --upgrade pip pipenv

# Сначала зависимости (для кеширования слоёв)
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile \
    && pip cache purge

# Код приложения
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]