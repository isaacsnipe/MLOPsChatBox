
FROM python:3.10-slim

EXPOSE 8185

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update

COPY requirements.txt .

RUN python -m pip install -r requirements.txt --no-cache-dir

WORKDIR /app

COPY . /app

RUN mkdir -p /app/data

RUN pip install --upgrade poetry && pip install --upgrade pip && poetry update

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8185", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
